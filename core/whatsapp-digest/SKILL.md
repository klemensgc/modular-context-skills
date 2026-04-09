---
name: whatsapp-digest
description: |
  Generuje interaktywny digest z grup WhatsApp: action items, blindspots, staleness.
  Mapuje rozmowy na projekty MC (ROS, Apolonia, FTE, Apollo) i cross-referencuje
  z quest-board, pipeline, team-roster. NIE modyfikuje vault bez zgody usera.
  Use when: chcesz przegląd co się dzieje na WhatsApp, daily standup, weekly review.
  Trigger phrases: "/whatsapp", "whatsapp digest", "daily digest", "co na whatsapp",
  "przegląd grup", "whatsapp update", "daj mi update z whatsapp"
allowed-tools: Read Grep Glob Bash(python3 *)
---

# WhatsApp Digest

Wyciąga świeże dane z WhatsApp Desktop na macOS, analizuje rozmowy w kontekście vault,
i prezentuje digest z action items. Wszystko READ-ONLY dopóki user nie zatwierdzi zmian.

---

## Faza 0: Ekstrakcja

Uruchom skrypt ekstrakcji:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/extract.py --groups-only --days 7 --output /tmp/whatsapp_digest.json
```

Jeśli user poda argument (np. `/whatsapp 30`), użyj tej liczby jako `--days`.
Jeśli user poda `--shared-with`, przekaż do skryptu.

Domyślnie: `--days 7` (ostatni tydzień).

Po ekstrakcji przeczytaj `/tmp/whatsapp_digest.json`.

---

## Faza 1: Przegląd (READ-ONLY)

Przedstaw userowi podsumowanie:

1. **Statystyki:** ile grup aktywnych, ile wiadomości, zakres dat
2. **Lista aktywnych grup** (posortowana po liczbie wiadomości):
   - Nazwa grupy | Wiadomości | Ostatnia wiadomość | Top sender
3. **Zapytaj usera:**
   - *"Które grupy chcesz przeanalizować? Wszystkie aktywne, konkretne, czy filtrować po projekcie (ROS/Apolonia/FTE/Apollo)?"*

Czekaj na odpowiedź.

---

## Faza 2: Analiza (READ-ONLY — NIE MODYFIKUJ PLIKÓW)

Dla wybranych grup:

### 2a. Przeczytaj routing
Przeczytaj `${CLAUDE_SKILL_DIR}/references/group-routing.md` — mapuje grupy → projekty MC i moduły.

### 2b. Cross-reference z vault
Dla każdego dotkniętego projektu przeczytaj odpowiednie moduły:
- **ROS** → najnowszy `1_receptionOS/8-strategy/quest-board-w*.md`, `pipeline.md`
- **Apolonia** → `2_apolonia/2_apolonia_index.md`, pliki z `3-team/`, `7-operations/`
- **FTE/Arcadian** → `3_fte/3_fte_index.md`, `2-arcadian/`
- **Apollo** → `4_apollo/4_apollo_index.md`
- **Ludzie** → `_culture/team/team-roster.md`
- **Decyzje** → `_decisions-log.md`

Sprawdź daty `updated:` w frontmatter — czy moduły są aktualne vs. co mówi WhatsApp.

### 2c. Analiza wiadomości
Dla każdej grupy wyciągnij:

| Kategoria | Co szukać |
|-----------|-----------|
| **Action items** | Pytania bez odpowiedzi, zadania przypisane, terminy, prośby |
| **Blindspots** | Grupy gdzie user milczy, ludzie czekający na odpowiedź |
| **Nowe ustalenia** | Decyzje podjęte na WhatsApp, których nie ma w vault |
| **Staleness** | Moduły vault starsze niż informacje z WhatsApp |

### 2d. Prezentacja digestu

Przedstaw wyniki userowi w strukturze:

```markdown
## 🔴 Pilne (wymaga odpowiedzi)
- [Grupa] Kto czeka na co, od kiedy

## 🟡 Blindspots (grupy/ludzie zaniedbani)
- [Grupa] User milczy X dni, Y wiadomości od innych

## 📋 Nowe ustalenia (nie ma ich jeszcze w vault)
- [Grupa] Co ustalono → który moduł powinien być zaktualizowany
  Powiązany moduł: [[nazwa-modulu]] (updated: YYYY-MM-DD)

## 📊 Kontekst
- Kto jest najbardziej aktywny
- Które projekty się ruszają
- Co się zmieniło od ostatniego digestu
```

**STOP TUTAJ. NIE modyfikuj żadnych plików. Czekaj na usera.**

---

## Faza 3: Interakcja

Zapytaj usera:

*"Co chcesz zrobić z tymi findings?"*

Opcje:
1. **Zaktualizuj moduły** — które ustalenia wpisać do vault?
2. **Dodaj do quest-board** — które action items dodać do tygodniowych priorytetów?
3. **Dodaj do decisions-log** — które decyzje zapisać?
4. **Zapisz digest** — zachować jako notatkę w `_workspace/`?
5. **Nic** — tylko przegląd, bez zmian

Czekaj na wybór. User może wybrać konkretne items z listy.

---

## Faza 4: Aktualizacja (TYLKO za zgodą usera)

Dla każdego zatwierdzonego elementu:

### Aktualizacja modułu
1. Przeczytaj moduł
2. Dodaj/zaktualizuj informację
3. Zaktualizuj `updated:` w frontmatter na dzisiejszą datę
4. Jeśli sprzeczność z istniejącą treścią → POKAŻ OBE WERSJE, zapytaj usera

### Quest-board
1. Znajdź najnowszy `quest-board-w*.md`
2. Dodaj action items w odpowiedniej sekcji

### Decisions-log
1. Dodaj wpis do `_decisions-log.md` w formacie:
   ```
   | YYYY-MM-DD | Decyzja | Kontekst (WhatsApp: [grupa]) | Status |
   ```

### Workspace note
1. Zapisz digest jako `_workspace/{YYYY-MM}/wN/whatsapp-digest-{YYYY-MM-DD}.md`
2. Frontmatter: `title`, `updated`, `status: stable`, `sources: WhatsApp`

---

## Faza 5: Podsumowanie

Pokaż co zostało zmienione:
- Lista zmodyfikowanych plików
- Zasugeruj `/log` do scommitowania zmian

---

## Uwagi techniczne

- Skrypt `extract.py` automatycznie znajduje WhatsApp DB na macOS
- Wymaga WhatsApp Desktop zainstalowanego i zsynchronizowanego
- Zero zewnętrznych zależności (Python stdlib)
- Dane nie opuszczają maszyny — JSON trafia do `/tmp/` i jest usuwany po sesji
- Skrypt kopiuje DB do temp file żeby nie blokować WhatsApp
