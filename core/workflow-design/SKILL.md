---
name: workflow-design
description: |
  Interactive designer for multi-agent workflows (the Workflow tool): interviews you about
  priorities, picks a graph topology with ASCII preview, then per-stage casting, models/effort,
  adversarial gates and flow control (barrier/pipeline), ending in a validated script ready to
  run or save to .claude/workflows/. Educated suggestions come from precedents grepped out of
  your own Claude Code session history plus a checklist of real parser failures.
  Use when: designing a new workflow / agent orchestration, improving or repairing an existing
  workflow script, unsure which topology fits (fan-out? verify? judge panel? pipeline?),
  wanting a repeatable workflow saved to .claude/workflows/.
  Trigger phrases: "workflow design", "workflow-design", "design a workflow", "new workflow",
  "agent graph", "workflow topology", "agent orchestration", "improve workflow", "fix workflow",
  "sketch the agent graph"
---

# Workflow Design

A wizard for designing multi-agent workflows. Governing principle: **the priorities collected in
the opening interview go into every agent prompt and every decision about the graph.** That is
the point of the interview — so the script chases what the user actually cares about instead of
a generic "do some research".

## Quick Start

1. Collect task and priorities — one batched AskUserQuestion round (Step 1)
2. Grep precedents: `python3 .claude/skills/workflow-design/scripts/find_precedents.py <keywords>`
3. Offer 2-4 topologies from `references/topologies.md` — AskUserQuestion with ASCII previews
4. Ask per stage, adaptively: casting, models, gates (`references/design-knobs.md`)
5. Assemble the script, validate against `references/gotchas.md`, show the design summary
6. Ask: run it / save to `.claude/workflows/` / just show it

## How to run the wizard

- **Batch the questions** — max 4 per AskUserQuestion round, never one at a time.
- **Recommendation always first**, suffixed "(Recommended)" — the user can click through with Enter.
- **Be adaptive**: graph with ≤2 stages → one shared per-stage round; 3+ stages → one round per
  stage. If the user says "defaults" / "you decide" → stop asking, run on your recommendations.
- **An educated suggestion is concrete**: number of agents, model, effort, number of votes, shape
  of the schema. Not "it depends". One sentence of justification (a precedent you found, or a
  rule from `references/`).
- The Workflow tool is launched only after an explicit user choice in Step 7 — picking an option
  there is the opt-in to multi-agent orchestration.

## Step 0 — Intake

- Task description from the arguments or the conversation. Missing → just ask (plain question,
  no AskUserQuestion).
