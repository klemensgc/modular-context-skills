# SKILL.md YAML Frontmatter — Pełna specyfikacja

## Wymagane pola

```yaml
---
name: kebab-case-nazwa          # musi pasować do nazwy folderu
description: |                  # max 1024 znaków
  [CO robi — 1 zdanie].
  Use when: [KIEDY].
  Trigger phrases: [frazy]
---
```

## Pole `name`

- Format: `kebab-case` (np. `svg-loader-animation`)
- Musi odpowiadać nazwie folderu w `.claude/skills/`
- NIE używaj "claude" ani "anthropic"
- Krótki, opisowy, unikalny

## Pole `description`

To jest **najważniejsze pole** — służy do automatycznego dopasowania skilla do zapytania usera.

### Struktura

```
[WHAT] — co skill robi, 1 zdanie, present tense
[WHEN] — kiedy użyć, 2-4 scenariusze
[TRIGGERS] — 5-10 naturalnych fraz usera
```

### Zasady

- Max 1024 znaków
- MUSI zawierać zarówno WHAT jak i WHEN
- Trigger phrases = frazy które user naturalnie powie, nie żargon techniczny
- Unikaj zbyt ogólnych opisów ("helps with coding") — prowadzą do false positives
- Unikaj zbyt wąskich opisów ("converts CSV to JSON using pandas") — pomijają warianty

### Dobre przykłady

```yaml
description: |
  Creates animated SVG loaders using strokeDasharray technique for any logo or shape.
  Use when: user wants a loading animation for their logo, animated stroke effect on SVG,
  trail/comet/draw-on animation, or needs to export loader as GIF or Lottie.
  Trigger phrases: "loader animation", "animated logo", "loading spinner"
```

```yaml
description: |
  Interactive guide for creating high-quality Claude Code skills (SKILL.md files).
  Use when: building a new skill, converting existing knowledge into a skill,
  improving an existing skill.
  Trigger phrases: "create a skill", "new skill", "make a skill", "SKILL.md"
```

### Złe przykłady

```yaml
description: Makes animations.
# Za ogólne, brak WHEN, brak trigger phrases

description: |
  Uses Python 3.12 with the lottie-py library version 0.7.2 to parse SVG path data
  and generate Lottie JSON with trim paths using hold keyframes.
# Za techniczne, user nigdy tak nie powie
```

## Opcjonalne pola

Frontmatter powinien zawierać TYLKO `name` i `description`. Nie dodawaj pól których skill system nie rozpoznaje.
