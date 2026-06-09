---
name: review-core
description: |
  INTERNAL shared library (do not trigger directly) — the shared core for the *-review skill family:
  a ClickUp client (multi-workspace my-tasks, funnel, v3 Docs / planning), a normalized Item model,
  channel adapters and a report renderer. Used by clickup-review, comms-review and tasklist (planning auto-read).
  Use when: NOT a user skill. Imported by other skills via sys.path.
  Trigger phrases: (none — internal core)
---

# review-core (internal shared library)

Shared core for the `*-review` family. **Not a user skill** — other skills import its `lib/`.

## Contents

```
lib/
  clickup_client.py   ClickUp() : auth+retry(90s), get_my_tasks(team)/all_teams,
                      get_list_tasks, list_statuses, doc_pages (v3), latest_planning_week,
                      + writes (create/update/set_field/comment) — ONLY after user approval
  model.py            Item (source/kind/title/owner/counterpart/due/status/priority/url/mine)
                      + from_clickup_task()
  clickup_adapter.py  gather() : my-tasks across workspaces + newest planning week + funnel headline;
                      health_lines(); CLI (--json / --today)
references/
  credentials.example.json
```

## Setup (one-time)

1. Get a ClickUp **personal API token**: ClickUp → Settings → Apps → API Token.
2. `mkdir -p ~/.modular-context/clickup`
3. Copy `references/credentials.example.json` → `~/.modular-context/clickup/credentials.json`, fill in:
   - `api_token`, `me_user_id` (your ClickUp user id — `GET /api/v2/user`)
   - `teams` — map of name → workspace id (`GET /api/v2/team`)
   - `crm_list_id` — your sales/CRM list (optional, for clickup-review)
   - `planning_doc_id` — a ClickUp Doc with weekly `W{N}` pages (optional, for tasklist auto-read)
   - `field_ids.estimated_value`, `field_ids.last_outreach_date` (optional custom fields)
4. `chmod 600 ~/.modular-context/clickup/credentials.json`. **Never commit it.**

## How to import (from another skill)

```python
import sys; sys.path.insert(0, '.claude/skills/review-core/lib')
from clickup_client import ClickUp
from clickup_adapter import gather, health_lines
cu = ClickUp()
data = gather(cu)                 # ClickUp cross-section
week = cu.latest_planning_week()  # newest weekly page from the Planning doc
```

## Notes

- **Cross-workspace my-tasks:** `GET /team/{id}/task?assignees[]=me` returns all your tasks across every list in a workspace — the backbone of "what's on my plate".
- **Planning** can be a ClickUp **Doc** (not a list). `latest_planning_week()` reads the doc via the v3 Docs API and returns the **newest** `W{N}` page (highest page-id suffix). The v3 Docs API works with a personal token but is slow → retry 90s.
- **Reminders:** the ClickUp public Reminder endpoint is unreliable (500s) — to "remind", set a task `due_date` + assignee instead.

## Hard rule

Read-first. Write functions exist but the review skills call them **only after explicit user approval**. Never write to the CRM autonomously.
