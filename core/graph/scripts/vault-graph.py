#!/usr/bin/env python3
"""vault-graph.py — Knowledge graph analysis for Obsidian vault.

Usage:
  python3 vault-graph.py <vault_root> [mode]

Modes:
  full       — all analyses (default)
  orphans    — modules with no incoming links
  dangling   — wiki-links pointing to non-existent files
  clusters   — connected components and bridge nodes
  depth      — dependency chain depth analysis (LEGACY: liczone po `depends-on:`,
               które w kanonie 2.0 nie istnieje — w czystym vaulcie wychodzi 0)
  staleness  — staleness x connectivity heatmap
  bridges    — cross-domain connections
"""

import os
import re
import sys
import json
import subprocess
from collections import defaultdict
from datetime import datetime, date
from pathlib import Path

# --- Configuration ---

# Drzewa wczytywane do grafu. `osoby/` i `_sales/` MUSZĄ tu być — bez nich budżety
# staleness dla typów `osoba` i `deal` są martwym kodem (nic ich nigdy nie dotyka).
# `_events/` wchodzi jako ŹRÓDŁO krawędzi (`owner:`/`osoby:`/`dotyczy:`), ale jest
# write-once: nie liczy się do orphanów ani do staleness.
GRAPH_DIRS = {
    "1_receptionOS",
    "2_apolonia",
    "3_fte",
    "4_apollo",
    "_culture",
    "osoby",
    "_sales",
    "_events",
}
SKIP_WALK = {".git", ".obsidian", "node_modules"}
DOMAIN_MAP = {
    "1_receptionOS": "ROS",
    "2_apolonia": "Apolonia",
    "3_fte": "Fundacja",
    "4_apollo": "Apollo",
    "_culture": "Culture",
    "osoby": "Osoby",
    "_sales": "Sales",
    "_events": "Events",
}

# Krawędzie encji z frontmattera (kanon 2.0). `depends-on:` NIE jest krawędzią kanonu —
# jest tylko wykrywane jako dług legacy (patrz LEGACY_FIELDS) i obsługiwane przez tryb
# `depth` dla vaultów, które jeszcze go nie posprzątały.
EDGE_FIELDS = ("owner", "osoby", "uczestnicy", "dotyczy", "podmiot", "kontakt")
LEGACY_FIELDS = ("depends-on", "sources", "cadence", "audience")

# Encje write-once — poza staleness i poza raportem orphanów (brak linków to nie dług).
WRITE_ONCE_TYPES = {"spotkanie", "event", "log"}

# --- Freshness / staleness (git-based) ---
#
# Świeżość pliku = data ostatniego commita, który go dotknął. Commity oznaczone
# trailerem `Meta: true` (batche mechaniczne: sweep, rename, lint-fix) są pomijane,
# bo nie niosą wiedzy. Budżet dni: whitelist HUBS wygrywa (7d), potem typ encji.
# Kanon tych progów: `_claude/9-automation/freshness.py` w modular-context —
# zmiana tutaj bez zmiany tam rozjeżdża digest SessionStart z raportem grafu.

HUB_STALENESS_DAYS = 7
# Whitelist hubów (ścieżki vault-relative, POSIX). Per-vault — w innym vaulcie podmień
# albo wyczyść na set(). Huby to jedyne pliki, których staleness jest sygnałem dziennym.
HUBS = {
    "1_receptionOS/4-go-to-market/pipeline.md",
    "1_receptionOS/1-product/roadmap.md",
    "1_receptionOS/1-product/features.md",
    "1_receptionOS/4-go-to-market/modular-offer.md",
    "_culture/team/team-roster.md",
    "_sales/_kanban.md",
}
TYPE_STALENESS_DAYS = {
    "modul": 60,
    "osoba": 180,
    "deal": 30,
}
DEFAULT_STALENESS_DAYS = 60  # plik poza mapą typów
DEAL_ACTIVE_PREFIX = "_sales/pipeline/active/"  # deal 30d TYLKO tu; reszta poza sygnałem
STALENESS_SKIP_PREFIXES = ("4_apollo/",)  # drzewo wygaszone — poza sygnałem
STALENESS_SKIP_STATUS = {"archive"}
META_TRAILER_KEY = "Meta"  # commity z `Meta: true` nie liczą się jako dotknięcie treści

