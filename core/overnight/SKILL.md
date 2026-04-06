---
name: overnight
description: |
  Plans and executes chained Ralph loops as ONE continuous loop with a queue file.
  Interviews user about priorities, scans repo, enters plan mode for approval,
  then runs a SINGLE Ralph loop that processes prompts from a queue file sequentially.
  Use when: setting up work for the night, wanting to chain Ralph prompts, planning overnight
  automation, preparing autonomous work while you sleep, chain prompts.
  Trigger phrases: "overnight", "night run", "run overnight", "chain ralph", "set up for tonight",
  "plan na noc", "przygotuj na noc", "nocny run", "ralph chain", "night work", "chain prompts"
---

# Overnight — Queue-Driven Single Loop

Plans and executes chained Ralph prompts as ONE continuous Ralph loop driven by a queue file.

---

## Architecture: Queue-Driven Single Loop

> **CRITICAL DESIGN DECISION (v3, 2026-02-22):**
>
> **ONE Ralph loop processes ALL prompts sequentially** via a persistent queue file.
> No multiple Skill calls. No bash scripts. One loop, one promise at the end.
>
> **How it works:**
> 1. `/overnight` creates a queue file: `_claude/overnight-queue.md`
> 2. `/overnight` creates a chain prompt: `_claude/overnight-chain-prompt.md`
> 3. `/overnight` invokes ONE `ralph-loop:ralph-loop` with the chain prompt
> 4. Each iteration: Claude reads queue → works on current prompt → updates progress
> 5. When current prompt is done: rename greenlit→done, mark DONE in queue, advance to next
> 6. Final promise (`OVERNIGHT_CHAIN_COMPLETE`) only when ALL queue items are DONE
>
> **Why this works:** The stop hook feeds the SAME chain prompt every iteration. Claude reads
> the queue file each time to know what to work on. Queue file persists across context compression.
> No handoff between loops = no breakage point.
>
> **Previous approaches (BROKEN):**
> - v1: Bash script piping stdin → `claude` exits immediately (2 seconds, exit 0)
> - v2: Sequential `Skill: ralph-loop:ralph-loop` calls → chain dies after first loop
>   because stop hook stops, session waits for user input, context compressed

---

## Quick Start

1. Interview user — priorities, wishes, specific ideas for the night
2. Scan repo — factory status, completed prompts, pending prompts, dependencies, backlog
3. Enter plan mode — present thorough plan with queue order, rationale, estimated time
4. User approves/modifies in plan mode
5. Generate any new Ralph prompts if user has custom wishes
6. **Create queue file + chain prompt** — persistent state on disk
7. **Start ONE Ralph loop** with chain prompt — runs until all items done

---

## Phase 1: Interview

Ask the user using AskUserQuestion. Gather:

**Question 1: "Co chcesz osiagnac tej nocy? Jaki jest priorytet?"**
Options based on current repo state:
- Continue factory execution order (next pending prompts)
- Focus on specific project (ROS / Apolonia / Fundacja / Culture)
- Custom tasks (user describes)
- Mix of factory + custom

**Question 2: "Ile czasu masz na noc? (wplyw na ilosc promptow)"**
- 4-6h (2-3 prompts, ~30 iterations)
- 8-10h (4-6 prompts, ~60 iterations)
- Unlimited (run everything pending)

**Question 3: "Jakies specyficzne pomysly, hipotezy, obawy ktore Ralph powinien zbadac?"**
Free text — user's input ideas. These get woven into the plan.

**Skip interview** when user provides clear direction in the initial command (e.g., "overnight on greenlit prompts in smart order"). Use the direction as answers.

---

## Phase 2: Repo Scan

Before entering plan mode, gather full picture:

### 2.1 Factory Status

Read the latest version's index: find the highest `v*/` dir in `_claude/6-prompts/ralph-factory/` and read its `_index.md` and `_progress.md`. Files with `done--` prefix = completed.

For each factory prompt, determine status:
- **COMPLETED**: `done--` prefix on prompt file
- **IN PROGRESS**: `greenlit--` prefix or `_progress.md` exists in output folder
- **PENDING**: No evidence of execution

Cross-reference with `_index.md` recommended execution order and dependency map.

### 2.2 Pre-Check: Done Detection

For each greenlit prompt, check:
1. Does `done--{base_name}` exist in factory dir?
2. Do the expected output files already exist? (check Target Output in the prompt)
3. Was the work partially done through other means? (check `updated:` dates on target files)

### 2.3 Transcript Backlog

Check `_transcripts-backlog/` for new unprocessed transcripts.
If significant backlog exists, consider adding `/process-transcripts` as first step.

### 2.4 Dependency Check

From `_index.md` dependency map, verify:
- No prompt in queue depends on an uncompleted prompt
- Order respects dependencies

---

## Phase 3: Plan Mode

Enter plan mode (EnterPlanMode). Present the plan with queue order, rationale, time estimate.
Wait for user approval via ExitPlanMode.

---

## Phase 4: Generate Custom Prompts (if needed)

If user requested custom tasks during interview:
1. Use the ralph-prompt template from `_claude/6-prompts/` patterns
2. Save to `_claude/6-prompts/ralph-factory/ralph-{topic}.md`
3. Add to the night queue

---

## Phase 5: Create Queue + Chain Prompt

### 5.1 Queue File

Create `_claude/overnight-queue.md`:

```markdown
---
status: active
total: {N}
completed: 0
started_at: "{ISO timestamp}"
---

# Overnight Queue — {date}

| # | Status | Prompt File | Max Iter | Promise |
|---|--------|------------|----------|---------|
| 1 | PENDING | greenlit--ralph-foo.md | 15 | FOO_COMPLETE |
| 2 | PENDING | greenlit--ralph-bar.md | 10 | BAR_COMPLETE |
| ... | ... | ... | ... | ... |
```

