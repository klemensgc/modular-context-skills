---
name: brief
description: |
  Creates polished PDF briefs, one-pagers, spec sheets, and guides through a structured pipeline:
  content (.md) -> design brief -> HTML wireframe -> WeasyPrint PDF.
  Use when: creating a PDF for a person (investor, partner, team member), building a spec sheet
  or product one-pager, making an onboarding guide, producing any designed multi-page deliverable.
  Trigger phrases: "brief", "one-pager", "spec sheet", "pdf brief", "create a pdf",
  "zrob brief", "przygotuj brief", "one pager", "pdf guide", "persona brief",
  "stwórz pdf", "brief dla", "guide for", "zrob pdf"
---

# Brief

Tworzy profesjonalne PDF briefy, one-pagery, spec sheety i guide'y przez 4-krokowy pipeline: Content -> Design Brief -> HTML Wireframe -> PDF. Prowadzi usera przez decyzje, researchy i iteracje.

Repo jest po polsku. Odpowiadaj po polsku, chyba że brief jest po angielsku.

---

## Quick Start

1. Zbierz decyzje (audience, pages, concept, tone, template)
2. Research kontekst (repo + web)
3. Draft content (.md)
4. Validate concept z userem
5. Build wireframe (.html)
6. Export PDF (weasyprint)
7. Iterate na feedback

---

## FAZA 0: INTAKE

Zapytaj usera przez AskUserQuestion (max 2 pytania, reszta domyślna):

### Pytanie 1: Kto i co?

```
"Dla kogo jest ten brief i jaki ma cel?"
```

Opcje: wyprowadź z kontekstu. Np.:
- "Investor one-pager (EN, 1-2 pages)"
- "Team onboarding guide (PL, 4-8 pages)"
- "Client spec sheet (EN/PL, 2-6 pages)"
- Other

### Pytanie 2: Styl

```
"Jaki styl wizualny?"
```

3 style — wybierz jeden:
- **Siebe Light** (default) — Inter + JetBrains Mono, jasne tlo, accent #EB670F. Dla zewnetrznych osob, clean professional.
- **Siebe Dark** — Inter + JetBrains Mono, ciemne tlo #0C0A09, accent #EB670F. Dla investor briefs, tech people, filmowy vibe.
- **Rada Starcow** — Cormorant Garamond + Inter, warm cream, accent #8b7355. Dla internal strategy, heritage, eventy, task briefs. Sub-warianty: Compact Task (1 str/task), Arcadian Event.

### Domyślne wartości (nie pytaj, chyba że user chce zmienić):

| Decyzja | Default |
|---------|---------|
| Page size | A4 portrait |
| Language | PL (lub EN jeśli audience = international) |
| Tone | Confident, direct, no buzzwords |
| Max words/page | ~100 |

---

## FAZA 1: RESEARCH

### 1a. Context z repo

Przeczytaj równolegle:
- Odpowiedni project index (ROS/Apolonia/FTE/Apollo/Culture)
- Hub files relevantne do tematu (pipeline, roadmap, team-roster)
- Istniejące briefy w `_workspace/` — sprawdź czy jest coś podobnego

### 1b. Recipient research (jeśli brief dla osoby)

Jeśli brief jest personalizowany:
1. Sprawdź czy osoba ma "baseball card" w `_culture/team/` lub `_culture/team/externals.md`
2. Grep `_transcripts/` po imieniu — czy są notatki ze spotkań?
3. Jeśli brak danych w repo: WebSearch po imieniu + firmie (LinkedIn, bio)
4. Zbierz: tło zawodowe, firma, rola, co ich interesuje, connection do naszych projektów

### 1c. Existing briefs check

```
Glob: _workspace/**/*brief*.html
Glob: _workspace/**/*wireframe*.html
```

Sprawdź czy istnieje brief w podobnym stylu — użyj jako CSS/layout reference.

---

## FAZA 2: CONTENT DRAFT

### 2a. Stwórz content file

