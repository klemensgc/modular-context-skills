# Topology library

Nine shapes cover almost everything people build with the Workflow tool. In our experience the
fan-out patterns (1, 2, 3) dominate real usage, while `pipeline`, `loop-until-dry` and worktree
isolation are systematically under-used — propose them actively when they fit, because most
scripts that feel slow are barriers that should have been streams.

## Selection table

| Task | Topology | Notes |
|------|----------|-------|
| Research / map / inventory / recon | 1. Recon fan-out → synthesis | the workhorse; most common by far |
| Diff review / audit / fact-check | 2. Diamond find → verify | pair with refute-by-default |
| Design / copy / concepts / naming | 3. Variants → judge panel | one answer out of a wide space |
| Bulk content production (courses, SOPs, sections) | 4. Content factory with QA | pipeline, not barrier |
| Implementing several areas of code | 5. Build fan-out | disjoint file ownership is the constraint |
| Feature end to end | 6. Understand → Design → Implement → Verify | consider splitting into separate runs |
| "Find every X", unknown size | 7. Loop-until-dry | the fix for truncated tails |
| Different paths depending on classification | 8. Router | agent classifies, code branches |
| Many items × many stages per item | 9. Streaming pipeline | an overlay, not a standalone shape |

Topologies compose: 4 = 1 + a QA pipeline; 6 = a chain of 1→3→5→2; 7 wraps 2 in a loop.

---

## 1. Recon fan-out → synthesis

**When:** research, mapping a system, inventory, gathering context from disjoint sources.
**Typical N:** 4-10 readers + 1 synthesizer. **Gate:** barrier before synthesis (the synthesizer
needs the whole set — a justified barrier).

```
[area A] ──┐
[area B] ──┼──[barrier]──> [synthesizer]
[area C] ──┘
```

```js
phase("Recon")
const raw = await parallel(AREAS.map(a => () =>
  agent(a.prompt, { label: "recon:" + a.key, schema: FINDINGS, effort: "low" })))
phase("Synthesis")
const report = await agent("Synthesize: " + JSON.stringify(raw.filter(Boolean)),
  { schema: REPORT, effort: "high" })
```

Defaults: readers at effort low (mechanical work), synthesizer at effort high on the session model.
Define area disjointness with concrete paths in the prompts, never "the rest of the repo".

## 2. Diamond find → verify (adversarial)

**When:** diff review, security/quality audit, fact-checking claims. **Typical N:** 3-5 finders
(different lenses) + 2-3 verify votes per finding + 1 report. **Gate:** a barrier after the finders
ONLY if you dedup across sources; otherwise pipeline (each finding gets verified as it appears).

```
[finder: correctness] ──┐                     ┌─> [verify ×3 votes] ─┐
[finder: security]    ──┼──(dedup, in code)───┼─> [verify ×3 votes] ─┼──> [report]
[finder: perf]        ──┘                     └─> [verify ×3 votes] ─┘
```

```js
const results = await pipeline(DIMENSIONS,
  d => agent(d.prompt, { label: "find:" + d.key, phase: "Find", schema: FINDINGS }),
  r => parallel((r?.findings || []).map(f => () =>
    agent("Try to REFUTE: " + f.title + ". If uncertain, set refuted=true.",
      { phase: "Verify", schema: VERDICT, effort: "high" })
      .then(v => ({ ...f, verdict: v })))))
const confirmed = results.flat().filter(Boolean).filter(f => !f.verdict?.refuted)
```

Verify is always refute-by-default. With a Certainty priority: 3 votes, majority 2, and different
lenses (correctness / security / reproduction) rather than three identical skeptics.

## 3. Variants → judge panel

**When:** design, copy, concepts, naming — a wide solution space, one answer needed.
**Typical N:** 3-7 generators (each a different lens/frame) + 3-5 judges + 1 synthesis.
**Gate:** barrier before the judges (they compare across variants — justified).

```
[gen: lens A] ──┐              ┌─ [judge 1] ─┐
[gen: lens B] ──┼─[barrier]────┼─ [judge 2] ─┼──> [synthesis: winner + grafts]
[gen: lens C] ──┘              └─ [judge 3] ─┘
```

Judges get their scoring criteria straight from the user's priorities (Step 1) plus a numeric
rubric in the schema. The synthesis takes the winner and grafts the best elements of the
runners-up. Generators can run on a cheaper model; judges and synthesis on the session model at
effort high.

## 4. Content factory with QA

