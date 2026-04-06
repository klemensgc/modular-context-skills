---
name: playscript
description: |
  Analyzes the repo (knowledge base) through the Playscript framework to surface new strategic angles.
  Scans all projects (ROS, Apolonia, Fundacja, Culture), identifies untapped opportunities, cross-project
  synergies, and blind spots. Outputs structured "plays" (Discover/Build/Amplify/Capture) with hypotheses,
  success factors, and milestones.
  Use when: looking for new strategic angles, wanting fresh perspective on what to do next, seeking
  cross-project opportunities, doing quarterly/monthly strategy review, feeling stuck on priorities.
  Trigger phrases: "playscript", "new angles", "strategic plays", "what am I missing",
  "fresh perspective", "cross-project synergy", "strategic review", "untapped opportunities"
---

# Playscript Engine

Analizuje repo jako second brain i surfacuje nowe strategiczne katy w formacie Playscript: Hypothesis, Plays (Discover/Build/Amplify/Capture), Success Factors, Milestones.

---

## Quick Start

1. Przeczytaj wszystkie 4 index files (ROS, Apolonia, Fundacja, Culture)
2. Przeczytaj kluczowe hub files (pipeline, roadmap, quest-board, priorities)
3. Przeskanuj ostatnie transkrypcje (2-4 tygodnie) pod katem nowych sygnalow
4. Wygeneruj 3-7 plays w formacie Playscript
5. Przeprowadz Rade Starcow — 5 person analizuje sytuacje i debatuje
6. Wygeneruj PDF (automatycznie po Verdict)
7. Zapytaj usera ktore plays chce eksplorowac
8. Zaproponuj deliverables (nowe MDs) na bazie wybranych plays
9. Wejdz w plan mode — user akceptuje, ty tworzysz pliki

---

## Framework: 4 typy plays

| Typ | Cel | Pytanie kluczowe |
|-----|-----|-------------------|
| **DISCOVER** | Eksploruj nowe mozliwosci, zrozum landscape | "Czego jeszcze nie wiemy, a powinnimy?" |
| **BUILD** | Stworzenie kluczowych capabilities | "Co musimy zbudowac zeby odblokować wartosc?" |
| **AMPLIFY** | Skaluj to co juz dziala | "Co juz dziala i mozna pomnożyc?" |
| **CAPTURE** | Monetyzacja, extract value | "Gdzie lezy wartosc ktorej nie zbieramy?" |

---

## Algorytm analizy

### Faza 1: Skan stanu aktualnego

Przeczytaj nastepujace pliki (rownolegle gdzie mozliwe):

**Index files (obowiazkowe):**
- `1_receptionOS/1_receptionOS_index.md`
- `2_apolonia/2_apolonia_index.md`
- `3_fte/3_fte_index.md`
- `_culture/culture_index.md`

**Hub files (obowiazkowe):**
- `1_receptionOS/4-go-to-market/pipeline.md` — status klientow
- `1_receptionOS/1-product/roadmap.md` — dokad zmierza produkt
- `1_receptionOS/8-strategy/strategy_index.md` — quest board
- `2_apolonia/5-strategy/priorities.md` — OKR-y Apolonii
- `_culture/team/team-roster.md` — kto jest wolny, kto przeciazony

**Opcjonalne (czytaj gdy potrzeba glebszej analizy):**
- `1_receptionOS/3-market/competitive.md` — landscape konkurencji
- `1_receptionOS/4-go-to-market/modular-offer.md` — oferta
- `1_receptionOS/1-product/features.md` — matryca funkcji
- `2_apolonia/7-operations/1-pozyskanie.md` — patient acquisition
- `_culture/philosophy.md` — zasady decyzyjne
- `_culture/influences.md` — modele mentalne

**Transkrypcje (ostatnie 2-4 tygodnie):**
- Sprawdz `_transcripts-backlog/` — nieprzepracowane dane
- Przeskanuj ostatnie pliki w `_transcripts/` (sortuj po dacie)

### Faza 2: Mining katow

Szukaj w przeczytanych danych:

**Cross-project synergies:**
- Co Apolonia ma czego ROS potrzebuje (i odwrotnie)?
- Jak Fundacja moze pomoc ROS/Apolonii (i odwrotnie)?
- Ktore zasoby (ludzie, tech, brand) sa wspoldzielone i niedostatecznie wykorzystane?

**Unexplored territories:**
- Tematy poruszone w transkrypcjach ale nieobecne w modulach
- Pytania otwarte (`Open Questions` w index files) od dawna bez odpowiedzi
- Pliki `status: stub` lub `status: needs-update` — zaniedbane obszary
- Stare daty `updated:` (>4 tygodnie) w strategicznych plikach

