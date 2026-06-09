---
name: comms-review
description: |
  Cross-channel owner overview — "how is the company doing" + "what belongs to me". Aggregates ClickUp
  (your tasks across every workspace + sales funnel + the current planning week), WhatsApp (groups) and
  Gmail (inbox) into one report. Surfaces owner action items, staleness and what needs a reply.
  Read-only — sends and changes nothing without approval.
  Use when: you want one overview of every channel, to check nothing is waiting on you, a daily/weekly
  owner review, "what's hanging", "did I miss anything".
  Trigger phrases: "comms review", "owner review", "what belongs to me", "what's hanging", "did I miss anything", "what needs a reply", "company review", "what's on my plate"
---

# Comms Review — cross-channel owner overview

One overview: **ClickUp + WhatsApp + Gmail** → "how is the company doing" + "what belongs to me to do". Read-only. Built on `review-core` (lib) and reuses `whatsapp-digest` + `gsuite-analysis`.

Optional arg: lookback days for WhatsApp/Gmail (default 7). `comms review 14` → 14 days.

Requires: `review-core`, `whatsapp-digest` (macOS), Google Workspace MCP (`gsuite-connected`).

---

## Phase 0 — Extract (3 channels)

### A. ClickUp (script)
```bash
python3 .claude/skills/review-core/lib/clickup_adapter.py --json --today {YYYY-MM-DD}
```
Gives: `my_tasks` (per workspace), `planning_week` (newest `W{N}` from the Planning doc, if configured), `funnel` (CRM headline, if configured).

### B. WhatsApp (script — reuse whatsapp-digest)
```bash
python3 .claude/skills/whatsapp-digest/scripts/extract.py --groups-only --days {N} --output /tmp/comms_wa.json
```
Then read `/tmp/comms_wa.json`. Group routing → `.claude/skills/whatsapp-digest/references/group-routing.md`.

### C. Gmail (MCP — the agent runs this, NOT a script)
Call the Google Workspace MCP (gmail search):
- `is:unread newer_than:{N}d` — unread
- `is:important newer_than:{N}d` — important
- (optional) threads where the last message is from someone else (awaiting your reply)
Extract: sender, subject, date, one-line ask.

---

## Phase 1 — Normalize

Map everything to the `Item` model (`review-core/lib/model.py`): source / kind / title / owner / counterpart / due / status / priority / url / container. ClickUp is already normalized by the adapter; the agent maps WhatsApp and Gmail.

## Phase 2 — Ownership (LLM classification — the agent)

For each item decide `mine` (is this a task/request **for me**):
- ClickUp: assignee = me → `mine=true` (certain).
- WhatsApp/Gmail: **judgment** — is someone asking you to act / waiting on your reply / decision. These are **candidates, not verdicts** — flag uncertain ones as "⚠ to confirm".

Never silently drop anything — show uncertain items separately.

## Phase 3 — Report

Two sections:

### 🏢 How is the company doing (per-channel health)
- ClickUp: open tasks per workspace, current planning week (main quest / side quests), funnel — who's near close.
- WhatsApp: active groups, hot threads, group action items.
- Gmail: unread/important count, threads waiting on you.

### ✅ On your plate (owned, deduped, prioritized)
One list of owner action items across all channels, sorted: overdue → due today/soon → high priority → rest. Each: `[channel] title — counterpart — due/status — link`. Dedup when the same thing appears in two channels (e.g. a ClickUp task + a WhatsApp ping about it).

### ⏳ Staleness / flags
Deals/threads/tasks with no movement past a threshold; mismatches (e.g. the planning mentions X but there's no ClickUp task for it).

## Rules

- **Read-only.** Don't send mail, change tasks, or reply on WhatsApp without explicit approval. You may **propose** actions — wait for OK.
- **Privacy:** extracts (`/tmp/comms_wa.json`, Gmail dumps) stay in `/tmp`, never committed.
- ClickUp "remind me" = due_date + assignee (the Reminder endpoint is unreliable).

## Troubleshooting

| Issue | Fix |
|---|---|
| ClickUp 401 | Token expired — refresh credentials.json |
| WhatsApp empty | WhatsApp Desktop not signed in / terminal lacks Full Disk Access (macOS) |
| Gmail MCP missing | Google Workspace MCP not connected — run auth or skip the Gmail leg (note it in the report) |
| Planning empty | check `planning_doc_id`; v3 Docs is slow → retry |