- The user points at an existing script (path, a name from `.claude/workflows/`, "the last
  workflow", a runId) → **REDESIGN mode** (section below).

## Step 1 — Priorities

One AskUserQuestion round, max 4 questions (skip any the task description already answers):

1. **Dominant priority** (multiSelect, max 2): Certainty / zero hallucination · Coverage /
   completeness · Wall-clock speed · Token cost
2. **Scale**: S (3-6 agents) · M (7-15, the session guideline) · L (16+ — only on explicit request)
3. **Deliverable**: report/analysis · code/files · content/variants · design decision
4. **Reuse**: one-off · saved workflow parameterized through `args`

Priority → design lever mapping: `references/design-knobs.md` §1. Write the priorities down —
you propagate them into every prompt in Step 5.

## Step 2 — Precedents

```
python3 .claude/skills/workflow-design/scripts/find_precedents.py "keyword1" "keyword2"
```

- Hits → show the top 3 (date, name, phases, `agent()` call sites, description) and offer one as
  a reuse baseline. Call sites are places in the source, not the number of agents spawned
  (a fan-out inside `.map` counts once).
  (`--extract <name>` prints the full script; save it to a scratch directory, not into the repo.)
- No hits → move on without comment. This step takes seconds — do not dig.
- `--all` searches sessions from every project on the machine.
- No session history at all (fresh machine, or Claude Code stores transcripts elsewhere) → the
  script says so and exits cleanly. Skip the step; the rest of the wizard does not depend on it.

## Step 3 — Topology

From `references/topologies.md` (selection table at the top) pick 2-4 candidates that fit the
task and the priorities. AskUserQuestion with a `preview` per option: ASCII graph plus one line
of "when to use this". Recommended candidate first. Previews only render for single-select.

## Step 4 — Per stage (adaptive)

For each stage of the graph, one AskUserQuestion round, max 4 questions:

1. **Casting**: how many agents, which lenses/styles — propose concrete lenses (design-knobs §3)
2. **Model + effort**: inherit, or explicit tiering (design-knobs §4). After a `/model` switch
   mid-session — ALWAYS set explicit `model:` on every agent (inheritance is unreliable).
3. **Quality gate behind the stage**: none · adversarial verify (N votes, refute-by-default) ·
   judge panel (N judges + grafts from the runners-up)
4. **Flow into the next stage**: barrier (`parallel()`) · stream (`pipeline()`) · router (branch
   in code). Barrier smell test: design-knobs §5.

Per-topology defaults live in topologies.md — offer them as "(Recommended)".

## Step 5 — Contracts and prompts (no questions)

- Every node that returns data → a `schema` (additionalProperties: false, enums, required).
  Patterns: design-knobs §7.
- Agent prompt: bounded input inline (concrete paths/data pasted into the prompt), one job,
  return = raw data.
- **Priority propagation**: weave the Step 1 priorities into every prompt — sentence patterns in
  design-knobs §6.
- Correctness-critical data goes inline in the script, not in `args` — args can reach prompts empty.

## Step 6 — Validation and design summary

Walk `references/gotchas.md` point by point (sections A-C are mandatory). Then show:

1. The final ASCII graph
2. A table: Stage | Agents (N × lens) | Model/Effort | Schema | Gate → next stage
3. An estimate: total agents, which nodes run on the expensive model

User corrections → go back to the relevant step, do not restart from zero.

## Step 7 — Emission and finish

Generate the script (`meta` is a pure literal; phase titles match the `phase()` calls 1:1).
AskUserQuestion:

- Run it now (Workflow with the script inline)
- Save to `.claude/workflows/{name}.mjs` and run it
- Save only
- Just show the script

After launching: monitor, then give a short report of the results. To iterate: edit the file at
the `scriptPath` returned in the tool result and resume via `resumeFromRunId` (stop the run
first). A successful one-off → still offer to save it. Commit only with the user's consent.

## REDESIGN mode

1. Load the script (from a file, or `find_precedents.py --extract <name>`)
2. Map the current graph: stages, N, gates, schemas — show it as ASCII plus a table
3. Diagnose: walk gotchas.md and name the structural gaps (barrier with no cross-item dependency
   → pipeline? no verify despite a Certainty priority? parallel writes without worktree isolation?
   a loop with no guard? one-round discovery where loop-until-dry belongs?)
4. Present the proposed changes with justification; run the wizard (Step 4) only for the stages
   that change
5. Continue as in Steps 6-7

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Script fails to parse | gotchas.md A1-A6: apostrophes in non-ASCII prose, TypeScript syntax, computed `meta` |
| Workflow returned empty / strange output | Read `journal.jsonl` in the transcript dir first — the real agent returns are there |
| Agent got empty context | The data lived in `args` — move it inline into the script |
| Too slow (wall-clock) | Barrier with no cross-item dependency → `pipeline()`; run the smell test (design-knobs §5) |
| Agents overwrite each other's files | `isolation: 'worktree'` on the build stage (only where writes are parallel) |
| Low-quality results | Raise judge/verify effort, add refute-by-default, narrow the node inputs |
| Loop never converges | Dedup against `seen`, not `confirmed`; add a dry-round counter and a budget guard |
| find_precedents finds nothing | Try `--all`, or a single broader keyword |
| Skill does not trigger | Check the phrase — autonomous-loop skills are a different tool (iterative single-agent loops, not Workflow graphs) |
