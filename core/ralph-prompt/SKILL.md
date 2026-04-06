---
name: ralph-prompt
description: |
  Prepares structured prompts for the Ralph Wiggum autonomous loop plugin, optimized for this knowledge base.
  Asks what the user wants to achieve, analyzes the repo, and generates a ready-to-paste Ralph prompt
  with phased iteration plan, completion criteria, search patterns, and self-correction guidelines.
  Use when: preparing a Ralph loop task, building a knowledge mining prompt, creating an autonomous
  research prompt, setting up iterative transcript processing, or any multi-iteration autonomous task.
  Trigger phrases: "ralph prompt", "ralph-prompt", "przygotuj prompt do ralpha", "nowy ralph",
  "prompt dla ralph loop", "autonomiczny prompt", "mining prompt", "iteracyjny prompt"
---

# Ralph Prompt Builder

Interaktywny wizard do budowania promptow dla Ralph Wiggum autonomous loop.
Generuje prompt zgodny z syntaxem pluginu i zapisuje do `_claude/6-prompts/`.

---

## Workflow

### Krok 1: Zbierz cel

Zapytaj usera:

**"Co Ralph ma osiagnac? Opisz zadanie w 1-3 zdaniach."**

Przyklady celow w tym repo:
- Zbudowac/zaktualizowac folder wiedzy (jak ralph-apolonia)
- Wyminowac transkrypcje pod katem tematu (jak ralph-culture)
- Zaktualizowac moduly na podstawie nowych transkrypcji
- Zrobic deep research w transkrypcjach
- Zrestrukturyzowac istniejacy folder

### Krok 2: Zidentyfikuj typ zadania

Na podstawie odpowiedzi usera, dopasuj do jednego z typow:

| Typ | Opis | Przykladowy istniejacy prompt |
|-----|-------|-------------------------------|
| **Knowledge Builder** | Zbuduj folder wiedzy od zera | `ralph-apolonia.md` |
| **Deep Mining** | Wyekstrahuj implicit knowledge z transkryptow | `ralph-culture-stage1.md` |
| **Quality Control** | Audytuj, weryfikuj, napraw istniejace pliki | `ralph-culture-stage3.md` |
| **Enrichment** | Uzupelnij istniejacy folder o nowe zrodla | `ralph-culture-stage2.md` |
| **Custom** | Inny typ — user opisze | (nowy) |

Powiedz userowi ktory typ rozpoznales i zapytaj czy sie zgadza.

### Krok 3: Zmapuj kontekst repo

Zanim wygenerujesz prompt, MUSISZ zbadac stan repo:

1. **Przeczytaj odpowiedni index file** z CLAUDE.md:
   - ROS: `1_receptionOS/1_receptionOS_index.md`
   - Apolonia: `2_apolonia/2_apolonia_index.md`
   - Fundacja: `3_fte/3_fte_index.md`
   - Culture: `_culture/culture_index.md`

2. **Sprawdz dostepne transkrypcje:**
   - Przeszukaj `_transcripts/` i `_transcripts-backlog/` pod katem relevantu
   - Policz ile plikow jest w kazdej relevantnej kategorii
   - Zanotuj jakie grep patterns beda potrzebne

3. **Sprawdz istniejace pliki docelowe:**
   - Czy folder docelowy istnieje?
   - Jakie pliki juz sa? W jakim stanie (status, updated)?
   - Co trzeba zbudowac vs zaktualizowac?

4. **Przedstaw userowi findings:**
   - "Znalazlem X transkryptow w Y kategoriach"
   - "Folder docelowy ma Z plikow, W stubbow"
   - "Proponuje N iteracji"

Zapytaj usera:
- Czy scope jest dobry?
- Ile iteracji? (default: 15-20)
- Jakie completion criteria?

### Krok 4: Wygeneruj prompt

Uzyj ponizszego szablonu. KAZDA sekcja jest wymagana.

---

## Szablon Ralph Prompt

