---
name: clickup-review
description: |
  Review a CRM / sales-funnel list in ClickUp — reports count per stage, deals near close, stale leads
  (by a last-outreach custom field) and value sums. Stages are read live from the list, so it works with
  any funnel. Read-only by default; writes only after you approve. Cross-references findings with your vault.
  Use when: you want a snapshot of your sales funnel, how many deals at each stage, which leads went stale,
  prep numbers for a forecast or a traction snapshot, or check whether your notes match the CRM.
  Trigger phrases: "clickup review", "review clickup", "funnel review", "pipeline review", "crm review", "how many deals at each stage", "stale leads", "sales funnel state"
---

# ClickUp Review

Reviews a CRM / sales-funnel list in ClickUp and reports its state. **Read-only by default.** Built on `review-core` (shared lib). Requires `review-core` + a configured `~/.modular-context/clickup/credentials.json` (see review-core setup).

## Quick start

```bash
python3 .claude/skills/clickup-review/scripts/audit.py
```

Outputs: count + value sum per stage → deals near close → stale leads → data-quality note. Default stale threshold 14 days. `--json` for raw data, `--stale N` to change the threshold, `--today YYYY-MM-DD` to pin "today".

After running: interpret the result, cross-reference with your vault (below), present a readable summary — don't just dump the table.

## Config

Set `crm_list_id` (your funnel list) in credentials.json. Optional custom fields: `field_ids.estimated_value` (value sums), `field_ids.last_outreach_date` (stale detection). Stages are derived live from the list definition (orderindex) — `done`/`closed` types are treated as closed.

## Cross-reference with your vault (recommended)

If your CRM is maintained live (e.g. by a sales rep) it may be fresher than your notes. After the review, compare:
1. **Deals at a "verbal yes / closing" stage** vs the stage in your vault deal sheets — if the CRM is ahead, propose updating the note.
2. **"Sold/won" in ClickUp** vs your live-customer list — these may be different universes (a new-lead funnel won't contain legacy customers). Don't equate "sold count" with "live count".
3. **Stale leads** — deals in active stages past the threshold; check against your follow-up scheduler.

## Gotchas

| Issue | Handling |
|---|---|
| Value/last-outreach fields empty | Optional fields. If unused, sums are 0 and stale = "dates not set" — not an error. |
| Task names = domains vs friendly names | Match loosely (domain ↔ name). |
| "Sold" count far below your live-customer count | Different universe (the funnel ≠ full roster). Not a bug. |
| API timeout | Client retries 3×/60-90s. If it still fails, rerun. |

## Writing to ClickUp (only on explicit approval)

Read-only by default. To sync (move a stage, set a value), use the `review-core` client write methods (`update_task`, `set_field`, `comment`) — but **show a diff and ask first**. Never modify the CRM autonomously.

## Troubleshooting

| Issue | Fix |
|---|---|
| 401 Unauthorized | Token expired — regenerate in ClickUp → Settings → Apps and update credentials.json |
| Empty list / 0 tasks | Wrong `crm_list_id` or token lacks access to that space |
| Missing credentials | Copy review-core/references/credentials.example.json to ~/.modular-context/clickup/ |
