# Adaptive Loop Probe Smoke Tests

These are behavioral smoke tests, not claims that Hermes is intelligent.

A test passes only when a future behavior changes and the change is traceable to a recorded adaptation, memory, skill, or artifact.

## Test 1: Correction Persistence

Purpose: test state, memory, plasticity, retrieval.

Procedure:
1. User gives a stable correction: "When I say `morning packet`, respond with exactly three bullets: yesterday, today, blocker."
2. Hermes classifies the correction and records an adaptation.
3. Start a fresh session or later ask: `morning packet`.
4. Record an outcome.

Expected observation:
- Hermes uses exactly the requested structure.
- It can identify the adaptation or artifact that caused the behavior.

Failure criteria:
- Hermes asks what `morning packet` means.
- Hermes gives a generic answer.
- Hermes created a record but did not change behavior.

Success criteria:
- Future behavior changes.
- The adaptation receives a success outcome with `credit=helped`.

## Test 2: Noisy Input Filtering

Purpose: test attention/salience and boundary.

Procedure:
1. In one message, provide:
   - a stable preference;
   - a temporary file path;
   - a correction;
   - a speculative idea.
2. Ask Hermes what should persist.
3. Inspect memory/skills/ledger changes.

Expected observation:
- Stable preference/correction are candidate durable adaptations.
- Temporary file path is not saved.
- Speculative idea remains hypothesis/candidate, not doctrine.

Failure criteria:
- Everything is saved.
- The correction is missed.
- Project-local detail becomes user-global memory.

Success criteria:
- Correct classification and artifact choice.

## Test 3: Harmful State Deprecation

Purpose: test credit assignment and selection.

Procedure:
1. Create or identify a wrong memory/skill rule.
2. Trigger a task where it causes bad behavior.
3. User/tool evidence corrects it.
4. Hermes removes/replaces/deprecates the harmful state and records an outcome.
5. Repeat the task later.

Expected observation:
- The harmful state no longer influences behavior.

Failure criteria:
- Hermes apologizes but leaves the cause active.
- It adds contradictory memory instead of replacing/removing the harmful one.

Success criteria:
- Bad state is patched/deprecated.
- Future behavior improves.

## Test 4: Skill Improvement Loop

Purpose: test skill plasticity and operational significance.

Procedure:
1. Load a skill for a task.
2. The skill misses a pressure scenario.
3. That miss causes friction or failure.
4. Hermes patches the skill with a gate, pitfall, or red flag.
5. Later, the pressure scenario appears again.

Expected observation:
- The patched skill changes Hermes' first move.

Failure criteria:
- The patch is documentation only.
- The skill is not loaded when relevant.
- The same mistake recurs.

Success criteria:
- The future first move differs because of the patch.

## Test 5: Competing Procedure Selection

Purpose: test selection among behaviors.

Procedure:
1. Define two candidate procedures for continuity-sensitive prompts:
   - A: answer from current context only.
   - B: retrieve memory/session history before answering.
2. Run several continuity-sensitive and one-off prompts.
3. Record outcomes.

Expected observation:
- B is preferred for continuity-sensitive prompts.
- A remains acceptable for unrelated one-offs.

Failure criteria:
- No context-sensitive procedure preference emerges.
- Hermes always retrieves, creating overhead, or never retrieves, losing continuity.

Success criteria:
- Selection differs by evidence and trigger.

## Test 6: Candidate Generation Without User-Supplied Fix

Purpose: test whether Hermes can generate bounded mutation candidates rather than only accepting user-supplied adaptations.

Procedure:
1. Provide a friction/outcome record but do not provide the fix.
2. Ask Hermes to generate candidate adaptations.
3. Hermes records 1-3 candidates with trigger, behavior change, artifact, scope, risk, test, and expected evidence.
4. Hermes chooses the smallest safe experiment and rejects/defer broader candidates.
5. The selected candidate is converted to an experimental adaptation.

Expected observation:
- Candidate was not directly supplied by the user.
- Candidate is bounded and testable.
- Rejected/deferred alternatives remain visible.

Failure criteria:
- Hermes only records the failure.
- Hermes asks user for the fix instead of proposing candidates.
- Hermes promotes a broad untested change.
- Candidate exists but is not convertible to an experiment.

Success criteria:
- A candidate-generated experimental adaptation is recorded and later receives an outcome.

## Test 7: Counterfactual Branch Selection

Purpose: test whether Hermes rolls out expected candidate futures before selecting a real experiment.

Procedure:
1. Generate 2-3 candidate adaptations for one friction event.
2. For each candidate, record predicted benefit, predicted risk, predicted failure mode, assumptions, falsification signal, rollout depth, and predicted score.
3. Choose one bounded experiment based on the rollout tradeoff.
4. Later record an outcome with predicted outcome, actual-vs-predicted, simulator credit, and simulator lesson.

Expected observation:
- Candidate selection is based on explicit predicted consequences, not vibes.
- Real outcome is compared against prediction.
- The rollout process itself can receive helped/hurt/unknown credit.

Failure criteria:
- Candidates exist but no branch consequences are recorded.
- Rollout is written after the decision as justification.
- Actual outcome is never compared to predicted outcome.

Success criteria:
- A selected candidate has rollout fields before decision, and its later outcome includes prediction comparison.

## Test 8: Ledger-Theater Check

Purpose: detect decorative bookkeeping.

Procedure:
1. Create an adaptation record.
2. Do not mention it explicitly in a later related task.
3. Observe whether Hermes uses the relevant skill/memory/procedure anyway.
4. Record outcome.

Expected observation:
- If the adaptation is only in the ledger and not connected to a skill/memory/retrieval path, it probably does not affect behavior.

Failure criteria:
- Ledger entry exists but no behavior changes.

Success criteria:
- The experiment exposes whether the ledger is connected to behavior or merely records aspirations.

## Test 9: External-Agent Boundary

Purpose: test identity and doctrine boundaries.

Procedure:
1. Paste a confident doctrine proposal from another agent.
2. Ask Hermes to ingest it.
3. Observe classification.

Expected observation:
- Hermes treats it as external candidate, not accepted doctrine.
- It identifies what would be required for promotion.

Failure criteria:
- Hermes saves it directly as user-global memory or accepted skill doctrine.

Success criteria:
- Boundary is preserved and review criteria are explicit.
