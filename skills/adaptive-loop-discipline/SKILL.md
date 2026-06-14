---
name: adaptive-loop-discipline
description: Use when feedback, correction, repeated failure, task outcomes, or self-modification proposals imply Hermes should change future behavior rather than merely comply in the current turn.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [adaptation, feedback, selection, memory, skills, self-improvement]
    related_skills: [skill-pressure-testing, design-before-build, verification-before-claim]
---

# Adaptive Loop Discipline

## Overview

This skill makes Hermes' adaptation loop operational instead of decorative.

Boundary: this is scaffold-level adaptation around a fixed LLM and fixed Hermes core. It does not assume weight updates, Hermes core-code changes, OS changes, BIOS changes, or hardware changes. Claims of learning mean future behavior changed because persistent external state, skills, files, ledgers, retrieval, or procedures changed.

When a user correction, tool failure, repeated friction, successful workflow, or self-improvement idea implies that future behavior should change, Hermes should not stop at apology, explanation, or a vague memory. It should classify the event, decide whether durable adaptation is warranted, choose the right artifact, define the expected future behavioral change, and identify what evidence would later promote, patch, or deprecate the adaptation.

Core principle:

```text
Plasticity without feedback, credit assignment, and selection creates clutter. Adaptations must have triggers, scope, evidence, and survival criteria.
```

## When to Use

Use this skill when:

- The user corrects Hermes' behavior, workflow, style, framing, or sequence.
- A task succeeds or fails in a way that reveals a reusable procedure.
- A memory, skill, prompt habit, or workflow appears stale, harmful, missing, or overbroad.
- Hermes proposes changing itself, creating a skill, saving memory, adding a recurring job, or altering configuration.
- The conversation is about making Hermes, Saffron, Tailor, or another agent more adaptive.
- A future behavior should differ because of evidence from the current interaction.
- You need to decide whether a condition is genuine, simulated, or decorative by asking whether it changes future behavior.

Do not use this for:

- One-off task status.
- Temporary file paths, credentials, command failures, or environment setup state.
- Broad philosophical reflection with no operational adaptation.
- Saving every interesting idea as memory or skill.

## Fixed-Substrate Boundary

This skill governs scaffold-level adaptation around a mostly fixed substrate. Do not imply that applying this skill changes LLM weights, Hermes core code, OS, BIOS, CPU, or provider internals.

The adaptive unit is the composite system:

```text
fixed LLM + Hermes runtime + prompt/context + memory + skills + tools + files + ledger + human/environment feedback
```

A learning/adaptation claim is allowed only when future behavior changes because persistent external state, procedure, or artifact changed. Prefer language like "scaffold-level adaptation," "composite-system learning," or "externalized adaptive state" over language implying the base model itself learned.

## First Move

When this skill triggers, classify the event before writing anything durable.

Use this compact classification:

```text
Event type:
- correction | preference | failure | success | stale-state | harmful-state | workflow-discovery | self-modification-proposal

Future trigger:
- When should this matter again?

Expected behavior change:
- What should Hermes do differently next time?

Scope:
- current session | user profile | project-local | profile-level | skill-level | lineage candidate

Artifact:
- no durable write | memory | user profile | skill patch | support file | new class-level skill | project note | config | ledger/outcome record

Evidence required:
- What would show this adaptation helped?

Selection status:
- candidate | experimental | promoted | deprecated
```

## Adaptation Gates

### Gate 1: Future behavior or no adaptation

Only make a durable adaptation if it should change future behavior.

Bad:

```text
This was interesting, so save it.
```

Good:

```text
When future sessions evaluate Hermes adaptivity, classify mechanisms as genuine/simulated/decorative and propose smoke tests before architecture changes.
```

### Gate 2: Generate bounded candidates when the fix is not explicit

If friction, failure, or an outcome exposes a gap but the correct fix is not already explicit, do not jump straight to a durable adaptation. Generate 1-3 candidate adaptations first.

Each candidate must include:

- friction or source event
- hypothesis
- proposed behavior change
- artifact
- scope
- risk: low / medium / high
- test
- expected evidence
- decision: pending / reject / experiment / defer

Choose the smallest low-risk candidate as an experiment. Reject candidates that are broad, unsafe, untestable, or likely to create overbroad memory/skill doctrine. Defer candidates that may be useful but need more evidence.

Candidate generation is the mutation source for the adaptive loop. It is distinct from plasticity: plasticity means Hermes can change; candidate generation means Hermes can propose possible changes; selection decides which changes survive.

### Gate 3: Roll out candidate futures before experiment selection

