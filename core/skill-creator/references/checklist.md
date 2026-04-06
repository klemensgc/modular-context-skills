# Checklist walidacyjny skilla

## Struktura

- [ ] Folder w `.claude/skills/{kebab-case-nazwa}/`
- [ ] Plik `SKILL.md` (dokładna nazwa, case-sensitive)
- [ ] Nazwa folderu nie zawiera "claude" ani "anthropic"

## Frontmatter

- [ ] Pole `name` — kebab-case, pasuje do nazwy folderu
- [ ] Pole `description` — max 1024 znaków
- [ ] Description zawiera WHAT (co robi)
- [ ] Description zawiera WHEN (kiedy użyć)
- [ ] Description zawiera trigger phrases (naturalne frazy usera)
- [ ] Brak nadmiarowych pól w frontmatter

## Instrukcje

- [ ] Quick Start na górze (5-7 linijek, happy path)
- [ ] Szczegółowe kroki w środku (Krok 1, 2, 3...)
- [ ] Sekcja Troubleshooting na dole (tabela Problem | Rozwiązanie)
- [ ] Imperatywny ton ("Stwórz", "Uruchom", nie "Możesz stworzyć")
- [ ] Konkretne przykłady kodu/komend
- [ ] Brak XML tags w treści
- [ ] Brak emoji (chyba że user prosi)

## Triggering

- [ ] Test pozytywny: każda trigger phrase dopasowuje skill
- [ ] Test negatywny: zapytania z sąsiedniej domeny NIE triggerują
- [ ] Description nie jest zbyt ogólny (brak false positives)
- [ ] Description nie jest zbyt wąski (pokrywa warianty zapytań)

## Jakość

- [ ] Progressive disclosure (3 poziomy: quick start → details → reference)
- [ ] Domyślne wartości podane (user nie musi definiować wszystkiego)
- [ ] Relatywne linki do references/ (jeśli istnieją)
- [ ] Output spełnia oczekiwania na happy path
- [ ] Edge cases opisane w troubleshooting
