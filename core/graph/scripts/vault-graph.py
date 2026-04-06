#!/usr/bin/env python3
"""vault-graph.py — Knowledge graph analysis for Obsidian vault.

Usage:
  python3 vault-graph.py <vault_root> [mode]

Modes:
  full       — all analyses (default)
  orphans    — modules with no incoming links
  dangling   — wiki-links pointing to non-existent files
  clusters   — connected components and bridge nodes
  depth      — dependency chain depth analysis
  staleness  — staleness x connectivity heatmap
  bridges    — cross-domain connections
"""

import os
import re
import sys
import json
from collections import defaultdict
from datetime import datetime, date
from pathlib import Path

# --- Configuration ---

MODULE_DIRS = {"1_receptionOS", "2_apolonia", "3_fte", "4_apollo", "_culture"}
SKIP_WALK = {".git", ".obsidian", "node_modules"}
DOMAIN_MAP = {
    "1_receptionOS": "ROS",
    "2_apolonia": "Apolonia",
    "3_fte": "Fundacja",
    "4_apollo": "Apollo",
    "_culture": "Culture",
}

# --- Cadence system ---

CADENCE_RE = re.compile(r"^cadence:\s*(\S+)", re.MULTILINE)
CADENCE_DAYS = {"hot": 7, "tactical": 30, "iron-cold": 60, "frozen": 99999}
DEFAULT_CADENCE = "tactical"

# --- Regex patterns ---

WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)\\?\|[^\]]+\]\]|\[\[([^\]]+?)\]\]")
UPDATED_RE = re.compile(r"^updated:\s*(\d{4}-\d{2}-\d{2})", re.MULTILINE)
STATUS_RE = re.compile(r"^status:\s*(\S+)", re.MULTILINE)
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

    m = CADENCE_RE.search(fm)
    if m:
        result["cadence"] = m.group(1)

    # depends-on: list of [[links]]
    deps_block = re.search(r"depends-on:\s*\n((?:\s+-\s+.*\n)*)", fm)
    if deps_block:
        result["depends_on"] = extract_wikilinks(deps_block.group(1))
    else:
        deps_inline = re.search(r"depends-on:\s*\[([^\]]*)\]", fm)
        if deps_inline:
            result["depends_on"] = extract_wikilinks(deps_inline.group(1))
        else:
            result["depends_on"] = []

    # sources: [list]
    src = re.search(r"sources:\s*\[([^\]]*)\]", fm)
    if src:
        raw = src.group(1)
        wl = extract_wikilinks(raw)
        if wl:
            result["sources"] = wl
        else:
            result["sources"] = [
                s.strip().strip('"').strip("'")
                for s in raw.split(",")
                if s.strip()
            ]
    else:
        result["sources"] = []

    return result


def extract_body_links(content):
    """Extract wiki-links from body text (excluding frontmatter and code blocks)."""
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            content = content[end + 4:]
    content = CODE_BLOCK_RE.sub("", content)
    return extract_wikilinks(content)


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

            if top_dir in MODULE_DIRS:
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


def build_graph(modules, all_paths, name_index):
    """Build the knowledge graph from module files."""
    nodes = {}
    incoming = defaultdict(set)  # target -> {sources}
    outgoing = defaultdict(set)  # source -> {targets}
    dangling = defaultdict(list)  # source -> [unresolved links]

    for path, content in modules.items():
        fm = parse_frontmatter(content)
        body_links = extract_body_links(content)
        top_dir = path.split(os.sep)[0]

        nodes[path] = {
            "updated": fm.get("updated"),
            "status": fm.get("status"),
            "cadence": fm.get("cadence", DEFAULT_CADENCE),
            "depends_on": fm.get("depends_on", []),
            "sources": fm.get("sources", []),
            "domain": DOMAIN_MAP.get(top_dir, "Other"),
        }

        # All structural links (depends-on + body wiki-links)
        source_dir = str(Path(path).parent)
        all_links = set(body_links + fm.get("depends_on", []))
        for link in all_links:
            resolved = resolve_link(link, name_index, all_paths, source_dir)
            if resolved:
                for target in resolved:
                    if target in modules:  # Only count edges to module files
                        incoming[target].add(path)
                        outgoing[path].add(target)
            else:
                # Skip non-md targets (audio files, yaml, directories)
                if any(link.endswith(ext) for ext in (".m4a", ".mp3", ".yaml", ".py")):
                    continue
                dangling[path].append(link)

    return nodes, incoming, outgoing, dangling