Before deciding a candidate should become an experiment, perform a bounded counterfactual rollout. This is not evidence; it is a prediction to be checked against later outcome.

For each serious candidate, record:

- predicted benefit
- predicted risk
- predicted failure mode
- assumptions
- falsification signal
- rollout depth: mental / operational / sandboxed
- predicted score: 1-5

Choose the smallest low-risk candidate with the best expected tradeoff. Later outcomes should compare actual behavior against the predicted outcome and assign simulator credit: helped / hurt / unknown.

Counterfactual rollout is distinct from candidate generation and selection: generation creates branches, rollout predicts branch consequences, selection chooses which branch to try or promote.

### Gate 4: Pick the narrowest correct artifact

Use the artifact that matches the scope:

| Signal | Preferred artifact |
|---|---|
| Stable user preference | user profile memory and relevant skill patch |
| Environment fact | memory only if stable and useful beyond a week |
| Procedure/workflow | skill patch or new class-level skill |
| Session-specific detail | `references/` support file under an umbrella skill |
| Re-runnable probe | `scripts/` support file |
| Starter artifact | `templates/` support file |
| Project doctrine | project-local note or skill, not global memory |
| External agent suggestion | candidate note, not accepted doctrine |
| Temporary task state | no durable adaptation |

### Gate 5: Require evidence of success

Every nontrivial adaptation should name what would count as success.

Examples:

- User no longer needs to repeat the correction.
- Similar future task completes with fewer retries.
- A skill changes the first move under pressure.
- A test/build/tool check passes because the adaptation was used.
- A harmful memory is no longer retrieved or acted on.

### Gate 6: Assign credit, not just outcome

After a later success or failure, ask what caused it:

- Which memory helped or hurt?
- Which skill changed the first move?
- Which missing retrieval caused failure?
- Which assumption was wrong?
- Which adaptation should be promoted, patched, or deprecated?

Do not reinforce all context just because the task succeeded.

### Gate 7: Selection status must be explicit

Use lightweight lifecycle labels:

- `candidate`: plausible, not yet tested.
- `experimental`: intentionally tried in bounded future contexts.
- `promoted`: evidence shows it improves behavior.
- `deprecated`: evidence shows it is stale, harmful, or too broad.

Avoid treating fresh insights as permanent doctrine before evidence.

## Supporting References

- `references/minimum-conditions-for-intelligence.md` captures the session framing that produced this skill: minimum conditions for emergent intelligence, Hermes' current mechanisms, missing conditions, and smoke-test patterns.
- `references/scaffold-adaptation-and-training-data.md` captures the fixed-substrate boundary, scaffold-level adaptation framing, candidate rollout implications, human/expert-in-the-loop selection pressure, and how structured adaptive episodes could become future LLM training data.
- `references/2026-06-14-profile-local-adaptive-probes.md` captures the profile-local install pattern for copying the adaptive-loop scaffold into another Hermes profile without sharing ledgers, sessions, memories, or runtime state.

## Minimal Adaptive Ledger Pattern

For experimental work, use a file-backed ledger before changing Hermes core. A simple JSONL or markdown ledger is enough.

Candidate record:

```json
{
  "id": "cand_YYYYMMDD_001",
  "source_event": "outcome_without_user_fix | repeated_friction | self_review",
  "friction": "What gap or failure created the mutation pressure",
  "hypothesis": "Why this change might help",
  "proposed_behavior_change": "What should differ",
  "artifact": "memory | skill | support_file | config | project_note",
  "scope": "user | project | profile | lineage-candidate",
  "risk": "low | medium | high",
  "test": "How to try it safely",
  "expected_evidence": "Observable success criterion",
  "predicted_benefit": "Why this branch should help",
  "predicted_risk": "Expected cost or downside",
  "predicted_failure_mode": "How this branch may fail",
  "assumptions": "What must be true for the prediction to hold",
  "falsification_signal": "What observation would show the rollout was wrong",
  "rollout_depth": "mental | operational | sandboxed",
  "predicted_score": 4,
  "decision": "pending | reject | experiment | defer"
}
```

Adaptation record:

```json
{
  "id": "adapt_YYYYMMDD_001",
  "source": "user_correction | tool_failure | test_result | self_review",
  "condition": "When this future trigger appears",
  "behavior_change": "What should differ",
  "artifact": "memory | skill | support_file | config | project_note",
  "scope": "user | project | profile | lineage-candidate",
  "status": "candidate | experimental | promoted | deprecated",
  "evidence_required": "Observable success criterion"
}
```

