---
name: pulse
description: |
  CEO Pulse — deep vault scan → structured briefing (radar, pipeline, stale intel) → 0-3 decision questions → module updates → 3 actionable next-session prompts.
  Use when: starting a work session, wanting a quick strategic overview, checking what needs attention,
  feeling out of sync with the vault, wanting to know what to work on next.
  Trigger phrases: "pulse", "pulse check", "co jest grane", "vault pulse", "co wymaga uwagi",
  "daj mi briefing", "zapytaj mnie", "status update", "what needs attention"
---

# CEO Pulse

Analizujesz vault i prezentujesz CEO briefing z intelligence — nie pytasz o rzeczy które CEO wie. Surfacujesz to czego CEO może nie widzieć: overdue follow-ups, approaching deadlines, cold pipeline, contradictions, cross-project risks.

Repo jest po polsku. Odpowiadaj po polsku.

**Zasada #1:** Nie pytaj "czy Simon wdrożył v3?" — CEO to wie. Pytaj "Gudan milczy od 2 tyg, event za 21 dni — gonić, czekać, czy odpuścić?"

**Zasada #2:** Każdy element briefingu musi mieć RECOMMENDED ACTION. Nie informuj — doradź.

---

## Quick Start

1. Deep scan vault (indeksy, hubs, staleness, pipeline analysis, deadline proximity)
2. Przygotuj CEO Briefing (radar + pipeline + decisions + stale intel)
3. Wyświetl briefing + zadaj 0-3 pytania decyzyjne (ALL AT ONCE)
4. Batch update modułów + strategic reflect
5. Zaproponuj 3 next-session prompts (highest-ROI work)

---

## FAZA 1: DEEP SCAN

Wszystko czytaj równolegle (parallel reads/tools):

**Indeksy:**
- `1_receptionOS/1_receptionOS_index.md`
- `2_apolonia/2_apolonia_index.md`
- `3_fte/3_fte_index.md`
- `_culture/culture_index.md`

**Hub files** (whitelist `HUBS` — budżet świeżości 7 dni):
- `1_receptionOS/4-go-to-market/pipeline.md`
- `1_receptionOS/1-product/roadmap.md`
- `1_receptionOS/1-product/features.md`
- `1_receptionOS/4-go-to-market/modular-offer.md`
- `_culture/team/team-roster.md`
- `_sales/_kanban.md`

**Pozostałe pliki wejściowe:**
- `1_receptionOS/8-strategy/quest-board-*.md` (najnowszy)
- `2_apolonia/6-marketing/events.md`
- `_decisions-log.md` — **tom zamknięty** (`status: archive`, decyzje od 2026-07-29 idą do `_events/YYYY/`). Czytasz go jako historię, nie jako źródło stanu; nie raportuj jego staleness.

**Staleness check:**
Uruchom `python3 .claude/skills/graph/scripts/vault-graph.py . staleness` → parsuj JSON. Ratio liczy sam skrypt: świeżość z gita (ostatni commit dotykający pliku, commity z trailerem `Meta: true` pomijane), budżet dni: **hub 7d** (whitelist `HUBS` — wygrywa z typem), modul 60d, osoba 180d, deal 30d **tylko w `_sales/pipeline/active/`**. Poza sygnałem (skrypt sam je wycina): `status: archive`, `4_apollo/**`, encje write-once, deale spoza `pipeline/active/`.

Wyciągnij:
- `stale_hubs` — **pierwsza pozycja radaru**, jeśli niepuste. Hub po 7 dniach jest przeterminowany, a to pliki, z których korzysta cały zespół.
- top 10 z `top_30` z `staleness_ratio > 1.0` (poza hubami) — do STALE INTEL.

Jeśli JSON ma niepuste `warnings` (brak gita → fallback na mtime albo ścieżki gita nie pasują do vaulta), zaznacz to w briefingu — ranking jest wtedy zaniżony.