# Fallback mapy typów, gdy vault nie ma `_schemas/map.yaml` (kolejność MA znaczenie).
DEFAULT_TYPE_GLOBS = [
    ("_transcripts/hive-ledger/**", "log"),
    ("_transcripts/**", "spotkanie"),
    ("osoby/**", "osoba"),
    ("_events/**", "event"),
    ("_sales/pipeline/**", "deal"),
    ("_sales/partnerships/**", "deal"),
    ("_archive/**", None),
    ("_workspace/**", None),
    ("_claude/**", None),
    ("1_receptionOS/**", "modul"),
    ("2_apolonia/**", "modul"),
    ("3_fte/**", "modul"),
    ("4_apollo/**", "modul"),
    ("_culture/**", "modul"),
]

# --- Regex patterns ---

WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)\\?\|[^\]]+\]\]|\[\[([^\]]+?)\]\]")
UPDATED_RE = re.compile(r"^updated:\s*(\d{4}-\d{2}-\d{2})", re.MULTILINE)
STATUS_RE = re.compile(r"^status:\s*(\S+)", re.MULTILINE)
TYPE_RE = re.compile(r"^type:\s*(\S+)", re.MULTILINE)
CODE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)


def extract_wikilinks(text):
    """Extract wiki-link targets from text, handling aliases, anchors, escapes."""
    results = []
    for m in WIKILINK_RE.finditer(text):
        target = m.group(1) or m.group(2)
        target = target.rstrip("\\")  # Strip trailing backslash from escaped pipes
        target = target.split("#")[0]  # Strip #section anchors
        target = target.strip()
        if target:
            results.append(target)
    return results


def parse_frontmatter(content):
    """Extract key fields from YAML frontmatter."""
    if not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end == -1:
        return {}
    fm = content[3:end]
    result = {}

    m = UPDATED_RE.search(fm)
    if m:
        try:
            result["updated"] = datetime.strptime(m.group(1), "%Y-%m-%d").date()
        except ValueError:
            pass

    m = STATUS_RE.search(fm)
    if m:
        result["status"] = m.group(1)

    m = TYPE_RE.search(fm)
    if m:
        result["type"] = m.group(1)

    # Krawędzie kanonu: owner:/osoby:/uczestnicy:/dotyczy:/podmiot:/kontakt:
    # (inline `["[[a]]", "[[b]]"]` albo blok `- [[a]]`)
    edges = []
    for field in EDGE_FIELDS:
        for em in re.finditer(
            r"^" + re.escape(field) + r":[ \t]*(.*(?:\n[ \t]+-[ \t].*)*)",
            fm,
            re.MULTILINE,
        ):
            edges.extend(extract_wikilinks(em.group(1)))
    result["edges"] = edges

    # Pola legacy — w kanonie 2.0 nie istnieją; raportujemy jako dług, nie jako krawędź
    result["legacy"] = [
        f for f in LEGACY_FIELDS
        if re.search(r"^" + re.escape(f) + r":", fm, re.MULTILINE)
    ]

    # depends-on: list of [[links]] — LEGACY, wyłącznie dla trybu `depth`
    deps_block = re.search(r"depends-on:\s*\n((?:\s+-\s+.*\n)*)", fm)
    if deps_block:
        result["depends_on"] = extract_wikilinks(deps_block.group(1))
    else:
        deps_inline = re.search(r"depends-on:\s*\[([^\]]*)\]", fm)
        if deps_inline:
            result["depends_on"] = extract_wikilinks(deps_inline.group(1))
        else:
            result["depends_on"] = []

    return result


def extract_body_links(content):
    """Extract wiki-links from body text (excluding frontmatter and code blocks)."""
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            content = content[end + 4:]
    content = CODE_BLOCK_RE.sub("", content)
    return extract_wikilinks(content)


