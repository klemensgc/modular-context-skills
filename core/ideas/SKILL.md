---
name: ideas
description: |
  Generates new ideas by reading current projects, interests, and open questions across the vault.
  Uses 6 idea triggers (gaps, intersections, analogies, contrarian, scale, subtraction) to produce
  ranked, actionable ideas grounded in your actual context.
  Use when: brainstorming, looking for new angles, wanting creative input based on vault reality,
  feeling stuck, exploring what to build or try next.
  Trigger phrases: "ideas", "generate ideas", "pomysły", "nowe pomysły", "brainstorm",
  "co mogę zrobić", "what could I do", "idea generation", "daj pomysły"
---

# Ideas

Generuje nowe pomysły czytając aktualne projekty, zainteresowania i otwarte pytania w vault. 6 typów triggerów.

Repo jest po polsku. Odpowiadaj po polsku.

---

## Quick Start

1. Przeczytaj 5 indeksów + quest-board + philosophy
2. Skanuj recent transkrypcje (30 dni)
3. Zastosuj 6 idea triggers
4. Wygeneruj 10-15 pomysłów z rankingiem
5. Pokaż top 5 z first steps

---

## Workflow

### Krok 1: Zbierz kontekst

Przeczytaj równolegle:

**Projekty:**
- `1_receptionOS/1_receptionOS_index.md`
- `2_apolonia/2_apolonia_index.md`
- `3_fte/3_fte_index.md`
- `4_apollo/4_apollo_index.md`
- `_culture/culture_index.md`

**Priorytety:**
- Najnowszy quest-board: `1_receptionOS/8-strategy/quest-board-*.md`
- `1_receptionOS/1-product/roadmap.md`

**Wartości i zasady:**
- `_culture/philosophy.md`
- `_culture/influences.md`

**Recent activity:**
- 5 najnowszych transkrypcji (across categories)
- 3 najnowsze session logs

### Krok 2: Szukaj open questions

Grep vault po sygnałach otwartych pytań:
- "?" w transkrypcjach (pytania zadane explicite)
- `status: needs-update` lub `status: stub` — luki w wiedzy
- Quest board items bez postępu
- Pipeline leads bez follow-up

### Krok 3: Zastosuj 6 idea triggers

**A. Gaps — Co brakuje?**
- Tematy wspominane ale nigdy pogłębione
- Rynki/segmenty niezaadresowane
- Problemy zidentyfikowane ale bez rozwiązania

**B. Intersections — Gdzie projekty się krzyżują?**
- Co z ROS może pomóc Apolonii?
- Co z Culture może wzmocnić GTM?
- Czy Fundacja i ROS mają wspólnych odbiorców?

**C. Analogies — Co z jednego projektu pasuje do drugiego?**
- Strategie sprzedaży ROS → Apolonia patient acquisition?
- Hormozi frameworks z GTM → Fundacja fundraising?
- Apollo automation → ROS internal ops?

**D. Contrarian — Co jeśli odwrotnie?**
- A gdyby NIE skalować ROS?
- A gdyby Apolonia była software company?
- A gdyby zespół był 2× mniejszy?

**E. Scale — Obecne podejście × 10**
- ROS × 10: co się łamie? Co trzeba zbudować?
- Apolonia × 10 klinik: co by się zmieniło?
- Co by umożliwiło 10× bez 10× ludzi?

**F. Subtraction — Co gdyby przestać?**
- Co gdyby zrezygnować z [projektu/aktywności]?
- Które aktywności dają <20% value przy >80% effort?
- Co by się stało gdyby nic nie robić przez miesiąc?

### Krok 4: Generuj i rankuj

Dla każdego pomysłu (celuj w 10-15):

```
IDEA #[N]: [Jednozadaniowe sformułowanie]

Type: [Gap / Intersection / Analogy / Contrarian / Scale / Subtraction]

Why now:
[Co w vault sprawia, że ten pomysł jest aktualny — 1-2 zdania
z odniesieniem do konkretnego pliku/transkryptu]

First step:
[JEDNA konkretna akcja żeby przetestować — max 2h pracy]

Risk:
[Co może pójść nie tak — 1 zdanie]

Impact: [HIGH / MEDIUM / LOW]
Effort: [HIGH / MEDIUM / LOW]
Alignment: [HIGH / MEDIUM / LOW] (z quest-board)
```

### Krok 5: Podsumuj

Posortuj po: Impact HIGH first, potem Effort LOW first, potem Alignment HIGH first.

```
IDEAS REPORT — [data]

TOP 5 (high impact, low effort, high alignment):
1. [Idea] — [type] — First step: [action]
2. ...

FULL LIST (10-15 ideas):
[Tabela: # | Idea | Type | Impact | Effort | Alignment]

PATTERNS:
[Co łączy najlepsze pomysły? Czy wskazują kierunek?
1-2 zdania meta-insight.]

CHALLENGE:
[Jeden pomysł który jest niewygodny ale potencjalnie
najważniejszy — dlaczego go unikasz?]
```

---

## Arguments

| Argument | Co robi |
|----------|---------|
| (none) | Cross-project ideas (default) |
| `ros` | Ideas only for ROS |
| `apolonia` | Ideas only for Apolonia |
| `fundacja` | Ideas only for Fundacja |
| `growth` | Focus na growth/scaling ideas |
| `product` | Focus na product ideas |
| `"temat"` | Ideas wokół konkretnego tematu |

---

## Troubleshooting

| Problem | Rozwiązanie |
|---------|-------------|
| Za generyczne pomysły | Idź głębiej do transkrypcji. Generic = za mało context. Przeczytaj więcej raw data. |
| Za dużo pomysłów (>20) | Filtruj po Alignment z quest-board — tylko HIGH alignment |
| Pomysły nie są actionable | Każdy MUSI mieć "First step" z limitem 2h. Jeśli nie da się opisać — pomysł jest za abstrakcyjny |
| Overlap z /playscript | /playscript = strategic plays (Discover/Build/Amplify/Capture framework). /ideas = brainstorm list (6 triggers). Inne formaty, inne podejście. |
| Overlap z /emerge | /emerge szuka implicit patterns (co JEST ale nie jest napisane). /ideas generuje NEW pomysły (co MOGŁOBY BYĆ). |
| User chce ideas na konkretny problem | Użyj `/ideas "problem"` — skip full scan, focus na 6 triggers dla jednego tematu |