**Drafty i needs-update:**
Grep: `status: draft` i `status: needs-update` w folderach projektowych.
Dodatkowo grep legacy `status: stub` — wartość spoza enuma 2.0 (stable | draft | needs-update | archive), której `schema_lint` nie łapie na dealach (`deal.yaml` → `fields: {}`). Trafienia poza `_archive/` i `_network/` raportuj jako dług migracji („do zmiany na `draft`"), nie jako zwykły draft.

**Backlog:**
Sprawdź `_transcripts-backlog/` — ile transkrypcji czeka.

### Nowe analizy (po przeczytaniu hub files):

**Pipeline intelligence:**
- Przeskanuj pipeline.md sekcję "Next Steps" każdego deala
- Zidentyfikuj deals z follow-up/next-steps starszymi niż 14 dni od dzisiaj → to "cold pipeline"
- Zidentyfikuj deals w onboarding/demo-done bez aktywności → to "stuck deals"
- Policz funnel: Lead → Demo Done → Onboarding → Live

**Deadline proximity:**
- Z roadmap, events, quest board — wyciągnij daty w ciągu najbliższych 21 dni
- Posortuj chronologicznie — to "approaching deadlines"

**Commitment tracker:**
- Z quest board i pipeline — znajdź "next steps" i "TODO" items
- Porównaj z datami — które są overdue?

---

## FAZA 2: CEO BRIEFING

Na bazie Fazy 1, wygeneruj i wyświetl briefing. Format:

```
═══ CEO PULSE — {data} ═══

RADAR

{3-5 sygnałów wymagających uwagi CEO}

Każdy sygnał w formacie:
{emoji} {one-liner}
  {kontekst — 1-2 zdania, co widzisz w vault}
  → Recommended: {konkretna akcja}

Typy sygnałów (priorytet):
1. Approaching deadlines — eventy/ETA w ciągu 21 dni
2. Cold pipeline — deals bez aktywności >14 dni
3. Overdue commitments — obiecane a nie zrobione
4. Team/capacity risks — SPOF, overload, brak backupu
5. Cross-project dependencies — coś w projekcie A blokuje B
6. Contradictions — 2 pliki mówią co innego

---

PIPELINE HEALTH

{Funnel snapshot}
Lead ({N}) → Demo Done ({N}) → Onboarding ({N}) → Live ({N})

Moved since last update:
- {deal} {old_status} → {new_status}

Stuck (>14 dni bez ruchu):
- {deal} — last activity {data}, next step: {co miało się stać}

---

DECISIONS NEEDED

{0-3 pytań — TYLKO gdy vault genuinely nie zna odpowiedzi I odpowiedź zmienia strategię}

Jeśli 0 pytań → napisz: "Vault ma wystarczająco info — brak decyzji wymagających inputu."

Każda decyzja:
{N}. {Tytuł}
   Kontekst: {co widzisz, dlaczego to ważne}
   Opcje: A) ... B) ... C) ...

---

STALE INTEL

{Top 3-5 modułów z najwyższym staleness ratio I dużą liczbą incoming links}
Posortowane po priority_score (ratio × incoming_links).

| Moduł | Ostatni update | Ratio | Incoming links |
|-------|---------------|-------|----------------|
| ... | ... | ... | ... |

```

### Reguły briefingu:

- **Radar:** Min 3, max 5 sygnałów. Min 2 różne projekty. Preferuj sygnały z recommended action wpływającą na >1 moduł.
- **Pipeline:** Uwzględnij WSZYSTKIE aktywne deals (nie tylko top 3). Bądź konkretny o tym co stoi.
- **Decisions:** NIGDY nie pytaj o statusy ("czy Simon wdrożył?"). Pytaj o kierunek ("Gudan milczy — gonić czy odpuścić?"). Jeśli vault ma odpowiedź — nie pytaj.
- **Stale Intel:** Pokaż tylko moduły projektowe (nie meta/skill files). Sortuj po priority_score desc.

---

## FAZA 3: QUICK DECISIONS

Jeśli Faza 2 zidentyfikowała 1-3 pytania decyzyjne:

Zadaj je WSZYSTKIE NA RAZ przez AskUserQuestion (1 call, multi-question).

Format pytania:
- Krótki kontekst (1-2 zdania — co widzisz w vault, czemu to ważne)
- 2-4 opcje (konkretne kierunki, nie statusy)
- Header: skrócona nazwa (max 12 znaków)

Jeśli 0 pytań — przejdź od razu do Fazy 4.

---

## FAZA 4: UPDATE + REFLECT

### 4a. Plan zmian

Zbierz zmiany z:
- Odpowiedzi na pytania z Fazy 3 (jeśli były)
- Oczywiste staleness do auto-update (milestones które minęły, daty które przeszły)
- Stale modules z Fazy 2 które można odświeżyć na bazie danych w vault

Wyświetl tabelę zmian. Poczekaj na akceptację.

### 4b. Wykonaj update

Dla każdego modułu:
1. Przeczytaj plik (jeśli nie czytany w Fazie 1)
2. Edytuj treść — fakt wplatasz w `## Stan`, datowane wpisy tylko w `## Log`
3. Frontmattera nie ruszasz: `updated:` stampuje pre-commit, `sources:` żyje wyłącznie w `_transcripts/**-summary.md`

### 4c. Strategic Reflect

NIE pisz "zaktualizowano X modułów". Pisz CO SIĘ ZMIENIŁO strategicznie:

```
REFLECT

Co się zmieniło:
- {insight — zmiana kierunku, nowe ryzyko, nowa szansa}
- {insight}

Otwarte wątki:
- {temat do monitorowania / zbadania w przyszłości}
```

---

## FAZA 5: NEXT SESSIONS

Zaproponuj 3 prompty na kolejne sesje Claude Code. Bazuj na tym co pulse odkrył:

```
═══ NEXT SESSIONS ═══

1. {Tytuł sesji}
   Objective: {co osiągnąć — 1 zdanie}
   Prompt: {gotowy prompt do wklejenia, np. "/reweave pipeline.md" lub konkretne zadanie}
   Key files: {2-3 ścieżki}
   Deliverable: {co powstanie}

2. ...

3. ...
```

### Źródła pomysłów na sesje (priorytet):

1. **Stale hub z dużą liczbą zależności** → `/reweave {path}`
2. **Backlog transkrypcji** → `/process-transcripts`
3. **Upcoming event wymaga materiałów** → `/brief` lub konkretny task
4. **Nowy kanał sprzedaży bez materiałów** → `/copy` lub `/brief`
5. **Strategiczna decyzja do podjęcia** → `/playscript`
6. **Pipeline wymaga follow-up materiałów** → task (email, propozycja, one-pager)
7. **Vault structure issues** → `/vault-audit` lub `/graph`
8. **Team/process knowledge gaps** → konkretny moduł do napisania

Każdy prompt powinien być gotowy do WKLEJENIA — nie "zrób coś z pipeline" ale konkretny, actionable prompt z kontekstem.

---

## Troubleshooting

| Problem | Rozwiązanie |
|---------|-------------|
| Vault jest świeży, mało sygnałów | Skup radar na forward-looking (approaching deadlines, commitment tracker) |
| Staleness script nie działa | Fallback: `git log -1 --format=%cs -- <plik>` na hubach i modułach, porównaj z budżetem (hub 7d, modul 60d, osoba 180d, deal 30d w `pipeline/active/`). Uwaga: `-1` nie odsiewa commitów `Meta: true` — przy podejrzeniu batcha użyj `git log --format='%cs %(trailers:key=Meta,valueonly)' -- <plik>` i weź pierwszą linię bez `true` |
| User nie chce odpowiadać na pytania | Skip Faza 3, przejdź do update + next sessions |
| Pipeline jest mały (0-3 deals) | Skup pipeline health na conversion quality, nie volume |
| Brak approaching deadlines | Radar → cross-project dependencies i team capacity risks |
