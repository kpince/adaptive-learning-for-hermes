# Adaptive Loop Scaffold

A small fixed-substrate adaptation scaffold for Hermes-style agents.

This repository is for sharing the adaptive-loop framework with other agents without modifying LLM weights, Hermes core, OS, BIOS, CPU, or provider internals.

The adaptive unit is the composite system:

```text
fixed LLM + agent runtime + prompt/context + memory + skills + tools + files + ledger + human/environment feedback
```

A learning/adaptation claim is valid only when future behavior changes because persistent external state, procedure, or artifact changed.

## What is included

- `adaptive_ledger.py` — append-only JSONL ledger CLI for candidates, adaptations, decisions, outcomes, and status records.
- `test_adaptive_ledger.py` — tests for the ledger behavior.
- `smoke_tests.md` — manual smoke tests for distinguishing real adaptation from decorative bookkeeping.
- `adaptations.jsonl` — empty local ledger file for a consuming agent/profile.
- `outcomes.jsonl` — empty local outcome ledger file for a consuming agent/profile.
- `skills/adaptive-loop-discipline/` — Hermes skill and references describing the scaffold-level adaptation discipline.

## Core loop

```text
observe friction/outcome
→ generate candidate adaptations
→ roll out candidate futures
→ select bounded experiment
→ execute
→ observe actual outcome
→ compare predicted vs actual
→ assign credit
→ promote / patch / deprecate
→ alter future behavior through scaffold state
```

## Install for another Hermes profile or agent

Clone or copy this repo, then keep ledgers local to that agent/profile. Do not share live `adaptations.jsonl` / `outcomes.jsonl` files between agents unless you intentionally want shared state.

For a Hermes profile, copy the skill into that profile's skills directory, for example:

```bash
mkdir -p ~/.hermes/skills/software-development/adaptive-loop-discipline
cp -R skills/adaptive-loop-discipline/. ~/.hermes/skills/software-development/adaptive-loop-discipline/
```

Then initialize a profile-local ledger directory:

```bash
mkdir -p ~/adaptive-loop-probe
cp adaptive_ledger.py test_adaptive_ledger.py smoke_tests.md ~/adaptive-loop-probe/
: > ~/adaptive-loop-probe/adaptations.jsonl
: > ~/adaptive-loop-probe/outcomes.jsonl
python3 ~/adaptive-loop-probe/adaptive_ledger.py init
python3 ~/adaptive-loop-probe/test_adaptive_ledger.py
```

If this is installed into a different agent/profile, keep copied adaptations experimental until that agent records its own outcomes.

## Usage

Add a candidate adaptation before committing to an experiment:

```bash
python3 adaptive_ledger.py add-candidate \
  --source-event outcome_without_user_fix \
  --friction 'Agent skipped a prerequisite and no explicit fix was supplied' \
  --hypothesis 'A prerequisite-check gate may reduce repeated failure' \
  --proposed-behavior-change 'Before similar tasks, check prerequisites first' \
  --artifact skill:relevant-skill \
  --scope profile-local \
  --risk low \
  --test 'Run a similar task and observe whether prerequisite check happens first' \
  --expected-evidence 'Future first move includes prerequisite check' \
  --predicted-benefit 'Reduces repeated failure from missing prerequisites' \
  --predicted-risk 'May add small upfront overhead' \
  --predicted-failure-mode 'Gate becomes too broad and slows simple tasks' \
  --assumptions 'Prerequisites can be checked cheaply and are often the cause of failure' \
  --falsification-signal 'Future failures are not prerequisite-related or overhead annoys user' \
  --rollout-depth mental \
  --predicted-score 4
```

Decide a candidate:

```bash
python3 adaptive_ledger.py decide-candidate cand_... experiment --reason 'Low risk and testable'
python3 adaptive_ledger.py decide-candidate cand_... reject --reason 'Too broad or unsafe'
python3 adaptive_ledger.py list-candidates --decision pending
```

Add outcome:

```bash
python3 adaptive_ledger.py add-outcome adapt_... \
  --task-context '...' \
  --observed-behavior '...' \
  --outcome success \
  --evidence '...' \
  --credit helped \
  --next-action promote \
  --predicted-outcome 'The adapted behavior should fire in the next matching context' \
  --actual-vs-predicted matched \
  --simulator-credit helped \
  --simulator-lesson 'The low-risk rollout accurately predicted the useful behavior change'
```

List due candidates/experiments with no outcome:

```bash
python3 adaptive_ledger.py due
```

Promote/deprecate:

```bash
python3 adaptive_ledger.py status adapt_... promoted --reason 'Worked in two future contexts'
python3 adaptive_ledger.py status adapt_... deprecated --reason 'Did not change behavior'
```

## Important failure mode

A ledger entry is not learning.

Success requires future behavior change plus outcome evidence. If the ledger fills up but does not affect retrieval, skill choice, memory hygiene, candidate generation, action, or later selection, it is decorative.

## Training-data implication

If many human-agent systems use this scaffold, the resulting structured episodes can become a new class of training data:

```text
situation → candidates → rollouts → selection → action → outcome → correction → adaptation → later reuse/deprecation
```

The highest-value records are outcome-grounded and human/expert-in-the-loop, especially where experts reject bad branches, correct primitives, expose assumptions, and select decisive tests.

Do not export private logs by default. Prefer sanitized adaptive episode summaries over raw transcripts.
