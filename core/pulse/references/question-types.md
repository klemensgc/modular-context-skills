# Question Types — Pulse

10 typow pytan. Kazdy typ ma inny cel i inny efekt na usera i vault.

---

## 1. TENSION

**Cel:** Vault mowi X, rzeczywistosc mogla sie zmienic.
**Efekt na usera:** Zmusza do konfrontacji vault vs. realia.
**Efekt na vault:** Aktualizacja stalych danych.

**Schemat:** "[Modul] mowi ze [fakt]. Minelo [N dni]. Nadal aktualne?"

**Przyklady:**
- "Pipeline mowi ze Dentus to 'warm lead'. 3 tygodnie bez kontaktu. Nadal warm?"
- "Roadmap zaklada launch feature X w Q1. Jestesmy w polowie Q1 — na torze?"
- "Team roster mowi Czarek robi 8 workstreamow. Zmienilo sie cos?"

**Dane do skanu:** Moduly z `updated:` > 14 dni + wysoka connectivity (depends-on count).

---

## 2. KILL

**Cel:** Wymus decyzje priorytetyzacyjna.
**Efekt na usera:** Klaruje prawdziwe priorytety vs. deklarowane.
**Efekt na vault:** Aktualizacja statusow, zamkniecie martych inicjatyw.

**Schemat:** "[N] inicjatyw walczy o uwage: [lista]. Gdybys musial zabic jedna — ktora?"

**Przyklady:**
- "3 open deale w pipeline: Dentus, Estomed, Magda. Gdybys mogl pogonic tylko 1 — ktory?"
- "W quest board masz 5 side questow. Ktory mozna spokojnie dropnac?"
- "Rekrutacja, product, sales — w tym tygodniu mozesz pchnac tylko 1. Co wybierasz?"

**Dane do skanu:** Quest board, pipeline, active projects — szukaj >3 rownoczesnych inicjatyw.

---

## 3. ASSUMPTION

**Cel:** Challenge zalozenie wbudowane w vault.
**Efekt na usera:** Testuje czy fundamenty strategii nadal trzymaja.
**Efekt na vault:** Fix stalych zalozen lub potwierdzenie (tez warto zalogowac).

**Schemat:** "Vault zaklada ze [zalozenie]. Ostatnie [dane] to potwierdzaja?"

**Przyklady:**
- "Oferta zaklada ze 3,900 PLN/mies to sweet spot. Klienci to potwierdzaja?"
- "Strategia zaklada ROS 50% twojego czasu. Tak wyglada w praktyce?"
- "Roadmap zaklada ze Igor zrobi X do konca miesiaca. Realne?"

**Dane do skanu:** Pliki strategy, pricing, roadmap — wyciagaj explicite i implicite zalozenia.

---

## 4. GHOST

**Cel:** Cos co bylo aktywne zniknelo z radaru.
**Efekt na usera:** Lapiemy upuszczone pilki.
**Efekt na vault:** Status update (zamkniete/pauza/zapomniane) lub wznowienie.

**Schemat:** "Temat [X] byl aktywny do [data]. Od tamtej pory cisza. Co sie stalo?"

**Przyklady:**
- "Academy byla w planach w grudniu. Zero wzmianek od stycznia. Status?"
- "Rozmowy z Felgdent ucichly 2 tygodnie temu. Swiadomy drop?"
- "Kampania Rebell byla w toku — ostatnia wzmianka 3 tygodnie temu."

**Dane do skanu:** Tematy z transkryptow >14 dni bez nowej aktywnosci. Cross-reference z modulami.

---

## 5. MISSING

**Cel:** Temat istnieje w transkryptach ale nie ma modulu.
**Efekt na usera:** Decyzja czy temat wart dokumentacji.
**Efekt na vault:** Nowy modul lub swiadoma decyzja "nie potrzebujemy".

**Schemat:** "Temat [X] pojawia sie w [N] transkryptach ale nie ma modulu. Warto stworzyc?"

**Przyklady:**
- "Pawilon pojawia sie 3 razy w rozmowach. Nie ma modulu w 2-assets/. Stworzyc?"
- "AI Dent to nowa nazwa Express Dent — ale modul nadal Express Dent. Rebrand?"
- "Temat 'man cave + podcast studio' nie ma wlasnego pliku. Potrzebny?"

**Dane do skanu:** Grep transkryptow za encjami nieobecnymi w modulach.

---

## 6. CONTRADICTION

**Cel:** Dwa moduly mowia co innego.
**Efekt na usera:** Rozstrzygniecie sprzecznosci.
**Efekt na vault:** Fix jednego z modulow.

**Schemat:** "W [plik A] jest [X], w [plik B] jest [Y]. Co aktualne?"

