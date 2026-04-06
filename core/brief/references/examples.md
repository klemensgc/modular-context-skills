# Brief — Real Examples

Przyklady z sesji repo. Patterns, lessons learned, common pitfalls.

---

## Example 1: Modular Context Guide (Wilson Wang)

**Sesja:** 2026-02-14, 3 iteracje wireframe (v1→v2→v3)
**Styl:** Siebe Light
**Output:** 2 strony A4, EN, one-pager dla investora

**Kluczowe decyzje:**
- v1 → za duzo tekstu, cramped layout → skrocono copy, zwiekszono spacing
- v2 → user chcial code block z frontmatter example → dodano `.fm-code` dark block
- v3 → final: hero + 3-col features + pipeline diagram + code example + advantages

**Pliki:**
- Content: `_workspace/2026-02/w2/modular-context/modular-context-guide-v5-wilson-wang.md`
- Wireframe: `_workspace/2026-02/w3/modular-context-guide-wilson-wang/modular-context-guide-v3-wireframe.html`

**Lesson:** Investor one-pagery = max 2 strony. Kazda strona = 1 core message. Zero filler.

---

## Example 2: Rada Starcow v8 (Playscript Pre-Miami)

**Sesja:** 2026-02-22, multi-page internal strategic brief
**Styl:** Rada Starcow
**Output:** 8 stron, PL, strategic analysis dla board

**Kluczowe decyzje:**
- Cover z centered SVG signet + ornament (• • •)
- Debate format: `.debate-entry` z `.debate-speaker` + `.debate-text`
- Consensus items: `.consensus-box` z numbered items
- Play cards: `.play-card` z `.tag-*` colored tags
- Verdict: `.verdict-box` dark inverted section

**Pliki:**
- Content: `_workspace/2026-02/w4/rada-starcow-v8.md`
- Wireframe: `_workspace/2026-02/w4/rada-starcow-v8-wireframe.html`

**Lesson:** Dla internal strategy → Rada Starcow styl. Cover, ornaments, serif headlines = premium feel. 8 stron = max dla tego formatu.

---

## Example 3: PR Brief Justyna

**Sesja:** 2026-02-24, press brief for PR person
**Styl:** Siebe Light (Brief White variant)
**Output:** multi-page, PL, deliverables + rules + context

**Kluczowe decyzje:**
- Wiekszy hero (48pt) vs standard (36pt) — brief jest bardziej "statementowy"
- Tabele z `.del-table` — structured deliverables z datami i statusami
- `.rules-grid` 3-kolumnowy — communication rules
- Signet watermark jako base64 CSS background (lzejsze niz inline SVG)

**Pliki:**
- Content: `_workspace/2026-02/w4/pr-brief-justyna/pr-brief-justyna.md`
- Wireframe: `_workspace/2026-02/w4/pr-brief-justyna/pr-brief-justyna-wireframe.html`

**Lesson:** External person briefs → Siebe Light. Duzy hero, clean tables, corporate but with ROS branding (accent orange).

---

## Example 4: Arcadian Brief wewnetrzny

**Sesja:** 2026-02-01
**Styl:** Rada Starcow (Arcadian sub-wariant)
**Output:** multi-page, PL, internal event brief

**Kluczowe decyzje:**
- Timeline component: `.timeline` z left-border + dots
- Framework flowchart: `.fw` z `.fw-node` cards connected by `.fw-arr` arrows
- Fact callouts: `.fact-item` z accent left-border
- Spec tables: `.spec-table` z uppercase headers

**Pliki:**
- Wireframe: `_workspace/2026-02/w1/arcadian-brief-call-wireframe.html`

**Lesson:** Event briefs = timeline + specs + fact callouts. Heritage styl works for prestige events.

---

## Example 5: Compact Task Brief (Czarek — Asset Library + Agent Optimization)

**Sesja:** 2026-02-25, compact task assignment brief
**Styl:** Rada Starcow (Compact Task sub-wariant)
**Output:** 2 strony A4 (1 task/strona), PL, internal task brief

**Kluczowe decyzje:**
- Styl Rada Starcow ale **skondensowany** — h1=26pt, body=8pt, desc=7pt
- Strona 1: Asset Library — karty 2-col (co zebrac), structure-tree (folder layout), consensus-boxes (jak opisywac), verdict-box (deliverable)
- Strona 2: Agent Optimization — consensus-boxes (4 kroki), structure-tree (vault na Mac mini), verdict-box + 2-col asset-cards (zaleznosc + referencja)
- Tagi kolorowe: `tag-collect` (blue), `tag-organize` (green), `tag-document` (yellow), `tag-required` (red)
- Pierwsza iteracja overflow — uciete 3 consensus-box + verdict. Fix: zmniejszone wszystkie marginesy i font sizes o ~15%

**Pliki:**
- Wireframe: `_workspace/2026-02/w4/task-czarek-assets-library.html`
- Template: `_claude/2-templates/compact-task-brief.md`

**Lesson:** Compact task briefs = 1 strona/task. Max ~6 sekcji. Kluczowe: pilnuj marginesow — Rada Starcow ma duze paddingi ktore trzeba zredukowac o ~15% zeby zmiescic content na jednej stronie. Zawsze testuj overflow przed PDF.

