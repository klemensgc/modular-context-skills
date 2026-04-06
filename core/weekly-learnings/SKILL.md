---
name: weekly-learnings
description: |
  Compiles the week's insights from session logs, transcripts, and module changes into a single
  writing-ready operational summary. Not for sharing — for your own review and continuity.
  Use when: wrapping up a week, wanting to see what happened and what carried over, doing
  a weekly review, preparing context for next week's planning.
  Trigger phrases: "weekly learnings", "weekly summary", "tygodniowe podsumowanie",
  "podsumowanie tygodnia", "week in review", "co było w tym tygodniu", "weekly recap"
---

# Weekly Learnings

Kompiluje tygodniowe insights z vault w jedno operacyjne podsumowanie — dla siebie, nie do sharing.

Repo jest po polsku. Odpowiadaj po polsku.

**Kluczowa różnica:** `/weekly-learnings` = OPERATIONAL review dla siebie (co się stało, co dalej). `/learned` = POLISHED post do sharing (refleksje, insights).

---

## Quick Start

1. Określ tydzień (bieżący default)
2. Zbierz dane: session logs, transkrypcje, module updates, quest board
3. Skompiluj 6 sekcji: Kontekst / Co się wydarzyło / Co zrobiono / Czego się nauczyłem / Co nie wyszło / Na przyszły tydzień
4. Zapisz do `_workspace/`

---

## Workflow

### Krok 1: Określ tydzień

Domyślnie: bieżący tydzień. Jeśli argument podany — parsuj:
- `last` → poprzedni tydzień
- `wNN` → konkretny tydzień (np. `w8`)

Oblicz date range: poniedziałek → niedziela.

### Krok 2: Zbierz dane tygodnia

Przeczytaj równolegle:

**Session logs:**
- `_claude/4-sessions/YYYY-MM/session-YYYY-MM-DD-*.md` — filtruj po datach tygodnia
- Wyciągnij: co zrobiono, jakie pliki zmienione, key outcomes

**Transkrypcje:**
- `_transcripts/` — pliki z datą w nazwie matching the week
- Wyciągnij: tematy spotkań, kluczowe ustalenia, decyzje

**Module updates:**
- Grep `updated: YYYY-MM-DD` for dates in the week
- Zanotuj: które moduły zmienione i w jakim projekcie

**Quest board:**
- Przeczytaj quest-board obowiązujący w tym tygodniu
- Porównaj: plan vs reality

**Backlog:**
- Ile transkrypcji czekało na początku tygodnia? Ile teraz?

### Krok 3: Skompiluj podsumowanie

```
WEEKLY SUMMARY — Week [WNN], [data start] → [data end]

## Kontekst
[Quest board na ten tydzień — main quest + side quests.
2-3 zdania o planowanych priorytetach.]

## Co się wydarzyło
[Key events, meetings, conversations z transkrypcji.
Bulleted list, max 10 items. Grouped by project.]

- **ROS:** [events]
- **Apolonia:** [events]
- **Fundacja:** [events]
- **Inne:** [events]

## Co zrobiono
[Deliverables, pliki created/updated z session logów.
Bulleted list z linkami do plików.]

- [plik1.md] — [co zmieniono]
- [plik2.md] — [co zmieniono]
- Session count: [N] sesji Claude Code

## Czego się nauczyłem
[3-5 key insights z tego tygodnia.
Każdy: 1-2 zdania, grounded w konkretnej sytuacji.]

1. [Learning — z jakiej sytuacji]
2. [Learning]
3. [Learning]

## Co nie wyszło
[Plans from quest board that didn't happen.
Blockers, surprises, delays. Honest assessment.]

- [Plan X] — nie wyszło bo [powód]
- [Plan Y] — częściowo, brakuje [co]

## Na przyszły tydzień
[Co carries over? Co nowego?
Sugestie priorytetów na bazie tego co widzę w vault.]

- Carry over: [items]
- New: [items from recent discoveries]
- Backlog: [N] transkrypcji czeka (trend: ↑/↓/→)
```

### Krok 4: Zapisz

Zapisz do: `_workspace/{YYYY-MM}/wN/weekly-learnings-wNN.md`

Gdzie:
- `YYYY-MM` = miesiąc tygodnia
- `wN` = tydzień miesiąca (w1: 1-7, w2: 8-14, w3: 15-21, w4: 22-31)
- `wNN` = numer tygodnia roku (np. w08)

---

## Arguments

| Argument | Co robi |
|----------|---------|
| (none) | Bieżący tydzień (default) |
| `last` | Poprzedni tydzień |
| `wNN` | Konkretny tydzień roku (np. `w08`) |

---

## Troubleshooting

| Problem | Rozwiązanie |
|---------|-------------|
| Brak session logów z tygodnia | Bazuj na transkrypcjach + module updates. Zaznacz: "Brak session logów — podsumowanie niepełne." |
| Brak quest boardu | Skip sekcję "Kontekst". Zbierz priorytety z session logów (often mentioned). |
| Tydzień bez aktywności | To też insight: "Cichy tydzień. Żadnych session logów, 0 module updates." Zaproponuj /pulse. |
| Overlap z /learned | /weekly-learnings = operational review (CO się stało). /learned = polished writing (CO ZROZUMIAŁEM). Inne cele, inne formaty. |
| Overlap z /7plan | /weekly-learnings patrzy WSTECZ (review). /7plan patrzy DO PRZODU (plan). Komplementarne: weekly-learnings → 7plan. |
| Overlap z /log | /log zamyka SESJĘ (1 session). /weekly-learnings zamyka TYDZIEŃ (all sessions). |
