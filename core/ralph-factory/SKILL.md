---
name: ralph-factory
description: |
  Runs the Ralph Prompt Factory meta-prompt — generates 20 strategic Ralph prompts targeting CEO success
  factors. Each run creates a versioned folder (v1, v2, v3...) with fresh prompts based on current repo state.
  Detects existing versions, prepares versioned meta-prompt copy, and executes via Ralph Loop.
  Use when: regenerating strategic Ralph prompts, refreshing prompt factory after repo changes,
  creating a new batch of Ralph prompts, versioning prompt factory output.
  Trigger phrases: "ralph factory", "ralph-factory", "factory", "regeneruj prompty",
  "nowa wersja promptow", "odpal factory", "prompt factory", "20 promptow"
---

# Ralph Prompt Factory

Generuje 20 strategicznych promptow Ralph z meta-promptu. Kazdy run tworzy nowa wersje (v1, v2, v3...).

**Template:** `_claude/6-prompts/ralph-prompt-factory.md` (825 linii, 25 iteracji Ralph Loop)
**Output:** `_claude/6-prompts/ralph-factory/v{N}/` (20 promptow + index + progress)

---

## Workflow

### Krok 1: Version detection

Skanuj `_claude/6-prompts/ralph-factory/` pod katem folderow `v*/`:

```bash
ls -d _claude/6-prompts/ralph-factory/v*/ 2>/dev/null | sort -V
```

**Scenariusze:**

| Stan | Akcja |
|------|-------|
| Brak `v*/` dirs + istnieja flat `.md` files | Pierwsza migracja: przenies flat files do `v1/`, nastepna wersja = `v2` |
| Istnieja `v*/` dirs | Wykryj najwyzsza wersje, nastepna = `v{max+1}` |
| Pusty folder | Pierwsza wersja = `v1` |

**Pierwsza migracja (jednorazowo):**

Jesli flat files istnieja (ralph-*.md, _index.md, _progress.md):

1. Stworz `_claude/6-prompts/ralph-factory/v1/`
2. Przenies WSZYSTKIE `.md` pliki z `ralph-factory/` do `v1/`
3. Wyswietl: "Zmigrowano {N} plikow do v1/"

**Po detekcji wyswietl:**

```
Ralph Factory — wersje:
  v1: 20 promptow (2026-02-21) ← current
Tworze: v2
```

### Krok 1.5: Repo State Scan (OBOWIĄZKOWY)

Zanim wygenerujesz prompty, MUSISZ przeskanować repo:

1. **Sprawdz outputy poprzednich wersji:**
   - Dla kazdego promptu z v{N-1}: sprawdz czy output file/folder ISTNIEJE
   - Czytaj first 10 lines → status, updated date
   - Klasyfikuj: DONE (comprehensive output) / PARTIAL / PENDING

2. **Przeczytaj current state:**
   - `pipeline.md` (hot cadence — klienci, deal stages)
   - `quest-board-w*.md` (latest — priorytety tygodnia)
   - `backlog_index.md` (reweave queue, drafts, synthesis opportunities)
   - Recent session logs (`_claude/4-sessions/` — last 5)

3. **Zidentyfikuj NOWE watki:**
   - Nowi klienci od ostatniego runa
   - Nowe partnerstwa/relationships
   - Nowe projekty/ekspansje
   - Deployed systems (cadence, sync, etc.)

4. **Wyswietl summary:**

```
Repo State Scan:
  Done prompts (skip or enrich): [list]
  Pending prompts (keep or update): [list]
  New threads to cover: [list]
  Key changes since v{N-1}: [list]
```

5. **Regula: NIE KOPIUJ poprzednich promptow.**
   - Done prompt → zastap NOWYM tematem LUB napisz "enrichment" (builds on existing output)
   - Pending prompt → zachowaj ale UPDATE context (nowi klienci, nowe dane)
   - Nowy watek → nowy prompt

---

### Krok 2: Quick prep

Zapytaj usera (AskUserQuestion):

**"Aktualizujesz success factors czy zachowujesz obecne?"**

| Opcja | Opis |
|-------|------|
| **Keep existing (Recommended)** | Uzyj tych samych 15 SF z ostatniego runa. Promptly beda swiezsze bo repo sie zmienilo. |
| **Update success factors** | Krotki interview: ktore SF dodac/usunac/zmienic? Zmienione SF wstawione do meta-promptu. |

Jesli "Keep existing" → przejdz do Kroku 3.

Jesli "Update" → zapytaj:
- "Ktore SF usunac lub zmienic?"
- "Nowe SF do dodania?"
- Wstaw zmiany do kopii meta-promptu.

### Krok 3: Generate versioned run

1. **Stworz folder:** `_claude/6-prompts/ralph-factory/v{N}/`

2. **Przeczytaj template:** `_claude/6-prompts/ralph-prompt-factory.md`
   - Template to WZORZEC struktury, NIE kopia do skopiowania
   - Ralph pisze prompty OD ZERA na bazie Repo State Scan (Krok 1.5)

3. **Stworz kopie meta-promptu z podmienionymi sciezkami:**
   - Zamien WSZYSTKIE wystapienia `_claude/6-prompts/ralph-factory/` → `_claude/6-prompts/ralph-factory/v{N}/`
   - Zamien promise: `PROMPT_FACTORY_COMPLETE` → `PROMPT_FACTORY_V{N}_COMPLETE`
   - Zaktualizuj `updated:` w frontmatter na dzisiejsza date
   - **WAZNE:** Meta-prompt instruuje Ralpha by pisal prompty na bazie CURRENT repo state (z Krok 1.5), NIE by kopiowal poprzednia wersje

