# Vault Audit — Real Examples

Przykłady z sesji repo. Metryki, findings, lessons learned.

---

## Example 1: Full Vault Coherence Audit (2026-02-22)

**Scope:** Cały vault (~567 plików .md, bez _transcripts/)
**Metoda:** 4 równoległe scan-agenty

### Metryki

| Metryka | Wartość | Ocena |
|---------|---------|-------|
| Moduły skanowane | ~567 | — |
| Wiki-links total | 476 | — |
| Broken wiki-links (structural) | ~17 + kilkadziesiąt ambiguous | MEDIUM |
| Orphaned dependencies | 70 | HIGH |
| True orphan files | 6 | LOW |
| Circular dependencies | 0 | OK |
| Missing cadence field | ~265 (46.8%) | MEDIUM |
| Missing frontmatter entirely | 43 (7.6%) | MEDIUM |
| Cross-module contradictions | 4 | MEDIUM |
| Index files correct | 15/15 | OK |
| Naming compliance | ~95% | OK |

### Overall: GOOD z known issues

### Top findings:
1. **`_principles/` broken path** — 8 plików referencuje nieistniejący `hormozi-frameworks_index.md`
2. **Ambiguous cross-project links** — `[[vision]]`, `[[roadmap]]` matchują wiele plików
3. **Pipe syntax w depends-on** — 6 plików ma `[[...|alias]]` w YAML (invalid)
4. **Orphaned dependencies** — 70 plików ma `depends-on` wskazujący na nieistniejące pliki
5. **Missing cadence** — 265 plików, ale ~200 to `.claude/` i `_drafts/` (expected)

### Lesson: Obsidian vs Claude Code links
~88.5% linków "technicznie broken" w grep, ale **działają w Obsidian** (relative resolution). Problem dotyczy Claude Code, nie usera. Raport powinien odróżniać "broken for Obsidian" vs "broken for tooling".

### Plik: `_workspace/vault-ops/coherence-audit.md`

---

## Example 2: Vault Consolidation (2026-02-15)

**Scope:** repo-wide audit + file consolidation
**Cel:** Zmniejszenie file count, usunięcie duplikatów, merge related modules

### Metryki before → after:
- **Files:** 122 workspace files → ~20 (po consolidation)
- **Orphans:** 34 pliki bez incoming links → 6
- **Duplikaty:** 8 znalezionych → 0

### Actions:
1. Merged 5 par `{topic}-v1.md` + `{topic}-v2.md` → jeden plik z historią
2. Przeniesiono `_drafts/` → `_workspace/` (jeden folder na deliverables)
3. Usunięto 14 pustych stubów (0 content poza frontmatter)
4. Zaktualizowano 22 broken links po rename/move

### Lesson: Rename cascade
Każdy rename generuje broken links w plikach referencujących. **ZAWSZE grep po starej nazwie** po każdym move i podmień na nową. Kolejność: (1) fix broken links, (2) frontmatter, (3) rename/move, (4) nowe indeksy.

---

## Example 3: Operations MECE Restructure (2026-01-20)

**Scope:** `1_receptionOS/5-operations/`
**Cel:** Restrukturyzacja flat folder → MECE (mutually exclusive, collectively exhaustive)

### Before:
```
5-operations/
  implementation-guide.md
  client-setup.md
  support-playbook.md
  scheduling.md
  deployment-process.md
  ...12 more flat files
```

### After:
```
5-operations/
  5-operations_index.md          ← NEW
  1-implementation/
    implementation-guide.md
    client-setup.md
    deployment-process.md
  2-support/
    support-playbook.md
    scheduling.md
  3-monitoring/
    ...
```

### Actions:
1. Categorized 17 files into 3 MECE groups
2. Created subfolder structure
3. Created index file linking all modules
4. Updated 8 cross-references from other projects

### Lesson: MECE restructure = PLAN mode
Zawsze pokaż userowi proposed structure PRZED move. User może mieć mental model inny niż logical grouping.

---

## Example 4: Prompts Reorg (2026-02-23)

**Scope:** `_claude/6-prompts/`
**Cel:** Porządkowanie promptów Ralph po wielu rundach

### Findings:
- 3 prompty z `status: completed` (powinny być archived)
- 2 duplikaty (ralph-culture-stage2 vs ralph-culture-enrichment)
- 5 promptów bez `updated:` w frontmatter
- Naming inconsistency: `ralph-{temat}.md` vs `{temat}-stage{N}.md`

### Actions:
1. Archived completed prompts (moved to `_claude/6-prompts/_archive/`)
2. Merged duplikat → 1 plik z combined content
3. Added missing frontmatter
4. Standardized naming: `ralph-{temat}.md`, `ralph-{temat}-stage{N}.md`

### Lesson: Post-Ralph cleanup
Po każdym batch Ralph run, prompty się rozrastają. Periodic audit `6-prompts/` zapobiega clutter.

---

## Audit Report Template (z sesji)

```markdown
VAULT AUDIT REPORT — {scope} — {date}

## Summary
- Files scanned: {N}
- Broken links: {N} (across {N} files)
- Naming issues: {N}
- Missing indices: {N}
- Frontmatter issues: {N}
- Organization issues: {N}

## HIGH Priority (structural breakage)
| # | Type | File | Issue | Fix |
|---|------|------|-------|-----|
| 1 | Broken link | path:line | [[target]] not found | Create / fix |

## MEDIUM Priority (conventions)
...

## LOW Priority (cosmetic)
...

## VERIFICATION (po naprawach)
- Broken links: {before} → {after}
- Naming issues: {before} → {after}
- Remaining: {N}
```
