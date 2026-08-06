# Emission checklist — real failures and the tool contract

Workflow scripts that die do so for a small set of repeatable reasons, all of them catchable
before emission. Walk sections A-C on EVERY script you emit, and D after the run.

## A. Parser (the most common real crashes)

1. **Apostrophes inside non-ASCII prose** — the top cause of crashes when prompts are written in
   a language with apostrophes inside words (French `l'agent`, Polish inflected loanwords, English
   `don't`) and the string is single-quoted. Rule: all natural-language text (prompts, descriptions,
   labels) goes in **double quotes** or template literals; single quotes only for short ASCII
   identifiers (keys, enum values, labels). Scan the script for `'...'` containing prose before
   you emit.
2. **No TypeScript.** No `: string[]`, no `interface`, no `as`, no generics. The script is plain
   JavaScript.
3. **`meta` is a pure literal** — no variables, calls, spreads or interpolation. Required:
   `name`, `description`. `phases` — titles IDENTICAL, character for character, to the `phase()`
   calls.
4. **Forbidden APIs**: `Date.now()`, `Math.random()`, `new Date()` with no argument → they throw
   (they would break resume). Pass timestamps through `args`, or stamp the result AFTER the
   workflow finishes. For randomness, vary the prompt/label by index.
5. **Template literals containing code**: escape backticks and `${` inside prompts that carry code
   examples — or build the string by concatenating double-quoted pieces.
6. **No filesystem/Node APIs in the script** — files are read by AGENTS, not by the script. The
   script only sees what agents return.

## B. Calling the tool

7. **Workflow does NOT accept `run_in_background`** (InputValidationError). Workflow always runs
   in the background; do not pass the parameter.
8. **`args` must be real JSON**, not a string containing JSON (`args: ["a", "b"]`, not
   `args: "[\"a\",\"b\"]"`). BUT: args can reach prompts EMPTY — put correctness-critical data
   **inline in the script**; use args only to parameterize saved workflows, always with a fallback.
9. **Iteration**: the tool result returns `scriptPath` — edit THAT file and resume with
   `{ scriptPath, resumeFromRunId }` (stop the run first). An unchanged prefix of `agent()` calls
   comes back from cache immediately.

## C. Runtime and structure

10. **`.filter(Boolean)` after every `parallel()`/`pipeline()`** — a thunk that errors (or is
    skipped by the user) yields `null`, not an exception. Design the fan-in to tolerate gaps.
11. **Loops**: dedup against `seen` (everything observed), NEVER against `confirmed` — otherwise
    refuted findings return every round and the loop never converges. Always add a guard:
    `dry >= 2`, a max-round counter, or `budget.total && budget.remaining() > threshold` (with no
    target set, `remaining()` is Infinity and the loop runs to the 1000-agent cap).
12. **Barriers only after the smell test** (design-knobs §5). `parallel → flatten → parallel` with
    no cross-item dependency = rewrite as a pipeline.
13. **`isolation: 'worktree'`** only when agents WRITE the same files in parallel — it costs a few
    hundred milliseconds plus disk per agent. Not a default.
14. **Limits**: concurrency is min(16, cores-2) — the excess queues (you may pass hundreds of
    thunks); 1000 agents per run; 4096 items per single parallel/pipeline call; session guideline
    under 15 agents — more only on explicit request. Show the fan-out × verify arithmetic before
    emitting (10 finders × 5 findings × 3 votes = 150 agents).
15. **Model**: omit by default (inherit). After a `/model` switch mid-session — explicit `model:`
    on every agent, because inheritance after a switch is unreliable.
16. **MCP inside workflow agents**: reachable through tool search per agent, BUT servers that
    authenticate interactively may not work in headless/cron runs.

## D. After the run

17. **Empty or strange output** → FIRST read `<transcriptDir>/journal.jsonl` — the actual return
    of every agent is there. Do not assume cached results are non-empty. Fallback: the
    `agent-<id>.jsonl` files in the transcript dir.
18. **Do NOT send messages to finished workflow agents** — that resumes them OUTSIDE the workflow
    as parallel instances operating on the same files.
19. **Saving and committing**: save to `.claude/workflows/` after the user agrees (Step 7); commit
    only on explicit request.
20. **Report faithfully**: if some agents returned null or garbage, say so with numbers instead of
    smoothing it over.
