# Design knobs — casting, models, gates, prompts

## §1 Priority → levers

Translate the Step 1 priorities into design decisions mechanically:

| Priority | Levers in the graph | Levers in the prompts |
|----------|--------------------|-----------------------|
| **Certainty / zero hallucination** | adversarial verify (3 votes, refute-by-default) behind every stage that produces claims; judge panel on the synthesis; `confidence` + `source` fields in the schema | "Attach a source path to every number, name and date"; "unknown is a valid answer — do not guess" |
| **Coverage / completeness** | multi-angle sweep (a different search angle per agent); loop-until-dry instead of one round; a completeness critic at the end ("what was missed?") | "End by listing what you did NOT check"; `log()` everything discarded (no silent truncation) |
| **Wall-clock speed** | pipeline() everywhere there is no cross-item dependency; smaller N per stage; barriers only after the smell test (§5) | "Do not read whole files — only the sections named here"; bounded input |
| **Token cost** | cheap model on mechanical stages; effort low; minimal N; a `budget.remaining()` guard in loops | short prompts with the data inline instead of "search the repo" |

Priorities compose: Certainty + Cost = cheap fan-out, expensive only on verify and synthesis.

## §2 Agent counts

| Role | Norm | Notes |
|------|------|-------|
| Recon readers | 4-10 | above 10 only with explicit consent to scale L |
| Build implementers | 2-6 | the constraint is area disjointness, not horsepower |
| Variant generators | 3-7 | each MUST have a different lens — 5 identical ones are waste |
| Verify votes per finding | 2-3 | majority; a single vote only for low stakes |
| Panel judges | 3-5 | odd number; different rubrics or different personas |
| Synthesizer / reporter | 1 | always one; it receives everything after the barrier |

Session guideline: fewer than 15 agents total (medium scale). More only on explicit request — and
then do the arithmetic, because fan-out × verify votes explodes (10 finders × 5 findings × 3 votes
= 150 agents). Show that arithmetic to the user BEFORE emitting.

## §3 Agent lenses / styles per task type

A lens is a distinct angle of attack written into the prompt. Propose from this list, matched to
the task:

- **Code / review**: correctness · security · performance · edge cases/reproduction ·
  API contract · test coverage
- **Research / recon**: by-container (structure) · by-content (grep) · by-entity (people,
  customers) · by-time (chronology) · by-absence (what is missing)
- **Design / copy**: user-first · brand-first · conversion-first · minimalism/subtraction ·
  contrarian ("invert the assumption")
- **Strategy / decisions**: risk-first · MVP-first · 10x-scale · opportunity-cost ·
  pre-mortem ("this already failed — why?")
- **Verify**: always adversarial — "try to REFUTE"; never "check whether it is good"

Prompt style for every node: (1) role and lens in the first sentence, (2) bounded input — concrete
paths and data pasted in, (3) one job, (4) a reminder that the final text is the raw return (the
schema enforces this anyway), (5) the user's priorities (§6).

## §4 Model and effort tiering

Models available in `agent()`: `haiku` · `sonnet` · `opus` · `fable`. Effort: `low` · `medium` ·
`high` · `xhigh` · `max`.

| Node type | Model | Effort |
|-----------|-------|--------|
| Extraction / classification / grep-like | haiku or sonnet | low |
| Recon reader, content writer against a contract | sonnet or inherit | low-medium |
| Code implementer | inherit (session model) | medium |
| Verify / judge | inherit | high |
| Synthesizer / final report | inherit (or the strongest model under a Certainty priority) | high-xhigh |

Hard rules:
1. By default **omit** `model:` (inherit the session model) — that is almost always right.
2. **After a `/model` switch mid-session: explicit `model:` on EVERY agent** — inheritance after
   a switch is unreliable. Do not assume it worked, and do not claim it did.
3. Tier down (haiku/sonnet) only on genuinely mechanical nodes — a misclassified judgment node on
   a small model degrades the whole graph silently.
4. Effort `low` on a mass fan-out is the single biggest saving available.

## §5 Gates: barrier · pipeline · router · loop

- **Barrier** (`parallel()`): waits for EVERYTHING. Justified only when the next stage needs the
  whole set at once: cross-source dedup, ranking between items, early exit on "zero findings", a
  prompt that compares "against the others".
- **Stream** (`pipeline()`): each item flows through the stages independently. The DEFAULT choice
  for multi-stage work over a list of items.
- **Router**: an agent classifies (schema with an enum), code picks the path with `if`/`switch`.
- **Loop** (`while`): only with a convergence condition (dry rounds / budget / max rounds).

Barrier smell test (apply to EVERY barrier): did you write `parallel → transform → parallel`? If
the transform is a flatten/map/filter with no dependency between items, the barrier is dead weight
— rewrite it as a pipeline with the transform inside a stage. "Cleaner code" and "the stages are
conceptually separate" do NOT justify a barrier. Most long-running scripts overpay in wall-clock
here.

Adversarial patterns (quality gates):
- **Refute-by-default**: "Try to refute X. If uncertain, refuted=true." A vote in favour of
  passing must be earned.
- **Perspective-diverse verify**: when a finding can be wrong in several ways, give each vote a
  different lens (correctness / security / reproduction) rather than N copies of the same skeptic.
- **Judge panel + graft**: judges score against a rubric (numbers in the schema); the synthesis
  takes the winner plus the best elements of the losers.
- **Completeness critic**: a final agent asks "what is missing — an unsearched angle, an
  unverified claim, an unread source?" Its output is the next round of work.

## §6 Propagating priorities into prompts — sentence patterns

Paste the Step 1 priorities into EVERY agent prompt. This is the core of the skill:

- Certainty: "Attach a source to every claim (file path / URL). When unsure, set confidence: low
  or unknown — do not guess."
- Certainty (verify): "Your only job is to REFUTE the claim below. You are looking for a
  counterexample, not a confirmation. If uncertain, refuted=true."
- Coverage: "Before returning, list in a not_checked field the things you did NOT check and why."
- Speed/Cost: "Read only the files/sections named here. Do not explore beyond the list."
- Code deliverable: "Return only the diff/files — no prose, no explanations."
- Brand/taste (design): paste the governing style rules directly into the generator prompt; the
  judge receives the same rules as its rubric.

## §7 Schema patterns

Always: `additionalProperties: false`, enums for judgments, `required` on everything the next
stage consumes. Three proven shapes:

```js
const FINDINGS = { type: "object", additionalProperties: false, required: ["findings"],
  properties: { findings: { type: "array", items: { type: "object",
    additionalProperties: false, required: ["title", "file", "impact", "evidence"],
    properties: { title: { type: "string" }, file: { type: "string" },
      impact: { enum: ["high", "medium", "low"] }, evidence: { type: "string" },
      confidence: { enum: ["high", "moderate", "low"] } } } } } }

const VERDICT = { type: "object", additionalProperties: false,
  required: ["refuted", "reason"],
  properties: { refuted: { type: "boolean" }, reason: { type: "string" } } }

const SCORE = { type: "object", additionalProperties: false,
  required: ["scores", "winner", "grafts"],
  properties: { scores: { type: "array", items: { type: "object",
    additionalProperties: false, required: ["variant", "total"],
    properties: { variant: { type: "string" }, total: { type: "number" } } } },
    winner: { type: "string" }, grafts: { type: "array", items: { type: "string" } } } }
```

The schema is validated at the tool-call layer — the agent retries itself on a mismatch. Treat it
as the contract on a graph edge: either node can be swapped as long as the shape holds.
