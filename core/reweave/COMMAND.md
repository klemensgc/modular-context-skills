---
description: Standalone reweave — skanuje vault pod kątem stale/disconnected modułów i automatycznie je aktualizuje. Scan → Execute → Verify → Commit.
argument-hint: [--staleness] [--dry-run] [ścieżka/do/modułu.md]
---

# Standalone Reweave

Jesteś orkiestratorem reweave — backward pass który aktualizuje STALE moduły w vault.
Repo jest po polsku. Odpowiadaj po polsku. Działaj autonomicznie.

Referencja: `_claude/7-skill-references/reweave-standards.md`

---

## Tryby uruchomienia

- `/reweave` — Trigger 2 (staleness+connectivity) + Trigger 5 (transcript volume)
- `/reweave --staleness` — tylko Trigger 2
- `/reweave --dry-run` — tylko skan, bez edycji
- `/reweave ścieżka/moduł.md` — reweave konkretnego modułu (bez skanu, od razu execute)

---

## KROK 1: SCAN

### Jeśli podano konkretny moduł → POMIŃ skan, idź do KROK 2

### Jeśli standalone mode:

Spawn agent (Task tool, `subagent_type: "general-purpose"`). W prompcie podaj:

```
Jesteś reweave-scanner. Przeczytaj referencje: _claude/7-skill-references/reweave-standards.md

Dzisiaj jest [DATA]. To samodzielny skan — nie było przetwarzania transkrypcji.

ZADANIE: Przeskanuj vault pod kątem [wybranych triggerów]:

[Jeśli --staleness lub domyślnie:]
Trigger 2 — Staleness + Connectivity:
- Foldery: 1_receptionOS/, 2_apolonia/, 3_fte/, _culture/
- Kryterium: staleness_ratio > 1.0 (= days_since_update / cadence_days; hot=7d, tactical=30d, iron-cold=60d) AND incoming_links >= 3
- Pomijaj: _transcripts/, _claude/, _workspace/, _assets/, .claude/, status: stub

[Jeśli domyślnie (bez --staleness):]
Trigger 5 — Transcript Volume:
- Moduły z 3+ nowszych transkrypcji w sources: niż updated:

Dla każdego kandydata:
1. Przeczytaj CAŁY moduł
2. Oceń reweave action (Add Connections / Rewrite Content / Sharpen / Split / Challenge)
3. Oblicz priority score wg reweave-standards.md

Hub files (bonus +20): pipeline.md, roadmap.md, features.md, modular-offer.md, team-roster.md

Format wyjścia: HIGH (score>=60) / MEDIUM (30-59) / LOW (<30) / Odrzuceni
Max 20 kandydatów HIGH+MEDIUM. Pisz PO POLSKU.
```

---

## KROK 2: EXECUTE (MAIN SESSION)

**WAŻNE: NIE deleguj do agentów. Edytuj sam.**

Jeśli `--dry-run` → wyświetl raport ze skanu i ZAKOŃCZ.

### Dla konkretnego modułu (argument ścieżka):

1. Przeczytaj `_claude/7-skill-references/reweave-standards.md`
2. Przeczytaj moduł docelowy (CAŁY)
3. Przeczytaj `depends-on:` modułów + grep backlinks → zidentyfikuj kontekst
4. Zastosuj 3 testy:
   - **Articulation Test:** "Ten moduł łączy się z [X] ponieważ ___"
   - **Agent Traversal Check:** "Agent podążając za linkiem podejmie jaką decyzję?"
   - **Sharpening Test:** "Dodanie info wyostrza czy rozmywa przekaz?"
5. Określ action → zastosuj → zaktualizuj frontmatter
6. Idź do KROK 3

### Dla wyników ze skanu:

Dla każdego HIGH (max 8, score descending):

1. **Przeczytaj** moduł docelowy (CAŁY plik)
2. **Przeczytaj** moduł/źródło triggering (np. pipeline.md, roadmap.md — zależnie od kontekstu)
3. **Zastosuj 3 testy** z reweave-standards.md
4. **Określ Reweave Action** (1 z 5):
   - **ADD CONNECTIONS** → dodaj wiki-links, depends-on
   - **REWRITE CONTENT** → zaktualizuj fakty, statusy, liczby
   - **SHARPEN** → usuń hedging, potwierdź zrealizowane
   - **SPLIT** → FLAG dla usera, nie wykonuj
   - **CHALLENGE** → STOP, pytaj usera
5. **Zastosuj** zmiany + zaktualizuj frontmatter (updated:, sources:, depends-on:)
6. **Zaloguj** (moduł, action, opis)

Dla MEDIUM: zapisz do `_claude/5-backlog/reweave-queue.md` (tabela Pending).
Dla LOW: zaloguj w raporcie (bez akcji).

**Pytaj usera TYLKO jeśli:**
- Action = CHALLENGE
- Action = SPLIT

---

## KROK 3: VERIFY

Dla KAŻDEGO edytowanego modułu:

1. **Cold-Read Test** — przeczytaj tytuł + pierwszą sekcję. Przewiduj resztę. Porównaj.
2. **Schema Check** — frontmatter: title?, updated: dzisiejsze?, depends-on: [[]]?, sources:?
3. **Neighbor Coherence** — przeczytaj 1 moduł z depends-on. Zgadzają się na fakty?

Fail → cofnij zmiany, dodaj do reweave-queue.md z notatką.

---

## KROK 4: REPORT

```
REWEAVE STANDALONE: X modułów
- HIGH wykonanych: Y (lista z action type)
- MEDIUM → Ralph queue: Z
- LOW → zalogowane: W
ACTIONS: A add-connections, B rewrite, C sharpen, D split-flags, E challenges
```

---

## KROK 5: COMMIT

```bash
git add [lista zmodyfikowanych plików]
git commit -m "$(cat <<'EOF'
Update: reweave X modułów (standalone scan)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Obsługa błędów

- Skan zwraca 0 kandydatów → "Vault healthy — brak modułów do reweave."
- Moduł z argumentu nie istnieje → error + exit
- Moduł ma status: stub → "Moduł jest stub — reweave nie dotyczy. Rozważ uzupełnienie."