# --- Type resolution (jawny `type:` → glob z _schemas/map.yaml) ---


def glob_to_re(glob):
    """Konwersja globa map.yaml → regex (fnmatch nie zna '**')."""
    out, i = [], 0
    while i < len(glob):
        c = glob[i]
        if glob[i:i + 2] == "**":
            out.append(".*")
            i += 2
            if i < len(glob) and glob[i] == "/":
                i += 1
        elif c == "*":
            out.append("[^/]*")
            i += 1
        elif c == "[":
            j = glob.index("]", i)
            out.append(glob[i:j + 1])
            i = j + 1
        else:
            out.append(re.escape(c))
            i += 1
    return re.compile("^" + "".join(out) + "$")


def load_type_globs(vault_root):
    """Lista (regex, typ|None) z `_schemas/map.yaml` → `default-type`.

    Kolejność globów ma znaczenie (pierwszy trafiony wygrywa), więc czytamy blok
    linia po linii. Vault bez `_schemas/map.yaml` dostaje DEFAULT_TYPE_GLOBS.
    """
    path = os.path.join(str(vault_root), "_schemas", "map.yaml")
    pairs = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            in_block = False
            for line in fh:
                if not in_block:
                    if line.startswith("default-type:"):
                        in_block = True
                    continue
                if line.strip() and not line[0].isspace():
                    break  # koniec bloku
                if not line.strip() or line.strip().startswith("#"):
                    continue
                m = re.match(r'^\s+"?([^"#]+?)"?:\s*([^#\s]*)', line)
                if not m:
                    continue
                raw = m.group(2).strip()
                typ = None if raw in ("null", "~", "") else raw
                pairs.append((glob_to_re(m.group(1).strip()), typ))
    except OSError:
        pairs = []
    if not pairs:
        pairs = [(glob_to_re(g), t) for g, t in DEFAULT_TYPE_GLOBS]
    return pairs


def resolve_type(rel, type_globs, fm_type=None):
    """(typ, źródło) — jawny `type:` wygrywa z globem; glob może mapować na None."""
    if fm_type:
        return fm_type, "frontmatter"
    rel = rel.replace(os.sep, "/")
    for rx, typ in type_globs:
        if rx.match(rel):
            return typ, "glob"
    return None, None


# --- Freshness ---


def git_last_touched(vault_root):
    """Mapa rel_path (vault-relative) → data (date) ostatniego commita NIE-Meta.

    Jeden zbiorczy `git log` na repo (nie per plik — per-plik jest O(n) procesów).
    `git log --name-only` zwraca ścieżki relatywne do KORZENIA REPO, więc gdy vault
    jest podkatalogiem repo, przeliczamy je przez `--show-prefix`. Bez tego lookup
    nigdy nie trafia, rc=0 nie zgłasza błędu i CAŁA staleness po cichu spada na mtime.

    Zwraca (dates, error). error != None gdy gita nie ma / katalog nie jest repo.
    """
    def git(*args):
        return subprocess.run(
            ["git"] + list(args), capture_output=True, text=True, cwd=str(vault_root)
        )

    try:
        top = git("rev-parse", "--show-toplevel")
        if top.returncode != 0:
            return {}, "katalog nie jest repo gitowym: %s" % (
                (top.stderr or "").strip()[:200]
            )
        prefix = git("rev-parse", "--show-prefix").stdout.strip()
        proc = git(
            "-c", "core.quotepath=false",
            "log", "--name-only", "--no-renames",
            "--format=@%cs|%(trailers:key=" + META_TRAILER_KEY
            + ",valueonly,separator=;)",
        )
    except (OSError, subprocess.SubprocessError) as e:
        return {}, "git niedostępny: %s" % e

    if proc.returncode != 0:
        return {}, "git log nie powiódł się: %s" % (proc.stderr or "").strip()[:200]

    dates = {}
    cur = None
    skip = False
    for line in proc.stdout.splitlines():
        if line.startswith("@"):
            cur, _, trailer = line[1:].partition("|")
            skip = "true" in trailer.lower()
            continue
        if not line.strip() or not cur or skip:
            continue
        if prefix:
            if not line.startswith(prefix):
                continue  # plik z innego podkatalogu repo — spoza vaulta
            line = line[len(prefix):]
        if line not in dates:
            dates[line] = cur  # git log jest od najnowszego — pierwsze trafienie wygrywa

    parsed = {}
    for rel, iso in dates.items():
        try:
            parsed[rel] = datetime.strptime(iso, "%Y-%m-%d").date()
        except ValueError:
            continue
    return parsed, None


