---
name: copy
description: |
  Creates brand-aligned copy and text content — ad variants, email templates, pitch blurbs,
  structured AI prompts, recruitment posts. Text-only output (no design/PDF).
  Use when: writing social media copy, creating email templates, drafting pitch text,
  building AI prompt instructions, producing any text deliverable that doesn't need PDF rendering.
  Trigger phrases: "copy", "write copy", "ad copy", "email template", "pitch",
  "napisz copy", "reklama", "ogłoszenie", "email prompt", "draft text",
  "blurb", "pitch text", "treść", "kopia", "szablon emaila", "recruitment post"
---

# Copy

Tworzy brand-aligned copy i treści tekstowe: warianty reklam, szablony emaili, pitche, prompty AI, ogłoszenia rekrutacyjne. Output = finalizowany .md (bez designu/PDF).

Repo jest po polsku. Odpowiadaj po polsku, chyba że copy jest po angielsku.

Jeśli user potrzebuje PDF/designed deliverable → przekieruj do `/brief`.

---

## Quick Start

1. Ustal co i dla kogo (typ copy, audience, tone)
2. Research kontekst (brand, existing copy, recipient)
3. Draft v1
4. Iterate na feedback
5. Finalize i zapisz

---

## FAZA 0: INTAKE

Zapytaj usera przez AskUserQuestion (1 pytanie):

```
"Jaki typ copy potrzebujesz?"
```

Opcje:
- **Ad copy** — warianty reklam (IG/FB/LinkedIn)
- **Email template** — szablon email/follow-up
- **Pitch/blurb** — krótki tekst prezentacyjny
- **AI prompt** — structured prompt for AI system (voicebot, email-bot)
- Other

### Domyślne wartości (nie pytaj, ustal z kontekstu):

| Decyzja | Jak ustalić |
|---------|-------------|
| Language | PL (default), EN jeśli audience = international |
| Tone | Z brand docs: confident, direct, expertise with human face |
| Length | Ad: 50-150 słów/wariant; Email: 100-300 słów; Pitch: 2-5 zdań; Prompt: no limit |
| Variants | Ad: 3-4 warianty; Email: 2-3 templates; Pitch: 1; Prompt: 1 |

---

## FAZA 1: RESEARCH

### 1a. Brand context

Przeczytaj (co relevantne do typu):
- `_culture/philosophy.md` — 10 zasad, ton komunikacji
- `1_receptionOS/3-market/positioning.md` — jak mówimy o produkcie
- `1_receptionOS/4-go-to-market/modular-offer.md` — pricing, pakiety
- `_culture/team/team-roster.md` — osoby, role (jeśli copy o zespole)

### 1b. Existing copy patterns

Grep po istniejących materiałach:
```
Grep: "copy|reklama|ogłoszenie|email|pitch" w _workspace/ i _transcripts/
```

Sprawdź: ton, formulacje, co działało wcześniej.

### 1c. Recipient/audience research

Jeśli copy jest personalizowane:
- Baseball card w `_culture/team/`
- Transkrypcje ze spotkań z tą osobą
- WebSearch jeśli brak danych w repo

### 1d. Hormozi frameworks (latent)

Nie nazywaj frameworku w copy. Po prostu stosuj:

| Framework | Jak zastosować |
|-----------|---------------|
| **Value Equation** | Dream Outcome (co zyskujesz), Likelihood (metryki), Time Delay (jak szybko), Effort (jak łatwo) |
| **EVP** (employer) | Top 1% pracodawca, Academy, międzynarodowy scale, career growth |
| **Benefit language** | Feature → patient/user outcome (nie "mamy CBCT" ale "oszczędzasz czas na skierowania") |

---

## FAZA 2: DRAFT

### Ad copy (3-4 warianty)

```markdown
---
title: {Kampania} — Copy Variants
type: log
data: {YYYY-MM-DD}
agent: /copy
language: pl|en
---

**Target:** {target} — odbiorca opisany w treści, nie w polu frontmattera.

## Wariant 1: {nazwa} (Short/Long/Heritage/Role-specific)

**Hook:** {1 zdanie otwierające}

{Treść — 50-150 słów}

**CTA:** {Call to action}

---

## Wariant 2: {nazwa}
...
```

### Email template

```markdown
---
title: {Kontekst} — Email Template
type: log
data: {YYYY-MM-DD}
agent: /copy
---

## Kontekst
{Kiedy wysyłać, do kogo, po czym}

## Template

**Subject:** {temat}

{Treść z placeholderami: {imię}, {firma}, {context}}

**Podpis:** {kto wysyła}

---

## Benefit Language Bank
| Feature | Benefit (patient/user outcome) |
|---------|-------------------------------|
| ... | ... |
```