4. **Zapisz kopie:** `_claude/6-prompts/ralph-factory/v{N}/ralph-prompt-factory.md`

5. **Wyswietl podsumowanie:**

```
Ralph Factory v{N} przygotowany:
  Template: _claude/6-prompts/ralph-factory/v{N}/ralph-prompt-factory.md
  Iteracje: 25
  Output: 20 promptow w v{N}/
  Promise: PROMPT_FACTORY_V{N}_COMPLETE
  Repo Scan: Done/Pending/New = X/Y/Z
```

### Krok 4: Greenlight Review

Po wygenerowaniu 20 promptow, user przegladal i zatwierdza ktore uruchomic.

1. **Wyswietl tablice review:**

```
# | Nazwa | SF | Iter | Blurb
1 | ralph-dentalway-activation | SF-1,2 | 12 | Activation plan for 100 klinik outreach via Kamil/Dentalway
2 | ralph-international-traction | SF-15 | 10 | Narrative from Charmain, Miami, Ola signals
...
```

Per prompt: #, nazwa (bez .md), SF, iteracje, 1-zdaniowy blurb (z sekcji Task).

2. **Zapytaj usera (AskUserQuestion, multiSelect: true):**

**"Ktore prompty greenlight do uruchomienia?"**

Opcje = lista 20 promptow. Label = `#{N} {nazwa}`, Description = blurb.

3. **Oznacz greenlit prompty:**
   - Rename: `ralph-*.md` → `greenlit--ralph-*.md`
   - NIE-greenlit: zostaja bez zmian (bez prefixu)
   - Update `_index.md`: dodaj kolumne `Greenlit` (YES / -)
   - Update `_progress.md`: status `GREENLIT` vs `SKIPPED`

4. **Wyswietl podsumowanie:**

```
Greenlit: X/20 promptow
Skipped: Y/20

Greenlit prompty:
  1. greenlit--ralph-dentalway-activation.md (12 iter)
  2. greenlit--ralph-v3-launch-strategy.md (12 iter)
  ...

Total iterations: Z
Estimated time: ~Z×5 min
```

---

### Krok 5: Execute

Generuj komendy TYLKO dla greenlit promptow (pliki z prefixem `greenlit--`).

Zapytaj usera (AskUserQuestion):

**"Jak uruchomic {X} greenlit promptow?"**

| Opcja | Opis |
|-------|------|
| **Uruchom teraz** | Invoke Ralph Loop w tej sesji. |
| **Daj komende do overnight** | Wyswietl gotowa komende do wklejenia w nowy terminal. |
| **Daj komende do skopiowania** | Tylko wyswietl komende, user sam zdecyduje kiedy. |

**Komenda per prompt (dla greenlit):**

```
/ralph-loop:ralph-loop "_claude/6-prompts/ralph-factory/v{N}/greenlit--ralph-{name}.md" --max-iterations {iter} --completion-promise "{PROMISE}"
```

**Jesli "Uruchom teraz":**
Invoke Skill `ralph-loop:ralph-loop` z pierwszym greenlit promptem.

**Jesli "Overnight":**
Wyswietl bash chain TYLKO z greenlit promptami, w kolejnosci Tier 1 → Tier 2 → Tier 3 → Tier 4:

```bash
cd /Users/kubagasienica/Desktop/all-transcripts/modular-context

# Greenlit prompt 1:
claude --dangerously-skip-permissions <<'EOF'
/ralph-loop:ralph-loop "_claude/6-prompts/ralph-factory/v{N}/greenlit--ralph-{name1}.md" --max-iterations {iter1} --completion-promise "{PROMISE1}"
EOF

# Greenlit prompt 2:
claude --dangerously-skip-permissions <<'EOF'
/ralph-loop:ralph-loop "_claude/6-prompts/ralph-factory/v{N}/greenlit--ralph-{name2}.md" --max-iterations {iter2} --completion-promise "{PROMISE2}"
EOF
# ... only greenlit prompts
```

---

## Struktura folderow

```
_claude/6-prompts/
├── ralph-prompt-factory.md          ← TEMPLATE (nigdy nie edytowany)
└── ralph-factory/
    ├── v1/                          ← pierwsza generacja
    │   ├── ralph-prompt-factory.md  ← kopia uzywanego meta-promptu
    │   ├── _index.md
    │   ├── _progress.md
    │   ├── greenlit--ralph-*.md     ← zatwierdzone do uruchomienia
    │   └── ralph-*.md               ← niezatwierdzone (bez prefixu)
    ├── v2/
    │   └── ...
    └── v3/
        └── ...
```

---

## Troubleshooting

| Problem | Rozwiazanie |
|---------|-------------|
| Flat files nie zmigrowane do v1 | Skill robi to automatycznie przy pierwszym runie |
| Ralph Loop nie startuje | Sprawdz czy `.claude/ralph-loop.local.md` nie istnieje (stale state) |
| Meta-prompt ma stare sciezki | Skill podmienia sciezki automatycznie w kopii |
| Za duzo iteracji | Zmniejsz `--max-iterations` w komendzie |
| Chce porownac wersje | `diff -r ralph-factory/v1/ ralph-factory/v2/` (porownaj foldery) |
| Overnight session nie rusza | Odpal z NOWEGO terminala, nie z wnetrza Claude Code |
| Chce zmienic greenlit | Rename plik: dodaj/usun prefix `greenlit--` i zaktualizuj _index.md |
| Chce greenlit wszystko | `for f in ralph-*.md; do mv "$f" "greenlit--$f"; done` w katalogu v{N}/ |
