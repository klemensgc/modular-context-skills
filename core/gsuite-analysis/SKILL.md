---
name: gsuite-analysis
description: Gmail + Calendar analysis playbook — orchestrates MCP Google Workspace tools (gmail_search, gmail_modify_labels, calendar_freebusy, etc.) for inbox sweeps, stale follow-ups, calendar gap analysis, meeting prep. Writes insights to vault, does not auto-send.
triggers: ["gmail", "gcal", "gsuite", "gmail analysis", "calendar analysis", "inbox sweep", "meeting prep", "free time", "catch up", "stale threads"]
required-tools: ["mcp__google-workspace__gmail_search", "mcp__google-workspace__gmail_modify_labels", "mcp__google-workspace__gmail_draft", "mcp__google-workspace__gmail_send", "mcp__google-workspace__calendar_list_calendars", "mcp__google-workspace__calendar_list_events", "mcp__google-workspace__calendar_create_event", "mcp__google-workspace__calendar_update_event", "mcp__google-workspace__calendar_delete_event", "mcp__google-workspace__calendar_freebusy"]
---

# Gmail + Calendar Analysis

Playbook using the Modular Context G-Suite MCP tools. Call this skill when you want to understand or act on your inbox + calendar state — NOT for sending emails blind or auto-scheduling.

**Multi-account aware.** Every MCP tool accepts optional `account` parameter (email). When working across multiple Google accounts (e.g., `apollo@receptionos.com` + `k@receptionos.com` + `k@fundacjaedisona.pl`), always pass `account` explicitly. Omit `account` to use primary.

**Privacy discipline:**
- NEVER log raw email bodies, subject lines, or message IDs in terminal output
- Write analysis/insights to vault files (which are gitignored for sensitive content areas)
- Only surface aggregate summaries to the user in chat

---

## Tools at your disposal (10)

### Gmail (4)
- `gmail_search(query, maxResults?, includeBody?, account?)` — Gmail search syntax (`is:unread`, `from:X`, `after:YYYY-MM-DD`, `has:attachment`, etc.)
- `gmail_draft(to[], cc?, subject, body, replyToThreadId?, account?)` — create draft (user sends from Gmail)
- `gmail_send(to[], cc?, bcc?, subject, body, replyToThreadId?, account?)` — real send (use sparingly; prefer draft)
- `gmail_modify_labels(messageId, addLabels?, removeLabels?, account?)` — presets: INBOX (remove = archive), UNREAD (remove = mark-read), STARRED, IMPORTANT, SPAM, TRASH. Custom labels supported by name.

### Calendar (6)
- `calendar_list_calendars(account?)` — all calendars user has access to. **Required first call** if operating on non-primary.
- `calendar_list_events(timeMin, timeMax, calendarId?, maxResults?, account?)` — events in range
- `calendar_create_event({summary, start, end, attendees?, location?, sendUpdates?, calendarId?, account?})` — `sendUpdates: "none"` default
- `calendar_update_event(eventId, {summary?, start?, end?, ...}, sendUpdates?, calendarId?, account?)` — patch existing
- `calendar_delete_event(eventId, calendarId?, sendUpdates?, account?)` — delete
- `calendar_freebusy(timeMin, timeMax, calendars?[], account?)` — busy ranges per calendar

---

## When to use this skill

| Situation | Pattern |
|-----------|---------|
| Morning routine (30 min) | Pattern 1: Morning Inbox Sweep |
| Friday review / week wrap | Pattern 2: Stale Thread Follow-up |
| Planning next week | Pattern 3: Calendar Gap Analysis |
| 15 min before meeting | Pattern 4: Meeting Prep |

Pick one pattern or combine. Each pattern ends with a vault artifact the user can review and act on.

---

## Pattern 1 — Morning Inbox Sweep

**Goal:** triage unread mail, surface what matters, draft top 3 replies. User reviews drafts in Gmail before sending.

### Steps

1. **Discover accounts** if user hasn't specified:
   ```
   What accounts should I sweep? (default: primary)
   ```
   If user has multiple accounts, offer to loop through all (one at a time, separate analyses).

2. **Fetch unread from last 24h** per account:
   ```
   gmail_search(query: "is:unread newer_than:1d", maxResults: 50, account: "<email>")
   ```

