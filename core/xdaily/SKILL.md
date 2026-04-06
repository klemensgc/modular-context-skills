---
name: xdaily
description: |
  Takes X/Twitter posts and threads them into the relevant vault modules. User pastes tweet text,
  skill classifies by project, finds related modules, and weaves the content into the vault.
  Use when: you posted something on X and want it captured in the vault, found an interesting
  thread to integrate, wanting to connect social media output with your knowledge base.
  Trigger phrases: "xdaily", "x daily", "twitter", "tweets", "wplecz tweety",
  "thread into vault", "x posts", "tweety do vault", "tweet to vault"
---

# XDaily

Przyjmuje treści z X/Twitter i wplata je w odpowiednie moduły vault.

Repo jest po polsku. Odpowiadaj po polsku.

**Ograniczenie:** Skill NIE ma dostępu do X API. User musi wkleić treść ręcznie (copy-paste z X lub screenshot).

---

## Quick Start

1. Przyjmij input od usera (tekst tweetów)
2. Parsuj i klasyfikuj każdy tweet
3. Znajdź powiązane moduły w vault
4. Zaproponuj akcje (update module / create note / add source)
5. Po akceptacji — wykonaj zmiany

---

## Workflow

### Krok 1: Przyjmij input

Jeśli argument zawiera tekst tweetów — parsuj bezpośrednio.

Jeśli brak argumentu, użyj AskUserQuestion:

"Wklej treść tweetów/postów z X (tekst, nie URL):"

Opcje:
- "Wkleję w następnej wiadomości"
- "Mam screenshot" (→ Read tool na ścieżkę)
- Other

### Krok 2: Parsuj input

Dla każdego tweeta/posta wyciągnij:
- **Treść:** Główny tekst
- **Kontekst:** Czy to reply? Quote? Thread?
- **Tematy:** Keywords, mentions, hashtags
- **Typ:** Insight / Decision / Announcement / Question / Conversation
- **Data:** Jeśli podana

Jeśli thread (wiele powiązanych postów) → zachowaj kolejność i kontekst.

### Krok 3: Klasyfikuj po projekcie

Dla każdego tweeta:

| Słowa kluczowe | Projekt |
|-----------------|---------|
| ROS, voicebot, recepcja, SaaS, dental AI | ReceptionOS |
| Apolonia, klinika, dentysta, pacjent | Apolonia |
| Fundacja, Edison, Arcadian, Ball | Fundacja |
| Apollo, system AI, klinika AI | Apollo |
| Zespół, kultura, filozofia, zasady | Culture |
| Inne | General (→ `_workspace/`) |

### Krok 4: Znajdź powiązane moduły

Dla każdego klasyfikowanego tweeta:

1. Grep vault po keywords z treści tweeta
2. Sprawdź indeks odpowiedniego projektu
3. Zidentyfikuj najlepsze dopasowanie (moduł z najwyższym keyword overlap)

### Krok 5: Zaproponuj akcje

Dla każdego tweeta pokaż userowi:

```
TWEET: "[skrócona treść, max 50 chars]..."
Project: [projekt]
Related: [[module-name]]

Proposed action:
[Jedna z poniższych]
```

**Możliwe akcje:**

| Akcja | Kiedy | Co robi |
|-------|-------|---------|
| **Add to sources** | Tweet potwierdza/rozszerza existing module | Dodaj do `sources:` w frontmatter |
| **Update module** | Tweet zawiera nową informację relevant do modułu | Dodaj paragraf/bullet do modułu |
| **Create note** | Tweet to standalone insight bez dobrego modułu | Stwórz `_workspace/{YYYY-MM}/wN/x-{date}-{topic}.md` |
| **Add to transcript** | Tweet to conversation/thread z wartością | Stwórz summary w `_transcripts/` |
| **Skip** | Tweet jest casual / no vault value | Nic nie rób |

Użyj AskUserQuestion dla batcha:

"Zaproponowane akcje — zaakceptować?"

Opcje (multiSelect jeśli wiele):
- "Tak, wszystkie"
- "Pokaż szczegóły"
- "Skip wszystkie"
- Other

### Krok 6: Wykonaj akcje

Dla zaakceptowanych:

1. **Add to sources:** Edytuj frontmatter modułu — dodaj `[[x-post-YYYY-MM-DD]]` do `sources:`
2. **Update module:** Dodaj content z tweetów jako nową sekcję/bullet. Oznacz: `(źródło: X post, [data])`
3. **Create note:** Użyj file-standard template. Status: `draft`. Cadence: `tactical`.
4. **Add to transcript:** Stwórz summary w odpowiedniej kategorii `_transcripts/`.

Każdą edycję rób przez Edit tool (nie nadpisuj całego pliku). Zaktualizuj `updated:` w frontmatter.

### Krok 7: Podsumuj

```
XDAILY REPORT — [data]

Processed: [N] tweets/posts

Actions taken:
- [[module1]] — updated (added [topic])
- [[module2]] — added to sources
- _workspace/...x-{date}-{topic}.md — created (standalone note)
- [N] skipped

Modules touched: [N]
New files: [N]
```

---

## Arguments

| Argument | Co robi |
|----------|---------|
| (none) | Interactive — pyta o input |
| `"tekst tweeta"` | Parsuje podany tekst bezpośrednio |

---

## Troubleshooting

| Problem | Rozwiązanie |
|---------|-------------|
| User podaje URL zamiast tekstu | Powiedz: "Nie mam dostępu do X API. Wklej TEKST tweeta, nie URL." |
| Screenshot zamiast tekstu | Użyj Read tool — Claude jest multimodal, może czytać screenshoty |
| Tweet nie pasuje do żadnego projektu | Stwórz standalone note w `_workspace/`. Nie na siłę dopasowuj. |
| Thread (wiele tweetów) | Zachowaj kolejność. Traktuj thread jako jeden input, nie osobne tweety. |
| Tweet po angielsku, vault po polsku | Zostaw tweet w oryginale. Komentarz/context w module po polsku. |
| Overlap z /copy | /copy TWORZY content na social media. /xdaily IMPORTUJE content z social media do vault. Odwrotny kierunek. |
| Tweet jest kontrowersyjny/wrażliwy | Powiedz: "Ten tweet może być wrażliwy. Chcesz go dodać do vault?" Czekaj na potwierdzenie. |
