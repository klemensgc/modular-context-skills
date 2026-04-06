---
name: skill-creator
description: |
  Interactive guide for creating high-quality Claude Code skills (SKILL.md files).
  Use when: building a new skill, converting existing knowledge into a skill, improving
  an existing skill, or learning how to structure skills properly.
  Trigger phrases: "create a skill", "new skill", "make a skill", "build skill",
  "convert to skill", "SKILL.md", "skill template"
---

# Skill Creator

Interaktywny przewodnik po tworzeniu skilli Claude Code. Przeprowadza krok po kroku od pomysłu do gotowego skilla.

---

## Workflow

### Krok 1: Zidentyfikuj use case

Zapytaj usera:

1. **Co skill ma robić?** — Jaki problem rozwiązuje? Jaki output produkuje?
2. **Kiedy się uruchamia?** — Jakie pytanie/polecenie usera powinno go triggerować?
3. **Jaka kategoria?**

| Kategoria | Opis | Przykłady |
|-----------|------|-----------|
| **Document & Asset Creation** | Generowanie plików wg szablonu | broszury, animacje, emaile |
| **Workflow Automation** | Automatyzacja procesów | deploy, migracje, review |
| **MCP Enhancement** | Rozszerzenie external tools | API queries, webhook setup |

4. **2-3 konkretne scenariusze** w których user użyłby tego skilla

### Krok 2: Napisz description

Description w frontmatter to **najważniejszy element** — decyduje o automatycznym triggerowaniu.

**Formuła:**

```yaml
description: |
  [CO robi — 1 zdanie, present tense].
  Use when: [KIEDY użyć — 2-4 scenariusze].
  Trigger phrases: [5-10 naturalnych fraz usera]
```

**Zasady:**
- Max 1024 znaków
- MUSI zawierać WHAT + WHEN
- Trigger phrases = frazy usera, nie żargon techniczny
- NIE używaj "claude" ani "anthropic" w nazwie
- Test: "Gdybym powiedział tę frazę, chciałbym żeby TEN skill się uruchomił?"

### Krok 3: Zaprojektuj strukturę

```
.claude/skills/{kebab-case-nazwa}/
├── SKILL.md              # Instrukcje (wymagany)
├── references/           # Szczegółowa dokumentacja (opcjonalny)
│   └── *.md
└── scripts/              # Skrypty pomocnicze (opcjonalny)
    └── *.py / *.sh
```

**Nazewnictwo:**
- Folder: `kebab-case`
- `SKILL.md`: dokładnie ta nazwa, case-sensitive
- Bez "claude"/"anthropic" w nazwie folderu

### Krok 4: Napisz instrukcje

**Progressive disclosure — 3 poziomy:**

**Poziom 1 — Quick Start (góra pliku, 5-7 linijek)**
Najczęstszy use case, happy path. User zaczyna działać od razu.

**Poziom 2 — Szczegółowe sekcje (środek)**
Krok po kroku dla każdego scenariusza. Parametry, opcje, przykłady kodu.

**Poziom 3 — Reference (dół lub `references/`)**
Pełna dokumentacja, edge cases, troubleshooting.

**Styl pisania:**
- Imperatywny ton: "Stwórz plik", nie "Możesz stworzyć"
- Konkretne przykłady > abstrakcyjne opisy
- Troubleshooting table na końcu
- Relatywne linki do references: `→ references/patterns.md`
- Bez XML tags w treści
- Bez emoji

**Interaktywne skille** (workflow/wizard):
- Sekwencja kroków z pytaniami do usera zamiast bloku tekstu
- Każdy krok: pytanie → analiza → działanie → następny krok
- Domyślne wartości żeby user mógł szybko przejść

### Krok 5: Dodaj error handling

Sekcja troubleshooting z najczęstszymi problemami:

```markdown
## Troubleshooting

| Problem | Rozwiązanie |
|---------|-------------|
| Skill nie triggeruje | Sprawdź description — ma trigger phrases? |
| Triggeruje na złe zapytania | Zawęź description, precyzuj "Use when" |
| Output niskiej jakości | Więcej przykładów, concrete steps |
```

### Krok 6: Przetestuj

**Pozytywne** (powinien się uruchomić): powiedz każdą trigger phrase
**Negatywne** (NIE powinien): zapytania z sąsiedniej domeny
**Funkcjonalne**: happy path od początku do końca

### Krok 7: Iteruj

Po pierwszym użyciu:
1. **Description tuning** — prawidłowe triggerowanie?
2. **Instruction gaps** — brakowało kroku?
3. **Reference expansion** — brakowało info?
4. **Scope creep** — za dużo? Rozdziel na 2 skille

---

## Referencje

- Specyfikacja YAML → `references/yaml-reference.md`
- Wzorce projektowe → `references/patterns.md`
- Checklist walidacyjny → `references/checklist.md`