**When:** producing many units of content against a shared contract (course modules, SOPs,
document sections, variant assets). **Typical N:** 1 writer per unit + 1 verifier per unit.
**Gate:** NO barrier between writing and QA — use `pipeline()` (units are independent; unit 1 can
be in QA while unit 7 is still being written). A barrier only before a whole-corpus consistency
pass, if you have one.

```
[unit 1: write] ─> [QA 1] ─> [fix 1] ─┐
[unit 2: write] ─> [QA 2] ─> [fix 2] ─┼──> (optional: whole-corpus consistency)
[unit N: write] ─> [QA N] ─> [fix N] ─┘
```

```js
const done = await pipeline(UNITS,
  m => agent(writePrompt(m), { phase: "Writing", schema: DRAFT }),
  (draft, m) => agent(qaPrompt(m, draft), { phase: "QA", schema: QA_VERDICT, effort: "high" })
    .then(qa => qa?.pass ? draft : agent(fixPrompt(m, draft, qa), { phase: "Fixes", schema: DRAFT })))
```

The shared content contract (style, length, structure) goes inline into EVERY writer prompt —
not into args. This shape scales to dozens of units without the wall-clock cost of a barrier.

## 5. Build fan-out over disjoint areas

**When:** implementing several features/areas of code in parallel. **Typical N:** 2-6
implementers. **Critical:** if the areas are NOT disjoint at file level → `isolation: 'worktree'`
per agent. Hand-partitioning "disjoint areas" and hoping is the fragile alternative.

```
[area map] ──> [impl A (worktree?)] ──┐
               [impl B (worktree?)] ──┼─[barrier]──> [verify / diff review → topology 2]
               [impl C (worktree?)] ──┘
```

Each implementer gets: the exact list of files it owns, a ban on touching anyone else's, and the
interface contract between areas (inline). After the build, switch to topology 2 for review.

## 6. Understand → Design → Implement → Verify

**When:** a feature end to end, rebuilding a module. A chain of topologies: recon (1) → designs +
critic (3) → build (5) → review (2). **Note:** this is sequential by nature — the barriers between
phases are justified (design needs all of understand, and so on).

Consider splitting it into SEPARATE workflows per phase, with the user in the loop between them.
For large features that is the default recommendation: you read the output of a phase before
commissioning the next one.

## 7. Loop-until-dry (discovery of unknown size)

**When:** "find every bug / inconsistency / instance of X" — you do not know how many there are.
A single-round fan-out truncates the tail; loop until K consecutive rounds yield nothing new.

```
┌──> [finders ×N, different angles] ──> (dedup vs SEEN, in code) ──> [verify] ──> confirmed
│                                                                        │
└─────────────── while fewer than 2 consecutive empty rounds <───────────┘
```

```js
const seen = new Set(); const confirmed = []; let dry = 0
while (dry < 2) {
  const found = (await parallel(FINDERS.map(f => () =>
    agent(f.prompt, { phase: "Search", schema: BUGS })))).filter(Boolean).flatMap(r => r.bugs)
  const fresh = found.filter(b => !seen.has(key(b)))
  if (!fresh.length) { dry++; continue }
  dry = 0; fresh.forEach(b => seen.add(key(b)))
  const judged = await parallel(fresh.map(b => () =>
    agent("Refute this: " + b.desc, { phase: "Verify", schema: VERDICT })))
  confirmed.push(...fresh.filter((b, i) => judged[i] && !judged[i].refuted))
  log(confirmed.length + " confirmed, another round")
}
```

Trap number one: dedup against `seen`, NOT against `confirmed` — otherwise refuted findings come
back every round and the loop never dries out. Always add a guard: a max-round counter or
`budget.remaining()`.

## 8. Router (conditional path)

**When:** the path depends on a classification — a small diff gets a quick pass, a large one gets
a full audit. An agent classifies (schema with an enum); the CODE picks the path (`if`/`switch`),
deterministically.

```js
const { severity } = await agent("Classify the risk of this diff:\n" + diff,
  { schema: { type: "object", properties: { severity: { enum: ["low", "high"] } },
    required: ["severity"], additionalProperties: false } })
const review = severity === "high"
  ? await parallel(FILES.map(f => () => agent("Audit " + f, { schema: FINDINGS })))
  : await agent("Quick review:\n" + diff, { schema: FINDINGS })
```

## 9. Streaming pipeline (overlay)

**When:** many items pass through the same 2+ stages and the stages do NOT compare items against
each other. Not a standalone topology — a way of connecting the stages inside 2 and 4: item A is
in stage 3 while item B is in stage 1. Wall-clock becomes the slowest single-item chain instead of
the sum of the slowest stages. Before you leave a barrier in place, check it against the smell
test (design-knobs §5).
