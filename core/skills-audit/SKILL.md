---
name: skills-audit
description: Scan your installed skills, detect eligibility gaps, motivate contribution. Run post-onboarding or quarterly as a library health check.
triggers:
  - "skills audit"
  - "skills-audit"
  - "audit skills"
  - "co mam zainstalowane"
  - "library check"
  - "which skills should i install"
  - "przegląd skilli"
required-tools:
  - Read
  - Grep
  - Glob
---

# Skills Audit

Scans your Modular Context install and classifies every skill in the library into one of 4 buckets based on what you have vs what's eligible. Then surfaces contribution opportunities (skills you've customized, stale ones you use often).

This is your **library onboarding compass** — run it after plugin install, after `/connect` flow changes, or quarterly to rebalance what's active.

---

## When to use

| Trigger | What you'll get |
|---------|-----------------|
| Just installed plugin | 4-bucket report → pick 1-2 eligible-not-installed to try first |
| Reconfigured Google Workspace / WhatsApp / vault structure | Re-classification (prereq-blocked → eligible) |
| Quarterly library review | Stale detection, contribution opportunities |
| Before onboarding teammate | Export current state as baseline recommendation |

**Don't run when:** you just want a specific skill — invoke that skill directly. This is for *surveying the whole shelf*.

---

## Tools at your disposal

Core Claude Code tools only:
- `Read` — skill registry (`~/.../modular-context-skills/registry.json`), plugin data (`.obsidian/plugins/modular-context/data.json`), vault root files
- `Glob` — detect vault structure (CLAUDE.md, project indices, `_workspace/` path)
- `Grep` — scan for customizations (diffs between local skills and library)
- `Bash` (read-only) — `ls` for filesystem prereq flags

**No MCP tools needed.** No API calls. Zero network — runs fully local.

---

## Pattern — 4-bucket classification

### Step 1 — Discover state

Read these files (silent, no user prompt):

1. **Skills registry** — `modular-context-skills/registry.json` — all 23 skills z `requires[]`
2. **Installed skills** — `{vault}/.obsidian/plugins/modular-context/data.json` → `installedSkills` object
3. **Prereq flags** — evaluate each flag from registry `requiresFlags` section:
   - `vault-structure` → `Glob("CLAUDE.md")` + `Glob("[0-9]*_*/[0-9]*_*_index.md")` both match?
   - `gsuite-connected` → `~/.modular-context/mcp-google/accounts-index.json` exists?
   - `whatsapp-macos` → `Bash("uname")` returns "Darwin" AND `Bash("ls /Applications/WhatsApp.app")` succeeds?
   - `git-initialized` → `Glob(".git/config")` matches?
   - `python3` → `Bash("which python3")` returns path?

### Step 2 — Classify each skill

For every skill in registry, assign to ONE bucket:

**✅ Bucket 1 — Installed & eligible** (green)
- Plugin data has it under installed
- All `requires[]` satisfied (skill IDs installed + flags true)

**🟡 Bucket 2 — Eligible, not installed** (amber — recommend next)
- All `requires[]` satisfied
- Not in installed list

**🔴 Bucket 3 — Prereq-blocked** (red — wants setup)
- In registry but some requires[] unsatisfied
- Report WHICH requires are missing

**⚪ Bucket 4 — Aspirational** (gray — long-term)
- Requires major setup (new Google account, WhatsApp macOS install, Python3 setup)
- Difficulty: `expert` AND at least 2 unmet requires

### Step 3 — Find contribution signals

Look for motivation triggers:

1. **Customizations** — for each Bucket 1 skill, compare content hash/bytes against library version:
   ```bash
   installed_path=".obsidian/plugins/modular-context/skills/{id}/SKILL.md"
   library_path="modular-context-skills/core/{id}/SKILL.md"
   diff "$installed_path" "$library_path"
   ```
   If different → "You've customized {skill} — consider PR'ing improvements back"

2. **Stale updates** — for Bucket 1 frequently-invoked skills, check registry `version`:
   - If `version: 1.0.0` AND released date >6mo ago → "Used often, hasn't been refreshed in 6+ months"

3. **Gap signals** — if Bucket 2 has ≥5 skills → "You're missing half the library — quick wins below"

4. **Integration opportunities** — if user has Bucket 1: {process-transcripts, whatsapp-digest} → "You could create a combined `daily-capture` skill — PR it."

### Step 4 — Write report

Target: `_workspace/{YYYY-MM}/w{N}/skills-audit-{YYYY-MM-DD}.md`

Use frontmatter:
```yaml
---
title: Skills Audit — {YYYY-MM-DD}
updated: {YYYY-MM-DD}
status: active
audited-by: skills-audit v1.0.0
---
```

