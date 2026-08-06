---
name: tasklist
description: |
  Transforms weekly plan (main quest + side quests) into actionable Claude Code session starters.
  Each task includes objective, context files, suggested prompt, deliverables, and recipient.
  Deep dives into modular-context repo to ground each session in current state.
  Use when: starting a new week, planning Claude Code sessions, converting quest board to execution plan,
  organizing weekly priorities into concrete work sessions.
  Trigger phrases: "tasklist", "weekly plan", "plan tygodnia", "session plan", "co robić ten tydzień",
  "rozplanuj tydzień", "weekly sessions", "plan sesji", "rozpisz taski"
---

# Tasklist — Weekly Session Planner

Transformuje surowy plan tygodnia w structured Claude Code session starters aligned z modular-context.

---

## Quick Start

1. User wkleja plan tygodnia (main quest + side quests, items z checkmarkami = done)
2. Określ week number (domyslnie: biezacy tydzien)
3. Deep dive: czytaj relevant pliki z repo per item
4. Wygeneruj `_tasklist/2026/week-2026-WNN.md` z session starters
5. Kazdy task = self-contained prompt gotowy do uruchomienia w Claude Code

---

## Workflow

### Krok 1: Przyjmij plan

User wkleja plan w dowolnym formacie. Szukaj struktury:
- **Main quest** — glowny thrust tygodnia (moze miec sub-items)
- **Side quests** — mniejsze taski
- Items oznaczone checkmarkiem = done, przenies do Completed

Parsuj na liste surowych itemow. Zachowaj hierarchie (main quest sub-items sa wazniejsze niz side quests).

### Krok 2: Klasyfikuj kazdy item

| Pole | Opcje |
|------|-------|
| **Projekt** | ROS / Apolonia / Fundacja / Culture / Cross-project |
| **Typ** | `claude-session` / `human-action` / `delegated` |
| **Effort** | Quick (15min) / Medium (30-60min) / Deep (1h+) |
| **Priority** | critical / high / medium / backlog |

Reguly klasyfikacji:
- Zakupy, rezerwacje, fizyczne akcje → `human-action`
- Kontakt z konkretna osoba bez prep work → `human-action`
- Czekamy na kogos → `delegated`
- Trzeba przygotowac material przed kontaktem → `claude-session` (prep) + `human-action` (wyslij)
- Research, dokument, strategia, plan, update modulu → `claude-session`
- Done items → Completed

### Krok 3: Deep dive per item

Dla kazdego `claude-session` itemu:

1. **Dopasuj projekt** → otworz `{projekt}_index.md`
2. **Znajdz relevant moduly** po keywords z itemu
3. **Przeczytaj 2-4 kluczowe pliki** zeby zrozumiec current state
4. **Sprawdz swiezosc z git log** (`git log -1 --format=%ad --date=short -- <plik>`) — prog per typ:
   hub 7 dni, `modul` 60, `osoba` 180, `deal` 30 (tylko `pipeline/active/`). Commity z trailerem
   `Meta: true` sie nie licza. Nie czytaj daty z pola `updated:`
5. **Sprawdz wiki-linki w tresci + krawedzie `owner:` / `osoby:` / `dotyczy:`** → follow the chain do powiazanych plikow
6. **Jesli brak modulu** → sprawdz `_transcripts/` i `_transcripts-backlog/`
7. **Zidentyfikuj gap:** co jest w repo vs co user chce osiagnac
8. **Sformuluj concrete deliverable(s)** — pliki do stworzenia lub aktualizacji

### Krok 4: Generuj session starters

Dla kazdego `claude-session` itemu, wygeneruj blok:

```markdown
### T{N}: [Concrete, SMART-ish name]

**Cel:** [1 zdanie — co dokladnie produkujemy]
**Projekt:** [ROS / Apolonia / Fundacja / Culture]
**Effort:** [Quick / Medium / Deep]

**Context files:**
- `path/to/file1.md` — [dlaczego relevant, 3-5 slow]
- `path/to/file2.md` — [dlaczego relevant]

**Sesja Claude Code:**

> [Prompt do wklejenia w Claude Code. Zasady:
> - Self-contained — nie wymaga dodatkowego kontekstu
> - Zaczyna od deliverable: "Stworz/Zaktualizuj plik X"
> - Sekwencyjny: "1. Przeczytaj... 2. Zidentyfikuj... 3. Stworz..."
> - Konczy definicja done]

**Deliverables:**
- [ ] `output-file.md` — [opis]
- [ ] Update `existing-file.md` — [co zmienic]

**Send to / Apply:**
- [Osoba] via [kanal] — [co z tym zrobia]
- LUB: Commit do repo
```

