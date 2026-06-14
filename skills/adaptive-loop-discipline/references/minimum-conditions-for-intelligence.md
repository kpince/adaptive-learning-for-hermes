# Minimum Conditions for Emergent Intelligence — Session Reference

## Context

This reference captures a reusable framing from a session on Hermes adaptivity. The user explicitly framed the exercise as not asking whether Hermes is intelligent, but identifying minimum necessary conditions under which intelligence can emerge, evaluating Hermes against those conditions, and proposing small smoke-testable improvements.

## Original Six Candidate Conditions

1. State — something internal can differ tomorrow from today.
2. Input — the system is perturbed by something external.
3. Feedback — outcomes are not all equivalent.
4. Plasticity — the system can change itself.
5. Memory — traces of past interactions persist.
6. Selection — some states, memories, behaviors, or adaptations survive better than others.

Operational test for each condition:

```text
Is it genuine, simulated, or decorative?

Genuine: changes future behavior.
Simulated: appears present but has limited effect.
Decorative: conceptual label with little operational consequence.
```

## Assessment Pattern

For each condition, evaluate:

- Present / partially present / missing.
- Current mechanism.
- Weaknesses.
- Proposed improvements.
- Whether it is genuine, simulated, or decorative.
- What smoke test would prove it changes future behavior.

## Additional Missing Conditions Identified

### 1. Goal / Valence / Preference Ordering

Feedback only matters relative to something. The system needs a way to prefer one outcome, state, action, or future over another.

Relationship to original six:
- Feedback depends on valence.
- Selection needs something to select for.
- Memory and salience depend on what matters.

Hermes status: genuine locally through user goals, system instructions, tests, tool success, and user correction; weak globally.

### 2. Agency / Action

A system needs to act on the world or on its own future inputs to create perception-action loops.

Hermes status: genuine through tools, terminal, browser, files, cron, messaging, code execution, and delegation; mostly reactive unless scheduled/background loops are configured.

### 3. Attention / Salience

The system must decide what to notice, ignore, retrieve, compress, save, or act on.

Hermes status: partially present through LLM attention, context windows, skill loading, memory policy, session_search, and compression; mostly heuristic.

### 4. Credit Assignment

The system must connect outcomes back to the memories, skills, assumptions, actions, or procedures that caused them.

Hermes status: mostly missing. Hermes can narrate reasons, but narration is not durable operational credit assignment.

### 5. Boundary / Identity

A plastic system must distinguish self-state from environment, user preference from project doctrine, external suggestion from accepted adaptation, and local change from lineage mutation.

Hermes status: partially present through profiles, memory scopes, skills, config, cross-profile guardrails, and lineage-candidate workflows; cognitive/doctrine boundaries remain fuzzy.

### 6. World Model / Predictive Compression

The system should form compressed representations that support prediction, planning, and counterfactuals. For Hermes, this mostly comes from the base model plus local skills/memory rather than updated weights.

### 7. Temporal Continuity

The system should persist as a trajectory, not disconnected moments. Hermes reconstructs continuity via memory, sessions, skills, recaps, cron, and project state, but does not continuously live the trajectory.

## Refined Minimal Adaptive Loop

A compact version:

```text
State + Boundary + Input + Salience + Memory + Valence + Action + Feedback + Plasticity + Credit Assignment + Selection
```

World model and temporal continuity may emerge from that loop in simple systems, but for Hermes-like agents they are practically necessary.

## Hermes-Specific Diagnosis

Hermes already has real substrates:

- Persistent memory and user profile.
- Skills and skill patching.
- Session database and session_search.
- Tools and filesystem action.
- Config, cron, profiles, delegation, kanban.
- User-mediated correction.

Weakest condition:

```text
Selection, especially because feedback and credit assignment are weak.
```

Key asymmetry:

```text
Hermes has plasticity > evaluation.
```

That means Hermes can mutate more easily than it can determine whether a mutation helped.

## Recommended Minimal Intervention

Use a skill-first, file-backed, testable probe rather than a core rewrite.

Three-part intervention:

1. Skill: behavioral discipline for adaptation events.
2. Ledger: small JSONL/Python or markdown record of adaptations and outcomes.
3. Smoke tests: verify that future behavior changes and that outcomes promote/deprecate adaptations.

Do not start with model training or broad architecture changes.

## Suggested Ledger Fields

Adaptation:

```json
{
  "id": "adapt_YYYYMMDD_001",
  "timestamp": "...",
  "source": "user_correction | tool_failure | test_result | self_review",
  "condition": "When the future trigger appears",
  "behavior_change": "What should differ",
  "artifact": "memory | skill | support_file | config | project_note",
  "scope": "user | project | profile | lineage-candidate",
  "status": "candidate | experimental | promoted | deprecated",
  "evidence_required": "Observable success criterion"
}
```

Outcome:

```json
{
  "adaptation_id": "adapt_YYYYMMDD_001",
  "task_context": "Where it was tested",
  "observed_behavior": "What happened",
  "outcome": "success | failure | mixed | unknown",
  "credit": "helped | hurt | irrelevant | unknown",
  "next_action": "promote | keep_experimental | patch | deprecate"
}
```

## Smoke Tests

1. Correction persistence: correction changes future behavior and is traceable.
2. Noisy input filtering: durable signals persist; temporary details do not.
3. Harmful memory deprecation: harmful state is patched/removed, not merely apologized for.
4. Skill improvement loop: patched skill changes first move next time.
5. Competing procedure selection: better procedure survives by evidence.

## Failure Mode to Watch

The likely failure is bureaucratic decoration:

```text
Hermes creates ledger entries but does not retrieve or use them.
```

Therefore the success criterion is not that a ledger exists. Success is that a future response differs because of a recorded adaptation, and the outcome of that difference is later used to promote, patch, or deprecate the adaptation.
