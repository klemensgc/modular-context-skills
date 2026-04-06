# Brief CSS Templates — Reference

3 systemy designu. Uproszczona taksonomia — copy-paste ready.

**Template HTML skeletons:** `references/template-{style}.html` — gotowe do uzycia.

---

## 1. Siebe Light (default)

**Kiedy:** Default dla wszystkiego. Zewnetrzne osoby, clean professional, investor briefs, onboarding guides.
**Fonty:** Inter (300-800) + JetBrains Mono (400, 500)
**Template:** `references/template-siebe-light.html`

```css
:root {
  --bg: #FFFFFF;
  --bg-card: rgba(0,0,0,0.025);
  --text: #050403;
  --text-secondary: #3d3a38;
  --text-muted: #8a8785;
  --accent: #EB670F;
  --accent-light: #E9955C;
  --accent-dim: rgba(235,103,15,0.10);
  --surface: #F7F6F6;
  --code-bg: #F7F6F6;
  --border: #e8e6e5;
  --border-accent: rgba(235,103,15,0.25);
}
```

**Fonty:**
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

**Kluczowe klasy:**
- `.page` — `width: 210mm; height: 297mm; padding: 20mm 24mm 18mm 24mm; display: flex; flex-direction: column;`
- `.page-content` — `flex: 1;`
- `.brand-header` — opacity 0.55, SVG signet (12pt) + "receptionOS", gap 7pt
- `.signet-bg` — `left: 12mm; top: 38mm; opacity: 0.03;` (watermark, fill: #050403)
- `.section-label` — `6.5pt, uppercase, letter-spacing: 2.5px, color: var(--accent)`
- `.hero h1` — `36pt, weight 800, letter-spacing: -1.2px`
- `.three-col` — `grid-template-columns: 1fr 1fr 1fr; gap: 16pt`
- `.card` — `background: var(--surface); border-radius: 4px; padding: 9pt 11pt`
- `.arch-bar` — 4 cells, warm gradient backgrounds (`#fef3eb` → `#f3f8f5`)
- `.fm-code` — dark code block: `bg: #1a1714; font: JetBrains Mono 6.5pt`
- `.footer-bar` — `border-top: 1px solid var(--border); margin-top: auto;`

**Font floor:** min 6pt

---

## 2. Siebe Dark

**Kiedy:** Tech people, filmowy vibe, pitch dla inwestorow, ciemne srodowisko.
**Fonty:** Inter (300-800) + JetBrains Mono (400, 500)
**Template:** `references/template-siebe-dark.html`

```css
:root {
  --bg: #0C0A09;
  --bg-card: rgba(255,255,255,0.035);
  --text: #F5F2EF;
  --text-secondary: #A8A29E;
  --text-muted: #6B6560;
  --accent: #EB670F;
  --accent-dim: rgba(235,103,15,0.15);
  --accent-glow: rgba(235,103,15,0.06);
  --border: rgba(255,255,255,0.07);
  --border-accent: rgba(235,103,15,0.25);
}
```

**Roznice vs Siebe Light:**
- Ciemne tlo (#0C0A09) zamiast bialego
- Signet watermark fill: `#F5F2EF` (jasny na ciemnym tle)
- Brand header opacity: 0.4 (zamiast 0.55)
- `.col-item` z `border: 1px solid var(--border)` (widoczne krawedzie na ciemnym)
- `.fm-code` bg: `rgba(255,255,255,0.03)` (subtler niz light)
- Signet position: `right: 14mm` (prawa strona, nie lewa)
- Print: `body { background: var(--bg); }` (zachowaj ciemne tlo w druku)

**Kluczowe klasy:** Identyczne nazwy jak Siebe Light, inne kolory.

**Font floor:** min 6pt

---

## 3. Rada Starcow

**Kiedy:** Internal strategy briefs, heritage materials, eventy, task briefs. Premium feel.
**Fonty:** Cormorant Garamond (serif, 400-700) + Inter (sans, 300-700)
**Template:** `references/template-rada-starcow.html`

```css
:root {
  --black: #0a0a0a;
  --near-black: #1a1a1a;
  --dark-gray: #2a2a2a;
  --medium-gray: #666;
  --light-gray: #999;
  --off-white: #f5f3ef;
  --cream: #ebe8e1;
  --warm-white: #faf9f6;
  --accent: #8b7355;
  --accent-light: #b5a48a;
  --accent-dark: #6b5a42;
  --rule: #d4cfc6;
  --green: #4a7c59;
  --green-bg: #e8f0ea;
  --red: #8c4040;
  --red-bg: #f0e8e8;
  --yellow-bg: #f0ede4;
  --blue: #4a6b8c;
  --blue-bg: #e8eef4;
}
```

**Fonty:**
```html
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,500&family=Inter:wght@300;400;500;600;700&display=swap');
```

**Kluczowe klasy:**
- `.page` — `width: 210mm; height: 297mm; background: var(--warm-white); padding: 18mm 22mm; display: flex; flex-direction: column;`
- `.page-content` — `flex: 1;`
- `h1` — Cormorant Garamond, 36pt, weight 600, letter-spacing -0.02em
- `h2` — Cormorant Garamond, 22pt, weight 600
- `h3` — Inter, 9pt, uppercase, letter-spacing 0.12em, color: var(--accent)
- `.tagline` — Cormorant Garamond italic, 13pt, medium-gray
- `.ornament` — `• • •` centered, accent-light, letter-spacing 0.5em
- `.pull-quote` — Cormorant italic 13pt, accent-dark
- `.metric-card .number` — Cormorant 22pt bold accent
- `.consensus-box` — cream bg, flex, number (Cormorant 26pt) + body
- `.verdict-box` — near-black bg, off-white text (dark inverted card)
- `.play-card` — border + border-radius 3px, z `.play-type` tag (capture/amplify/build/discover)
- `.header-bar` — flex, space-between, border-bottom rule
- `.footer-bar` — flex, space-between, border-top rule, **margin-top: auto**
- `.watermark` — text "R", Cormorant 120pt, opacity 0.03, absolute bottom-right

**Body background:** `#c8c4bc` (browser), white (print)

### Sub-wariant: Compact Task Brief

Dla 1-page task assignments. Identyczna paleta, **zmniejszone rozmiary** (~15% reduction):

| Element | Rada Starcow | Compact Task |
|---------|-------------|-------------|
| h1 | 36pt | 26pt |
| h2 | 22pt | 16pt |
| h3 | 9pt | 7.5pt |
| body | 9pt | 8pt |
| .tagline | 13pt | 11pt |
| .consensus-number | 26pt | 20pt |
| .consensus-desc | 8pt | 7pt |
| .asset-card padding | 10px 12px | 6px 9px |
| .section-divider margin | 4mm | 2.5mm |

Dodatkowe klasy compact:
- `.tag-collect` (blue), `.tag-organize` (green), `.tag-document` (yellow), `.tag-required` (red) — 6pt inline tags
- `.checklist li::before` — checkbox `\2610` in accent
- `.structure-tree` — JetBrains Mono 6.5pt, folder tree

Max ~6 sekcji per A4. Template: `_claude/2-templates/compact-task-brief.md`

### Sub-wariant: Arcadian Event

Dla event briefs (Ball, Winter Lounge). Identyczna paleta + dodatkowe klasy:
- `.timeline` — left-border 2px z `.tl-item::before` dot
- `.fact-item` — `border-left: 3px solid accent; bg: cream`
- `.spec-table` — th uppercase 7pt, td 8pt, border-bottom rule

---

## Wspolne zasady (wszystkie systemy)

```css
@page { size: A4; margin: 0; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }

.page {
  display: flex; flex-direction: column;  /* QG-1 */
  height: 297mm;                          /* QG-1 */
}
.page-content { flex: 1; }               /* QG-1 */
.footer-bar { margin-top: auto; }        /* QG-1 */

@media print {
  body { background: white; }  /* lub var(--bg) dla Siebe Dark */
  .page { margin: 0; }
}
```

**Font floor:** Minimum 6pt w kazdym systemie.

**Signet SVG:** viewBox `0 0 25.75 51.49`. Pelny path w template HTML files. Nie kopiuj fragmentow — uzyj template.