### Pitch/blurb

Krótki tekst (2-5 zdań). Zapisz bezpośrednio w odpowiednim pliku (np. baseball card osoby) LUB jako osobny .md jeśli potrzebny.

### AI prompt (structured)

```markdown
---
title: {System} — {Typ} Prompt
type: modul
updated: {YYYY-MM-DD}
status: draft
---

## Stan
{Gdzie ten prompt jest wdrożony i w jakiej wersji — 2-3 zdania. Sekcja wymagana przez
`_schemas/modul.yaml` (kontrakt living-state).}

## Role
{Kim jest AI — 1-2 zdania}

## Quick Reference
{Kluczowe dane: firma, usługi, cennik, kontakt}

## Templates
### Template 1: {scenariusz}
{Struktura + przykład}

## Benefit Language Bank
{Feature → outcome pairs}

## Competency Boundaries
{Co AI może, czego NIE może}
```

Prompt systemowy żyje w folderze projektu (`1_receptionOS/5-operations/` itp.) i ktoś go potem
edytuje → to `type: modul` (`title` + `updated` + `status` wymagane przez `_schemas/modul.yaml`).
`updated:` wpisujesz **tylko przy tworzeniu pliku** (inaczej PostToolUse daje FAIL na brak pola),
potem nie ruszasz — dalej stampuje pre-commit. Jeśli prompt zostaje w `_workspace/` jako
jednorazowy draft, użyj frontmattera `type: log` jak w szablonach wyżej.

---

## FAZA 3: ITERATE

Pokaż v1 userowi. Typowe feedback:

| User mówi | Akcja |
|-----------|-------|
| "Za formalnie" | Rozluźnij ton, dodaj personality |
| "Za casualowo" | Podkręć profesjonalizm, dodaj metryki |
| "Za długie" | Skróć, usuń filler, zostaw hook + CTA |
| "Brak konkretu" | Dodaj metryki, case study, social proof |
| "Nie trafiony ton" | Przeczytaj `philosophy.md` jeszcze raz, dostosuj |
| "Dodaj wariant" | Nowy wariant z innym angle |
| "OK, dobrze" | Przejdź do finalizacji |

Iteruj max 3 razy. Jeśli po 3 iteracjach nadal nie OK → zapytaj: "Co dokładnie nie gra? Daj mi przykład tekstu który Ci się podoba."

---

## FAZA 4: FINALIZE

1. Frontmatter wg typu pliku (`_schemas/`):
   - deliverable w `_workspace/` → `type: log` + `data:` + `agent:` (bez `status:` — `log.yaml` nie ma tego pola)
   - prompt/moduł w drzewie projektu → `type: modul`, `status: draft` → `status: stable` po akceptacji
2. `updated:` stampuje pre-commit — nie wpisuj ręcznie (jedyny wyjątek: wpisanie daty przy **tworzeniu** nowego `modul`)
3. Plik lokalizacja:
   - Workspace deliverable: `_workspace/{YYYY-MM}/wN/{name}.md`
   - Prompt for system: odpowiedni folder projektu (np. `1_receptionOS/5-operations/`)
   - Blurb/pitch: embeduj w istniejącym pliku (baseball card, module)
4. Sprawdź lint przed pokazaniem: `python3 _claude/9-automation/schema_lint.py <plik>` → 0 FAIL
5. Jeśli user chce PDF → powiedz: "Użyj `/brief` żeby zamienić content w PDF"

---

## Troubleshooting

| Problem | Rozwiązanie |
|---------|-------------|
| Nie wiem jaki ton | Przeczytaj `philosophy.md` + 2-3 istniejące materiały marketingowe |
| Brak danych o produkcie | Przeczytaj `features.md` + `modular-offer.md` + `positioning.md` |
| Copy ma być po angielsku ale repo po polsku | Researchy po polsku, pisz copy po angielsku, odpowiadaj userowi po polsku |
| User chce PDF nie copy | Przekieruj: "To zadanie dla `/brief` — chcesz żebym uruchomił?" |
| Za dużo wariantów (>4) | Zapytaj usera: "Które 2 warianty najlepsze? Dropnę resztę." |
| Benefit language trudna | Pattern: {feature} → "dzięki temu {osoba} {outcome}" |

---

## References

→ `references/examples.md` — Real copy examples z sesji (reklamy rekrutacyjne 4 warianty, email oferty Violetta, setup guide dla publikującego) + copy formulas (ad structure, heritage variant, benefit language pattern)