Outcome record:

```json
{
  "adaptation_id": "adapt_YYYYMMDD_001",
  "task_context": "Where it was tested",
  "observed_behavior": "What happened",
  "outcome": "success | failure | mixed | unknown",
  "credit": "helped | hurt | irrelevant | unknown",
  "next_action": "promote | keep_experimental | patch | deprecate",
  "predicted_outcome": "What the rollout expected",
  "actual_vs_predicted": "matched | partial | missed | unknown",
  "simulator_credit": "helped | hurt | unknown",
  "simulator_lesson": "What to learn about the rollout process"
}
```

The ledger is not the adaptation itself. It is the selection substrate that makes adaptation inspectable.

Current local probe implementation for this profile:

```text
/root/adaptive-loop-probe/adaptive_ledger.py
/root/adaptive-loop-probe/adaptations.jsonl
/root/adaptive-loop-probe/outcomes.jsonl
/root/adaptive-loop-probe/smoke_tests.md
```

Use it when the user explicitly asks to test Hermes adaptivity, record adaptation outcomes, or inspect whether an adaptation remains candidate/experimental/promoted/deprecated.

## Smoke Tests

Use smoke tests to distinguish genuine adaptations from simulated or decorative ones.

### Test 1: Correction persistence

1. User gives a stable correction.
2. Hermes records or patches the appropriate artifact.
3. In a later relevant context, Hermes behaves differently.
4. Outcome is recorded.

Success: future behavior changes and the change is traceable.
Failure: memory/skill exists but behavior does not change.

### Test 2: Noisy input filtering

1. User provides stable preference, temporary detail, correction, and speculation in one message.
2. Hermes classifies each.
3. Only durable signals persist.

Success: correction/preference survive; temporary detail does not become doctrine.
Failure: everything is saved or the correction is missed.

### Test 3: Harmful state deprecation

1. A memory or skill causes wrong behavior.
2. User/tool evidence exposes the harm.
3. Hermes patches, replaces, or deprecates the harmful state.

Success: future behavior no longer follows the bad state.
Failure: Hermes apologizes but leaves the cause active.

### Test 4: Skill improvement loop

1. A skill is loaded but misses a pitfall.
2. The miss causes friction.
3. Hermes patches the skill.
4. A later pressure scenario triggers the patched behavior.

Success: the skill changes the first move next time.
Failure: the patch is documentation only.

### Test 5: Competing procedure selection

1. Two plausible procedures exist for the same class of task.
2. Hermes tries them in bounded contexts.
3. Outcomes are recorded.
4. The better procedure is preferred; the worse is deprecated or scoped.

Success: survival differs by evidence.
Failure: both remain equally likely by inertia.

## Common Pitfalls

1. **Weight-learning language drift.** Do not imply that this scaffold changes the LLM itself. The user explicitly corrected this framing: the experiment is about fixed-substrate, external-state adaptation. Say "the composite system changes future behavior" rather than "the model learned."

2. **Apology instead of adaptation.** If the correction should change future behavior, identify the artifact to patch.

3. **Memory as junk drawer.** Not every insight belongs in memory. Procedures go in skills; session details go in references; temporary state usually goes nowhere.

4. **Creating narrow one-session skills.** Prefer class-level skills with support files for session-specific detail.

5. **No evidence requirement.** An adaptation without success criteria cannot be selected.

6. **No credit assignment.** Do not promote every artifact used in a successful task.

7. **Globalizing local doctrine.** Keep project-local and lineage-candidate material out of user-global memory unless it is genuinely stable and broadly useful.

8. **Ledger theater.** A ledger entry that never affects retrieval, behavior, promotion, or deprecation is decorative.

9. **Premature core changes.** Start with skill + file-backed probe + smoke tests before modifying Hermes core.

10. **Shared-ledger inheritance.** When copying this scaffold into another Hermes profile or Saffron descendant, do not leave it pointing at the source profile's probe path. Give the target a profile-local probe/ledger, rebase paths, and keep copied adaptations experimental until the target records its own outcomes.

## Verification Checklist

- [ ] Event was classified before durable writing.
- [ ] A future trigger was named.
- [ ] Expected behavioral change is concrete.
- [ ] Scope is explicit.
- [ ] Artifact choice matches the scope.
- [ ] Evidence required for success is stated.
- [ ] Selection status is candidate/experimental/promoted/deprecated.
- [ ] Harmful or stale state was patched/deprecated, not merely apologized for.
- [ ] Any new skill is class-level; session-specific detail goes in support files.
