---
name: graph
description: |
  Analyzes the knowledge graph of the Obsidian vault — orphans, dangling links, clusters, dependency depth, staleness heatmap, cross-domain bridges.
  Use when: checking vault health, finding disconnected modules, detecting broken links, understanding graph structure, identifying stale high-connectivity modules, finding cross-project bridges.
  Trigger phrases: "graph", "graph analysis", "vault health", "orphans", "dangling links", "broken links", "clusters", "staleness heatmap", "cross-domain bridges", "dependency depth", "connectivity", "analyze graph", "vault graph", "graph report"
---

# Graph Analysis

Analizujesz graf wiedzy Obsidian vault. Uruchamiasz skrypt Python, interpretujesz wyniki, proponujesz akcje.

Repo jest po polsku. Odpowiadaj po polsku.

---

## Quick Start

Uruchom skrypt:

```bash
python3 .claude/skills/graph/scripts/vault-graph.py . [mode]
```

Modes: `full` (default), `orphans`, `dangling`, `clusters`, `depth`, `staleness`, `bridges`

Skanowane drzewa: `1_receptionOS/`, `2_apolonia/`, `3_fte/`, `4_apollo/`, `_culture/`,
`osoby/`, `_sales/`, `_events/` (stała `GRAPH_DIRS` w skrypcie). `_events/` wchodzi tylko
jako źródło krawędzi (`owner:`/`osoby:`/`dotyczy:`) — jest write-once, więc nie liczy się
ani do orphanów, ani do staleness.

Wynik = JSON. Sformatuj go w czytelny raport po polsku.

---

## Tryby

Zidentyfikuj z kontekstu usera jaki tryb uruchomić:

| Fraza usera | Mode |
|-------------|------|
| "graph", "vault health", "full analysis" | `full` |
| "orphans", "orphanki", "osierocone" | `orphans` |
| "dangling", "broken links", "złamane linki" | `dangling` |
| "clusters", "klastry", "connectivity" | `clusters` |
| "depth", "głębokość", "łańcuchy" | `depth` |
| "staleness", "stale", "heatmap" | `staleness` |
| "bridges", "mosty", "cross-domain" | `bridges` |

Jeśli user nie podał trybu, uruchom `full`.

---

## Formatowanie raportu

### Po uruchomieniu skryptu, sformatuj wyniki wg poniższych szablonów:

### Stats (zawsze na górze)

```
VAULT GRAPH: X plików w grafie, Y krawędzi
Domeny: ROS (A), Apolonia (B), Fundacja (C), Culture (D), Osoby (E), Sales (F), Events (G)
Typy: modul (N), deal (N), osoba (N), event (N) — z globa: N, bez typu: N
```

Jeśli `legacy_fields` jest niepuste — dopisz linijkę „Dług legacy: `depends-on` N plików,
`sources` N, `cadence` N". To pola usunięte z kanonu 2.0; niezerowa liczba = do sprzątnięcia
(`sources:` legalne wyłącznie w `_transcripts/**-summary.md`, których graf nie skanuje).

### Orphans (pliki bez incoming links)

```
ORPHANS: X plików bez żadnych incoming links

Prawdziwe orphans (moduły z treścią, nie-styleguide):
- ścieżka (domain, type, status, last_change)

Oczekiwane (nowe pliki, drzewa celowo niezalinkowane jak _culture/team-private/):
- [lista]
```

Rozróżniaj prawdziwych orphanów (moduły które POWINNY być połączone) od oczekiwanych (np. nowo zaimportowane styleguide pliki, karty prywatne). Skrypt sam pomija indeksy, encje write-once (`event`/`spotkanie`/`log`) i `status: archive` — brak linków nie jest tam długiem. `last_change` to ta sama świeżość co w staleness (git, bez commitów `Meta: true`), nie frontmatterowe `updated:`.

### Dangling Links (wiki-links do nieistniejących plików)

```
DANGLING LINKS: X złamanych linków

| Źródło | Złamany link |
|--------|-------------|
```

Grupuj po pliku źródłowym. Zaproponuj fix: czy to literówka, brak pliku, czy zmieniona nazwa.

### Clusters

```
CLUSTERS: X komponentów (Y w głównym, Z izolowanych)

Główny komponent: X modułów
Izolowane: [lista]

TOP 15 MOST CONNECTED:
| # | Moduł | Out | In | Total | Domain |
```

### Depth (LEGACY)

Tryb liczy łańcuchy po `depends-on:` — polu **usuniętym z kanonu 2.0**. W posprzątanym
vaulcie `files_with_depends_on` = 0, więc sekcja jest pusta z definicji: **wtedy jej nie
drukuj**, napisz jedną linijkę „depth: brak `depends-on:` w vaulcie (pole poza kanonem)".
Raportuj tylko gdy licznik > 0 — i wtedy jako dług do usunięcia, nie jako strukturę.

```
DEPENDENCY DEPTH (legacy depends-on): max X poziomów, N plików z depends-on
Distribution: [0: A, 1: B, 2: C, ...]
Cycles: [lista jeśli są]

Najgłębsze łańcuchy:
- moduł (depth X) → [[cel]] → [[cel]] → ...
```

### Staleness Heatmap

Świeżość liczona **z gita, nie z frontmattera**: `last_change` = data ostatniego commita
dotykającego pliku, z pominięciem commitów z trailerem `Meta: true` (batche mechaniczne —
sweep, rename, lint-fix — nie odświeżają wiedzy). Kaskada źródeł (`last_change_source`):