---

## Example 6: Siebe Dark (Marcin Badach Brief)

**Sesja:** 2026-02-19, confidential recruitment brief
**Styl:** Siebe Dark
**Output:** 5 stron A4, PL, poufny brief z danymi finansowymi i strategia

**Kluczowe decyzje:**
- Ciemne tlo (#0C0A09) — profesjonalny, poufny feel
- SVG signet watermark na kazdej stronie (fill: #F5F2EF, opacity 0.04)
- Brand header z signet + "receptionOS" (opacity 0.4)
- Metric cards z orange accent na ciemnym tle — czytelne i wyraziste
- Python generator (`generate_brief.py`) do rozwiazania problemu output token limit — SVG wyciagane z pliku zrodlowego zamiast inline

**Pliki:**
- Content: `_workspace/2026-02/w3/marcin-badach-brief/marcin-badach-brief.md`
- Wireframe: generowany przez Python script

**Lesson:** Siebe Dark doskonaly dla poufnych briefow (investor, recruitment). Problem: dlugie SVG paths zjadaja output tokeny — dla >4 stron rozwaz Python generator lub template z plikiem SVG. Watermark MUSI byc na kazdej stronie — latwo zapomniec.

---

## Example 7: OmniCreatio Brief

**Sesja:** 2026-03-19, exploration brief for external partner
**Styl:** Siebe Dark (po odrzuceniu v1 w Siebe Light)

**Kluczowe decyzje:**
- **v1 (ODRZUCONY):** Siebe Light — user feedback: "to pizda jest, za konkretne rozwiazanie". Za duzo specifics, za malo exploration.
- **v2 (ZAAKCEPTOWANY):** Siebe Dark z exploratory tone. Placeholder circles zastapione JetBrains Mono numbers (lepiej na ciemnym tle).
- **Footer fix:** Zmieniono `.page` z `min-height/max-height` na `height: 297mm` — naprawilo problem z footer nie przyczepiony do spodu.

**Pliki:**
- Wireframe: `_workspace/2026-03/w3/omnicreatio-brief-wireframe.html`

**Lesson:** Nie kazdemu brief pasuje Siebe Light. Gdy tone ma byc exploratory/filmowy → Siebe Dark. Footer fix: ZAWSZE `height: 297mm` (nie min/max-height) + flexbox + `margin-top: auto`.

---

## Example 8: Nowak Report v1

**Sesja:** 2026-03-06, raport analityczny z 2768 rozmow
**Styl:** Siebe Light
**Output:** 6 stron A4, PL, data-heavy report z metric cards

**Kluczowe decyzje:**
- 6 stron — duzo metric cards, tabel, wykresow tekstowych
- **Bug: brakujace watermarki pp.4-6** — signet-bg byl tylko na stronach 1-3. Naprawiono: dodano signet-bg do KAZDEJ .page div.
- **Bug: uciety SVG path** — brand header SVG mial niekompletny path (brakowalo wewnetrznych ksztaltow signetu). Naprawiono: uzyto pelnego SVG z viewBox 25.75x51.49.
- **Footer standardization** — zmieniono footer text na "v1 Proof of Concept" na wszystkich stronach.

**Pliki:**
- Wireframe: `_workspace/2026-03/w1/nowak-raport-v1-wireframe.html`

**Lesson:** Dla reportow >3 stron: (1) signet-bg MUSI byc na KAZDEJ stronie — kopiuj pelny div, (2) SVG path MUSI byc kompletny — sprawdzaj viewBox i oba ksztalty (zewnetrzny + wewnetrzny), (3) Footer text musi byc spojny across all pages.

---

## Common Pitfalls (z sesji)

| Problem | Co sie stalo | Fix |
|---------|-------------|-----|
| Cramped layout | Za duzo tekstu na stronie | Max ~80-100 slow body/strone |
| Generic concept | User: "no concept, just facts" | Zaproponuj 2-3 angle'e: heritage, tech, human |
| WeasyPrint font issue | Google Fonts nie zaladowaly sie | Zawsze testuj w przegladarce PRZED PDF export |
| Signet nie renderuje | SVG wewnatrz `<a>` | SVG bezposrednio w div, nie w linku |
| Content/wireframe desync | Edytowano HTML bezposrednio | ZAWSZE: content .md → wireframe .html (content = source of truth) |
| Za duzo iteracji (>5) | User zmienial concept w kolko | Po 3 iteracjach zapytaj: "Co dokladnie nie gra?" |
| **Footer nie na dole** | min-height/max-height nie dziala | `height: 297mm` + flexbox + `margin-top: auto` |
| **Pusta strona (60%)** | Content nie wypelnia A4 | Dodaj: metric callout, pull-quote, spacing, diagram |
| **Watermark brakuje pp.2+** | Signet-bg tylko na str.1 | Kopiuj signet-bg div na KAZDA .page |
| **SVG uciety** | Niekompletny path w brand header | Sprawdz viewBox i oba ksztalty. Uzyj template. |
| **Zly styl** | Siebe Light za korporacyjny | Zaproponuj zmiane: "Moze Siebe Dark lub Rada Starcow?" |