3. **Group by sender domain + thread topic** in your analysis. Categorize each as:
   - **Important** — known key people (check `_culture/team/team-roster.md` or equivalent), explicit @mentions, response expected <24h
   - **Newsletter/automated** — sender signature pattern (`no-reply`, `@newsletter`, `@mailer`, etc.) — candidate for batch archive
   - **FYI / non-urgent** — everything else

4. **Draft replies** for top 3 Important items:
   ```
   gmail_draft(to: ["<sender>"], subject: "Re: <thread>", body: "<draft>", replyToThreadId: "<threadId>", account: "<email>")
   ```
   Draft body should be 2-3 sentences. User polishes in Gmail UI.

5. **Write vault artifact:** `_workspace/{YYYY-MM}/w{N}/inbox-sweep-{YYYY-MM-DD}-{account}.md`
   Format:
   ```markdown
   ---
   title: Inbox sweep — {account} — {YYYY-MM-DD}
   updated: {YYYY-MM-DD}
   status: active
   source: {account}
   ---
   # Inbox sweep {account} {date}

   ## Important ({count})
   - {Sender} — {1-line summary} — [draft webUrl]

   ## Newsletter/automated ({count})
   - {Sender}: {count} messages — consider batch archive via gmail_modify_labels

   ## FYI ({count})
   - {Sender}: {1-line}

   ## Drafts created
   - [{subject}]({webUrl}) → for review + send
   ```

6. **Offer batch archive** for Newsletter category: "Archive all {N} newsletter messages? [y/N]"
   If user accepts:
   ```
   for each messageId in newsletter_list:
     gmail_modify_labels(messageId, removeLabels: ["INBOX", "UNREAD"], account: "<email>")
   ```

---

## Pattern 2 — Stale Thread Follow-up

**Goal:** find conversations where user committed to follow up but hasn't, surface for action.

### Steps

1. **Identify key-people scope.** Ask user for list of emails (or read `_culture/team/team-roster.md`, pipeline files, etc.).

2. **Per person, search last reply from them + last reply from user:**
   ```
   gmail_search(query: "from:<person> older_than:7d newer_than:60d", maxResults: 20, account: "<email>")
   gmail_search(query: "to:<person> older_than:7d newer_than:60d", maxResults: 20, account: "<email>")
   ```

3. **Stale detection heuristic:**
   - Last message in thread FROM them, user has not replied → **stale, your turn**
   - Last message in thread FROM user, no reply for 7+ days → **stale, nudge them**
   - Reciprocal replies within 7 days → healthy, skip

4. **Write vault artifact:** `_workspace/{YYYY-MM}/w{N}/stale-threads-{YYYY-MM-DD}.md`
   ```markdown
   ---
   title: Stale threads — {YYYY-MM-DD}
   updated: {YYYY-MM-DD}
   status: active
   ---
   # Stale threads {date}

   ## Your turn ({count})
   - {Person} — last message from them {days} days ago — {thread subject} — [thread link]

   ## Nudge them ({count})
   - {Person} — you messaged {days} days ago, no reply — {thread subject} — [thread link]
   ```

5. **Offer to draft nudges** for "Nudge them" list:
   ```
   For each stale thread:
     gmail_draft(to: [person], subject: "Following up: {subject}", body: "Quick nudge on {topic} — any update on your end?", replyToThreadId: threadId, account: <email>)
   ```

---

## Pattern 3 — Calendar Gap Analysis

**Goal:** find focus blocks (unscheduled time ≥ 90 min) in the next 7 days across user's calendars.

### Steps

1. **Discover calendars** (if user has multiple accounts or shared calendars):
   ```
   For each account:
     calendar_list_calendars(account: "<email>")
   ```
   Ask user which to include. Default: primary of each account.

2. **Query freebusy for next 7 days, work hours (9-17 local):**
   ```
   calendar_freebusy(
     timeMin: <today 9:00>,
     timeMax: <today+7d 17:00>,
     calendars: ["primary", "<shared-calendar-id>"],
     account: "<email>"
   )
   ```
   (Iterate per account if user has multiple.)

3. **Compute free windows:** for each day, invert `busy` ranges against 9-17 → free windows. Keep only windows ≥ 90 min.

