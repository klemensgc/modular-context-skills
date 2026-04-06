---
name: vault-audit
description: |
  Audits vault structure — finds broken links, naming inconsistencies, missing indices, orphaned files,
  and proposes a reorganization plan. Optionally executes approved changes with verification.
  Use when: vault feels messy, after batch Ralph runs, before/after major restructuring,
  checking structural health beyond graph/reweave scope.
  Trigger phrases: "vault audit", "audit the vault", "check structure", "fix structure",
  "reorganize", "reorg", "cleanup vault", "vault cleanup", "sprawdź strukturę",
  "posprzątaj vault", "reorganizacja", "audit", "co jest zepsute"
---

# Vault Audit

Audytuje strukturę vault — broken links, naming, brakujące indeksy, orphany. Proponuje plan naprawy. Opcjonalnie wykonuje zaakceptowane zmiany z weryfikacją.

Repo jest po polsku. Odpowiadaj po polsku.

Różni się od `/graph` (graf wiedzy) i `/reweave` (stale content). Vault Audit = **struktura plików i folderów**, nie content.

---

## Quick Start

1. Zapytaj o scope (cały vault? konkretny folder?)
2. AUDIT — skanuj (links, naming, indices, orphans, frontmatter)
3. REPORT — pokaż findings z priorytetami
4. PLAN — zaproponuj naprawy (user wybiera)
5. EXECUTE — wykonaj zaakceptowane zmiany
6. VERIFY — sprawdź integralność po zmianach

---

## FAZA 1: SCOPE

Zapytaj usera przez AskUserQuestion:

```
"Co audytować?"
```

Opcje:
- **Cały vault** (Recommended) — pełny przegląd 5 projektów + _claude/ + _workspace/
- **Jeden projekt** — np. "1_receptionOS", "2_apolonia"
- **Konkretny folder** — user poda ścieżkę
- Other

Default: cały vault.

---

## FAZA 2: AUDIT

Uruchom 5 równoległych skanów (Explore agents lub bezpośrednie Glob/Grep):

### Skan 1: Broken Wiki-Links

```
Grep: \[\[([^\]]+)\]\]
```

Dla każdego `[[link]]`:
1. Sprawdź czy plik istnieje (Glob po nazwie)
2. Jeśli nie istnieje → BROKEN
3. Zbierz: plik źródłowy, linia, broken link target

### Skan 2: Naming Conventions

Sprawdź:
- Pliki z spacjami w nazwie (powinno być kebab-case)
- Indeksy NIE w formacie `{folder}_index.md`
- Foldery z podkreśleniem na początku (np. `_principles/` zamiast `principles/`)
- Pliki UPPER CASE (np. `UPDATE.md`, `README.md`) poza dozwolonymi (.claude/)
- Duplikaty nazw (ten sam plik w różnych folderach)

### Skan 3: Missing Indices

Dla każdego folderu z >3 plikami .md:
1. Sprawdź czy istnieje `{folder}_index.md`
2. Jeśli nie → MISSING INDEX
3. Jeśli istnieje → sprawdź czy linkuje do wszystkich plików w folderze

### Skan 4: Frontmatter Health

Grep po plikach w scope:
- Brak `title:` → ERROR
- Brak `updated:` → ERROR
- Brak `status:` → WARNING
- `status: stub` lub `status: needs-update` → INFO (do przeglądu)

### Skan 5: File Organization

- Pliki .md poza strukturą projektów (np. w root)
- Binaria w repo (PDF, PNG, CSV) — powinny być w .gitignore
- Puste pliki (0 content)
- Pliki >50KB (potencjalnie do rozdzielenia)

---

## FAZA 3: REPORT

Pokaż userowi raport:

```markdown
VAULT AUDIT REPORT — {scope} — {date}

## Summary
- Files scanned: {N}
- Broken links: {N} (across {N} files)
- Naming issues: {N}
- Missing indices: {N}
- Frontmatter issues: {N}
- Organization issues: {N}

## HIGH Priority (structural breakage)
| # | Type | File | Issue | Fix |
|---|------|------|-------|-----|
| 1 | Broken link | path/file.md:15 | [[missing-file]] not found | Create stub / fix link |
...

## MEDIUM Priority (conventions)
| # | Type | File | Issue | Fix |
|---|------|------|-------|-----|
...

## LOW Priority (cosmetic)
| # | Type | File | Issue | Fix |
|---|------|------|-------|-----|
...
```

---

## FAZA 4: PLAN

Na bazie raportu, zaproponuj plan naprawy:

### Auto-fixes (bezpieczne, odwracalne):
- Dodanie brakujących `updated:` w frontmatter
- Naprawienie broken links (jeśli jednoznaczne — plik istnieje pod inną ścieżką)
- Dodanie plików do .gitignore

### User-decision fixes:
- Rename plików (naming conventions) → pokaż old → new, zapytaj
- Tworzenie brakujących indeksów → pokaż proposed content, zapytaj
- Przenoszenie plików → pokaż plan moves, zapytaj
- Usunięcie duplikatów → pokaż oba, zapytaj który zachować

Zapytaj usera:
```
"Które naprawy wykonać?"
- Auto-fixes (bezpieczne) — Recommended
- Auto-fixes + user-approved
- Tylko raport (nie naprawiaj)
```

---

## FAZA 5: EXECUTE

Dla każdej zaakceptowanej naprawy:

1. **Przeczytaj plik** przed edycją (twarda reguła repo)
2. **Edytuj** — napraw issue
3. **Zaktualizuj `updated:`** w frontmatter na dzisiejszą datę
4. **Zaktualizuj referencje** — jeśli rename/move, grep po starym linku i podmień

### Kolejność wykonania:
1. Najpierw: naprawy broken links (nie tworzą nowych problemów)
2. Potem: frontmatter fixes
3. Potem: rename/move (mogą tworzyć nowe broken links → napraw od razu)
4. Na końcu: tworzenie nowych indeksów (referencują istniejące pliki)

---

## FAZA 6: VERIFY

Po wykonaniu napraw:

1. Re-run Skan 1 (broken links) na zmienionych plikach
2. Sprawdź czy count broken links zmniejszył się
3. Pokaż before/after:

```
VERIFICATION:
- Broken links: {before} → {after} ({diff})
- Naming issues: {before} → {after}
- Missing indices: {before} → {after}
- Remaining issues: {N} (list if any)
```

Jeśli nowe problemy pojawiły się (np. rename spowodował nowe broken links):
- Napraw automatycznie jeśli jednoznaczne
- Zapytaj usera jeśli ambiguous

---

## Troubleshooting

| Problem | Rozwiązanie |
|---------|-------------|
| Za dużo issues (>100) | Filtruj: tylko HIGH najpierw, reszta w kolejnym rundzie |
| Rename spowodował nowe broken links | Grep po starej nazwie, podmień na nową |
| User nie chce naprawiać | OK — raport sam w sobie jest wartościowy |
| Plik referenced przez wiele plików | Pokaż listę referencji przed rename/delete |
| Merge conflict po rename | Git mv (zachowuje historię), potem git add |
| Indeks nie jest kompletny | Glob `{folder}/**/*.md`, porównaj z linkami w indeksie |
| .gitignore nie obejmuje binariów | Zaproponuj dodanie wzorców (*.pdf, *.html, *.csv, *.png) |

---

## References

→ `references/examples.md` — Real vault audit examples z sesji (full coherence audit 567 plików, vault consolidation 122→20, MECE restructure, prompts reorg) + audit report template