Zapisz do `_workspace/{YYYY-MM}/wN/{name}.md` (wN = tydzień: w1=1-7, w2=8-14, w3=15-21, w4=22-31).

Struktura zgodna z `_claude/2-templates/brochure.md`:

```markdown
---
title: {Nazwa} — {Koncept}
updated: YYYY-MM-DD
sources: [[source1]], [[source2]]
audience: {lista}
status: draft
language: en|pl
---

<!--
  FORMAT NOTES FOR DESIGN:
  - {N} pages, {size}, {orientation}
  - Concept: "{nazwa konceptu}"
  - Tone: {opis}
  - Max ~100 words body text per page
  - Style: {template name}
-->

<!-- PAGE 1 — {NAZWA} -->
## {Tytuł strony}

**{Tagline}**

<!-- [GRAPHIC: {opis}] -->

{Treść}

> **{Metric callout}**

---

<!-- PAGE 2 — {NAZWA} -->
...
```

### 2b. Copy rules

- Max ~80-100 słów body text per page (tabele/diagramy nie liczą się)
- Zero vendor names w treści (chyba że świadomie)
- Zero buzzwords: "powerful", "cutting-edge", "revolutionary", "game-changing"
- Graphic placeholders: `<!-- [GRAPHIC: opis] -->`
- Metric callouts: `> **[stat]**`
- Hormozi Value Equation (latent — nie nazywaj, po prostu stosuj):
  - Dream Outcome, Likelihood, Time Delay, Effort & Sacrifice
- StoryBrand (latent): klient = hero, produkt = guide

### 2c. Concept validation

Pokaż userowi:
1. Proposed concept (1-2 zdania)
2. Page breakdown (co na jakiej stronie)
3. Key metric/stat na każdej stronie

Zapytaj: "Concept OK? Coś zmienić?"

Jeśli user mówi "no concept" / "too generic" / "normie slogan" → zmień framing, zaproponuj 2-3 alternatywne koncepty.

---

## FAZA 3: HTML WIREFRAME

### 3a. Template skeleton

**Uzyj gotowy template HTML jako skeleton — nie buduj od zera:**

| Styl | Template | Copy-paste i wypelnij |
|------|----------|----------------------|
| Siebe Light | `references/template-siebe-light.html` | Default |
| Siebe Dark | `references/template-siebe-dark.html` | Ciemne tlo |
| Rada Starcow | `references/template-rada-starcow.html` | Warm heritage |

Kazdy template zawiera:
- Pelny CSS z palette, fontami, @page setup
- Inline SVG signet (kompletny path) — watermark + brand header
- Flexbox footer anchoring (QG-1 compliant)
- 2 strony z `<!-- REPLACE: -->` komentarzami
- Signet-bg na KAZDEJ stronie

**Procedura:** Read template → copy-paste → zamien `<!-- REPLACE: -->` na content → dodaj/usun strony.

Pelne CSS reference: `references/css-templates.md` (3 systemy z wszystkimi klasami).
Compact Task Brief template: `_claude/2-templates/compact-task-brief.md`

### 3b. Page structure

```html
<!DOCTYPE html>
<html lang="{en|pl}">
<head>
  <meta charset="UTF-8">
  <title>{Nazwa}</title>
  <style>
    @page { size: {W} {H}; margin: 0; }
    body { background: #e0e0e0; margin: 0; }
    .page {
      width: {W}; height: {H};
      background: white;
      margin: 20px auto;
      position: relative;
      overflow: hidden;
      page-break-after: always;
      display: flex; flex-direction: column;
    }
    @media print {
      body { background: white; }
      .page { margin: 0; box-shadow: none; }
    }
    /* ... style-specific CSS ... */
  </style>
</head>
<body>
  <div class="page"> <!-- PAGE 1 --> </div>
  <div class="page"> <!-- PAGE 2 --> </div>
</body>
</html>
```

### 3c. Placement

- All finalized copy from content .md
- Graphic placeholders: `<div class="graphic-placeholder">{opis}</div>`
- Tables, bullets, cards rendered as final markup
- Metric callouts w accent color na dole strony

