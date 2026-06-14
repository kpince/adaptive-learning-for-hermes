# Scaffold Adaptation and Training Data

## Session Context

This reference captures the conceptual refinement around the adaptive-loop probe: the system is deliberately not modifying LLM weights, Hermes core code, OS, BIOS, CPU, or provider internals. It is building an external adaptive scaffold around a fixed model/runtime and asking whether the composite system changes future behavior.

## Fixed-Substrate Boundary

Use this framing:

```text
fixed LLM + Hermes runtime + prompt/context + memory + skills + tools + files + ledger + human/environment feedback
```

Allowed claim:

```text
The composite system adapted because persistent external state/procedure changed future behavior.
```

Avoid:

```text
The LLM learned.
The model updated itself.
Hermes changed its core cognition.
```

Unless weights/core code were actually modified, which this probe explicitly avoids.

## Scaffold-Level RSI

The loop can still be recursive at the scaffold level:

1. Adapt behavior through memory/skills/procedures.
2. Improve the adaptation discipline itself.
3. Add candidate generation when fixes are not explicit.
4. Add counterfactual rollout before selecting experiments.
5. Compare predicted outcomes with actual outcomes to improve the rollout heuristic.

This is weak/bounded RSI: the self-improvement target is the external adaptive machinery, not the base model weights.

## Human-in-the-Loop Requirement

Human-in-the-loop is not optional in this framing. The human supplies high-value selection pressure:

- goal/valence;
- salience;
- correction;
- branch culling;
- domain taste;
- boundary decisions;
- credit assignment when tool evidence is insufficient.

The system should amplify the human's selection function, not replace it.

## Expert-in-the-Loop Extension

If the humans in the loop are domain experts or world-class minds, the interaction can capture rare training signals:

- expert rejection of wrong primitives;
- candidate branch culling;
- counterfactual evaluation;
- experimental design corrections;
- what counts as evidence in the domain;
- why plausible candidates are misleading;
- how the expert reframes the problem.

This is more valuable than final expert answers alone. It captures expert judgment over possible futures.

## Training Data Implication

At scale, scaffold adaptation can become a data-generating outer loop for future weight adaptation.

Local loop:

```text
human + fixed LLM + scaffold -> interaction -> candidates -> rollout -> outcome -> selection -> improved scaffold behavior
```

Global loop:

```text
many structured human-agent adaptive episodes -> curated datasets/evals -> future LLM training/fine-tuning/preference models -> changed weights
```

The valuable data unit is an adaptive episode, not a chat message:

```text
situation -> goal/valence -> candidates -> predicted futures -> human/expert culling -> action -> outcome -> correction -> durable adaptation -> later reuse/failure
```

## Data Quality Warnings

Bad data version:

- unverified agent logs;
- self-justifying rationales;
- synthetic sludge;
- claimed success without outcome;
- private raw transcripts without consent.

Good data version:

- structured episodes;
- explicit human/expert corrections;
- rejected candidates and reasons;
- tool/user/outcome evidence;
- prediction-vs-actual comparison;
- deprecations and failures preserved;
- sanitized/consented export.

Failures and deprecations are first-class training data because they teach credit assignment and epistemic humility.

## Domain-Specific Potential

Each domain needs its own selection criteria:

- Physics: mathematical structure, invariance, decisive experiment, illegitimate simplification.
- Biology: controls, mechanism, context dependence, causal direction.
- Psychology: construct validity, confounds, operationalization, population variance.
- Mathematics: definitions, proof gaps, counterexamples, abstraction boundaries.
- Engineering: failure modes, interfaces, observability, maintainability.
- Medicine: differential diagnosis, risk, triage, evidence hierarchy.
- Organizations: incentives, tacit workflow, informal power, trust, lived operations.

The generic adaptive loop is the scaffold; expert-domain loops provide the domain valence and culling function.

## Practical Rule

When discussing this project, keep the ladder explicit:

1. Scaffold-level adaptation now.
2. Structured adaptive episodes as data.
3. Sanitized/evaluated datasets later.
4. Future LLM weight updates only at ecosystem/training time.

Do not blur these levels.
