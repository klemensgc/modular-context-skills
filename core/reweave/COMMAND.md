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
- Foldery: 1_receptionOS/, 2_apolonia/, 3_fte/, _culture/, osoby/, _sales/pipeline/active/
- Kryterium: staleness_ratio > 1.0 AND incoming_links >= 3.
  Ratio liczy `graph/scripts/vault-graph.py . staleness` — świeżość z gita (ostatni commit
  dotykający pliku, commity z trailerem `Meta: true` pomijane), budżet: hub 7d (whitelist
  HUBS, wygrywa z typem), modul 60d, osoba 180d, deal 30d (tylko `_sales/pipeline/active/`),
  brak typu 60d. Nie licz ratio ręcznie z `updated:`.
  Wyjątek od progu incoming_links: każdy plik ze `stale_hubs` jest kandydatem HIGH
  niezależnie od liczby linków.
- Poza rankingiem: `status: archive`, 4_apollo/**, encje write-once, deale spoza
  pipeline/active/ — skrypt wycina je sam, zanim policzy ratio; nie filtruj ich po fakcie.
  Sam skan pomijaj w: _transcripts/, _claude/, _workspace/, _assets/, .claude/

[Jeśli domyślnie (bez --staleness):]
Trigger 5 — Transcript Volume:
- Moduły, do których od ostatniej realnej zmiany (data z gita) doszły 3+ nowe transkrypty:
  szukaj po `_transcripts/**-summary.md` — pole `sources:` żyje wyłącznie tam, nigdy w module.

Dla każdego kandydata:
1. Przeczytaj CAŁY moduł
2. Oceń reweave action (Add Connections / Rewrite Content / Sharpen / Split / Challenge)
3. Oblicz priority score wg reweave-standards.md

Hub files (bonus +20) — whitelist HUBS: 1_receptionOS/4-go-to-market/pipeline.md,
1_receptionOS/1-product/roadmap.md, 1_receptionOS/1-product/features.md,
1_receptionOS/4-go-to-market/modular-offer.md, _culture/team/team-roster.md, _sales/_kanban.md

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
3. Grep backlinki (wiki-linki do modułu) + krawędzie z frontmattera (`owner:`, `osoby:`, `dotyczy:`) → zidentyfikuj kontekst
4. Zastosuj 3 testy:
   - **Articulation Test:** "Ten moduł łączy się z [X] ponieważ ___"
   - **Agent Traversal Check:** "Agent podążając za linkiem podejmie jaką decyzję?"
   - **Sharpening Test:** "Dodanie info wyostrza czy rozmywa przekaz?"
5. Określ action → zastosuj (edytujesz **treść** modułu; `updated:` stampuje pre-commit — nie wpisuj go ręcznie)
6. Idź do KROK 3

### Dla wyników ze skanu:

Dla każdego HIGH (max 8, score descending):

1. **Przeczytaj** moduł docelowy (CAŁY plik)
2. **Przeczytaj** moduł/źródło triggering (np. pipeline.md, roadmap.md — zależnie od kontekstu)
3. **Zastosuj 3 testy** z reweave-standards.md
4. **Określ Reweave Action** (1 z 5):
   - **ADD CONNECTIONS** → dodaj wiki-links w treści (krawędzie osobowe tylko przez `owner:`/`osoby:`/`uczestnicy:`)
   - **REWRITE CONTENT** → zaktualizuj fakty, statusy, liczby
   - **SHARPEN** → usuń hedging, potwierdź zrealizowane
   - **SPLIT** → FLAG dla usera, nie wykonuj
   - **CHALLENGE** → STOP, pytaj usera
5. **Zastosuj** zmiany w treści modułu — `updated:` stampuje pre-commit, nie dopisujesz go ręcznie; `sources:` nie istnieje poza `-summary.md`
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
2. **Schema Check** — frontmatter: `type:` obecny? `status:` z enuma **właściwego dla typu**?
   - `modul` → stable | draft | needs-update | archive
   - `osoba` → aktywna | eks | zamknieta (plus wymagane `relacja:`)
   - `deal` → `_schemas/deal.yaml` ma `fields: {}`, więc `status:` nie ma tu enuma; legacy `status: stub` zamień na `draft` tylko jeśli i tak edytujesz plik
   Bez `cadence:`/`depends-on:`/`audience:`/`sources:` (`sources:` legalne wyłącznie w `_transcripts/**-summary.md`). `updated:` zostawiasz pre-commitowi.
   Przy wątpliwości nie zgaduj enuma — otwórz `_schemas/{typ}.yaml`.
3. **Neighbor Coherence** — przeczytaj 1 moduł, do którego prowadzi wiki-link. Zgadzają się na fakty?

Fail → jeśli to Schema Check na polu, którego sam dotknąłeś: popraw pole, nie cofaj treści.
W pozostałych przypadkach cofnij zmiany i dodaj do reweave-queue.md z notatką.
Frontmatter niezgodny ze schematem, ale zastany (nie Twoja edycja) → zgłoś w raporcie, nie kasuj poprawnego reweave.

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
- Moduł ma `status: draft` → "Moduł jest draftem — reweave nie dotyczy. Rozważ uzupełnienie."
- Moduł ma `status: archive` → pomiń, archiwum jest poza staleness
- Plik ma legacy `status: stub` (wartość spoza enuma 2.0, `schema_lint` nie łapie jej na dealach) → traktuj jak `draft`; podmianę na `draft` zrób tylko przy okazji realnej edycji tego pliku
- Kandydat jest kartą osoby (`osoby/**`) → reweave dotyczy treści `## Stan`; enum statusu to aktywna | eks | zamknieta, NIE stable/draft