**Asymetric opportunities (high leverage):**
- Male dzialania ktore moga dac duzy efekt
- Istniejace assety ktore mozna ponownie wykorzystac
- Relacje/partnerstwa ktore mozna poglebic
- Quick wins ktore nikt nie podejmuje

**Blind spots:**
- Co powinno byc w repo ale nie istnieje?
- Jakie decyzje sa odkladane?
- Gdzie brakuje danych do podjecia decyzji?
- Ktore ryzyka nie maja mitygacji?

**Timing signals:**
- Deadlines, eventy, okna mozliwosci
- Zmiany w zespole (nowi ludzie, odejscia)
- Zmiany rynkowe wspomniane w transkrypcjach

### Faza 3: Formulowanie plays

Dla kazdego znalezionego kata stworz play:

```markdown
### [DISCOVER/BUILD/AMPLIFY/CAPTURE] Play: [nazwa]

**Hypothesis:** [bold statement — co uwazasz ze jest mozliwe]

**Evidence:** [2-3 konkretne zrodla z repo, z linkami [[wiki-link]]]

**Success Factors:**
- [ ] [mierzalny warunek sukcesu 1]
- [ ] [mierzalny warunek sukcesu 2]
- [ ] [mierzalny warunek sukcesu 3]

**Milestones:**
1. [krok 1] — [timeframe]
2. [krok 2] — [timeframe]
3. [krok 3] — [timeframe]

**Dependencies:** [co musi byc prawda/gotowe zeby to zadziałalo]

**Risk:** [co moze pojsc nie tak]
```

### Faza 4: Priorytetyzacja i prezentacja

Posortuj plays wedlug:
1. **Leverage** — maly wysilek, duzy efekt (styl Naval)
2. **Timing** — okno mozliwosci sie zamyka
3. **Evidence strength** — ile danych wspiera hipoteze

Prezentuj userowi w formacie:

```markdown
# Playscript Analysis — [data]

## Stan gry (1 akapit)
[Krotkie podsumowanie: co sie dzieje teraz across all projects]

## Plays (posortowane wg leverage)

### 1. [AMPLIFY] Nazwa play — HIGH LEVERAGE
...

### 2. [DISCOVER] Nazwa play — TIMING SENSITIVE
...

### 3. [BUILD] Nazwa play — FOUNDATION
...

## Blind Spots
[Lista rzeczy ktorych brakuje w repo]

## Recommended Next Move
[1 konkretny nastepny krok — co zrobic DZISIAJ]

## Rada Starcow

[Debata 5 person — patrz Faza 5]
```

---

## Faza 5: Rada Starcow (5 agentow)

Po zakonczeniu analizy plays i blind spots, uruchom 5 ROWNOLEGLYCH agentow.
Kazdy agent to gleboka, wielowarstwowa analiza z perspektywy jednej persony.

### Persony

Kazda persona ma pelny brief (~100 linii) w `references/personas/`.
Przeczytaj odpowiedni brief PRZED uruchomieniem agenta.

| Persona | Lens | Brief |
|---------|------|-------|
| Elon Musk | First-principles, 10x scale, bottleneck hunting | `references/personas/elon-musk.md` |
| Naval Ravikant | Leverage, asymmetric bets, specific knowledge | `references/personas/naval-ravikant.md` |
| Steve Jobs | Radical focus, user experience, subtraction | `references/personas/steve-jobs.md` |
| Marek Aureliusz | Dichotomy of control, virtue, premeditatio malorum | `references/personas/marcus-aurelius.md` |
| Howard Roark | Integrity of vision, zero compromise, creator vs second-hander | `references/personas/howard-roark.md` |

### Krok 1: Przygotuj CONTEXT BRIEF

Zanim uruchomisz agentow, przygotuj CONTEXT BRIEF — jedno streszczenie
calej analizy z Faz 1-4 ktore kazdy agent dostanie w prompcie:

```
CONTEXT BRIEF:

## Stan gry
[1 akapit — co sie dzieje teraz across all projects]

## Kluczowe metryki
[3-7 liczb z repo — klienci, marza, pipeline, team size, runway]

## Plays (z Fazy 3)
[Lista: tytul + hypothesis kazdego play]

## Blind spots
[Lista z Fazy 2]

## Dane zrodlowe
[Sciezki do kluczowych plikow ktore agent powinien przeczytac
aby poglebic analize — np. pipeline.md, team-roster.md, roadmap.md]
```

### Krok 2: Uruchom 5 agentow ROWNOLEGLE

Uzyj Task tool. Wyslij WSZYSTKIE 5 w JEDNYM message (parallel tool calls).