### 5.2 Chain Prompt

Create `_claude/overnight-chain-prompt.md`:

```markdown
# Overnight Chain — Queue-Driven Execution

You are processing a queue of Ralph prompts. ONE AT A TIME. This is a CONTINUOUS loop.

## EVERY ITERATION — follow this protocol:

### Step 1: Read queue
Read `_claude/overnight-queue.md`. Find the first row with Status = ACTIVE or PENDING.

### Step 2: Determine action

**If current prompt is ACTIVE (in progress):**
- Read the prompt file at `_claude/6-prompts/ralph-factory/v2/{prompt_file}`
- Read its progress file (if exists): `_claude/6-prompts/ralph-factory/v2/{prompt_base}-progress.md`
- Continue working on the next unfinished iteration of that prompt
- Update the progress file after each iteration of work

**If no ACTIVE prompt, first PENDING prompt:**
- Mark it ACTIVE in `_claude/overnight-queue.md`
- Read the full prompt file
- Start working from Iteration 1
- Create progress file

**If current prompt's work is COMPLETE:**
- Rename the prompt file: `greenlit--{name}.md` → `done--{name}.md`
- Mark it DONE in `_claude/overnight-queue.md`
- Update `completed:` count in frontmatter
- Log: "=== PROMPT COMPLETE: {name} ==="
- Move to next PENDING prompt (go to Step 1)

**If ALL prompts are DONE:**
- Show final summary of all completed prompts
- Output: `<promise>OVERNIGHT_CHAIN_COMPLETE</promise>`

### Step 3: Do ONE iteration of work
Each iteration = one meaningful unit of work from the current prompt's iteration plan.
This might be: reading source files, mining transcripts, writing a section, quality checking.
Update the progress file after each iteration.

## IMPORTANT RULES:
- NEVER output `<promise>OVERNIGHT_CHAIN_COMPLETE</promise>` until ALL queue items are DONE
- Each individual prompt has its OWN completion criteria — check them before marking DONE
- The queue file is your SINGLE SOURCE OF TRUTH — always read it fresh each iteration
- If a prompt has a per-prompt promise (like SALES_PLAYBOOK_ENRICHMENT_COMPLETE), do NOT output it — just mark DONE in queue and move on
- Work on ONE prompt at a time, in order
- Context will compress — that's fine. The queue file and progress files persist on disk
```

**Important:** The chain prompt MUST be customized per run with the actual queue contents.

### 5.3 Invoke Ralph Loop

Call exactly ONE Ralph loop:

```
Skill: ralph-loop:ralph-loop
Args: "_claude/overnight-chain-prompt.md" --max-iterations {TOTAL_ITERATIONS} --completion-promise "OVERNIGHT_CHAIN_COMPLETE"
```

Where `TOTAL_ITERATIONS` = sum of all prompt iterations + buffer (add 20% for transitions).
E.g., 5 prompts × avg 12 iter = 60 + 12 buffer = 72 iterations.

---

## Phase 6: Post-Run

After chain completes (or user interrupts):

1. Show `git diff --stat` summary
2. List new `done--` files
3. List any remaining `greenlit--` files
4. Ask user if they want to commit changes

---

## Estimation Heuristics

Rough time estimates per iteration (for planning):
- Simple iterations (read + analyze): ~2-3 min
- Writing iterations (create files): ~3-5 min
- Quality check iterations: ~2-3 min

So a 15-iteration prompt takes roughly 45-75 min.

| Queue size | Iterations | Estimated time |
|-----------|------------|----------------|
| 2 prompts | ~30 iter | 1.5-2.5h |
| 3 prompts | ~45 iter | 2.5-4h |
| 5 prompts | ~70 iter | 4-6h |
| 8 prompts | ~100 iter | 6-9h |

---

## Troubleshooting

| Problem | Rozwiazanie |
|---------|-------------|
| Ralph loop doesn't start | Sprawdź czy chain prompt istnieje. `rm -f .claude/ralph-loop.local.md` |
| Loop processes only first prompt | Check queue file — is next item marked PENDING? Is chain prompt instruction clear? |
| Context overflow | Normal — queue file and progress files persist. Quality may degrade after 60+ iterations |
| Want to stop mid-chain | Ctrl+C. Queue file preserves state — re-run /overnight to resume from where it stopped |
| Resume after crash | Re-run /overnight. It reads queue file, skips DONE items, continues from ACTIVE/PENDING |
| Morning review | `git diff --stat` + `git log --oneline -20` |

---

## State Files

- Queue file: `_claude/overnight-queue.md` (persistent, survives context compression)
- Chain prompt: `_claude/overnight-chain-prompt.md` (the meta-prompt fed to Ralph loop)
- Ralph state: `.claude/ralph-loop.local.md` (managed by ralph-loop plugin)
- Per-prompt progress: each Ralph prompt writes its own `*-progress.md`
- Factory index: `_claude/6-prompts/ralph-factory/{version}/_index.md`

## Known Limitations

- **Context accumulates** — single loop = later iterations have compressed context. Queue file and progress files are the antidote. For 8+ prompts, quality of later prompts may degrade.
- **One chain at a time** — don't run /overnight while another Ralph loop is active.
- **Resumable** — if session drops, re-run /overnight. Queue file preserves state. Done prompts are skipped.
- **Max iterations cap** — Ralph loop has a max-iterations limit. Set it high enough (total + 20% buffer).
