---
name: sync
description: |
  Synchronizes knowledge between modular-context (CEO brain) and apollo-vault (clinic AI brain).
  Reads sync contract, detects desync between repos, generates strategy brief, pulls operational insights.
  Use when: after pulse or process-transcripts, when team changes happen, before important decisions,
  when you suspect the two repos are out of sync, periodically (weekly).
  Trigger phrases: "sync", "synchronize vaults", "update apollo", "bridge", "sync repos",
  "zsynchronizuj", "aktualizuj apollo", "co jest desync", "sync vaults"
---

# Sync

Synchronizujesz wiedzę między modular-context (MC) i apollo-vault (AV). Czytasz contract, wykrywasz desync, proponujesz zmiany, po akceptacji wykonujesz sync.

Repo jest po polsku. Odpowiadaj po polsku.

---

## Quick Start

1. Czytaj contract: `_claude/7-skill-references/apollo-sync-contract.md`
2. Skanuj kluczowe pliki w obu repo (DETECT)
3. Porównaj i wylistuj desync (PROPOSE)
4. Po akceptacji usera: zaktualizuj pliki + strategy-brief + sync-log (EXECUTE)

---

## Architektura: One-Way Glass

```
modular-context (MC)              apollo-vault (AV)
  CEO brain                         Clinic AI brain
  /Users/.../modular-context/       /Users/.../apollo-vault/
       │                                  │
       │  MC → AV: strategy brief         │
       │  AV → MC: operational insights   │
       │                                  │
       └──── /sync = jedyny most ─────────┘
```

**Reguła #1:** MC może czytać i pisać do AV (via /sync).
**Reguła #2:** AV agents NIGDY nie widzą MC. Czytają tylko `0-system/strategy-brief.md`.
**Reguła #3:** `/sync` jest jedynym mostem. Ręczny trigger (nie automatyczny).

---

## Ścieżki repo

| Repo | Ścieżka |
|------|---------|
| MC (modular-context) | `/Users/kubagasienica/Desktop/all-transcripts/modular-context/` |
| AV (apollo-vault) | `/Users/kubagasienica/Desktop/apollo-vault/` |

---

## FAZA 1: DETECT

Przeczytaj contract: `_claude/7-skill-references/apollo-sync-contract.md`

Następnie skanuj kluczowe pliki w obu repo (parallel reads):

**MC — Sources of Truth:**

| Domena | Plik MC |
|--------|---------|
| Team roster | `_culture/team/team-roster.md` |
| Entity status | `2_apolonia/1-entities/*.md` |
| Priorities | `1_receptionOS/8-strategy/quest-board-w*.md` (najnowszy) |
| Roadmap | `1_receptionOS/1-product/roadmap.md` |
| Operations (high-level) | `2_apolonia/7-operations/*.md` |
| Recruitment | `2_apolonia/3-team/recruitment/*.md` |

**AV — Sources of Truth:**

| Domena | Plik AV |
|--------|---------|
| Personnel cards | `2-personel/personel_index.md` + karty |
| Patient journey SOPs | `3-pacjent/*.md` |
| Locations | `4-lokalizacje/*.md` |
| Insights | `0-system/insights/*.md` |

**AV — Bridge file:**
- `0-system/strategy-brief.md` — sprawdź `updated:` i `last-sync:`

**MC — Sync log:**
- `4_apollo/6-operations/sync-log.md` — ostatni wpis

### Porównanie

Dla każdej domeny z contract Ownership Table:
1. Sprawdź `updated:` w pliku Source of Truth
2. Sprawdź `updated:` w pliku konsumenta
3. Jeśli SoT nowszy niż konsument → **DESYNC**
4. Jeśli treści się różnią (nazwiska, statusy, daty) → **CONTRADICTION**

### Output DETECT

Wyświetl tabelę:

```
SYNC DETECT:

| # | Domena | SoT updated | Consumer updated | Status | Priority |
|---|--------|-------------|------------------|--------|----------|
| 1 | Team roster | 2026-02-19 | 2026-02-15 | DESYNC | HIGH |
| 2 | Priorities | 2026-02-19 | 2026-02-19 | OK | - |
...
```

Jeśli wszystko OK → "Repos are in sync. Last sync: [date]." i zakończ.
Jeśli znaleziono desync → przejdź do FAZY 2.

---

## FAZA 2: PROPOSE