def build_freshness(vault_root, paths, nodes):
    """Data ostatniej realnej zmiany per plik + informacja skąd pochodzi.

    Kolejność źródeł:
      1. git — ostatni commit BEZ trailera `Meta: true` (kanon świeżości)
      2. frontmatter `updated:` — gdy git nie zna pliku. Dwa przypadki: plik jeszcze
         niecommitowany ALBO plik, którego JEDYNE commity to mechaniczne batche
         `Meta: true`. W drugim przypadku batch szedł z pominięciem stampowania, więc
         `updated:` bywa STARSZE niż faktyczne powstanie pliku — to dolne oszacowanie
         świeżości, nie data, którą ktokolwiek ostemplował.
      3. mtime — fallback gdy vault nie jest repo gitowym; wtedy leci ostrzeżenie.
    """
    git_dates, git_error = git_last_touched(vault_root)
    freshness = {}
    warnings = []
    if git_error:
        warnings.append(
            "Brak danych z gita (%s) — staleness liczona z mtime plików, "
            "co zawyża świeżość po każdym mechanicznym sweepie." % git_error
        )
    elif paths and git_dates and not any(
        p.replace(os.sep, "/") in git_dates for p in paths
    ):
        warnings.append(
            "git log nie zna ŻADNEGO z %d skanowanych plików — ścieżki się nie zgadzają "
            "(vault poza repo? inny worktree?). Staleness spada na frontmatter/mtime "
            "i jest zaniżona." % len(paths)
        )

    for rel in paths:
        d = git_dates.get(rel.replace(os.sep, "/"))
        source = "git"
        if d is None:
            d = (nodes.get(rel) or {}).get("updated")
            source = "frontmatter"
        if d is None:
            try:
                mtime = os.path.getmtime(os.path.join(str(vault_root), rel))
                d = datetime.fromtimestamp(mtime).date()
                source = "mtime"
            except OSError:
                continue
        freshness[rel] = {"date": d, "source": source}

    return freshness, warnings


def staleness_budget(rel, node_type, type_source=None, status=None):
    """Budżet świeżości w dniach albo None = plik POZA sygnałem staleness.

    Kolejność kanonu (referencja: `_claude/9-automation/freshness.py`):
      `status: archive`                → poza sygnałem (dotyczy też hubów)
      HUBS                             → 7 dni
      drzewa wygaszone (4_apollo/**)   → poza sygnałem
      deal                             → 30 dni TYLKO w `_sales/pipeline/active/`
      modul 60 dni · osoba 180 dni
      spotkanie/event/log (write-once) → poza sygnałem
      glob mapujący na null            → poza sygnałem (_workspace, _claude, _archive)
      brak typu                        → DEFAULT_STALENESS_DAYS
    """
    rel = rel.replace(os.sep, "/")
    if status in STALENESS_SKIP_STATUS:
        return None
    if rel in HUBS:
        return HUB_STALENESS_DAYS
    if any(rel.startswith(p) for p in STALENESS_SKIP_PREFIXES):
        return None
    if node_type == "deal":
        return (
            TYPE_STALENESS_DAYS["deal"]
            if rel.startswith(DEAL_ACTIVE_PREFIX)
            else None
        )
    if node_type in TYPE_STALENESS_DAYS:
        return TYPE_STALENESS_DAYS[node_type]
    if node_type in WRITE_ONCE_TYPES:
        return None
    if node_type is None and type_source == "glob":
        return None  # drzewo świadomie zmapowane na null
    return DEFAULT_STALENESS_DAYS