Parametry kazdego agenta:
- `subagent_type`: `"general-purpose"`
- `model`: `"opus"` (wymagany dla glebokiej analizy)
- `name`: `"rada-[persona]"` (np. `"rada-musk"`, `"rada-naval"`)
- `description`: `"Rada Starcow: [persona name] analysis"`

### Krok 3: Agent prompt

Kazdy agent dostaje TEN PROMPT (z podmienionymi wartosciami):

```
# Rada Starcow — [PERSONA NAME]

## Twoja rola

Jestes [PERSONA NAME]. Przeanalalizuj sytuacje z perspektywy swojej filozofii.

ZANIM zaczniesz analize, przeczytaj:
1. Swoj persona brief: [SCIEZKA DO references/personas/{name}.md]
2. Kluczowe pliki zrodlowe (lista w CONTEXT BRIEF)

To NIE jest szybki komentarz. To pelna sesja strategiczna — gleboki internal
monologue jak gdybys analizowal to w samotnosci, szczerze, bez publicznosci.

## CONTEXT BRIEF

[WKLEJ PELNY CONTEXT BRIEF Z KROKU 1]

## Format odpowiedzi

### Internal Monologue (3-5 akapitow)
Stream of consciousness w stylu twojej persony. Mysl glosno. Zadawaj sobie
pytania. Kwestionuj zalozenia. Podazaj za watkami. Jesli widzisz cos w danych
co cie niepokoi — rozwin ten watek. Jesli widzisz szanse ktora inni przegapiaja
— rozwin. Badz SZCZERY — nie serwilizuj, nie mow co user chce uslyszec.
Odnosl sie do KONKRETNYCH danych z repo (nazwy plikow, liczby, imiona ludzi).

### Kluczowe Obserwacje (3-5 numerowanych)
Kazdy insight: 2-3 zdania z EVIDENCE z repo.
Nie ogolniki — konkrety z plikow, transkrypcji, metryk.

### Rekomendacja
JEDNA konkretna akcja. Co zrobic JUTRO RANO.
Z uzasadnieniem DLACZEGO z perspektywy twojej filozofii.

### Punkt Napiecia
Gdzie twoja perspektywa koliduje z innymi personami Rady?
Z kim sie nie zgadzasz i dlaczego? 2-3 zdania.

## Zasady
- JEZYK: polski z angielskimi terminami (jak w repo)
- TON: bezposredni, bezkompromisowy, w pierwszej osobie
- NIGDY nie wymyslaj danych — tylko to co jest w CONTEXT BRIEF i w plikach
- Cytuj pliki: [[nazwa-pliku]], liczby, imiona ludzi
- Pisz TAK JAK ta persona by mowila — nie jak akademicki esej
```

### Krok 4: Zbierz i przedstaw

Po otrzymaniu 5 odpowiedzi:

1. Przedstaw KAZDA analize W PELNI (nie streszczaj, nie parafrazuj)
2. Dodaj na koncu **VERDICT** (pisz TY, nie agent):

```markdown
## Verdict

**Punkt zbiegu:** [Gdzie 3+ person sie ZGADZA — sformuluj jasno]

**Punkt konfliktu:** [Gdzie sie ROZCHODZA — sformuluj jasno]

**Rekomendowany nastepny krok:** [Wazony konsensus — co zrobic JUTRO,
uwzgledniajac argumenty kazdej strony]
```

### Zasady Rady

- Agenci MUSZA czytac persona briefs i pliki zrodlowe — nie polegaj na streszczeniach
- 5 agentow rownolegle = ~2-3 min. NIE uruchamiaj sekwencyjnie
- Jezeli user chce poglebic debata (np. "niech porozmawiaja dalej o X"):
  uruchom ponownie 5 agentow z zawezonym CONTEXT BRIEF do tematu X
- Verdict pisz TY (glowny agent), nie deleguj do sub-agenta
- Jezeli user poprosi o PDF Rady Starcow — uzyj pipeline z Fazy 6

---

## Faza 6: PDF

Po Verdict AUTOMATYCZNIE generuj PDF.

### Szablon

Referencyjny design: `_workspace/2026-02/rada-starcow-v2-wireframe.html`