Body structure:

```markdown
# Skills Library Audit — {YYYY-MM-DD}

**Registry version:** {registry.version} · **Total skills:** {count}

## Summary

- ✅ Installed & eligible: {N}
- 🟡 Eligible, not installed: {N} ← **start here**
- 🔴 Prereq-blocked: {N}
- ⚪ Aspirational: {N}

## ✅ Installed & eligible (N)

| Skill | ⭐ | Last used* | Health |
|-------|---|------------|--------|
| pulse | ⭐⭐⭐⭐⭐ | (plugin state) | ✓ |
| ...

*Usage frequency not currently tracked — placeholder for v2.2+

## 🟡 Eligible, not installed — RECOMMENDED (N)

Sorted by value (high first):

| Skill | ⭐ | Difficulty | Value | Why try it |
|-------|---|------------|-------|------------|
| brief | ⭐⭐⭐⭐⭐ | operator | high | You write PDFs occasionally — this pipelines it |
| ...

## 🔴 Prereq-blocked (N)

| Skill | Missing | How to unblock |
|-------|---------|----------------|
| reweave | `process-transcripts` | Install process-transcripts first |
| gsuite-analysis | `gsuite-connected` | Run `Google Workspace: Connect` command |
| ...

## ⚪ Aspirational (N)

Requires significant setup — consider when you have time.

- **whatsapp-digest** — needs macOS WhatsApp.app (⚪ if not on macOS)
- ...

## 🎁 Contribution opportunities

### You've customized these (consider PR)
{list of skills where local differs from library — or "none detected"}

### Skills you use often that haven't been updated in 6+ months
{list — or "all fresh"}

### Combo skill ideas
{based on installed combinations — or "no obvious gaps"}

## Next 3 actions

1. **Try `{top-recommendation}`** — {1-line why}
2. **Unblock `{top-blocked}`** — {1-line how}
3. **Read `CONTRIBUTING.md`** if you want to PR improvements

---

_Generated by skills-audit. Run again after setup changes or quarterly._
```

---

## Output standards

**Location:** `_workspace/{YYYY-MM}/w{N}/skills-audit-{YYYY-MM-DD}.md`

**Frontmatter required:** title, updated, status, audited-by (versioned self-reference)

**Idempotent:** re-running on same day overwrites (not appends) — user gets fresh snapshot

**No side effects:** never modifies registry, never calls network, never writes to plugin data. Read-only audit.

---

## Edge cases

- **No plugin installed yet:** skip Step 2; report all 23 skills as "Not installed — install plugin first"
- **No vault structure:** many skills flagged Prereq-blocked by `vault-structure` → recommend `start-here` onboarding path
- **No `_workspace/` folder exists:** create `_workspace/{YYYY-MM}/w{N}/` before writing report
- **Registry unreachable:** fall back to cached plugin registry (`data.json` → `installedSkills`); flag "running in offline mode"
- **Diff check fails** (installed path missing): skip customization detection for that skill, log once

---

## Not in scope

- **Auto-install skills** — recommendations only; user picks from plugin UI
- **Modify registry** — this is a scanner, not editor
- **Telemetry / send metrics** — fully local, no network
- **Run the other skills** — orchestration is a separate skill (see `overnight` for chained execution)
- **Rate individual skills** — uses registry ratings as-is, doesn't second-guess
- **Unit test coverage** — if you want quality checks, use admin skill `skill-validator` (lives in maintainer's vault)

---

## Examples

### Fresh install (no skills yet)
→ Bucket 2 dominant. Recommendation: "Start with Synthesise Files + Pulse + Log. These cover capture → analyze → commit loop."

### Power user (15+ installed)
→ Bucket 1 large. Motivation triggers kick in: "You've customized 3 skills. PR `brief` improvements?"

### macOS user without WhatsApp
→ `whatsapp-digest` flagged Aspirational. "Install WhatsApp for macOS if you want group digests — skip otherwise."

### Non-MC user (vault but no project folders)
→ `vault-structure` flag false → many skills flagged Prereq-blocked. Surface: "Run `start-here` to scaffold project folders, unblocks 8 skills."

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "No installed skills found" but I see them in sidebar | Plugin data path wrong | Check `data.json` location — may be in `{vault}/.obsidian/plugins/modular-context/` |
| Ratings don't match what I see in sidebar | Registry + plugin out of sync | Reload plugin to re-fetch registry from GitHub |
| Report says all skills Prereq-blocked | Vault doesn't have CLAUDE.md | Create CLAUDE.md (or run `start-here` onboarding) |
| `whatsapp-macos` flagged true on Linux | False positive | Report as bug — flag logic checks uname=Darwin |
