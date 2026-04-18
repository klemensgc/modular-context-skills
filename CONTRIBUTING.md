# Contributing to Modular Context Skills

Thanks for considering a contribution. This library is **opinionated** — not every prompt belongs here. Skills shipped in `core/` must meet the standards below so the plugin's skill picker feels curated, not cluttered.

If you're not sure whether your idea fits, open a Discussion first.

---

## Quality bar

A skill ships when it's:

- **Reusable** — works beyond one project, one person's workflow
- **Standalone** — invokable without reading 3 other docs first
- **Bounded** — one playbook, not a toolkit
- **Honest** — rated accurately (don't inflate stars/value)

If it's a one-off prompt for your setup, keep it in your own vault — that's what `_claude/skills/` locally is for.

---

## Required frontmatter

Every `SKILL.md` (or `COMMAND.md` for slash-command type) must start with:

```yaml
---
name: skill-id                          # kebab-case, matches registry.json id
description: One-sentence purpose.      # Under 140 chars
triggers: ["trigger 1", "skill alias"]  # Phrases the skill activates on
required-tools: ["Read", "Grep"]        # Optional — only if skill needs specific Claude tools or MCP tools
---
```

- `name` — must match your registry.json `id`
- `description` — same text as registry `description` field (keep in sync)
- `triggers` — 3-10 phrases (mix PL/EN if bilingual)
- `required-tools` — optional. Include if skill fails without specific tools (e.g. `mcp__google-workspace__gmail_search`)

---

## Required SKILL.md sections

```markdown
## When to use
When does this skill fit? What trigger conditions make it the right choice vs another skill?

## Tools at your disposal
Enumerate tools/MCPs the skill calls. If none beyond core Claude Code tools, say so.

## Pattern(s)
The playbook. Numbered steps. Reference specific tool calls, file paths, output formats.
Most skills have 1-4 patterns (e.g. morning / weekly / on-demand variants).

## Output standards
Where does output go? What filename convention? What frontmatter does the written file need?
Default: `_workspace/{YYYY-MM}/w{N}/{skill-id}-{YYYY-MM-DD}.md`

## Edge cases
What fails gracefully? What errors surface to user? What's the fallback when data missing?

## Not in scope
What does this skill explicitly NOT do? Guards against scope creep and misuse.
```

Optional but appreciated sections: **Examples**, **Motivation**, **Troubleshooting**.

---

## MC methodology compliance checklist

Check each before opening PR:

- [ ] **Output paths follow `_workspace/{YYYY-MM}/w{N}/` pattern** (not vault root, not `_transcripts/`)
- [ ] **Uses wiki-links `[[]]`** for vault references (not raw markdown links to local files)
- [ ] **Respects frontmatter standards** — `updated:` + `status:` + `cadence:` when modifying modules
- [ ] **Privacy discipline** — skill never logs: email bodies, subject lines, tokens, API keys, PII
- [ ] **Multi-account aware** (if using Google Workspace MCP) — always passes `account` param explicitly when working across boundaries
- [ ] **Reads before writes** — verifies target file exists + reads current content before overwriting
- [ ] **Autonomous by default** — minimize user prompts. Only ask when ambiguous / destructive / edge case
- [ ] **Dry-run supported** (for skills that write) — `--dry-run` flag shows what would change without doing it

---

## Required metadata in `registry.json`

New fields (v2.1+) needed per skill entry:

```jsonc
{
  "id": "skill-id",
  "label": "Human Label",                    // Max 24 chars; title case
  "description": "One sentence.",
  "version": "1.0.0",                         // Semver per skill
  "category": "analyze",                      // REQUIRED: one of analyze/capture/create/maintain/automate
  "tier": "core",                             // core | community (future)
  "files": ["SKILL.md"],                      // Paths relative to core/{id}/
  "size": "8KB",                              // Human estimate — updates on content changes
  "primary": false,                           // true = pre-checked in onboarding
  "type": "command",                          // OPTIONAL: "command" for slash-command-style (uses COMMAND.md not SKILL.md)
  "stars": 4,                                 // REQUIRED: 1-5 overall polish + utility
  "difficulty": "operator",                   // REQUIRED: learner | operator | expert
  "value": "high",                            // REQUIRED: low | medium | high (time saved vs setup cost)
  "scope": "universal",                       // REQUIRED: universal | native-mc
  "requires": []                              // REQUIRED: array of skill IDs or vault-setup flags (see below)
}
```

### Valid `category` values (mirrors main groups)

- **analyze** — read + understand (pulse, graph, vault-audit)
- **capture** — ingest external data (process-transcripts, whatsapp-digest, xdaily, gsuite-analysis)
- **create** — produce content (brief, copy, ideas, learned)
- **maintain** — vault housekeeping (reweave, graduate, sync, log)
- **automate** — tooling / meta (ralph-prompt, ralph-factory, overnight, skill-creator)

### Valid `requires` values

**Skill IDs** (dependencies on other skills):
- `"process-transcripts"` — skill's output is prerequisite
- Any other skill id from `registry.json`

**Setup flags** (vault / plugin / environment state):
- `"vault-structure"` — vault has `CLAUDE.md` + at least one `{num}_{name}/{num}_{name}_index.md`
- `"gsuite-connected"` — Google Workspace MCP configured (`~/.modular-context/mcp-google/accounts-index.json` exists)
- `"whatsapp-macos"` — macOS with WhatsApp.app installed
- `"git-initialized"` — vault is a git repo (for commit-based skills)
- `"python3"` — Python 3 available in PATH (for skills with scripts)

### Rating guidance

**Stars:**
- ⭐ concept only, barely tested
- ⭐⭐ basic impl, rough edges
- ⭐⭐⭐ polished, several runs, edge cases handled
- ⭐⭐⭐⭐ proven in production workflow
- ⭐⭐⭐⭐⭐ flagship, indispensable, heavily used

**Difficulty:**
- `learner` — runs out of box in fresh Obsidian vault
- `operator` — requires vault conventions + ~1 dependency
- `expert` — multi-system + OAuth / API config / native tools

**Value:**
- `low` — nice-to-have, saves < 15 min
- `medium` — saves 15-60 min per use
- `high` — saves 1h+ OR unlocks workflow otherwise impossible

---

## PR checklist

Before opening PR:

1. [ ] SKILL.md / COMMAND.md has required frontmatter
2. [ ] All 6 required sections present (When to use / Tools / Pattern / Output / Edge cases / Not in scope)
3. [ ] MC methodology compliance checklist passes (8 items above)
4. [ ] Registry entry has all required fields (stars, difficulty, value, scope, requires, category)
5. [ ] Ratings honest (don't inflate)
6. [ ] No leaked secrets / tokens / PII in skill content
7. [ ] Triggers are unique enough to not collide with other skills
8. [ ] Tested manually in your own vault (describe test in PR body)

### Optional but appreciated

- **GIF / screenshot** of skill in action (embed in PR body, not in repo)
- **Example output file** for skills that write artifacts (as gist, not in repo)
- **Use-case motivation** — 1-paragraph why this belongs here vs user's local vault

---

## What we reject

- Skills that duplicate existing ones without clear differentiation
- Skills that require proprietary / paid services without clear value differential
- Skills that send data to third parties without user consent / explicit warning
- Skills that log sensitive content to terminal (even once — see Privacy discipline)
- Prompts that are "copy-paste templates" (a skill is a playbook, not a template)
- Skills that hardcode personal names, project names, private keys

---

## Governance

- **Merge authority:** repo maintainer reviews + merges
- **Validation:** GitHub Action runs basic schema check on PR (light-touch, reports not blocks)
- **Deep validation:** use the **skill-validator** admin skill (lives in maintainer's vault, not this repo) for pre-merge compliance check
- **Semver per skill:** bump `version` in registry when changing SKILL.md body (patch for fixes, minor for new patterns, major for breaking pattern changes)
- **Deprecation:** we don't delete skills — move to `core/archived/{id}/` + mark `tier: "archived"` in registry

---

## Example PR template

```markdown
## Skill: `{skill-id}` — {label}

**Category:** analyze / capture / create / maintain / automate
**Stars:** ⭐⭐⭐⭐
**Difficulty:** operator
**Value:** high

### What it does
One paragraph.

### How I tested
1. Ran in my vault with {state}
2. Invoked via {trigger}
3. Verified output at `_workspace/...`

### MC methodology compliance
- [x] Output to `_workspace/`
- [x] Wiki-links
- [x] Privacy
- [x] Multi-account (N/A — no Google tools used)

### Rationale for ratings
Stars: {why}. Difficulty: {why}. Value: {why}.
```
