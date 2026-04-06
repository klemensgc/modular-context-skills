---
name: log
description: |
  Zamyka sesje pracy: generuje session log, dzieli zmiany na logiczne commity, pilnuje
  zeby nie nadpisac nowszych plikow starszymi commitami. Na koncu pyta o push.
  Use when: konczysz prace, chcesz udokumentowac sesje, chcesz scommitowac zmiany,
  zamykasz dzien pracy.
  Trigger phrases: "/log", "zamknij sesje", "zakoncz sesje", "session log",
  "podsumuj sesje", "scommituj", "zamykamy", "konczymy"
---

# Session Logger

Zamyka sesje: dokumentuje co sie zadzialo, commituje zmiany, opcjonalnie pushuje.

---

## Quick Start

1. Przeskanuj git status + git diff
2. Przeanalizuj konwersacje — wyciagnij kluczowe ustalenia
3. Wygeneruj session log (szczegolowsc proporcjonalna do wagi sesji)
4. Podziel zmiany na logiczne commity
5. Wykonaj commity (z conflict detection)
6. Zapytaj o push

---

## Faza 1: Rekonesans

Uruchom ROWNOLEGLE:

```bash
git status
git diff --stat
git diff --cached --stat
git log --oneline -5
```

Zbierz:
- **Nowe pliki** (untracked) — pogrupuj tematycznie
- **Zmodyfikowane pliki** — sprawdz co sie zmienilo
- **Staged vs unstaged** — nie zakladaj ze wszystko jest staged

Przeczytaj KAZDEMU zmodyfikowanemu plikowi `updated:` z frontmatter.
To bedzie potrzebne w Fazie 3 do conflict detection.

---

## Faza 2: Session Log

### Okresl poziom szczegolowosci

| Kryterium | Lekki log | Pelny log |
|-----------|-----------|-----------|
| Pliki zmodyfikowane | 1-3 | 4+ |
| Projekty dotkniene | 1 | 2+ |
| Decyzje podjete | 0-1 | 2+ |
| Sprzecznosci rozstrzygniete | 0 | 1+ |
| Nowe ustalenia strategiczne | nie | tak |

**Lekki log:** Zlecenie, Wykonane Akcje (zwiezle), Zmodyfikowane Pliki, Commits.
**Pelny log:** Wszystkie sekcje szablonu wlacznie z Otwarte Kwestie i Notatki.

### Generuj session log

Sciezka: `_claude/4-sessions/{YYYY-MM}/session-{YYYY-MM-DD}-{slug}.md`

Slug: 2-3 slowa opisujace sesje, kebab-case (np. `pipeline-update`, `backlog-processing`, `ros-pricing`).

Szablon: `_claude/2-templates/session-log.md` — uzyj go ale dostosuj sekcje do poziomu szczegolowosci.

**Kluczowe ustalenia** — przeanalizuj konwersacje i wyciagnij:
- Decyzje podjete (co postanowiono)
- Sprzecznosci rozstrzygniete (co sie rozniło i jak rozwiazano)
- Nowe informacje wplywajace na projekty w repo
- Action items / otwarte kwestie na przyszlosc

Zapisz plik. Pokaz userowi streszczenie session logu (nie caly plik).

---

## Faza 3: Planowanie commitow

### Grupowanie zmian

Pogrupuj zmodyfikowane pliki w logiczne commity:

| Zasada grupowania | Przyklad |
|-------------------|---------|
| Ten sam projekt + ten sam temat | `pipeline.md` + `haldent_index.md` = "Update: ros - Haldent pipeline status" |
| Cross-project ale ten sam trigger | `team-roster.md` + `operations-team.md` = "Update: team - Recruitment changes" |
| Session log osobno | `session-*.md` = "Add: session log [slug]" |
| Nowe pliki osobno od updateow | Nowy plik to `Add:`, edycja to `Update:` |
| Transkrypcje osobno | Moved/new transcripts = osobny commit |

### Conflict detection

Dla KAZDEGO pliku w KAZDYM zaplanowanym commicie:

1. Sprawdz `updated:` w frontmatter NASZEJ WERSJI
2. Sprawdz `updated:` w OSTATNIM COMMICIE na remote (jesli dostepny):
   ```bash
   git show HEAD:{sciezka} 2>/dev/null | head -10
   ```
3. Jezeli remote ma NOWSZA date niz nasza wersja — STOP:
   - Pokaz userowi: "Plik {sciezka} ma na uzywanej wersji `updated: X`, ale w HEAD jest `updated: Y` (nowsza). Nadpisac?"
   - Czekaj na odpowiedz przed kontynuacja

### Prezentacja planu

Pokaz userowi plan commitow w formacie:

```
Commit 1: Add: session log [slug]
  - _claude/4-sessions/YYYY-MM/session-*.md (new)

Commit 2: Update: ros - [opis]
  - 1_receptionOS/path/file1.md (modified)
  - 1_receptionOS/path/file2.md (modified)

Commit 3: Update: culture - [opis]
  - _culture/team/file.md (modified)
```

Zapytaj: "Plan commitow OK? Moge wykonac?"

---

## Faza 4: Wykonanie commitow

Po akceptacji planu, dla KAZDEGO commita sekwencyjnie:

```bash
# 1. Stage tylko pliki z tego commita
git add plik1.md plik2.md

# 2. Commit z HEREDOC
git commit -m "$(cat <<'EOF'
Update: ros - Pipeline status after Haldent demo

- Haldent network fix confirmed
- Dentalway moved to warm pipeline

Sources: k@fundacjaedisona-16-feb-2026
Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

**Zasady:**
- Session log ZAWSZE jako PIERWSZY commit (inne commity beda go referencowac)
- HEREDOC dla wielolinijkowych messages
- `Sources:` jezeli commit wynika z transkrypcji
- `Co-Authored-By:` w KAZDYM uzyj aktualnego modelu
- Jezeli `git add` albo `git commit` FAIL — nie ponawiaj, pokaz error userowi
- NIGDY `git add -A` ani `git add .` — ZAWSZE konkretne pliki

Po KAZDYM ustanym commicie: zapisz hash. Pokaz go userowi.

---

## Faza 5: Weryfikacja

Po wszystkich commitach:

```bash
git status
git log --oneline -{N}  # N = liczba commitow z tej sesji
```

Pokaz userowi podsumowanie:
- Ile commitow
- Lista hashy + messages
- Czy cos zostalo unstaged

---

## Faza 6: Push

Zapytaj usera:

```
Wszystko scommitowane. Pushnac na remote?
- Branch: {current branch}
- Remote: origin
- Commitow: {N}
```

Uzyj `AskUserQuestion`:
- "Pushnac na origin/{branch}?"
- Opcje: "Tak, pushuj" / "Nie, tylko lokalnie"

Jezeli tak:
```bash
git push origin {branch}
```

Jezeli push FAIL (np. rejected) — pokaz error, NIE rob `--force`. Zapytaj usera.

---

## Troubleshooting

| Problem | Rozwiazanie |
|---------|-------------|
| Brak zmian do commitowania | Powiedz userowi, nie twórz pustego session logu |
| Conflict z remote | Pokaz obie wersje, zapytaj usera |
| Pre-commit hook FAIL | Napraw problem, NOWY commit (nie --amend) |
| Plik staged ale nie powinien byc | `git reset HEAD {plik}` przed commitem |
| User chce zmienic commit message | Zapytaj czy --amend (ostatni commit) czy nowy revert+commit |
| Push rejected | NIE --force. Zaproponuj `git pull --rebase` i zapytaj |
| Merge conflict po pull | Pokaz conflicty, zapytaj usera jak rozwiazac |