**Przyklady:**
- "Pipeline mowi Kamil ogarnia Dentus, ale Kamil twierdzi ze nie wie o Dental Fraternity."
- "Roadmap mowi Q1 launch, quest board mowi 'po Miami'. Ktore aktualne?"
- "Team roster: Weronika active. Operations: Weronika closed. Ktore?"

**Dane do skanu:** Consistency check miedzy powiazanymi modulami (depends-on chains).

---

## 7. ENERGY

**Cel:** Temperatura emocjonalna / motywacyjna.
**Efekt na usera:** Wglad w wlasny stan, swiadomosc energii.
**Efekt na vault:** Maping energia → projekty (hidden priority signal).

**Schemat:** Otwarte pytanie o to co daje i zabiera energie.

**Przyklady:**
- "Z czym masz teraz najwiekszy momentum? Co ciazy?"
- "Ktory projekt budzi ekscytacje, a ktory obowiazek?"
- "Gdybys mial wolny tydzien na JEDEN temat — co bys wybral?"

**Dane do skanu:** Nie wymaga specjalnego skanu — zawsze wartosc w deep mode.

---

## 8. BET

**Cel:** Explicite wyartylulowanie biggest bet.
**Efekt na usera:** Klaruje implicytna strategie.
**Efekt na vault:** Update strategii, quest board, priorytetow.

**Schemat:** Pytanie o concentrated bet i downside risk.

**Przyklady:**
- "Jaki jest twoj biggest bet na najblizsze 30 dni? Co sie stanie jesli nie wyjdzie?"
- "Na co stawiasz ten miesiac — co musi wyjsc zeby miesiac byl udany?"
- "Gdyby jedna rzecz miala sie udac w lutym — co to?"

**Dane do skanu:** Quest board, roadmap, strategy — szukaj implicit bets.

---

## 9. PERSON

**Cel:** Pulse na relacje i zespol.
**Efekt na usera:** Refleksja o ludziach, nie tylko taskach.
**Efekt na vault:** Update team modulow, baseball cards.

**Schemat:** Pytanie o konkretne osoby — kto zaskakuje, kto martwi.

**Przyklady:**
- "Kto w zespole teraz pozytywnie zaskakuje? Kto martwi?"
- "Z kim miales ostatnio rozmowe ktora zmienila twoje zdanie o czyms?"
- "[Osoba] ma 3 otwarte watki w vault. Jak oceniasz ich execution?"

**Dane do skanu:** Team roster, recent transcripts z osobami, task assignments.

---

## 10. DRIFT

**Cel:** Wykryj niezamierzony drift strategiczny.
**Efekt na usera:** Swiadomosc gap miedzy planem a realizacja.
**Efekt na vault:** Korekta strategii lub akceptacja nowego kursu.

**Schemat:** Porownanie deklaracji vs. obserwowanej aktywnosci.

**Przyklady:**
- "Deklarujesz ROS 50%, Apolonia 30%, Fundacja 20%. Jak wyglada ostatni tydzien?"
- "Quest board mowi priorytet to [X]. Transkrypcje z tygodnia dotycza glownie [Y]. Swiadomie?"
- "Roadmap mowi focus na enterprise. 3 z 4 ostatnich rozmow to SMB. Pivot?"

**Dane do skanu:** Compare quest board / strategy vs. recent transcript categories.

---

## Reguly selekcji pytan

### Tryb quick (/pulse) — 3 pytania:
- 1x z grupy CHALLENGE: TENSION, KILL, ASSUMPTION, CONTRADICTION
- 1x z grupy VAULT-FIX: GHOST, MISSING, CONTRADICTION
- 1x z grupy FORWARD: ENERGY, BET, DRIFT
- Kazde musi referencowac konkretne dane z vault skanu

### Tryb deep (/pulse deep) — 5 pytan:
- 1x CHALLENGE (TENSION / KILL / ASSUMPTION)
- 1x VAULT-FIX (GHOST / MISSING / CONTRADICTION)
- 1x FORWARD (BET / DRIFT)
- 1x PEOPLE (ENERGY / PERSON)
- 1x WILDCARD (dowolny typ najciekawszy ze skanu)
- Min 2 projekty pokryte
- Min 1 pytanie o temat z poprzedniego pulse (follow-up)

### Anty-reguly (NIGDY):
- Nie zaczynaj od "Jaki jest status..."
- Nie pytaj o cos co user sam ci powiedzial w tej sesji
- Nie powtarzaj tego samego typu 2x w jednym pulse
- Nie zadawaj pytan generycznych (bez danych z vault)
- Nie pytaj o rzeczy rozstrzygniete w poprzednim pulse (chyba ze follow-up)
