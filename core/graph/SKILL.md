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
VAULT GRAPH: X modułów, Y krawędzi
Domeny: ROS (A), Apolonia (B), Fundacja (C), Culture (D)
depends-on: X plików, sources: Y plików
```

### Orphans (moduły bez incoming links)

```
ORPHANS: X modułów bez żadnych incoming links

Prawdziwe orphans (moduły z treścią, nie-styleguide):
- ścieżka (domain, status, updated)

Styleguide/asset orphans (oczekiwane, nowe pliki):
- [lista]
```

Rozróżniaj prawdziwych orphanów (moduły które POWINNY być połączone) od oczekiwanych (np. nowo zaimportowane styleguide pliki).

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

### Depth

```
DEPENDENCY DEPTH: max X poziomów
Distribution: [0: A, 1: B, 2: C, ...]
Cycles: [lista jeśli są]

Najgłębsze łańcuchy:
- moduł (depth X) → depends-on → depends-on → ...
```

### Staleness Heatmap

```
STALENESS HEATMAP: avg X ratio, avg Y dni, avg Z incoming links

TOP 30 (staleness ratio x connectivity):
Kolor wg ratio: ✅ <0.5 fresh | 🟡 0.5-1.0 aging | 🟠 1.0-2.0 stale | 🔴 >2.0 critical

| # | Score | Ratio | Cadence | Dni | Links | Moduł | Domain | Status |
```

Flaguj moduły z ratio > 1.0 jako reweave candidates.

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

1. **Orphans z treścią** → "Dodać linki z odpowiednich index files?"
2. **Dangling links** → "Naprawić X złamanych linków?" (pokaż propozycje fixów)
3. **Staleness ratio > 1.0** → "Uruchomić `/reweave` na top kandydatach?"
4. **Izolowane klastry** → "Sprawdzić czy te moduły powinny być połączone z głównym grafem?"
5. **Brak frontmatter** → "Dodać brakujące `updated:` i `status:` do X plików?"

Pytaj usera o decyzję. Nie wykonuj automatycznie.

---

## Obsługa błędów

| Problem | Rozwiązanie |
|---------|-------------|
| Skrypt nie działa | Sprawdź `python3 --version`, sprawdź ścieżkę |
| Brak modułów | Upewnij się że foldery 1_receptionOS/, 2_apolonia/, 3_fte/, _culture/ istnieją |
| Za dużo orphanów | Sprawdź czy nowe pliki (np. styleguide import) nie zaburzają wyniku — filtruj oczekiwane orphany |
| JSON parse error | Skrypt wypisuje na stdout — sprawdź czy stderr nie zaśmieca output |