# --- Discovery ---


def discover_vault(vault_root):
    """Scan vault. Returns module contents + set of all .md paths."""
    modules = {}
    all_paths = set()

    for root, dirs, files in os.walk(vault_root):
        dirs[:] = [d for d in dirs if d not in SKIP_WALK]
        rel_root = os.path.relpath(root, vault_root)
        top_dir = rel_root.split(os.sep)[0] if rel_root != "." else ""

        for f in files:
            if not f.endswith(".md"):
                continue
            filepath = os.path.join(root, f)
            rel_path = os.path.relpath(filepath, vault_root)
            all_paths.add(rel_path)

            if top_dir in GRAPH_DIRS:
                try:
                    with open(filepath, "r", encoding="utf-8") as fh:
                        modules[rel_path] = fh.read()
                except (IOError, UnicodeDecodeError):
                    continue

    return modules, all_paths


def build_name_index(all_paths):
    """Map filenames/paths to actual file paths for wiki-link resolution."""
    idx = defaultdict(list)
    for p in all_paths:
        stem = Path(p).stem
        idx[stem].append(p)
        no_ext = p.rsplit(".", 1)[0]
        idx[no_ext].append(p)
    return idx


def resolve_link(link, name_index, all_paths, source_dir=None):
    """Resolve a wiki-link target to actual file path(s)."""
    # Handle relative paths (../) by resolving from source directory
    if source_dir and ("../" in link or link.startswith("./")):
        resolved = os.path.normpath(os.path.join(source_dir, link))
        if resolved + ".md" in all_paths:
            return [resolved + ".md"]
        if resolved in all_paths:
            return [resolved]

    # Exact path match (with .md)
    if link + ".md" in all_paths:
        return [link + ".md"]
    if link in all_paths:
        return [link]
    # Try name index
    if link in name_index:
        return name_index[link]
    # Try just filename part
    parts = link.split("/")
    stem = parts[-1]
    if stem in name_index:
        return name_index[stem]
    return []


# --- Graph ---


def build_graph(modules, all_paths, name_index, type_globs):
    """Build the knowledge graph from module files."""
    nodes = {}
    incoming = defaultdict(set)  # target -> {sources}
    outgoing = defaultdict(set)  # source -> {targets}
    dangling = defaultdict(list)  # source -> [unresolved links]

    for path, content in modules.items():
        fm = parse_frontmatter(content)
        body_links = extract_body_links(content)
        top_dir = path.split(os.sep)[0]
        node_type, type_source = resolve_type(path, type_globs, fm.get("type"))

        nodes[path] = {
            "updated": fm.get("updated"),
            "status": fm.get("status"),
            "type": node_type,
            "type_source": type_source,
            "edges": fm.get("edges", []),
            "depends_on": fm.get("depends_on", []),
            "legacy": fm.get("legacy", []),
            "domain": DOMAIN_MAP.get(top_dir, "Other"),
        }

        # Wszystkie krawędzie: wiki-linki w treści + krawędzie encji z frontmattera
        # (+ legacy depends-on, dopóki jakiś vault go trzyma)
        source_dir = str(Path(path).parent)
        all_links = set(
            body_links + fm.get("edges", []) + fm.get("depends_on", [])
        )
        for link in all_links:
            resolved = resolve_link(link, name_index, all_paths, source_dir)
            if resolved:
                for target in resolved:
                    if target in modules:  # Only count edges to scanned files
                        incoming[target].add(path)
                        outgoing[path].add(target)
            else:
                # Skip non-md targets (audio files, yaml, directories)
                if any(link.endswith(ext) for ext in (".m4a", ".mp3", ".yaml", ".py")):
                    continue
                dangling[path].append(link)

    return nodes, incoming, outgoing, dangling


# --- Analysis functions ---


