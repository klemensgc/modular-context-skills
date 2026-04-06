---
name: learned
description: |
  Turns recent learnings from the vault into a polished "What I Learned" post ready for sharing.
  Reads session logs, transcripts, and module changes to extract insights, then composes a
  personal, reflective piece with Context-Insight-Implication structure.
  Use when: wanting to write about recent learnings, reflecting on a period, creating content
  from vault knowledge, preparing a newsletter or social post about lessons.
  Trigger phrases: "learned", "what I learned", "co się nauczyłem", "learnings post",
  "czego się nauczyłem", "lessons", "write about learnings", "post o lekcjach"
---

# Learned

Zamienia ostatnie learningi z vault w dopracowany post "What I Learned" gotowy do udostępnienia.

Repo jest po polsku. Odpowiadaj po polsku (chyba że user poprosi o EN).

**Kluczowa różnica:** `/learned` = dopracowany post do SHARING (polished writing). `/weekly-learnings` = operacyjne podsumowanie dla SIEBIE (review).

---

## Quick Start

1. Zapytaj o okres (tydzień / miesiąc / kwartał)
2. Zbierz raw learnings — session logs, transkrypcje, module changes
3. Pogrupuj po tematach
4. Skomponuj post: 5-8 learnings, każdy Context → Insight → Implication
5. Draft → feedback → finalize → zapisz

---

## Workflow

### Krok 1: Określ okres

Użyj AskUserQuestion:

"Z jakiego okresu chcesz wyciągnąć learningi?"

Opcje:
- "Ostatni tydzień"
- "Ostatni miesiąc"
- "Ostatni kwartał"
- Other (custom period)

### Krok 2: Zbierz raw learnings

Na bazie wybranego okresu, przeczytaj równolegle:

**Session logs z okresu:**
- `_claude/4-sessions/` — Glob for matching dates
- Wyciągnij: key decisions, discoveries, fixes, aha moments

**Transkrypcje z okresu:**
- `_transcripts/` — filtruj po dacie w nazwie lub frontmatter
- Wyciągnij: insights, surprises, zmiany myślenia

**Module changes z okresu:**
- Grep `updated: [YYYY-MM]` matching the period
- Sprawdź co się zmieniło i dlaczego (porównaj z sources)

**Quest board changes:**
- Porównaj quest-boards z początku i końca okresu (jeśli istnieją oba)
- Zidentyfikuj: co się przesunęło w priorytetach

### Krok 3: Pogrupuj i wyfiltruj

Pogrupuj raw learnings po temacie:

| Temat | Opis |
|-------|------|
| Product | Learnings o produkcie, features, UX |
| Team | Learnings o zespole, delegowaniu, hiring |
| Strategy | Learnings o strategii, rynku, competition |
| Personal | Learnings o sobie, productivity, nawykach |
| Technical | Learnings techniczne, narzędzia, procesy |
| Business | Learnings o pieniądzach, cenach, sprzedaży |

Wyfiltruj do 5-8 najsilniejszych (tych z najjaśniejszym "aha").

### Krok 4: Skomponuj post

**Format per learning:**

```
## [N]. [Tytuł learningu — max 10 słów]

[CONTEXT — 1-2 zdania: co się działo, sytuacja]

[INSIGHT — 1-2 zdania: co zrozumiałem, aha moment]

[IMPLICATION — 1-2 zdania: co zmieniam, jak to wpływa na przyszłość]
```

**Ton:**
- Osobisty, refleksyjny, szczery
- Jak pisanie do przyjaciela, nie do bloga
- Unikaj buzzwords i generycznych "porad"
- Grounded w KONKRETNYCH sytuacjach z vault (ale bez wrażliwych danych)

**Struktura posta:**

```
# What I Learned — [okres]

[1-2 zdania intro: kontekst okresu, co się działo ogólnie]

---

## 1. [Learning]
[Context → Insight → Implication]

## 2. [Learning]
...

## [5-8]. [Learning]
...

---

[1-2 zdania closing: co łączy te learningi, jaki pattern widzę]
```

### Krok 5: Iterate i finalize

1. Pokaż draft userowi
2. Zapytaj o feedback (zbyt osobiste? Za mało konkretne? Zmienić ton?)
3. Iteruj
4. Zapisz do `_workspace/{YYYY-MM}/wN/learned-{YYYY-MM-DD}.md`

---

## Arguments

| Argument | Co robi |
|----------|---------|
| (none) | Pyta o okres (interactive) |
| `week` | Learnings z ostatniego tygodnia |
| `month` | Learnings z ostatniego miesiąca |
| `quarter` | Learnings z ostatniego kwartału |
| `en` | Post po angielsku |

---

## Troubleshooting

| Problem | Rozwiązanie |
|---------|-------------|
| Za mało danych w okresie | Rozszerz okres. Powiedz: "Tydzień ma za mało — proponuję miesiąc." |
| Learnings brzmią banalnie | Idź głębiej do transkrypcji. Szukaj momentów zaskoczenia, zmiany zdania, porażek. |
| Za osobiste / wrażliwe | Zaproponuj generalizację: "Zamiast 'klient X odmówił' → 'odmowa od klienta ujawniła...'." |
| User chce EN | Użyj `/learned en` lub powiedz po askuseru |
| Overlap z /weekly-learnings | /learned = POLISHED post do sharing. /weekly-learnings = OPERATIONAL review dla siebie. Inne cele. |
| Overlap z /pulse | /pulse aktualizuje VAULT. /learned generuje CONTENT z vault. Odwrotny kierunek. |