Zasady promptow:
- Zaczynaj od concrete output, nie od "zbadaj"
- Referencuj specific repo files: "Przeczytaj [[1_receptionOS/4-go-to-market/pipeline]] i [[roadmap]]"
- Definiuj done: "Deliverable: zaktualizowany pipeline.md z sekcja Z"
- Low friction: male pliki, updates istniejacych, nie nowe systemy
- Jesli task wymaga >5 plikow, rozdziel na 2 sesje

### Krok 5: Compose weekly file

Zloz plik `_tasklist/2026/week-2026-WNN.md`:

```markdown
---
title: Week 2026-WNN (DD-DD.MM)
type: log
data: YYYY-MM-DD
agent: /tasklist
week-start: YYYY-MM-DD
week-end: YYYY-MM-DD
---

# Week WNN (DD-DD.MM.YYYY)

**Main Quest:** [z planu usera, 1-2 zdania]

**Links:** [[_tasklist/tasklist_index|Dashboard]] | [[1_receptionOS/8-strategy/quest-board-wNN|Quest Board]]

---

## Critical Path Sessions

[T1-T3: najwazniejsze claude-session taski z main quest]

---

## Side Quest Sessions

[T4+: claude-session taski z side quests, posortowane effort: quick first]

---

## Human Actions

- [ ] [Item] — [kontekst, kto, kiedy]

---

## Delegated / Waiting

- [ ] [Item] 👤 [Osoba] — [czekamy na co]

---

## Done

- [x] [Items oznaczone checkmarkiem z input]

---

## Week Notes

**Stale files detected:** [pliki bez merytorycznego commita ponad prog swojego typu — z git log, nie z frontmattera]
**Missing modules:** [tematy bez dedykowanego pliku w repo, jesli sa]
**Suggested first session:** T[N] — [dlaczego zaczynac od tego]
```

Plik tygodniowy jest write-once → `type: log`, wiec `data:` i `agent:` sa **wymagane**
(`_schemas/log.yaml`); bez nich `schema_lint.py` daje 2 FAIL i blokuje commit. `status:` nie jest
polem typu `log` — nie dopisuj. Uwaga: `_tasklist/**` nie figuruje ani w `map.yaml` →
`default-type`, ani w `log.yaml` → `location`, wiec jawny `type: log` jest tu jedyna rzecza,
ktora nadaje plikowi typ. Sprawdz przed pokazaniem:
`python3 _claude/9-automation/schema_lint.py _tasklist/2026/week-2026-WNN.md` → 0 FAIL.

### Krok 6: Podsumowanie

Po wygenerowaniu pliku, wyswietl userowi:

1. Ile sesji Claude Code (critical + side)
2. Ile human actions
3. Ile delegated
4. Suggested order: ktora sesje odpalic pierwsza i dlaczego
5. Stale files / missing modules jesli wykryto

---

## Item decomposition rules

Jesli item jest zbyt duzy na 1 sesje (np. "Full strategy revamp"), rozloz go:

1. Zidentyfikuj sub-deliverables
2. Kazdy sub-deliverable = osobna sesja (T1a, T1b, T1c)
3. Zachowaj zaleznosci: T1b.context moze referencowac output T1a
4. Oznaczy w sesji: "Wymaga wczesniejszego T1a"

Jesli item jest zbyt maly na sesje (np. "wyslij maila do X"), to nie jest `claude-session`:
- Jesli wymaga prep work → `claude-session` (prep) + `human-action` (wyslij)
- Jesli nie → `human-action`

---

## Troubleshooting

| Problem | Rozwiazanie |
|---------|-------------|
| Za duzo sesji (>10) | Merge related items, priorytetyzuj top 5 critical |
| Item niejasny | Zapytaj usera zamiast zgadywac |
| Brak relevant pliku w repo | Zanotuj w "Missing modules", zaproponuj stub creation jako osobny task |
| Stale context files | Oznacz w Week Notes, zaproponuj update jako T0 (pre-session) |
| Item jest zarowno claude + human | Rozdziel: prep session (claude) + execution (human) |
| Duzy main quest z wieloma sub-items | Decompose na T1a/T1b/T1c z zaleznosciami |
| Side quest nie pasuje do zadnego projektu | Przypisz do Cross-project, oznacz context files jesli sa |
