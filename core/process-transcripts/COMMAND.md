---
name: Synthesise Files
description: Synthesise raw files (transcripts, notes, chosen files) into vault modules — categorizes, tags, updates modules, reweave neighbors, reflect connections, detects conflicts, surfaces CEO insights. Autonomous — asks only on edge cases.
argument-hint: [--dry-run] [--skip-pull]
triggers: ["synthesise", "synthesise files", "synthesise-files", "process-transcripts", "ingest", "ingest data", "process backlog", "syntetyzuj"]
---

# Synthesise Files (transcripts / notes / chosen raw files)

Jesteś orkiestratorem autonomicznego pipeline'u przetwarzania transkrypcji w Obsidian vault.
Repo jest po polsku. Odpowiadaj po polsku. Działaj autonomicznie — pytaj usera TYLKO gdy:
- Znalazłeś sprzeczność (nowe dane vs moduł)
- Kategoria ambiguous (pasuje do 2+ równo)
- Nowa encja nie w taksonomii
- Moduł do stworzenia (nie istnieje)
- Sensitive content (team tensions, finanse, equity)
- Git conflict

Dla business as usual → po prostu zrób. Nie pytaj o oczywiste rzeczy.

---

## FAZA 0: Setup

### 0.1 Git pull (chyba że user podał --skip-pull)

Użyj Bash tool (NIE blok kodu z wykrzyknikiem) do wykonania pull:

```bash
git pull origin master --no-rebase 2>&1 || true
```

**Obsługa wyniku:**
- Jeśli pull SUCCEEDS → kontynuuj
- Jeśli pull FAILS z "CONFLICT" → uruchom auto-resolve:
  1. Sprawdź `git status` — zidentyfikuj conflicted pliki
  2. Dla "file location" conflicts (backlog → transcripts): accept theirs (`git checkout --theirs <path> && git add <path>`)
  3. Dla content conflicts: pokaż userowi, czekaj na decyzję
  4. Po resolve: `git commit -m "Fix: resolve merge conflicts from pull"`
- Jeśli pull FAILS z credential/network error → kontynuuj z ostrzeżeniem: "⚠ Pull failed (network/auth), working with local state."
- Jeśli pull FAILS z innego powodu → pokaż error, kontynuuj z ostrzeżeniem

### 0.2 Inwentaryzacja backlogu

Przeczytaj zawartość `_transcripts-backlog/` używając Glob i Read:
1. Policz pliki — zidentyfikuj pary (transkrypcja + summary)
2. Zidentyfikuj standalone (brak pary)
3. Jeśli backlog PUSTY → powiedz "Backlog pusty, nic do przetworzenia." i zakończ

Wyświetl krótki raport:
```
Backlog: X plików (Y par + Z standalone)
```

Kontynuuj automatycznie (nie pytaj).

---

## FAZA 1: Analiza transkrypcji

### 1.1 Przeczytaj referencje

Przeczytaj te pliki PRZED spawnem agentów:
- `_claude/7-skill-references/tagging-taxonomy.md`
- `_claude/7-skill-references/category-routing.md`
- `_claude/7-skill-references/transcript-standards.md`

### 1.2 Spawn transcript-analyzer agentów

Podział na batche:
- <= 4 pliki (2 pary): 1 agent
- 5-10 plików: 2 agenty
- > 10 plików: 3 agenty (max)

Użyj Task tool z `subagent_type: "transcript-analyzer"`. W prompcie podaj:
- Listę ścieżek plików do analizy
- Instrukcję: "Przeczytaj referencje z _claude/7-skill-references/ i przeanalizuj transkrypcje."

Uruchom batche RÓWNOLEGLE.

### 1.3 Merge wyników

Zbierz wyniki ze wszystkich agentów. Stwórz zbiorczą tabelę:

```
| # | Transkrypt | Kategoria | Tagi | Priorytet |
|---|-----------|-----------|------|-----------|
```

**Pytaj usera TYLKO jeśli:**
- Agent zaproponował 2 kategorie (ambiguous)
- Znaleziono nowy tag nieistniejący w taksonomii

W przeciwnym razie kontynuuj automatycznie.

---

## FAZA 2: Skanowanie modułów

### 2.1 Spawn agentów równolegle (3 agenty)