def analyze_orphans(nodes, incoming, freshness=None):
    """Pliki bez incoming links.

    Pomijane: indeksy (punkty wejścia), encje write-once (event/spotkanie/log — brak
    linków to ich normalny stan) oraz `status: archive`. Data raportowana jako
    `last_change` — to samo pojęcie świeżości co w staleness (git, bez commitów
    `Meta: true`), a nie frontmatterowe `updated:`.
    """
    freshness = freshness or {}
    orphans = []
    for path, node in nodes.items():
        if "_index" in path:
            continue  # Index files are entry points
        if node.get("type") in WRITE_ONCE_TYPES:
            continue
        if node.get("status") in STALENESS_SKIP_STATUS:
            continue
        inc = len(incoming.get(path, set()))
        if inc == 0:
            entry = freshness.get(path)
            orphans.append(
                {
                    "path": path,
                    "domain": node["domain"],
                    "type": node.get("type"),
                    "status": node.get("status"),
                    "last_change": str(entry["date"]) if entry else None,
                    "last_change_source": entry["source"] if entry else None,
                }
            )
    orphans.sort(key=lambda x: (x["domain"], x["path"]))
    return orphans


def analyze_dangling(dangling_links):
    """Wiki-links pointing to non-existent files."""
    result = []
    for source, links in dangling_links.items():
        for link in sorted(set(links)):
            result.append({"source": source, "target": link})
    result.sort(key=lambda x: (x["source"], x["target"]))
    return result


def analyze_clusters(nodes, outgoing, incoming):
    """Connected components + bridge nodes."""
    # Undirected adjacency (modules only)
    adj = defaultdict(set)
    for path in nodes:
        for t in outgoing.get(path, set()):
            if t in nodes:
                adj[path].add(t)
                adj[t].add(path)

    # BFS connected components
    visited = set()
    components = []
    for path in nodes:
        if path in visited:
            continue
        comp = set()
        queue = [path]
        while queue:
            n = queue.pop(0)
            if n in visited:
                continue
            visited.add(n)
            comp.add(n)
            for nb in adj.get(n, set()):
                if nb not in visited:
                    queue.append(nb)
        components.append(comp)

    components.sort(key=len, reverse=True)

    # Connectivity stats per node
    connectivity = []
    for path in nodes:
        out_c = len(outgoing.get(path, set()) & set(nodes.keys()))
        in_c = len(incoming.get(path, set()) & set(nodes.keys()))
        connectivity.append(
            {
                "path": path,
                "domain": nodes[path]["domain"],
                "outgoing": out_c,
                "incoming": in_c,
                "total": out_c + in_c,
            }
        )
    connectivity.sort(key=lambda x: x["total"], reverse=True)

    return {
        "component_count": len(components),
        "component_sizes": [len(c) for c in components[:10]],
        "isolated_nodes": sorted([sorted(c)[0] for c in components if len(c) == 1]),
        "most_connected": connectivity[:15],
    }


def analyze_depth(nodes, name_index, all_paths):
    """LEGACY: głębokość łańcuchów po `depends-on:`.

    Pole `depends-on:` zostało usunięte z kanonu 2.0 (core.yaml → removed-fields), więc
    w posprzątanym vaulcie `files_with_depends_on` = 0 i cała sekcja jest pusta z
    definicji — wtedy jej nie raportuj. Tryb zostaje dla vaultów w trakcie migracji.
    """
    deps = {}
    for path, node in nodes.items():
        resolved = []
        source_dir = str(Path(path).parent)
        for dep in node["depends_on"]:
            targets = resolve_link(dep, name_index, all_paths, source_dir)
            for t in targets:
                if t in nodes:
                    resolved.append(t)
        deps[path] = resolved

    cache = {}

    def get_depth(path, visited=None):
        if path in cache:
            return cache[path]
        if visited is None:
            visited = set()
        if path in visited:
            return -1  # Cycle
        visited.add(path)
        if not deps.get(path):
            cache[path] = 0
            return 0
        max_d = 0
        for d in deps[path]:
            val = get_depth(d, visited.copy())
            if val == -1:
                cache[path] = -1
                return -1
            max_d = max(max_d, val + 1)
        cache[path] = max_d
        return max_d

    depths = {}
    cycles = []
    for path in nodes:
        d = get_depth(path)
        if d == -1:
            cycles.append(path)
        else:
            depths[path] = d

    sorted_d = sorted(depths.items(), key=lambda x: x[1], reverse=True)
    dist = defaultdict(int)
    for _, d in sorted_d:
        dist[d] += 1

    # No-depends (leaf nodes)
    no_deps = [p for p, d in sorted_d if d == 0]

    return {
        "legacy_field": "depends-on",
        "files_with_depends_on": len([p for p in nodes if nodes[p]["depends_on"]]),
        "max_depth": sorted_d[0][1] if sorted_d else 0,
        "depth_distribution": dict(sorted(dist.items())),
        "cycles": cycles[:10],
        "deepest": [{"path": p, "depth": d} for p, d in sorted_d[:15]],
        "leaf_count": len(no_deps),
        "total_with_deps": len([p for p in depths if depths[p] > 0]),
    }


