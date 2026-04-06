---
name: graduate
description: |
  Extracts ideas buried in transcripts and promotes them into standalone permanent modules.
  Discovers topics that appear across multiple transcripts but have no dedicated module yet.
  Use when: feeling like transcripts contain unextracted knowledge, wanting to grow the vault
  organically, looking for ideas that the processing pipeline missed.
  Trigger phrases: "graduate", "promote ideas", "wyciągnij z transkrypcji", "new modules",
  "awansuj notatki", "promote to module", "graduate ideas", "ideas to modules"
---

# Graduate

Wyciąga idee zagrzebane w transkrypcjach i promuje je do samodzielnych modułów (permanent notes).

Repo jest po polsku. Odpowiadaj po polsku.

**Kluczowa różnica:** `/process-transcripts` przetwarza backlog systematycznie i aktualizuje ISTNIEJĄCE moduły. `/graduate` ODKRYWA idee i tworzy NOWE moduły z tego co pipeline pominął.

---

## Quick Start

1. Skanuj transkrypcje — wyciągnij tematy cross-cutting
2. Cross-reference z istniejącymi modułami — co NIE ma dedykowanego pliku
3. Zidentyfikuj kandydatów do graduacji (3+ wzmianek, brak modułu)
4. Pokaż userowi → po akceptacji stwórz moduły
5. Zaktualizuj indeksy i dodaj wiki-links

---

## Workflow

### Krok 1: Skanuj transkrypcje

Przeczytaj transkrypcje — po 5-10 najnowszych z każdej aktywnej kategorii:

```
_transcripts/
├── ros-product/        # ROS features, sprinty
├── ros-clients/        # Haldent, Dentus, demo
├── ros-integrations/   # Felgdent, Estomed, PMS
├── ros-research/       # User interviews
├── apolonia-team/      # Recepcja, rekrutacja
├── apolonia-marketing/ # Rebell, kampanie
├── apolonia-clinical/  # Konsultacje, zabiegi
├── apolonia-infra/     # Infrastruktura kliniki
├── arcadian/           # Ball, Winter Lounge
├── fundacja/           # FTE, granty
└── strategy/           # Strategic planning
```

Dla każdej transkrypcji wyciągnij:
- Główne tematy (2-5 per transcript)
- Powtarzające się frazy i koncepty
- Decyzje i ustalenia
- Osoby i organizacje

### Krok 2: Cross-reference z modułami

Dla każdego znalezionego tematu:

1. Grep vault (excl. `_transcripts/`) — czy istnieje moduł na ten temat?
2. Sprawdź indeksy projektów — czy temat jest wymieniony?
3. Kategorie wyniku:
   - **Ma moduł:** Skip (pipeline powinien obsłużyć)
   - **Częściowo pokryty:** Notatka do rozszerzenia (nie graduation)
   - **Brak modułu:** Kandydat do graduacji

### Krok 3: Zidentyfikuj graduation candidates

Kandydat musi spełnić WSZYSTKIE:

| Kryterium | Minimum | Dlaczego |
|-----------|---------|----------|
| Wzmianki | 3+ transkrypcje | Nie jest fleeting mention |
| Cross-cutting | 2+ kategorie LUB 5+ w jednej | Ma substancję |
| Brak modułu | Nie ma dedicated .md | Luka w vault |
| Substancja | Można napisać >200 słów | Nie jest one-liner |

Celuj w 5-10 kandydatów.

### Krok 4: Przedstaw kandydatów

Dla każdego kandydata przygotuj:

```
GRADUATION CANDIDATE #[N]: [Nazwa]

Evidence:
- [transkrypt1.md] — "[cytat/parafraza]"
- [transkrypt2.md] — "[cytat/parafraza]"
- [transkrypt3.md] — "[cytat/parafraza]"

Proposed module:
- File: [folder/nazwa-pliku.md]
- Project: [ROS / Apolonia / Fundacja / Culture]
- depends-on: [[related-module-1]], [[related-module-2]]

Content sketch:
- [Bullet 1 — main idea]
- [Bullet 2 — key detail]
- [Bullet 3 — implication]
- [Bullet 4 — open question]

Strength: [STRONG / MODERATE]
```

Użyj AskUserQuestion:

"Które idee promować do modułów?"

Opcje (multiSelect):
- Lista kandydatów (top 4, reszta w "Other")

### Krok 5: Stwórz moduły

Dla każdego zaakceptowanego kandydata:

1. **Stwórz plik** wg szablonu `_claude/2-templates/file-standard.md`:
   ```yaml
   ---
   title: [Tytuł]
   updated: [dziś YYYY-MM-DD]
   status: draft
   cadence: tactical
   sources: [[transkrypt1]], [[transkrypt2]], [[transkrypt3]]
   depends-on: [[related-module]]
   ---
   ```

2. **Wypełnij content** — bazuj na transkrypcjach, cytuj źródła
3. **Dodaj wiki-links** w powiązanych modułach → nowy moduł
4. **Zaktualizuj index** odpowiedniego projektu

### Krok 6: Podsumuj

```
GRADUATE REPORT — [data]

Created modules:
- [ścieżka1.md] — [1 zdanie opis] (sources: N transkrypcji)
- [ścieżka2.md] — [opis]
- ...

Skipped candidates:
- [nazwa] — [powód: za mało danych / user declined / overlap]

Index updates:
- [index_file] — dodano [N] nowych wpisów

Wiki-links added:
- [[existing-module]] → [[new-module]] (N linków)
```

---

## Arguments

| Argument | Co robi |
|----------|---------|
| (none) | Skanuje wszystkie kategorie transkrypcji |
| `ros` | Tylko ROS transkrypcje |
| `apolonia` | Tylko Apolonia transkrypcje |
| `strategy` | Tylko strategy transkrypcje |
| `"temat"` | Szuka konkretnego tematu do graduacji |

---

## Troubleshooting

| Problem | Rozwiązanie |
|---------|-------------|
| Za mało transkrypcji (<10 total) | Powiedz: "Vault ma za mało transkrypcji na graduation. Potrzebuję min. 30+ żeby znaleźć cross-cutting patterns." |
| Wszystko już ma moduły | To dobry sign. Powiedz: "Vault jest dobrze pokryty. Zero graduation candidates." |
| Candidate overlap z istniejącym modułem | Zaproponuj ROZSZERZENIE istniejącego modułu zamiast nowego (dodaj sekcję, nie plik) |
| Overlap z /process-transcripts | /process-transcripts PRZETWARZA backlog → update existing. /graduate ODKRYWA → creates new. Komplementarne |
| Overlap z /emerge | /emerge szuka IMPLICIT patterns (idee nie napisane). /graduate szuka EXPLICIT ideas buried in transcripts (idee napisane ale nie w module). |
| User chce graduować jedną konkretną ideę | Użyj `/graduate "nazwa idei"` — skip scanning, go straight to module creation |
