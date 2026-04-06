# Modular Context Skills

Skill library for [Modular Context](https://github.com/klemensgc/modular-context-obsidian-plugin) — the AI-native knowledge terminal for Obsidian.

## What are skills?

Skills are structured prompts that give Claude Code specialized capabilities. Each skill is a `SKILL.md` file (+ optional references) that lives in your vault's `.claude/skills/` folder. When you type `/{skill-name}` in Claude Code, it reads the skill file and executes the workflow.

## Installing skills

### Via the plugin (recommended)

The Modular Context plugin includes a **Skill Marketplace** — browse, install, and update skills directly from the Obsidian sidebar. Skills are installed automatically on first use.

### Manual installation

1. Download the skill folder (e.g., `core/pulse/`)
2. Copy it to your vault: `.claude/skills/pulse/`
3. Use it in Claude Code: `/pulse`

## Available skills

### Core skills (curated by klemensgc)

| Skill | Category | Description |
|-------|----------|-------------|
| **Pulse** | Analysis | CEO Pulse — vault scan, structured briefing, decision questions, next-session prompts |
| **Brief** | Creation | PDF briefs, one-pagers, spec sheets — content → design → HTML → PDF pipeline |
| **Ingest Data** | Workflow | Process sources — categorize, extract insights, update wiki modules |
| **Log** | Workflow | Close work sessions — session log, logical commits, push workflow |
| **Ideas** | Ideation | Generate ideas using 6 triggers grounded in your vault context |
| **Graph** | Analysis | Knowledge graph analysis — orphans, clusters, staleness heatmap |
| **Vault Audit** | Analysis | Find broken links, naming issues, missing indices, orphaned files |
| **Graduate** | Mining | Extract buried transcript ideas into standalone modules |
| **Reweave** | Workflow | Cascade-update stale or disconnected modules |
| **Copy** | Creation | Brand-aligned copy — ads, emails, pitch blurbs, AI prompts |
| **Learned** | Creation | Turn learnings into polished "What I Learned" posts |
| **Weekly Learnings** | Analysis | Compile week's insights into operational summary |
| **X Daily** | Workflow | Thread X/Twitter posts into vault modules |
| **Sync** | Workflow | Synchronize knowledge between vaults |
| **Playscript** | Analysis | Strategic analysis through multi-persona framework |
| **Ralph Prompt** | Automation | Build structured prompts for autonomous loops |
| **Ralph Factory** | Automation | Generate 20 strategic prompts per run |
| **Overnight** | Automation | Chain autonomous loops for batch processing |
| **Tasklist** | Workflow | Transform weekly plans into session starters |
| **Skill Creator** | Automation | Interactive guide for building new skills |

### Community skills

Community-contributed skills live in the `community/` folder. Submit a PR to add yours!

## Contributing a skill

1. Fork this repo
2. Create your skill folder: `community/{your-skill-name}/SKILL.md`
3. Follow the [skill format](#skill-format) specification
4. Submit a PR with a description of what your skill does

### Skill format

```yaml
---
name: your-skill-name
description: |
  One-paragraph description of what the skill does.
  Use when: list 2-4 scenarios when this skill is useful.
  Trigger phrases: list 5-10 natural ways users might ask for this.
---

# Skill Title

Brief intro.

## Quick Start
(5-7 lines: happy path)

## Phase 1: ...
(Detailed steps)

## Troubleshooting
| Problem | Solution |
|---------|----------|
```

### Guidelines

- Skills must be **vault-agnostic** — no hardcoded file paths
- Keep `SKILL.md` under 500 lines for optimal Claude Code performance
- Include a `references/` folder for templates, examples, or scripts
- Test your skill in a fresh vault before submitting

## License

MIT