def analyze_staleness(nodes, incoming, freshness, warnings=None):
    """Staleness x connectivity heatmap — świeżość z gita, budżet per typ encji.

    Pliki bez budżetu (huby wykluczone przez `status: archive`, drzewa wygaszone,
    encje write-once, deale spoza `pipeline/active/`) NIE wchodzą do rankingu ani do
    średnich — inaczej nagrobki i archiwum rozcieńczają sygnał.
    """
    today = date.today()
    results = []
    no_date = 0
    excluded = 0

    for path, node in nodes.items():
        status = node.get("status")
        node_type = node.get("type")
        budget_days = staleness_budget(path, node_type, node.get("type_source"), status)
        if budget_days is None:
            excluded += 1
            continue

        entry = freshness.get(path)
        if not entry:
            no_date += 1
            continue
        last_change = entry["date"]
        days = (today - last_change).days
        inc = len(incoming.get(path, set()))

        is_hub = path.replace(os.sep, "/") in HUBS
        staleness_ratio = round(days / budget_days, 2) if budget_days > 0 else 0

        # Priority score: ratio * connectivity (min 1 to rank isolated stale files)
        score = round(staleness_ratio * max(inc, 1), 2)

        results.append(
            {
                "path": path,
                "domain": node["domain"],
                "last_change": str(last_change),
                "last_change_source": entry["source"],
                "staleness_days": days,
                "type": node_type or "(brak typu)",
                "type_source": node.get("type_source"),
                "is_hub": is_hub,
                "budget_days": budget_days,
                "budget_source": "hub" if is_hub else ("type" if node_type else "default"),
                "staleness_ratio": staleness_ratio,
                "incoming_links": inc,
                "priority_score": score,
                "status": status,
            }
        )

    results.sort(key=lambda x: x["priority_score"], reverse=True)

    # Stats
    if results:
        avg_staleness = sum(r["staleness_days"] for r in results) / len(results)
        avg_ratio = sum(r["staleness_ratio"] for r in results) / len(results)
        avg_incoming = sum(r["incoming_links"] for r in results) / len(results)
    else:
        avg_staleness = avg_ratio = avg_incoming = 0

    sources = defaultdict(int)
    per_type = defaultdict(lambda: [0, 0])
    for r in results:
        sources[r["last_change_source"]] += 1
        label = "hub" if r["is_hub"] else r["type"]
        per_type[label][0] += 1
        if r["staleness_ratio"] > 1:
            per_type[label][1] += 1

    return {
        "freshness_source": dict(sources),
        "warnings": list(warnings or []),
        "scored_files": len(results),
        "excluded_from_staleness": excluded,
        "per_type": {k: {"files": v[0], "stale": v[1]} for k, v in sorted(per_type.items())},
        "stale_hubs": [
            {
                "path": r["path"],
                "staleness_days": r["staleness_days"],
                "staleness_ratio": r["staleness_ratio"],
            }
            for r in results
            if r["is_hub"] and r["staleness_ratio"] > 1
        ],
        "avg_staleness_days": round(avg_staleness, 1),
        "avg_staleness_ratio": round(avg_ratio, 2),
        "avg_incoming_links": round(avg_incoming, 1),
        "no_date": no_date,
        "top_30": results[:30],
    }