4. **Write vault artifact:** `_workspace/{YYYY-MM}/w{N}/focus-blocks-{YYYY-MM-DD}.md`
   ```markdown
   ---
   title: Focus blocks — {YYYY-MM-DD} → {YYYY-MM-DD+7d}
   updated: {YYYY-MM-DD}
   status: active
   ---
   # Focus blocks next 7d

   ## {Day 1}
   - 10:00-12:30 (2.5h) — {account} primary
   - 14:00-16:00 (2h) — {account} primary

   ## {Day 2}
   - 09:00-11:00 (2h) — both calendars free
   ...
   ```

5. **Offer to block** 1-2 focus blocks as "Focus work" calendar events:
   ```
   calendar_create_event(
     summary: "Focus block",
     start: "<ISO>",
     end: "<ISO>",
     sendUpdates: "none",
     account: "<email>"
   )
   ```

---

## Pattern 4 — Meeting Prep

**Goal:** before a scheduled meeting, gather context on attendees + recent email history with them. Write pre-meeting briefing.

### Steps

1. **Fetch next meetings** within specified window (default: next 48h):
   ```
   calendar_list_events(timeMin: <now>, timeMax: <now+48h>, maxResults: 10, account: "<email>")
   ```

2. **For each meeting, extract attendees** (excluding the user themselves).

3. **For each external attendee, fetch recent email history:**
   ```
   gmail_search(query: "from:<attendee> OR to:<attendee> newer_than:30d", maxResults: 10, includeBody: false, account: "<email>")
   ```

4. **Check vault** for matching modules — e.g., `2_apolonia/3-team/`, pipeline entries, roster. Read 1-2 relevant modules (Claude's Read tool, not MCP).

5. **Write briefing per meeting:** `_workspace/{YYYY-MM}/w{N}/meeting-prep-{YYYY-MM-DD}-{summary-slug}.md`
   ```markdown
   ---
   title: Meeting prep — {event summary} — {YYYY-MM-DD HH:MM}
   updated: {YYYY-MM-DD}
   status: active
   source: {account} calendar + Gmail history
   ---
   # Meeting prep: {event summary}

   ## When + where
   {start} → {end} | {location or meetingLink}

   ## Attendees
   - {name} ({email}) — {role from vault if known}

   ## Recent email context ({N} threads)
   - {YYYY-MM-DD}: {thread subject} — 1-line summary

   ## Relevant vault context
   - [[2_apolonia/3-team/...]] — {1-line}
   - [[1_receptionOS/4-go-to-market/pipeline]] — {1-line if pipeline match}

   ## Suggested agenda
   1. {opener — based on last thread}
   2. {main topic — based on pipeline state}
   3. {action items — based on open threads}

   ## Questions to ask
   - {based on gaps in what you know}
   ```

---

## Output standards

Every pattern writes ONE artifact per invocation to `_workspace/{YYYY-MM}/w{N}/`.

Frontmatter required fields:
- `title` — descriptive
- `updated` — today's date
- `status: active`
- `source` — which account(s) + which tools used (for audit trail)

Never commit these artifacts blindly — they may contain sensitive email excerpts. User's responsibility to move/delete.

---

## Edge cases

- **OAuth scope missing** → MCP returns `PERMISSION_DENIED`. Tell user: run `Google Workspace: Reconnect (upgrade scopes)` command.
- **Account not found** → user asked for account not connected. Tell user: run `Google Workspace: Add another account`.
- **Rate limited (429)** → MCP returns `RATE_LIMITED`. Back off 60s, retry once. If still rate limited, abort and write partial artifact.
- **Empty result sets** → don't fabricate content. State "no results in this window" in artifact.
- **Ambiguous user request** (e.g. "check my emails") → ask which account + which pattern (sweep / stale / prep), don't guess.

---

## Not in scope (DO NOT do)

- Don't bulk-send emails without explicit per-recipient confirmation
- Don't delete emails (gmail_modify_labels removing INBOX is archive, not delete — never add TRASH automatically)
- Don't create calendar events that email attendees — `sendUpdates: "none"` unless user explicitly requests `"all"`
- Don't modify events other people own unless user explicitly asks
- Don't reveal any account's emails to another account's context (account scoping is strict)