1. `git` — kanon.
2. `frontmatter` — git nie zna pliku. Dwa przypadki: plik jeszcze niecommitowany **albo**
   plik, którego jedyne commity to batche `Meta: true`. W tym drugim batch szedł z
   `MC_SKIP_STAMP=1`, więc `updated:` bywa **starsze** niż faktyczne powstanie pliku —
   traktuj tę datę jako dolne oszacowanie, nie jako stamp.
3. `mtime` — vault nie jest repo gitowym; leci ostrzeżenie w `warnings` i na stderr.

Budżet dni (`budget_source`): **hub 7d** (whitelist `HUBS` — wygrywa z typem) · `modul` 60d ·
`osoba` 180d · `deal` 30d **tylko w `_sales/pipeline/active/`** · brak rozstrzygalnego typu 60d.
Typ bierze się z jawnego `type:`, a przy jego braku z globa `_schemas/map.yaml` →
`default-type` (`type_source`: `frontmatter` / `glob`). Progi to stałe na górze
`vault-graph.py` (`HUBS`, `HUB_STALENESS_DAYS`, `TYPE_STALENESS_DAYS`, `DEAL_ACTIVE_PREFIX`) —
tam je zmieniasz, nie w treści plików. Muszą się zgadzać z `_claude/9-automation/freshness.py`,
bo inaczej digest SessionStart i raport grafu mówią co innego.

**Poza sygnałem** (pole `excluded_from_staleness`, nie wchodzi do rankingu ani do średnich):
`status: archive`, drzewa wygaszone (`4_apollo/**`), encje write-once (`spotkanie`/`event`/`log`),
deale spoza `pipeline/active/`, ścieżki zmapowane w map.yaml na `null` (`_workspace`, `_claude`,
`_archive`). Nie filtrujesz tego ręcznie po fakcie — skrypt liczy to zanim posortuje.

`staleness_ratio` = `staleness_days / budget_days`, `priority_score` = ratio × incoming links.

```
STALENESS HEATMAP: N plików w rankingu (M poza sygnałem)
avg X ratio, avg Y dni, avg Z incoming links
Źródło świeżości: git (N) / frontmatter (M) / mtime (K)
Per typ: hub A/B stale · modul A/B · osoba A/B · deal A/B

TOP 30 (staleness ratio x connectivity):
Kolor wg ratio: ✅ <0.5 fresh | 🟡 0.5-1.0 aging | 🟠 1.0-2.0 stale | 🔴 >2.0 critical

| # | Score | Ratio | Typ | Budżet | Dni | Links | Moduł | Domain | Status |
```

Huby ze `stale_hubs` wypisz **osobno, na górze sekcji** — 7-dniowy budżet znaczy, że każdy
z nich to zadanie na dziś, nie pozycja w długim rankingu. Poza tym flaguj wszystko z
ratio > 1.0 jako reweave candidates. Jeśli `warnings` jest niepuste (brak gita → mtime,
albo ścieżki gita nie pasują do vaulta), powiedz to wprost — wtedy staleness jest zaniżona
i nie ufaj rankingowi.

### Bridges

```
CROSS-DOMAIN BRIDGES: X linków cross-domain

Domain pairs:
| Pair | Links |
|------|-------|

TOP HUB NODES (łączą najwięcej domen):
| Moduł | Domain | Łączy z |
```

---

## Akcje po raporcie

Po wyświetleniu raportu, zaproponuj actionable next steps:

1. **Stale huby (`stale_hubs`)** → "Odświeżyć hub X (Nd / budżet 7d)?" — priorytet nad resztą
2. **Orphans z treścią** → "Dodać linki z odpowiednich index files?"
3. **Dangling links** → "Naprawić X złamanych linków?" (pokaż propozycje fixów)
4. **Staleness ratio > 1.0** → "Uruchomić `/reweave` na top kandydatach?"
5. **Izolowane klastry** → "Sprawdzić czy te moduły powinny być połączone z głównym grafem?"
6. **Brak frontmatter** → "Uzupełnić brakujące `type:` i `status:` w X plikach?" (`updated:` stampuje pre-commit — nigdy nie wpisuj go ręcznie)
7. **Dług legacy** (`legacy_fields` > 0) → "Usunąć `depends-on:`/`cadence:`/`sources:` z X plików?"

Pytaj usera o decyzję. Nie wykonuj automatycznie.

---

## Obsługa błędów

| Problem | Rozwiązanie |
|---------|-------------|
| Skrypt nie działa | Sprawdź `python3 --version`, sprawdź ścieżkę |
| Brak modułów | Upewnij się że foldery z `GRAPH_DIRS` (1_receptionOS/, 2_apolonia/, 3_fte/, _culture/, osoby/, _sales/, _events/) istnieją |
| `warnings`: git nie zna plików | Vault jest podkatalogiem repo albo innym worktree — sprawdź `git -C <vault> rev-parse --show-prefix`; do czasu fixu staleness jest zaniżona |
| Za dużo orphanów | Sprawdź czy nowe pliki (np. styleguide import) nie zaburzają wyniku — filtruj oczekiwane orphany |
| JSON parse error | Skrypt wypisuje na stdout — sprawdź czy stderr nie zaśmieca output |
