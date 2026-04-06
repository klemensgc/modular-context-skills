# Anatomia Ralph Prompt — co i dlaczego

Referencja do istniejacych promptow w `_claude/6-prompts/ralph-*.md`.

---

## Struktura (w kolejnosci)

| Sekcja | Cel | Wymagana |
|--------|-----|----------|
| **Frontmatter** | Metadane pliku (title, updated, status) | Tak |
| **Task** | Jednoliniowy opis + 2-3 zdania kontekstu | Tak |
| **Source Material** | Pelne sciezki do transkryptow/folderow | Tak |
| **Iterative Work Plan** | Fazy z konkretnymi iteracjami | Tak |
| **Target Structure** | Docelowa struktura folderow/plikow | Tak (jesli tworzy pliki) |
| **Template** | Szablon dla tworzonych plikow | Opcjonalna |
| **Completion Criteria** | Checklista "done" | Tak |
| **Self-Correction** | Co robic w kazdej iteracji + escape hatch | Tak |
| **Key Search Patterns** | Grep patterns pogrupowane per temat | Tak |
| **START** | Instrukcja startu + promise output | Tak |

---

## Dobre praktyki z istniejacych promptow

### Z ralph-apolonia.md (Knowledge Builder)
- 4 fazy: Setup > Entity Research > Cross-Cutting > Synthesis
- Kazdy entity = 1 iteracja
- Entity file template wbudowany w prompt
- 50 unique sources jako minimum

### Z ralph-culture-stage1.md (Deep Mining)
- Mining framework na poczatku (Explicit > Implicit > Hidden)
- Person profile template + Philosophy template
- Extraction tips (jak znalezc implicit content)
- Emotionalne grep patterns (frustr, excit, worried)

### Z ralph-culture-stage2.md (Enrichment)
- Zaczyna od "Critical Context" (investment agreement)
- Discovery-first approach (DO NOT ASSUME)
- Rating system dla transkryptow (1-5 gwiazdek)
- Quality control criteria per typ pliku

### Z ralph-culture-stage3.md (Quality Control)
- Zaczyna od "Problemy Zidentyfikowane"
- Docelowa struktura MECE
- "Decyzje Projektowe" sekcja (dlaczego robimy X)
- Explicit lista plikow do usuniecia

---

## Wzorce iteracji

### Iteracja research (mining)
```
**Iteration N:** [Temat do zbadania]
- Grep for "[pattern1]", "[pattern2]", "[pattern3]"
- For EACH file found, read and determine: [kryteria relevance]
- Extract: [co wyciagnac]
- Write to `[sciezka]`
- Update `_progress.md`
```

### Iteracja tworzenia (build)
```
**Iteration N:** [Co stworzyc]
- Create `[sciezka]` folder
- Create [pliki] per [szablon]
- [Logika wypelniania]
- Update `_progress.md`
```

### Iteracja quality check
```
**Iteration N:** Quality Check
- Read through all created files
- Verify sources are cited
- Check for contradictions
- Ensure consistent formatting
- Fix any issues found
```

### Iteracja finalizacji
```
**Iteration N:** Final Compilation
- Create/update [summary/index]
- Verify all [N] [items] are documented
- Confirm folder answers: "[kluczowe pytanie]"
- If complete, output: `<promise>[PROMISE]</promise>`
```

---

## Promise naming

| Typ zadania | Pattern | Przyklad |
|-------------|---------|----------|
| Knowledge Builder | `{TOPIC}_KNOWLEDGE_COMPLETE` | `APOLONIA_KNOWLEDGE_COMPLETE` |
| Deep Mining | `{TOPIC}_MINING_COMPLETE` | `CULTURE_MINING_COMPLETE` |
| Quality Control | `{TOPIC}_STAGE{N}_COMPLETE` | `CULTURE_STAGE3_COMPLETE` |
| Enrichment | `{TOPIC}_ENRICHMENT_COMPLETE` | `ROS_ENRICHMENT_COMPLETE` |
| Custom | `{TOPIC}_{ACTION}_COMPLETE` | `PIPELINE_AUDIT_COMPLETE` |
