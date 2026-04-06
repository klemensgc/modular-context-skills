# Wzorce projektowe skilli

## Wzorzec 1: Document Generator

**Kategoria:** Document & Asset Creation

**Struktura:**
```
.claude/skills/{nazwa}/
├── SKILL.md          # Workflow: zbierz info → generuj
├── templates/        # Szablony wyjściowe
└── references/       # Standardy formatowania
```

**Cecha:** SKILL.md pyta o parametry, potem generuje dokument wg szablonu. Output to plik.

**Przykłady:** generatory emaili, broszur, raportów, spec sheets

---

## Wzorzec 2: Interactive Wizard

**Kategoria:** Workflow Automation

**Struktura:**
```
.claude/skills/{nazwa}/
├── SKILL.md          # Sekwencja kroków z pytaniami
└── references/       # Szczegóły techniczne
```

**Cecha:** Prowadzi usera krok po kroku. Każdy krok to pytanie → analiza → działanie. Defoltowe wartości żeby szybko przejść.

**Przykłady:** skill-creator, setup wizards, migration guides

---

## Wzorzec 3: Analysis + Action

**Kategoria:** Workflow Automation

**Struktura:**
```
.claude/skills/{nazwa}/
├── SKILL.md          # Analiza → diagnoza → akcja
├── scripts/          # Skrypty diagnostyczne
└── references/       # Known issues, patterns
```

**Cecha:** Najpierw analizuje stan (czyta pliki, uruchamia diagnostykę), potem proponuje i wykonuje akcję.

**Przykłady:** debuggery, code reviewers, performance analyzers

---

## Wzorzec 4: Toolchain Wrapper

**Kategoria:** Workflow Automation / MCP Enhancement

**Struktura:**
```
.claude/skills/{nazwa}/
├── SKILL.md          # Orchestracja narzędzi
├── scripts/          # Skrypty pipeline'u
└── references/       # Dokumentacja narzędzi
```

**Cecha:** Orkiestruje sekwencję zewnętrznych narzędzi (CLI, API, skrypty). SKILL.md opisuje pipeline.

**Przykłady:** export pipelines (GIF, PDF), deployment, CI/CD

---

## Wzorzec 5: Knowledge Base

**Kategoria:** Dowolna

**Struktura:**
```
.claude/skills/{nazwa}/
├── SKILL.md          # Quick reference + navigation
└── references/       # Głęboka wiedza per topic
    ├── topic-a.md
    ├── topic-b.md
    └── topic-c.md
```

**Cecha:** SKILL.md to hub z quick answers. Szczegóły w `references/`. Progressive disclosure.

**Przykłady:** API references, coding standards, architecture guides

---

## Który wzorzec wybrać?

| User chce... | Wzorzec |
|--------------|---------|
| Wygenerować plik | Document Generator |
| Być prowadzonym krok po kroku | Interactive Wizard |
| Zdiagnozować problem | Analysis + Action |
| Uruchomić pipeline narzędzi | Toolchain Wrapper |
| Szybko znaleźć informację | Knowledge Base |