Zapisz do `_workspace/{YYYY-MM}/wN/{name}-wireframe.html`

---

## FAZA 3.5: QUALITY GATE (obowiazkowa przed user review)

Przed pokazaniem wireframe userowi, przejdz te checkliste. Jesli ktorylkolwiek punkt FAIL → napraw PRZED pokazaniem.

### QG-1: Footer anchoring
- Kazda `.page` ma `display: flex; flex-direction: column;`
- `.page-content` (lub equivalent) ma `flex: 1;`
- `.footer-bar` (lub equivalent) ma `margin-top: auto;`
- `.page` ma `height: 297mm;` (NIE min-height/max-height)
- Footer jest na KAZDEJ stronie, nie tylko pierwszej

### QG-2: Content fill (2-step)

**Step A — visual scan:**
- Zadna strona nie ma >30% pustej przestrzeni pod contentem
- Jesli content krotki → NIE dodawaj filler (pull-quote, metric). Zamiast tego: napisz glebszy content albo polacz strony
- Jesli content za dlugi → compresuj: zmniejsz font (min 6pt floor), skroc copy
- Kazda strona = 1 core message — nie pakuj 3 tematow na strone

**Step B — audience perspective review:**
Przeczytaj KAZDA strone oczami odbiorcy (ktory zwykle NIE zna kontekstu). Dla kazdej strony zapytaj:
- Czy odbiorca rozumie DLACZEGO to jest wazne? Jesli nie → dodaj kontekst
- Czy sa terminy/skroty ktore odbiorca moze nie znac? Jesli tak → wyjasnij lub rozwin
- Czy odbiorca wie CO ma z tym zrobic? Jesli nie → dodaj konkretne przykladowe actions
- Czy sa luki informacyjne ktore CEO zna ale odbiorca nie? Jesli tak → uzupelnij

Po Step B: przepisz content z uzupelnieniami, POTEM przebuduj wireframe. Nie pokazuj userowi wireframe dopoki Step B nie jest zrobiony.

### QG-3: SVG watermark & logo
- Signet watermark (`.signet-bg`) jest na KAZDEJ stronie (nie tylko pierwszej)
- SVG path jest KOMPLETNY — viewBox="0 0 25.75 51.49" i path ma oba ksztalty
- SVG NIE jest wewnatrz `<a>` — musi byc bezposrednio w `<div>`
- Brand header SVG (jesli uzywany) ma kompletny path
- Opacity watermark: 0.03-0.07 (Siebe Light: 0.03, Siebe Dark: 0.04, Rada Starcow: text watermark)

### QG-4: WeasyPrint compatibility
- Brak `inset: 0` (longhand: top/right/bottom/left)
- Brak `box-shadow` (usuniete lub zastapione border)
- `-webkit-print-color-adjust: exact; print-color-adjust: exact;` na body
- `@page { size: A4; margin: 0; }`
- Google Fonts link jest na gorze `<head>`

### QG-5: Content-wireframe sync
- Kazdy tekst w HTML odpowiada contentowi w .md
- Zaden fragment nie zostal dodany "ad hoc" tylko w HTML

### QG-6: Polskie znaki
- Jesli brief jest po polsku: HTML MUSI miec polskie znaki (ą, ę, ś, ć, ź, ż, ó, ł, ń)
- NIE zamieniaj polskich znakow na ASCII (np. "ą" → "a", "ł" → "l") — to blad
- `<meta charset="UTF-8">` jest w `<head>`
- Sprawdz tytuly, paragrafy, tabele, karty — wszedzie gdzie jest polski tekst

---

## FAZA 4: USER REVIEW + ITERATE

Pokaż userowi:
1. "Wireframe gotowy: `{path}`"
2. "Otwórz w przeglądarce żeby zobaczyć layout"

### Typowe feedback i jak reagować:

| User mówi | Akcja |
|-----------|-------|
| "Za dużo tekstu" / "cramped" | Skróć copy w .md, powiększ fonty |
| "Słabe fonty" / "nie czyta się" | Zwiększ font-size, zmień line-height |
| "Brak konceptu" / "generic" | Wróć do Fazy 2c, zaproponuj nowy concept |
| "Zmień styl" | Przepisz CSS na inny template |
| "Dodaj stronę" / "Usuń stronę" | Edytuj .md i .html |
| "Logo/watermark nie tak" | Adjust CSS positioning |
| "OK, good" / "Akceptuję" | Przejdź do PDF export |

Iteruj: content .md → wireframe .html. Content jest źródłem prawdy — zawsze edytuj content NAJPIERW, potem wireframe.

---

## FAZA 5: PDF EXPORT

```bash
weasyprint {name}-wireframe.html {name}-wireframe.pdf && open {name}-wireframe.pdf
```

**ZAWSZE** otwieraj PDF natychmiast po wygenerowaniu (`open`). User chce widziec wynik od razu.

Znane ograniczenia WeasyPrint (ignoruj, cosmetic):
- Brak `box-shadow`
- Brak `overflow-x`
- SVG inside `<a>` tags may not render — fix: SVG bezposrednio w `<div>`
- `inset: 0` nie dziala — uzyj longhand: `top: 0; right: 0; bottom: 0; left: 0;`

PDF gitignored (generowany z HTML). HTML = source of truth.

Po eksporcie:
1. PDF otwiera sie automatycznie (komenda `open` wyzej)
2. Zapytaj: "Cos jeszcze do poprawienia, czy zamykamy?"

---

## FAZA 6: CLEANUP

1. Upewnij się że pliki są w `_workspace/{YYYY-MM}/wN/`
2. Jeśli >2 pliki → subfolder: `_workspace/{YYYY-MM}/wN/{name}/`
3. Content .md ma `status: stable` (jeśli zaakceptowany)
4. Wersje: `{name}-v2-wireframe.html` (zachowaj poprzednie wersje)

---

## Troubleshooting

| Problem | Rozwiazanie |
|---------|-------------|
| User nie wie co chce | Zaproponuj 3 koncepty z 1-zdaniowym opisem kazdego |
| Brak danych o osobie | WebSearch + sprawdz transkrypcje |
| WeasyPrint nie renderuje poprawnie | Sprawdz: @page size, font imports, SVG paths, brak `inset: 0` |
| Brief za dlugi (>8 stron) | Kompresuj: kazda strona = 1 key message, zero filler |
| Brief za krotki (1 strona) | Dodaj: metric callout, diagram placeholder, quote |
| Styl nie pasuje | Zaproponuj zmiane: Siebe Light / Siebe Dark / Rada Starcow |
| Iteracji za duzo (>5) | Zatrzymaj sie, zapytaj: "Co dokladnie nie gra?" |
| Content i wireframe rozjechane | ZAWSZE edytuj content .md NAJPIERW, potem wireframe |
| **Footer nie na dole** | `height: 297mm` + `display: flex; flex-direction: column;` + `.footer-bar { margin-top: auto; }` |
| **Pusta strona / content 60%** | Dodaj spacing, pull-quote, metric callout. Kazda strona musi byc wypelniona naturalnie |
| **Watermark brakuje pp.2+** | Signet-bg div MUSI byc na KAZDEJ `.page` — kopiuj pelny div |
| **SVG uciety / nie renderuje** | Sprawdz viewBox (25.75x51.49), pelny path (2 ksztalty). SVG w `<div>`, NIE w `<a>`. Uzyj template |

---

## References

→ `references/template-siebe-light.html` — HTML skeleton Siebe Light (default, copy-paste ready)
→ `references/template-siebe-dark.html` — HTML skeleton Siebe Dark (copy-paste ready)
→ `references/template-rada-starcow.html` — HTML skeleton Rada Starcow (copy-paste ready)
→ `references/css-templates.md` — 3 design systems z pelnymi CSS variables, fontami, kluczowymi klasami
→ `references/examples.md` — 8 real brief examples z sesji + 11 common pitfalls