**Agent 1 — module-scanner (topic-based):**
```
Strategia: Topic-based. Na podstawie poniższej kategoryzacji znajdź moduły do aktualizacji.
[wklej tabelę kategoryzacji z Fazy 1]
```

**Agent 2 — module-scanner (entity-based):**
```
Strategia: Entity-based. Przeszukaj moduły pod kątem tych encji:
Osoby: [lista osób z Fazy 1]
Klienci/produkty/vendorzy: [lista z tagów]
```

**Agent 3 — consistency-checker:**
```
Sprawdź spójność pomiędzy nowymi danymi a modułami.
Nowe dane: [TL;DR i action items z Fazy 1]
Moduły do sprawdzenia: [lista kandydatów jeśli znana, inaczej "znajdź sam"]
```

Uruchom RÓWNOLEGLE.

### 2.2 Merge i priorytetyzacja

Połącz wyniki obu module-scannerów (deduplikacja). Stwórz finalną listę:

```
HIGH priority: [lista]
MEDIUM priority: [lista]
LOW priority: [lista]
```

### 2.3 Obsługa konfliktów

Jeśli consistency-checker znalazł SPRZECZNOŚCI:
- Pokaż userowi każdą sprzeczność z obiema wersjami
- Zapytaj o decyzję
- Zastosuj decyzję w Fazie 3

Auto-fixy (nieaktualne statusy, brakujące wiki-links) → zastosuj automatycznie w Fazie 3.
Duplikaty → pomiń w miningu.

---

## FAZA 3: Mining i aktualizacje

**WAŻNE: Ta faza w main session, NIE deleguj do agentów.**

### 3.1 Przeniesienie transkrypcji

Dla każdego transkryptu z zatwierdzoną kategoryzacją — przenieś z backlogu:

```bash
mv "_transcripts-backlog/nazwa.md" "_transcripts/[kategoria]/nazwa.md"
mv "_transcripts-backlog/nazwa-summary.md" "_transcripts/[kategoria]/nazwa-summary.md"
```

### 3.2 Mining modułów

Dla każdego modułu (HIGH → MEDIUM → LOW):

1. Przeczytaj moduł docelowy (CAŁY plik)
2. Przeczytaj źródłowy transkrypt (summary + pełny)
3. Sprawdź `depends-on:` — czy powiązane pliki też wymagają zmian
4. Edytuj moduł:
   - Dodaj nowe informacje (NIE nadpisuj istniejących)
   - Dodaj transkrypt do `sources:` w frontmatter
   - Zaktualizuj `updated:` na dziś
   - Zaktualizuj `status:` jeśli potrzeba
5. Zastosuj auto-fixy z consistency-checker (wiki-links, statusy)

**Pytaj usera TYLKO jeśli:**
- Sensitive content (team tensions, finanse, equity informacje)
- Moduł docelowy nie istnieje (zapytaj czy stworzyć)

### 3.3 Safety checks

Po każdej edycji weryfikuj:
- updated: zaktualizowane?
- sources: zawiera nowy transkrypt?
- Nie nadpisano nowszych danych?

### 3.4 Tracking dla Reweave

Zanotuj dane potrzebne dla Fazy 3.5:
- `touched_modules[]` — lista WSZYSTKICH modułów edytowanych w Fazie 3 (pełne ścieżki + krótki opis zmian)
- `resolved_contradictions[]` — lista sprzeczności rozwiązanych w Fazie 2.3/3 (moduł + stara vs nowa wartość)
- `updated_indexes[]` — lista index files zaktualizowanych w Fazie 3 (jeśli jakiekolwiek)

---

## FAZA 3.5: Reweave (backward pass)

Cel: sprawdź czy SĄSIEDZI zaktualizowanych modułów stali się nieaktualni. Inspiracja: Ars Contexta.

### 3.5.0 Warunek uruchomienia

- Jeśli touched_modules PUSTA (Faza 3 nic nie edytowała) → **POMIŃ Fazę 3.5**
- Jeśli --dry-run → **POMIŃ Fazę 3.5**

### 3.5.1 Spawn reweave-scanner agenta

Użyj Task tool z `subagent_type: "reweave-scanner"`. W prompcie podaj:

```
Przeczytaj referencje: _claude/7-skill-references/reweave-standards.md

Moduły zaktualizowane w tej sesji (Phase 3):
[wklej touched_modules[] z 3.4 — ścieżka + opis zmian]

Sprzeczności rozwiązane:
[wklej resolved_contradictions[] z 3.4, lub "brak"]

Index files zaktualizowane:
[wklej updated_indexes[] z 3.4, lub "brak"]

Wykonaj pełną ewaluację 5 triggerów. Zwróć priorytetyzowaną kolejkę reweave.
```

### 3.5.2 Reweave Execute (MAIN SESSION)

**WAŻNE: Ta faza w main session, NIE deleguj do agentów.**

Dla każdego modułu z HIGH priority (max 8, w kolejności score descending):

1. **Przeczytaj** moduł docelowy (CAŁY plik)
2. **Przeczytaj** moduł triggering (ten co spowodował reweave)
3. **Zastosuj 3 testy** z reweave-standards.md:
   - Articulation Test: "Moduł [[A]] łączy się z [[B]] ponieważ ___"
   - Agent Traversal Check: "Jeśli agent podąża za linkiem, jaką decyzję podejmie?"
   - Sharpening Test: "Czy dodanie info wyostrza czy rozmywa przekaz?"
4. **Określ Reweave Action** (1 z 5):
   - **ADD CONNECTIONS** → dodaj wiki-links, depends-on
   - **REWRITE CONTENT** → zaktualizuj fakty, statusy, liczby
   - **SHARPEN** → usuń hedging, potwierdź zrealizowane
   - **SPLIT** → FLAG dla usera, nie wykonuj automatycznie
   - **CHALLENGE** → STOP, pokaż sprzeczność, pytaj usera
5. **Zastosuj** zmiany + zaktualizuj frontmatter (updated:, sources:, depends-on:)
6. **Zaloguj** co zrobiłeś (moduł, action, opis — do raportu w 3.5.4)

Dla MEDIUM priority: zapisz do `_claude/5-backlog/reweave-queue.md` (tabela Pending).
Dla LOW priority: zaloguj w session logu (bez akcji).

**Pytaj usera TYLKO jeśli:**
- Reweave Action = CHALLENGE (sprzeczność z fundamentalnym założeniem)
- Reweave Action = SPLIT (user decyduje jak dzielić)

### 3.5.3 Reweave Verify

Dla KAŻDEGO reweaved modułu:

1. **Cold-Read Test** — przeczytaj tytuł i pierwszą sekcję. Czy reszta modułu jest przewidywalna z kontekstu? Jeśli treść odbiega od oczekiwań → potencjalna inkoherencja.
2. **Schema Check** — frontmatter kompletny? `updated:` dzisiejsze? `depends-on:` używa `[[]]`? `sources:` aktualne?
3. **Neighbor Coherence** — przeczytaj 1 moduł z `depends-on:`. Czy nadal się zgadzają na fakty?

Jeśli weryfikacja FAIL → cofnij zmiany w module, dodaj do `reweave-queue.md` z notatką "verification failed, needs human review".

### 3.5.4 Raport reweave

Stwórz podsumowanie (wyświetl + zachowaj do Phase 4):

```
REWEAVE: X modułów przetworzonych
- HIGH: Y wykonanych (lista z action type)
- MEDIUM → Ralph queue: Z (lista ścieżek)
- LOW → zalogowane: W
ACTIONS: A add-connections, B rewrite, C sharpen, D split-flags, E challenges
```

---

## FAZA 4: CEO Advisory

### 4.1 Spawn ceo-advisor agenta

Użyj Task tool z `subagent_type: "ceo-advisor"`. W prompcie podaj:

```
Przeanalizuj przetworzone transkrypcje:
[lista transkrypcji z TL;DR z Fazy 1]

Zaktualizowane moduły:
[lista z Fazy 3 z opisem zmian]

Efekt kaskadowy (reweave):
[raport z Fazy 3.5.4 — jakie moduły-sąsiedzi zaktualizowano, jakie actions, jakie triggery]
[jeśli Faza 3.5 pominięta → "Faza 3.5 pominięta (brak touched modules)"]

Overflow do Ralph queue:
[lista MEDIUM candidates z reweave-queue.md, lub "brak"]

Przeczytaj index files projektów aby zrozumieć kontekst.
Szukaj unknown unknowns — sygnały, szanse, luki, trendy.
Zwróć uwagę na efekt kaskadowy — co ripple z reweave mówi o strukturze wiedzy.
```

Ten agent używa modelu opus dla głębokiej analizy.

---