Kopiuj z niego:
- CSS (Cormorant Garamond + Inter, accent #8b7355, warm-white)
- SVG logo
- Klasy: `.play-card`, `.persona-full`, `.verdict-box`, `.conv-table`, `.metric-card`
- Layout: A4 (210mm x 297mm), `@page`, `page-break-after: always`

### Struktura stron (8-9 stron)

1. Cover (tytul, data, persony)
2. Stan Gry + Metryki
3. Plays 1-3 (`.play-card` z type badge)
4. Plays 4-6 + Blind Spots
5. Rada Starcow I (2 persony)
6. Rada Starcow II (3 persony)
7. Convergence/Divergence (`.conv-table`)
8. Verdict & Action Plan

### Generowanie

```bash
# plik w _workspace/{YYYY-MM}/
weasyprint rada-starcow-v{N}-wireframe.html rada-starcow-v{N}-wireframe.pdf
```

Wersja: inkrementuj od ostatniej (v3, v4, v5...).
Informuj usera o sciezce po wygenerowaniu.

---

## Faza 7: Wybor plays do eksploracji

Po dostarczeniu PDF, ZAPYTAJ usera ktore plays chce eksplorowac dalej.

Uzyj `AskUserQuestion`:
- Pytanie: "Ktore plays chcesz eksplorowac?"
- `multiSelect: true`
- Opcje: lista plays z Fazy 3 (nazwy + typy)
- User moze tez napisac wlasna odpowiedz

### Po wyborze

Dla kazdego wybranego play:
1. Przeczytaj WSZYSTKIE powiazane pliki z repo (evidence + depends-on)
2. Rozwin play do pelnego planu z konkretnymi deliverables
3. Zaproponuj NOWE pliki .md ktore powinny powstac

---

## Faza 8: Deliverables — propozycja nowych MDs

Na podstawie wybranych plays + calej analizy Rady Starcow,
zaproponuj userowi liste nowych plikow .md do stworzenia.

### Format propozycji

Dla kazdego deliverable:

```markdown
### [PLAY TYPE] Deliverable: [nazwa pliku]

**Play source:** [nazwa play z Fazy 3]
**Sciezka:** [folder/nazwa-pliku.md]
**Cel:** [co ten plik rozwiazuje — 1 zdanie]
**Content outline:**
1. [sekcja 1]
2. [sekcja 2]
3. [sekcja 3]
**Nowe dane z Rady:** [co Rada surfacowala czego nie bylo w repo]
```

### Typowe deliverables

| Typ play | Typowy deliverable |
|----------|-------------------|
| AMPLIFY | Partnership brief, outreach template, case study draft |
| BUILD | SOP, checklist, process doc, architecture decision |
| CAPTURE | Pricing doc update, offer simplification, financial model |
| DISCOVER | Research brief, experiment design, feasibility analysis |

Pytaj usera ktore deliverables chce wykonac (AskUserQuestion, multiSelect).

---

## Faza 9: Plan Mode — wykonanie plays

Po wyborze deliverables, WEJDZ w plan mode (`EnterPlanMode`).

W planie:
1. Lista wybranych deliverables z Fazy 8
2. Dla kazdego: sciezka pliku, content outline, zrodla danych
3. Kolejnosc tworzenia (dependencies)
4. Estymacja: ktore pliki wymagaja dodatkowego czytania z repo

Po zaakceptowaniu planu: twórz pliki jeden po drugim.
Po kazdym pliku: aktualizuj `updated:` w powiazanych index files.

---

## Parametry uruchomienia

User moze zawezic scope dodajac argumenty:

| Argument | Efekt |
|----------|-------|
| `playscript` | Pelna analiza all projects |
| `playscript ros` | Tylko ReceptionOS |
| `playscript apolonia` | Tylko Apolonia |
| `playscript fundacja` | Tylko Fundacja Edison |
| `playscript cross` | Tylko cross-project synergies |
| `playscript blindspots` | Tylko blind spots i missing pieces |

Parsuj argument po spacji. Domyslnie: pelna analiza.

---

## Zasady

- NIGDY nie wymyslaj danych — kazdy play musi miec `Evidence` z konkretnych plikow
- NIGDY nie powtarzaj tego co user juz wie (obecne priorytety z index files) — szukaj NOWYCH katow
- Preferuj kontrintuicyjne obserwacje nad oczywiste
- Jezyk: mieszany PL/EN jak w repo (polski z angielskimi terminami)
- Nie proponuj plays ktore wymagaja zasobow ktorych team nie ma (sprawdz team-roster)
- Kazdy play musi byc actionable — "zbadaj rynek X" to za malo, podaj konkretny pierwszy krok
- Minimum 3 plays, maksimum 7. Jezeli jest wiecej, wybierz najsilniejsze

---

## Troubleshooting

| Problem | Rozwiazanie |
|---------|-------------|
| Za malo plays | Sprawdz transkrypcje — tam sa surowe dane |
| Plays sa oczywiste | Skup sie na cross-project i blind spots |
| Brak evidence | Nie wymyslaj — lepiej mniej plays z mocnym evidence |
| User chce glebiej w 1 play | Przeczytaj wszystkie powiazane pliki i rozwin play do pelnego planu |