def analyze_bridges(nodes, outgoing):
    """Cross-domain connections and hub nodes."""
    links = []
    for path in nodes:
        src = nodes[path]["domain"]
        for target in outgoing.get(path, set()):
            if target in nodes:
                tgt = nodes[target]["domain"]
                if src != tgt:
                    links.append(
                        {
                            "source": path,
                            "source_domain": src,
                            "target": target,
                            "target_domain": tgt,
                        }
                    )

    # Domain pair counts
    pairs = defaultdict(int)
    for bl in links:
        pair = tuple(sorted([bl["source_domain"], bl["target_domain"]]))
        pairs[pair] += 1

    # Hub nodes (nodes connecting most domains)
    cross = defaultdict(set)
    for bl in links:
        cross[bl["source"]].add(bl["target_domain"])

    hubs = sorted(
        [
            {
                "path": p,
                "domain": nodes[p]["domain"],
                "connects_to": sorted(doms),
                "cross_links": len(doms),
            }
            for p, doms in cross.items()
        ],
        key=lambda x: x["cross_links"],
        reverse=True,
    )

    return {
        "total_cross_domain_links": len(links),
        "domain_pairs": {
            f"{a} <-> {b}": c
            for (a, b), c in sorted(
                pairs.items(), key=lambda x: x[1], reverse=True
            )
        },
        "hub_nodes": hubs[:15],
        "sample_links": links[:20],
    }


# --- Main ---


def run(vault_root, mode="full"):
    """Run analysis and return results dict."""
    vault_root = Path(vault_root)
    modules, all_paths = discover_vault(vault_root)
    type_globs = load_type_globs(vault_root)
    name_index = build_name_index(all_paths)
    nodes, inc, out, dang = build_graph(modules, all_paths, name_index, type_globs)

    type_counts = defaultdict(int)
    for n in nodes.values():
        type_counts[n["type"] or "(brak typu)"] += 1
    legacy_counts = defaultdict(int)
    for n in nodes.values():
        for f in n["legacy"]:
            legacy_counts[f] += 1

    stats = {
        "total_scanned_files": len(modules),
        "total_vault_files": len(all_paths),
        "domains": {
            d: len([p for p in nodes if nodes[p]["domain"] == d])
            for d in sorted(set(DOMAIN_MAP.values()))
        },
        "types": dict(sorted(type_counts.items())),
        "type_from_glob": len([n for n in nodes.values() if n["type_source"] == "glob"]),
        "without_type": len([n for n in nodes.values() if not n["type"]]),
        # Pola usunięte z kanonu 2.0 — niezerowa liczba = dług do sprzątnięcia
        "legacy_fields": dict(sorted(legacy_counts.items())),
        "total_edges": sum(len(v) for v in out.values()),
    }

    result = {"stats": stats}

    freshness, warnings = {}, []
    if mode in ("full", "orphans", "staleness"):
        freshness, warnings = build_freshness(vault_root, list(nodes.keys()), nodes)
        for w in warnings:
            print("WARN: %s" % w, file=sys.stderr)

    if mode in ("full", "orphans"):
        result["orphans"] = analyze_orphans(nodes, inc, freshness)
    if mode in ("full", "dangling"):
        result["dangling"] = analyze_dangling(dang)
    if mode in ("full", "clusters"):
        result["clusters"] = analyze_clusters(nodes, out, inc)
    if mode in ("full", "depth"):
        result["depth"] = analyze_depth(nodes, name_index, all_paths)
    if mode in ("full", "staleness"):
        result["staleness"] = analyze_staleness(nodes, inc, freshness, warnings)
    if mode in ("full", "bridges"):
        result["bridges"] = analyze_bridges(nodes, out)

    return result


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    mode = sys.argv[2] if len(sys.argv) > 2 else "full"
    data = run(root, mode)
    print(json.dumps(data, indent=2, default=str))