```markdown
---
title: [Tytul zadania]
updated: [YYYY-MM-DD]
status: active
audience: [all]
depends-on: []
---
# [Tytul zadania]

## Task: [Jednoliniowy opis]

[2-3 zdania kontekstu: co robimy, dlaczego, jaki output]

---

## Source Material Location

All transcripts are in: `/Users/kubagasienica/Desktop/all-transcripts/`

Key directories to scan:
[Lista konkretnych folderow z opisem co w nich jest]

---

## Iterative Work Plan ([N] Loops)

### Phase 1: [Nazwa] (Iterations 1-X)

**Iteration 1:** [Konkretne zadanie]
- [Krok 1]
- [Krok 2]
- [Krok 3]
- Update `_progress.md`

**Iteration 2:** [Konkretne zadanie]
...

### Phase 2: [Nazwa] (Iterations X-Y)
...

### Phase [N]: Finalization (Iterations Z-[max])

**Iteration [max-1]:** Quality Check
- Read through all created files
- Verify sources are cited
- Check for contradictions
- Ensure consistent formatting
- Fix any issues found

**Iteration [max]:** Final Compilation
- [Ostatnie kroki]
- Ask user: "Usunac `_progress.md`? (zawiera audit trail calego runa)"
- If user says yes: delete `_progress.md`
- If user says no: keep for reference
- If complete, output: `<promise>[PROMISE_NAME]</promise>`
- **After promise:** Rename prompt file to done:
  `git mv _claude/6-prompts/ralph-{temat}.md _claude/6-prompts/done/done--ralph-{temat}.md`

---

## Target [Folder Structure / Output]

```
[Docelowa struktura folderow/plikow]
```

---

## [Template / Format] (jesli dotyczy)

[Szablon dla tworzonych plikow, jesli Ralph ma tworzyc wiele plikow tego samego typu]

---

## Completion Criteria

Before outputting the completion promise, verify:

- [ ] [Kryterium 1]
- [ ] [Kryterium 2]
- [ ] [Kryterium 3]
- [ ] `_progress.md` cleanup — user asked whether to keep or delete
...

---

## Self-Correction Guidelines

Each iteration:
1. Read `_progress.md` to see what was done before
2. [Kontekstowe wskazowki dla tego zadania]
3. If stuck:
   - Document the blocker in `_progress.md`
   - Move to next iteration
   - Return with fresh approach

If after [70% iteracji] iterations progress is stalled:
- Document all blockers
- List alternative approaches tried
- Complete what is possible
- Output completion promise with partial flag

---

## Key Search Patterns

```bash
[Konkretne grep patterns relevantne do zadania]
```

---

## START

Begin with Iteration 1. Read this prompt fully, then execute the iteration plan.

Track your progress in `_progress.md` after each iteration.

When all criteria are met, output:

```
<promise>[PROMISE_NAME]</promise>
```
```

---

## Zasady generowania

### Nazewnictwo pliku
- Format: `ralph-{temat}.md` (np. `ralph-ros-pipeline.md`)
- Jesli jest wiele stage'ow: `ralph-{temat}-stage{N}.md`

### Promise name
- SCREAMING_SNAKE_CASE
- Format: `{TEMAT}_{TYP}_COMPLETE` (np. `ROS_PIPELINE_MINING_COMPLETE`)

### Iteracje
- Kazda iteracja = 1 konkretny, zamkniety task
- Kazda iteracja konczy sie "Update `_progress.md`"
- Iteracje pogrupowane w fazy (3-5 faz)
- Ostatnia iteracja ZAWSZE = final compilation + promise output

### Search patterns
- Uzyj `grep -ri` syntax (to co Ralph bedzie widzial w prompcie)
- Patterns po polsku I angielsku (repo jest dwujezyczne)
- Pogrupuj per temat

### Self-correction
- ZAWSZE wlacz `_progress.md` tracking
- ZAWSZE wlacz escape hatch (co robic gdy utkniesz)
- ZAWSZE wlacz quality check iteration przed finalem

### Post-completion (auto-rename)
- ZAWSZE dodaj na KONIEC ostatniej iteracji (po `<promise>`):
  ```
  - **After promise:** Rename this prompt to done:
    `git mv _claude/6-prompts/ralph-{temat}.md _claude/6-prompts/done/done--ralph-{temat}.md`
  ```
- Konwencja: `done--` prefix (podwojne myslniki) + przeniesienie do `done/`
- Prompt file po wykonaniu NIE powinien zostac w rootcie `6-prompts/`

### Source material
- ZAWSZE podaj pelne sciezki absolutne (zaczynajace od `/Users/kubagasienica/`)
- ZAWSZE wymien konkretne foldery transkrypcji
- NIGDY nie zakladaj ze transkrypty istnieja — Ralph musi zweryfikowac

---

## Krok 5: Zapisz i pokaz

1. Zapisz prompt do `_claude/6-prompts/ralph-{temat}.md`
2. Wyswietl pelny prompt w konsoli
3. Podaj userowi gotowa komende:
   ```
   /ralph-loop "{sciezka-do-promptu}" --max-iterations {N} --completion-promise "{PROMISE_NAME}"
   ```

---

## Krok 6: Review

Zapytaj usera:
- Czy prompt jest OK?
- Czy cos zmienic (scope, iteracje, kryteria)?
- Czy dodac/usunac fazy?

Po akceptacji — gotowe.

---

## Troubleshooting

| Problem | Rozwiazanie |
|---------|-------------|
| Za duzo iteracji | Zmniejsz scope, polaicz fazy |
| Za malo iteracji | Dodaj quality check i gap analysis |
| Niejasne completion criteria | Dodaj checklisty z konkretnymi plikami/metrykami |
| Ralph utyka w petli | Dodaj escape hatch w self-correction |
| Prompt za dlugi | Przenies templates do osobnych plikow, linkuj w prompcie |
| Ralph tworzy smieci | Dodaj quality check iteration po kazdej fazie, nie tylko na koncu |
