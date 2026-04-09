# WhatsApp Group → Modular Context Routing

Mapuje grupy WhatsApp na projekty i moduły w vault.
Grupy matchowane po nazwie (case-insensitive substring).
Jeśli grupa nie pasuje do żadnego wzorca → kategoria "Inne".

---

## ReceptionOS (1_receptionOS/)

| Wzorzec nazwy | Moduły vault | Key people |
|---------------|-------------|------------|
| `rOS` | `1-product/roadmap.md`, `4-go-to-market/pipeline.md`, `8-strategy/quest-board-w*.md` | Adam Wroński, Klemens, Igor |
| `receptionOS` | `1-product/features.md`, `4-go-to-market/pipeline.md` | Klemens |
| `Descope` | `2-architecture/` | Igor |
| `Klemens saas` | `8-strategy/quest-board-w*.md` | Klemens |

## Apolonia (2_apolonia/)

| Wzorzec nazwy | Moduły vault | Key people |
|---------------|-------------|------------|
| `Apolonia` | `2_apolonia_index.md` | Klemens, Czarek |
| `Riotters` | `6-marketing/`, `4-brand/` | Olga Riotters, Paweł Drzewiecki |
| `Taskforce` | `5-strategy/`, `4-go-to-market/pipeline.md` | Kamil Kuczewski |
| `Kuba` | `3-team/team-roster.md`, `5-strategy/` | Kuba Sieńko |
| `zespół` or `Informacje` | `3-team/`, `7-operations/` | Violetta Kozłowska |
| `Asystentki` | `7-operations/`, `7-operations/patient-journey.md` | Violetta, Agata Janiszewska |
| `Lekarze` | `7-operations/` | Violetta |
| `Recepcja` | `7-operations/`, `7-operations/patient-journey.md` | Violetta |
| `Travel` | `7-operations/` | Jan Kempa, Czarek |
| `rekrutac` | `3-team/` | Klemens |
| `Kampania` | `6-marketing/` | Czarek |
| `MrOptim` | `6-marketing/` | Klemens |

## Fundacja Edison / Arcadian (3_fte/)

| Wzorzec nazwy | Moduły vault | Key people |
|---------------|-------------|------------|
| `Arcadian` | `2-arcadian/`, `3_fte_index.md` | Klemens, Siebe Dirckx |
| `Creative` | `2-arcadian/brand.md` | Siebe Dirckx, Gillian, Daniel Film |
| `Champions` | `2-arcadian/` | |
| `Logistyka` | `4-operations/` | |
| `Fundacja` | `1-mission/`, `6-legal/` | Czarek |
| `Rada Fundacji` | `6-legal/` | Czarek |
| `Zespół filmowy` | `2-arcadian/` | |
| `Bolt` | `4-operations/` | |

## Apollo (4_apollo/)

| Wzorzec nazwy | Moduły vault | Key people |
|---------------|-------------|------------|
| `Apollo` | `4_apollo_index.md`, `1-strategy/roadmap.md` | Klemens, Czarek |

Apollo discussions most often surface in Riotters and Taskforce groups.

## Culture / Cross-project (_culture/)

| Wzorzec nazwy | Moduły vault | Key people |
|---------------|-------------|------------|
| `Załatwianie` | `_culture/team/team-roster.md` | |
| `Wszyscy` | general | |
| `Wjeżdżacze` | general | |

---

## Jak matchować

1. Dla każdej grupy z WhatsApp JSON, szukaj wzorca (case-insensitive) w tabeli powyżej
2. Jeśli pasuje → użyj wskazanych modułów do cross-reference
3. Jeśli nie pasuje → oznacz jako "Inne" i pokaż userowi
4. Jedna grupa może pasować do wielu wzorców (np. "Apolonia <> Riotters" → Apolonia + Riotters)

## Jak dodać nowe grupy

Jeśli user ma grupę WhatsApp, której nie ma w tabeli:
1. Zapytaj do którego projektu należy
2. Zaproponuj update tego pliku
