# Modular Context Skills — Curated Library

> **24 opinionated Claude Code workflows** for Obsidian-native knowledge work. Stars rated. Prerequisites explicit. Install via plugin.

Designed for users of the [Modular Context plugin](https://github.com/klemensgc/modular-context-obsidian-plugin). Each skill is a self-contained playbook — not a tip, not a template.

---

## 🏢 The AI Company Stack

This library isn't a pile of tips — it's a **whole AI company stack** built on one workflow: your vault is the brain, Claude Code is the operator, and each layer plugs into the next.

| Layer | What it does | Skills |
|-------|--------------|--------|
| 🎙️ **Notetaker** | Turn raw transcripts, calls and tweets into structured, tagged knowledge | `process-transcripts`, `xdaily`, `graduate` |
| 🧠 **Self-healing Knowledge Base** | The vault keeps itself current — reweaves stale modules, fixes links, audits structure, syncs sibling vaults | `reweave`, `vault-audit`, `graph`, `sync`, `pulse` |
| 📡 **Communication layer** | One read across mail, WhatsApp and Google Workspace — what's happening and what belongs to you | `comms-review`, `whatsapp-digest`, `gsuite-analysis` |
| 📊 **CRM / ops** | Ready skills that connect to ClickUp — review your sales funnel and pull your weekly plan straight from the workspace | `clickup-review`, `review-core`, `tasklist` |
| 🕸️ **Orchestration** | Design multi-agent workflows for the work no single session finishes — topology, casting, adversarial gates, emitted script | `workflow-design` |

Each layer is independently useful; together they run a one-person company on autopilot.

---

## 📚 The Library

```
╔══════════════════════════════════════════════════════════════════════════════╗
║      🦀  MODULAR CONTEXT SKILLS v2.2 — 24 CURATED WORKFLOWS                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

 ┌───────────────┬───────────────┬───────────────┬───────────────┬───────────────┐
 │    CAPTURE    │    ANALYZE    │    CREATE     │   MAINTAIN    │   AUTOMATE    │
 │      (3)      │      (9)      │      (5)      │      (4)      │      (3)      │
 ├───────────────┼───────────────┼───────────────┼───────────────┼───────────────┤
 │  process- 🟡  │  pulse        │  brief        │  log          │  workflow- 🟡 │
 │  transcripts  │  ⭐⭐⭐⭐⭐   │  ⭐⭐⭐⭐⭐   │  ⭐⭐⭐⭐     │  design       │
 │  ⭐⭐⭐⭐⭐   │               │               │               │  ⭐⭐⭐⭐⭐   │
 │               │  vault-audit  │  ideas        │  reweave      │               │
 │  whatsapp- 🟡 │  ⭐⭐⭐⭐     │  ⭐⭐⭐⭐     │  ⭐⭐⭐⭐     │  skill-       │
 │  digest       │               │               │               │  creator      │
 │  ⭐⭐⭐⭐     │  graph        │  copy         │  graduate     │  ⭐⭐⭐       │
 │               │  ⭐⭐⭐⭐     │  ⭐⭐⭐⭐     │  ⭐⭐⭐⭐     │               │
 │  xdaily       │               │               │               │  review-core  │
 │  ⭐⭐⭐       │  weekly-learn │  learned      │  sync         │  ⭐⭐⭐       │
 │               │  ⭐⭐⭐⭐     │  ⭐⭐⭐       │  ⭐⭐⭐       │               │
 │               │               │               │               │               │
 │               │  playscript   │  tasklist     │               │               │
 │               │  ⭐⭐⭐⭐     │  ⭐⭐⭐⭐     │               │               │
 │               │               │               │               │               │
 │               │  gsuite- 🟡   │               │               │               │
 │               │  analysis     │               │               │               │
 │               │  ⭐⭐⭐⭐     │               │               │               │
 │               │               │               │               │               │
 │               │  skills-audit │               │               │               │
 │               │  ⭐⭐⭐⭐     │               │               │               │
 │               │               │               │               │               │
 │               │  clickup- 🟡  │               │               │               │
 │               │  review       │               │               │               │
 │               │  ⭐⭐⭐⭐     │               │               │               │
 │               │               │               │               │               │
 │               │  comms- 🟡    │               │               │               │
 │               │  review       │               │               │               │
 │               │  ⭐⭐⭐⭐⭐   │               │               │               │
 ├───────────────┼───────────────┼───────────────┼───────────────┼───────────────┤
 │ Ingest data   │ Understand +  │ Produce       │ Vault health  │ Meta tools    │
 │ into vault    │ summarize     │ content       │ + housekeeping│ + workflows   │
 └───────────────┴───────────────┴───────────────┴───────────────┴───────────────┘

   🟡 = pre-checked primary skill in plugin onboarding (6 total)
```

**Total:** 24 skills across 5 categories. Primary skills (🟡) auto-selected in onboarding. Others available via sidebar browse. Three Ralph-era automation skills were archived in v2.2 — see the **Archived** section below.

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ⭐ → ⭐⭐⭐⭐⭐ | Overall polish + utility (1 = concept, 5 = indispensable) |
| 🟡 | Primary skill — pre-checked during onboarding (6 total) |
| 🌐 | Universal — works in any Obsidian vault |
| 🏠 | Native to Modular Context — requires project folders + CLAUDE.md |
| 🔒 | Has prerequisites (other skills or vault setup) — plugin gates install |
| 🎓 L / 👷 O / 🧠 E | Difficulty: Learner / Operator / Expert |

---

## Quick start

**New install?** Enable the 6 primary skills (auto-checked in plugin onboarding). Run `skills-audit` for tailored recommendations on the rest.

**One-paragraph install:**
1. Install the [Modular Context plugin](https://github.com/klemensgc/modular-context-obsidian-plugin) via BRAT or manual.
2. Plugin auto-fetches this registry on load.
3. Pick skills in onboarding modal OR browse 5-category sidebar.
4. Primary skills 🟡 are pre-selected; everything else is opt-in.
5. Run **skills-audit** after install to see what's eligible, what's blocked, and what fits your setup.

---

## Skills by Category

### 📥 CAPTURE (3 skills) — ingest external data

| Skill | ⭐ | Difficulty | Scope | Requires | Purpose |
|-------|---|-----------|-------|----------|---------|
| **process-transcripts** 🟡 | ⭐⭐⭐⭐⭐ | 👷 O | 🏠 | `vault-structure` | Turn raw files (transcripts, notes, backlog) into categorized vault modules |
| **whatsapp-digest** 🟡 | ⭐⭐⭐⭐ | 🧠 E | 🏠 | `vault-structure` + `whatsapp-macos` | Mine WhatsApp groups → action items + blindspots + staleness |
| **xdaily** | ⭐⭐⭐ | 🎓 L | 🏠 | `vault-structure` | Thread X/Twitter posts into vault modules by project |

### 🔍 ANALYZE (9 skills) — understand vault + external

| Skill | ⭐ | Difficulty | Scope | Requires | Purpose |
|-------|---|-----------|-------|----------|---------|
| **pulse** | ⭐⭐⭐⭐⭐ | 👷 O | 🏠 | `vault-structure` | Deep vault scan → CEO briefing → 3 next-session prompts |
| **vault-audit** | ⭐⭐⭐⭐ | 👷 O | 🌐 | — | Broken links, naming inconsistencies, missing indices, orphans |
| **graph** | ⭐⭐⭐⭐ | 🧠 E | 🌐 | `python3` | Knowledge graph — clusters, bridges, staleness heatmap |
| **weekly-learnings** | ⭐⭐⭐⭐ | 👷 O | 🌐 | — | Aggregate session logs + module changes into week summary |
| **playscript** | ⭐⭐⭐⭐ | 🧠 E | 🏠 | `vault-structure` | 5-persona strategic analysis — surface cross-project plays |
| **gsuite-analysis** 🟡 | ⭐⭐⭐⭐ | 🧠 E | 🌐 | `gsuite-connected` | Full Google Workspace — inbox sweep, calendar gap, meeting prep (25 MCP tools) |
| **skills-audit** | ⭐⭐⭐⭐ | 🎓 L | 🌐 | — | Scan your library → 4-bucket report + contribution motivators |
| **clickup-review** 🟡 🔒 | ⭐⭐⭐⭐ | 👷 O | 🌐 | `clickup-connected` + `python3` + `review-core` | Sales-funnel review — count per stage, deals near close, stale leads, value sums |
| **comms-review** 🟡 🔒 | ⭐⭐⭐⭐⭐ | 🧠 E | 🌐 | `clickup-connected` + `whatsapp-macos` + `gsuite-connected` + `python3` + `review-core` | Cross-channel owner overview — ClickUp + WhatsApp + Gmail in one read |

### ✏️ CREATE (5 skills) — produce content

| Skill | ⭐ | Difficulty | Scope | Requires | Purpose |
|-------|---|-----------|-------|----------|---------|
| **brief** | ⭐⭐⭐⭐⭐ | 👷 O | 🌐 | `python3` | Polished PDFs: content → design brief → HTML → WeasyPrint |
| **ideas** | ⭐⭐⭐⭐ | 🎓 L | 🌐 | — | 6-trigger idea generation grounded in vault context |
| **copy** | ⭐⭐⭐⭐ | 🎓 L | 🌐 | — | Brand copy — ads, emails, pitches, prompts, recruitment posts |
| **learned** | ⭐⭐⭐ | 🎓 L | 🌐 | — | Polished "What I Learned" posts from session logs |
| **tasklist** | ⭐⭐⭐⭐ | 👷 O | 🏠 | `vault-structure` | Weekly plan → Claude Code session starters (objectives + context) |

### 🧹 MAINTAIN (4 skills) — vault housekeeping

| Skill | ⭐ | Difficulty | Scope | Requires | Purpose |
|-------|---|-----------|-------|----------|---------|
| **log** | ⭐⭐⭐⭐ | 🎓 L | 🌐 | `git-initialized` | Session close — log + logical commits + push workflow |
| **reweave** 🔒 | ⭐⭐⭐⭐ | 🧠 E | 🏠 | `vault-structure` + `process-transcripts` | Cascade-update stale modules, respect backward links |
| **graduate** 🔒 | ⭐⭐⭐⭐ | 👷 O | 🏠 | `vault-structure` + `process-transcripts` | Promote buried transcript ideas → standalone modules |
| **sync** | ⭐⭐⭐ | 🧠 E | 🏠 | `vault-structure` | Bi-directional vault sync (CEO brain ↔ secondary brain) |

### 🤖 AUTOMATE (3 skills) — meta-tools + orchestration

| Skill | ⭐ | Difficulty | Scope | Requires | Purpose |
|-------|---|-----------|-------|----------|---------|
| **workflow-design** 🟡 | ⭐⭐⭐⭐⭐ | 👷 O | 🌐 | `python3` | Design multi-agent workflows — priorities interview, topology pick, per-stage casting, adversarial gates, validated script |
| **skill-creator** | ⭐⭐⭐ | 👷 O | 🌐 | — | Interactive guide for building your own high-quality skills |
| **review-core** | ⭐⭐⭐ | 🧠 E | 🌐 | `clickup-connected` + `python3` | Internal library for the `*-review` family — not user-triggered, installed as a dependency |

### 🗄️ Archived (no longer shipped)

Removed from `skills[]` in registry v2.2 (2026-08-06) and recorded in the registry's top-level `archived[]`. The folders stay in `core/` with a deprecation note at the top of `SKILL.md`, so existing installs keep working — but the plugin no longer offers them.

| Skill | Archived | Reason |
|-------|----------|--------|
| **ralph-prompt** | 2026-08-06 | Superseded by native Claude Code workflow orchestration — see `workflow-design` |
| **ralph-factory** | 2026-08-06 | Superseded by native Claude Code workflow orchestration — see `workflow-design` |
| **overnight** | 2026-08-06 | Superseded by native Claude Code workflow orchestration — see `workflow-design` |

---

## Getting started — recommendation paths

**First time? Pick one path:**

### Path A — "I want to digitize my daily ops" (fastest payoff)
1. `process-transcripts` — capture raw files into vault
2. `gsuite-analysis` — inbox + calendar awareness
3. `pulse` — weekly briefing

### Path B — "I want to understand my existing vault" (analytical)
1. `vault-audit` — structural health
2. `graph` — dependency + staleness heatmap
3. `playscript` — strategic cross-project angles

### Path C — "I write a lot and want polish" (content ops)
1. `brief` — PDF pipeline
2. `copy` — on-brand short-form content
3. `weekly-learnings` — reflection rhythm

**Anytime:** run `skills-audit` for a personalized 4-bucket view.

---

## For new team members (e.g. Czarek)

**You just joined and want to get productive?**

1. **Install the Modular Context plugin** ([guide](https://github.com/klemensgc/modular-context-obsidian-plugin#install))
2. **Enable primary skills** — they're pre-checked in onboarding (Synthesise Files, Workflow Design, WhatsApp Digest, Gmail + G-Suite, ClickUp Review, Comms Review)
3. **Run `skills-audit`** → see which additional skills fit your role and vault state
4. **Pick 1-2 per week** — don't overload. Each skill is a playbook to learn, not just a button to press.
5. **Ask in the team channel** when stuck — the `description` field is a hint, the `SKILL.md` body is the manual.

**You'll go from 0 → productive in about 1 week** following this path.

---

## Install / Uninstall

### Via plugin (recommended)

- **Install a skill:** Plugin sidebar → browse categories → click skill → Install. Prerequisites are auto-checked; install button is disabled (with tooltip) if prereqs missing.
- **Uninstall:** Sidebar → skill entry → right-click → Uninstall. Removes from `.obsidian/plugins/modular-context/data.json`; files cached locally can be manually purged.

### Manual (for power users)

1. `git clone https://github.com/klemensgc/modular-context-skills`
2. Pick a skill folder `core/{id}/`
3. Drop `SKILL.md` (or `COMMAND.md` for slash-command-type) into your vault's `.claude/skills/{id}/`
4. Reload Claude Code session → new skill available

---

## Your skills library

Once you have 5+ skills installed, run **`skills-audit`** periodically.

What you'll get:
- ✅ What you have + what's healthy
- 🟡 What's eligible but not installed (recommendations ranked by value)
- 🔴 What's blocked by missing prereqs (with unblock steps)
- ⚪ What's aspirational (major setup required)
- 🎁 Contribution opportunities (skills you've customized, skills you use heavily that haven't been updated)

Writes report to `_workspace/{YYYY-MM}/w{N}/skills-audit-{date}.md` for reference.

---

## Contributing

**Thinking of adding a new skill?** You're welcome. This is an opinionated library — quality > quantity. Before PR:

### 1. Read [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Required frontmatter + sections
- MC methodology compliance checklist (8 items)
- Registry metadata schema

### 2. Use **`skill-validator`** locally before PR
The maintainer runs this validator on every incoming PR. Running it yourself first catches ~80% of issues.

```
Invoke in Claude Code session:
> validate skill _claude/skills/your-new-skill/SKILL.md
```

Validator checks 5 layers: frontmatter schema, required sections, MC methodology, rating sanity, security anti-patterns.

### 3. PR checklist
- [ ] SKILL.md / COMMAND.md complete per CONTRIBUTING.md
- [ ] Registry entry has all required fields (stars, difficulty, value, scope, requires, category)
- [ ] Tested manually (describe test in PR body)
- [ ] No secrets / tokens / PII
- [ ] Triggers don't collide with existing skills
- [ ] Ran `skill-validator` locally — 0 critical issues

### 4. PR template
See [CONTRIBUTING.md](CONTRIBUTING.md#example-pr-template).

---

## Repo structure

```
modular-context-skills/
├── registry.json                   (source of truth — fetched by plugin)
├── README.md                       (you are here)
├── CONTRIBUTING.md                 (standards for contributors)
├── core/
│   ├── {skill-id}/
│   │   ├── SKILL.md                (or COMMAND.md for slash-commands)
│   │   ├── references/             (optional — templates, examples, personas)
│   │   └── scripts/                (optional — Python helpers)
│   └── ... (24 shipped + 3 archived folders kept for existing installs)
└── .github/workflows/
    └── validate-skills.yml         (light-touch CI: JSON schema + folder presence)
```

---

## Status + versioning

- **Registry version:** `2.2.0` (schema v2 — stars/difficulty/value/scope/requires, categories analyze/capture/create/maintain/automate; v2.2 adds `workflow-design` and the top-level `archived[]` array)
- **Per-skill version:** independent semver; bump on SKILL.md content changes (patch for fixes, minor for new patterns, major for breaking pattern changes)
- **Tier:** all 24 shipped skills in `core/` (curated by maintainer). Future: `community/` tier for user-contributed non-core skills.
- **Sync:** plugin fetches registry + skill content from GitHub raw on load (5 min cache); push to `main` → reachable ~5 min later.

---

## License

MIT © klemensgc / receptionOS. Skills use MIT unless noted otherwise in their individual `SKILL.md` frontmatter.