## FAZA 4.5: Reflect (forward pass)

Cel: odkryj NIEOCZYWISTE połączenia między modułami dotkniętymi w tej sesji. Inspiracja: Ars Contexta.

### 4.5.0 Warunek uruchomienia

- Jeśli łącznie (touched_modules + reweaved_modules) < 2 → **POMIŃ Fazę 4.5** (za mało danych do discovery)
- Jeśli --dry-run → **POMIŃ Fazę 4.5**

### 4.5.1 Spawn knowledge-weaver agenta

Użyj Task tool z `subagent_type: "knowledge-weaver"`. W prompcie podaj:

```
Przeczytaj referencje: _claude/7-skill-references/reweave-standards.md (sekcje 6 i 7)

Moduły dotknięte w tej sesji (Phase 3 mining + Phase 3.5 reweave):
[wklej PEŁNĄ listę — ścieżka + opis zmian]

Projekty dotknięte: [ROS / Apolonia / Fundacja / Culture — które]

Wykonaj Dual Discovery (MOC traversal + semantic search).
Dla każdego potencjalnego połączenia zastosuj Articulation Test.
Szukaj cross-project connections i synthesis opportunities.
```

### 4.5.2 Reflect Apply (MAIN SESSION)

**WAŻNE: Ta faza w main session, NIE deleguj do agentów.**

1. **New Connections** — dla każdego zaakceptowanego połączenia z raportu:
   - Przeczytaj target module
   - Dodaj wiki-link inline w odpowiednim miejscu (preferuj prose, nie "See also")
   - Jeśli bidirectional → dodaj reverse link
   - Zaktualizuj `updated:` na dziś

2. **Synthesis Opportunities** — dla każdej wykrytej:
   - **NIE** twórz nowych modułów
   - Dodaj do `_claude/5-backlog/synthesis-opportunities.md` (sekcja Open)

3. **Index Updates** — z raportu knowledge-weaver:
   - Zastosuj bezpośrednio (dodawanie linków do index files jest bezpieczne)

### 4.5.3 Raport reflect

```
REFLECT: X nowych połączeń dodanych, Y synthesis opportunities, Z index updates
```

---

## FAZA 5: Finalizacja

### 5.1 Aktualizacja indexów

1. Przeczytaj `_transcripts/transcripts_index.md` → zaktualizuj countery kategorii
2. Przeczytaj `_claude/5-backlog/backlog_index.md` → refresh statusów

### 5.2 Session log

Stwórz session log w `_claude/4-sessions/2026-02/`:
- Przeczytaj szablon: `_claude/2-templates/session-log.md`
- Wypełnij: data, zmodyfikowane pliki, decyzje, zmiany

### 5.3 Raport końcowy

Wyświetl:
```
PRZETWORZONO: X transkrypcji (Y par + Z standalone)
PRZENIESIONO: [kategorie z liczbami]
ZAKTUALIZOWANO: X modułów (HIGH: Y, MEDIUM: Z, LOW: W)
KONFLIKTY: X rozwiązanych
REWEAVE: X modułów (HIGH: Y wykonanych, MEDIUM → Ralph: Z)
REFLECT: X nowych połączeń, Y synthesis opportunities, Z index updates
```

Następnie wyświetl CEO Advisory Report z Fazy 4.

Jeśli są synthesis opportunities → wyświetl listę z `synthesis-opportunities.md`.
Jeśli reweave-queue.md ma >10 pending → zaznacz: "Reweave queue ma X items — rozważ Ralph loop."

### 5.4 Commit

Automatycznie commitnij zmiany:

```bash
git add [lista zmodyfikowanych plików]
git commit -m "$(cat <<'EOF'
Add: backlog processing (X transkrypcji) + Y module updates + Z reweave + W reflect connections

Sources: [lista transkrypcji]
Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Argumenty

- **--dry-run** — tylko analiza (Fazy 0-2), bez zmian w plikach. Pokaż co BY było zrobione.
- **--skip-pull** — pomiń git pull (gdy już zrobiony ręcznie)

## Obsługa błędów

- Pusty backlog → info + exit
- Git conflict → pokaż, czekaj na usera (jedyny hard block)
- Transkrypt bez summary → przetwarzaj sam, zaznacz
- Duplikat → skip, zaznacz
- Moduł nie istnieje → zapytaj usera
- Sprzeczne dane → zapytaj usera