Dla każdego DESYNC/CONTRADICTION, zaproponuj konkretną zmianę:

### MC → AV (push down)

| Typ | Przykład propozycji |
|-----|---------------------|
| Team change | "Elena start 01.03 — dodaj kartę w AV `2-personel/elena-sychla.md`" |
| Entity status | "AI Dent zmiana nazwy — zaktualizuj strategy-brief" |
| Priority shift | "Nowy quest board w8 — zaktualizuj strategy-brief sekcja Priorities" |
| Tool decision | "IQ Dental → Felgdent — dodaj do strategy-brief sekcja Tool Decisions" |

### AV → MC (pull up)

| Typ | Przykład propozycji |
|-----|---------------------|
| New insight | "insights/voicebot-bug-001.md — dodaj do MC pipeline/known issues" |
| SOP pattern | "Nowy pattern w emergency.md — zaktualizuj MC sop-emergency skeleton" |
| Onboarding done | "Elena onboarding complete — zaktualizuj MC team-roster status" |

### Contradictions

Dla każdej sprzeczności:
1. Pokaż obie wersje: "MC mówi X, AV mówi Y"
2. Zapytaj usera która wersja aktualna
3. Zanotuj rozwiązanie

### Output PROPOSE

```
SYNC PROPOSAL:

MC → AV (push):
1. [opis zmiany] → [plik AV]
2. ...

AV → MC (pull):
1. [opis zmiany] → [plik MC]
2. ...

Contradictions:
1. [MC mówi X, AV mówi Y] → zapytaj usera

Regenerate strategy-brief: TAK/NIE
```

Poczekaj na akceptację usera.

---

## FAZA 3: EXECUTE

Po akceptacji:

### 3a. Wykonaj zatwierdzone zmiany

Dla każdej zatwierdzonej propozycji:
1. Przeczytaj plik docelowy
2. Edytuj treść
3. Zaktualizuj `updated:` w frontmatter

### 3b. Regeneruj Strategy Brief

Jeśli były zmiany MC → AV, regeneruj `apollo-vault/0-system/strategy-brief.md`:

```yaml
---
title: "Strategy Brief — from modular-context"
updated: [dzisiaj]
generated-by: /sync skill
source: modular-context
do-not-edit-manually: true
---
```

Sekcje:
- **Current Priorities** — z najnowszego quest-board
- **Team Changes** — ostatnie zmiany (join/leave/rola)
- **Entity Status** — tabela 8 entities z aktualnym statusem
- **Tool Decisions** — aktywne migracje
- **Roadmap Alerts** — milestones wpływające na operacje
- **ROS Product Context** — skrót co ROS robi i w jakiej fazie
- **Last Sync** — timestamp + co się zmieniło

### 3c. Append do Sync Log

Dodaj wpis do `4_apollo/6-operations/sync-log.md`:

```markdown
## YYYY-MM-DD — Sync [tytuł]
- Pushed: [co MC → AV]
- Pulled: [co AV → MC]
- Contradictions resolved: [lista]
- Strategy brief: regenerated / unchanged
```

### 3d. Walidacja

Po wykonaniu:
1. Sprawdź `updated:` we wszystkich zmodyfikowanych plikach
2. Potwierdź brak otwartych contradictions
3. Wyświetl podsumowanie

---

## Troubleshooting

| Problem | Rozwiązanie |
|---------|-------------|
| apollo-vault nie istnieje | Sprawdź ścieżkę, zapytaj usera |
| Contract file brakuje | Stwórz z `_claude/7-skill-references/apollo-sync-contract.md` |
| Oba pliki mówią co innego | NIGDY nie wybieraj sam — pokaż obie wersje, zapytaj usera |
| Dużo desync (>10) | Priorytetyzuj: HIGH (team, entities) → MED (priorities) → LOW (insights) |
| AV jest puste/seed | Pierwsza synchronizacja — wygeneruj strategy-brief od zera |
| Plik w AV nie istnieje jeszcze | Stwórz go (np. nowa karta personelu) |

---

## Powiązane

- Contract: `_claude/7-skill-references/apollo-sync-contract.md`
- Sync log: `4_apollo/6-operations/sync-log.md`
- Strategy brief (AV): `apollo-vault/0-system/strategy-brief.md`
- Pulse skill: może triggerować sync po wykryciu zmian
- Process-transcripts: może triggerować sync po przetworzeniu backlogu