# --- Analysis functions ---


def analyze_orphans(nodes, incoming):
    """Modules with zero incoming links from other modules."""
    orphans = []
    for path, node in nodes.items():
        if "_index" in path:
            continue  # Index files are entry points
        inc = len(incoming.get(path, set()))
        if inc == 0:
            orphans.append(
                {
                    "path": path,
                    "domain": node["domain"],
                    "status": node.get("status"),
                    "updated": str(node["updated"]) if node.get("updated") else None,
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
    """Dependency chain depth via depends-on."""
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
        "max_depth": sorted_d[0][1] if sorted_d else 0,
        "depth_distribution": dict(sorted(dist.items())),
        "cycles": cycles[:10],
        "deepest": [{"path": p, "depth": d} for p, d in sorted_d[:15]],
        "leaf_count": len(no_deps),
        "total_with_deps": len([p for p in depths if depths[p] > 0]),
    }


def analyze_staleness(nodes, incoming):
    """Staleness x connectivity heatmap (cadence-aware, ratio-based)."""
    today = date.today()
    results = []

    for path, node in nodes.items():
        if not node.get("updated"):
            continue
        days = (today - node["updated"]).days
        inc = len(incoming.get(path, set()))

        cadence = node.get("cadence", DEFAULT_CADENCE)
        cadence_days = CADENCE_DAYS.get(cadence, 30)
        staleness_ratio = round(days / cadence_days, 2) if cadence_days > 0 else 0

        # Priority score: ratio * connectivity (min 1 to rank isolated stale files)
        score = round(staleness_ratio * max(inc, 1), 2)

        results.append(
            {
                "path": path,
                "domain": node["domain"],
                "updated": str(node["updated"]),
                "staleness_days": days,
                "cadence": cadence,
                "cadence_days": cadence_days,
                "staleness_ratio": staleness_ratio,
                "incoming_links": inc,
                "priority_score": score,
                "status": node.get("status"),
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

    return {
        "avg_staleness_days": round(avg_staleness, 1),
        "avg_staleness_ratio": round(avg_ratio, 2),
        "avg_incoming_links": round(avg_incoming, 1),
        "no_date": len([p for p in nodes if not nodes[p].get("updated")]),
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
    name_index = build_name_index(all_paths)
    nodes, inc, out, dang = build_graph(modules, all_paths, name_index)

    stats = {
        "total_modules": len(modules),
        "total_vault_files": len(all_paths),
        "domains": {
            d: len([p for p in nodes if nodes[p]["domain"] == d])
            for d in sorted(set(DOMAIN_MAP.values()))
        },
        "with_depends_on": len([n for n in nodes.values() if n["depends_on"]]),
        "with_sources": len([n for n in nodes.values() if n["sources"]]),
        "total_module_edges": sum(len(v) for v in out.values()),
    }

    result = {"stats": stats}

    if mode in ("full", "orphans"):
        result["orphans"] = analyze_orphans(nodes, inc)
    if mode in ("full", "dangling"):
        result["dangling"] = analyze_dangling(dang)
    if mode in ("full", "clusters"):
        result["clusters"] = analyze_clusters(nodes, out, inc)
    if mode in ("full", "depth"):
        result["depth"] = analyze_depth(nodes, name_index, all_paths)
    if mode in ("full", "staleness"):
        result["staleness"] = analyze_staleness(nodes, inc)
    if mode in ("full", "bridges"):
        result["bridges"] = analyze_bridges(nodes, out)

    return result


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    mode = sys.argv[2] if len(sys.argv) > 2 else "full"
    data = run(root, mode)
    print(json.dumps(data, indent=2, default=str))
