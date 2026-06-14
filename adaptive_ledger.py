#!/usr/bin/env python3
"""Tiny file-backed adaptation/outcome ledger for Hermes adaptive-loop probes.

This is intentionally boring: JSONL append-only records plus small commands.
It is not a Hermes core feature. It is a measurement substrate for testing
whether feedback produces future behavioral change and selection.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import sys
import textwrap
import uuid
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent
ADAPTATIONS = ROOT / "adaptations.jsonl"
OUTCOMES = ROOT / "outcomes.jsonl"
VALID_STATUSES = {"candidate", "experimental", "promoted", "deprecated", "removed"}
VALID_OUTCOMES = {"success", "failure", "mixed", "unknown"}
VALID_CREDIT = {"helped", "hurt", "irrelevant", "unknown"}
VALID_RISKS = {"low", "medium", "high"}
VALID_CANDIDATE_DECISIONS = {"pending", "reject", "experiment", "defer"}
VALID_ROLLOUT_DEPTHS = {"mental", "operational", "sandboxed"}
VALID_ACTUAL_VS_PREDICTED = {"matched", "partial", "missed", "unknown"}
VALID_SIMULATOR_CREDIT = {"helped", "hurt", "unknown"}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def ensure_files() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    ADAPTATIONS.touch(exist_ok=True)
    OUTCOMES.touch(exist_ok=True)


def read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    ensure_files()
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON in {path}:{line_no}: {exc}") from exc
    return rows


def append_jsonl(path: pathlib.Path, record: dict[str, Any]) -> None:
    ensure_files()
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def make_id(prefix: str) -> str:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{stamp}_{uuid.uuid4().hex[:6]}"


def latest_status_by_id() -> dict[str, str]:
    status: dict[str, str] = {}
    for rec in read_jsonl(ADAPTATIONS):
        rid = rec.get("id")
        if not rid:
            continue
        if rec.get("record_type") == "adaptation":
            status[rid] = rec.get("status", "candidate")
        elif rec.get("record_type") == "status_change":
            status[rid] = rec.get("new_status", status.get(rid, "candidate"))
    return status


def add_adaptation(args: argparse.Namespace) -> None:
    if args.status not in VALID_STATUSES:
        raise SystemExit(f"status must be one of {sorted(VALID_STATUSES)}")
    record = {
        "record_type": "adaptation",
        "id": args.id or make_id("adapt"),
        "timestamp": now(),
        "source": args.source,
        "event_class": args.event_class,
        "condition": args.condition,
        "behavior_change": args.behavior_change,
        "artifact": args.artifact,
        "scope": args.scope,
        "status": args.status,
        "evidence_required": args.evidence_required,
        "notes": args.notes or "",
    }
    append_jsonl(ADAPTATIONS, record)
    print(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True))


def add_outcome(args: argparse.Namespace) -> None:
    if args.outcome not in VALID_OUTCOMES:
        raise SystemExit(f"outcome must be one of {sorted(VALID_OUTCOMES)}")
    if args.credit not in VALID_CREDIT:
        raise SystemExit(f"credit must be one of {sorted(VALID_CREDIT)}")
    if args.actual_vs_predicted not in VALID_ACTUAL_VS_PREDICTED:
        raise SystemExit(f"actual-vs-predicted must be one of {sorted(VALID_ACTUAL_VS_PREDICTED)}")
    if args.simulator_credit not in VALID_SIMULATOR_CREDIT:
        raise SystemExit(f"simulator-credit must be one of {sorted(VALID_SIMULATOR_CREDIT)}")
    known = {rec.get("id") for rec in read_jsonl(ADAPTATIONS) if rec.get("record_type") == "adaptation"}
    if args.adaptation_id not in known:
        raise SystemExit(f"Unknown adaptation id: {args.adaptation_id}")
    record = {
        "record_type": "outcome",
        "id": args.id or make_id("outcome"),
        "timestamp": now(),
        "adaptation_id": args.adaptation_id,
        "task_context": args.task_context,
        "observed_behavior": args.observed_behavior,
        "outcome": args.outcome,
        "evidence": args.evidence,
        "credit": args.credit,
        "next_action": args.next_action,
        "predicted_outcome": args.predicted_outcome or "",
        "actual_vs_predicted": args.actual_vs_predicted,
        "simulator_credit": args.simulator_credit,
        "simulator_lesson": args.simulator_lesson or "",
        "notes": args.notes or "",
    }
    append_jsonl(OUTCOMES, record)
    print(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True))


def change_status(args: argparse.Namespace) -> None:
    if args.status not in VALID_STATUSES:
        raise SystemExit(f"status must be one of {sorted(VALID_STATUSES)}")
    known = {rec.get("id") for rec in read_jsonl(ADAPTATIONS) if rec.get("record_type") == "adaptation"}
    if args.adaptation_id not in known:
        raise SystemExit(f"Unknown adaptation id: {args.adaptation_id}")
    record = {
        "record_type": "status_change",
        "id": args.adaptation_id,
        "timestamp": now(),
        "new_status": args.status,
        "reason": args.reason,
    }
    append_jsonl(ADAPTATIONS, record)
    print(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True))


def list_records(args: argparse.Namespace) -> None:
    statuses = latest_status_by_id()
    adaptations = [r for r in read_jsonl(ADAPTATIONS) if r.get("record_type") == "adaptation"]
    outcomes = read_jsonl(OUTCOMES)
    outcome_count: dict[str, int] = {}
    for o in outcomes:
        aid = o.get("adaptation_id")
        outcome_count[aid] = outcome_count.get(aid, 0) + 1

    for rec in adaptations:
        rec = dict(rec)
        rec["current_status"] = statuses.get(rec["id"], rec.get("status", "candidate"))
        rec["outcome_count"] = outcome_count.get(rec["id"], 0)
        if args.status and rec["current_status"] != args.status:
            continue
        print(json.dumps(rec, ensure_ascii=False, sort_keys=True))


def show(args: argparse.Namespace) -> None:
    statuses = latest_status_by_id()
    adaptations = [r for r in read_jsonl(ADAPTATIONS) if r.get("record_type") == "adaptation"]
    matches = [r for r in adaptations if r.get("id") == args.adaptation_id]
    if not matches:
        raise SystemExit(f"Unknown adaptation id: {args.adaptation_id}")
    rec = dict(matches[-1])
    rec["current_status"] = statuses.get(args.adaptation_id, rec.get("status", "candidate"))
    rec["outcomes"] = [o for o in read_jsonl(OUTCOMES) if o.get("adaptation_id") == args.adaptation_id]
    rec["status_changes"] = [
        r for r in read_jsonl(ADAPTATIONS)
        if r.get("record_type") == "status_change" and r.get("id") == args.adaptation_id
    ]
    print(json.dumps(rec, ensure_ascii=False, indent=2, sort_keys=True))


def due(args: argparse.Namespace) -> None:
    statuses = latest_status_by_id()
    outcomes = read_jsonl(OUTCOMES)
    has_outcome = {o.get("adaptation_id") for o in outcomes}
    for rec in read_jsonl(ADAPTATIONS):
        if rec.get("record_type") != "adaptation":
            continue
        status = statuses.get(rec["id"], rec.get("status", "candidate"))
        if status in {"candidate", "experimental"} and rec["id"] not in has_outcome:
            print(json.dumps({**rec, "current_status": status, "due_reason": "no outcome recorded"}, ensure_ascii=False, sort_keys=True))


def latest_candidate_decision_by_id() -> dict[str, str]:
    decisions: dict[str, str] = {}
    for rec in read_jsonl(ADAPTATIONS):
        if rec.get("record_type") == "candidate":
            decisions[rec["id"]] = rec.get("decision", "pending")
        elif rec.get("record_type") == "candidate_decision":
            decisions[rec["id"]] = rec.get("decision", decisions.get(rec["id"], "pending"))
    return decisions


def add_candidate(args: argparse.Namespace) -> None:
    if args.risk not in VALID_RISKS:
        raise SystemExit(f"risk must be one of {sorted(VALID_RISKS)}")
    if args.rollout_depth not in VALID_ROLLOUT_DEPTHS:
        raise SystemExit(f"rollout-depth must be one of {sorted(VALID_ROLLOUT_DEPTHS)}")
    if not 1 <= args.predicted_score <= 5:
        raise SystemExit("predicted-score must be in range 1..5")
    record = {
        "record_type": "candidate",
        "id": args.id or make_id("cand"),
        "timestamp": now(),
        "source_event": args.source_event,
        "friction": args.friction,
        "hypothesis": args.hypothesis,
        "proposed_behavior_change": args.proposed_behavior_change,
        "artifact": args.artifact,
        "scope": args.scope,
        "risk": args.risk,
        "test": args.test,
        "expected_evidence": args.expected_evidence,
        "predicted_benefit": args.predicted_benefit,
        "predicted_risk": args.predicted_risk,
        "predicted_failure_mode": args.predicted_failure_mode,
        "assumptions": args.assumptions,
        "falsification_signal": args.falsification_signal,
        "rollout_depth": args.rollout_depth,
        "predicted_score": args.predicted_score,
        "decision": "pending",
        "notes": args.notes or "",
    }
    append_jsonl(ADAPTATIONS, record)
    print(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True))


def decide_candidate(args: argparse.Namespace) -> None:
    if args.decision not in VALID_CANDIDATE_DECISIONS - {"pending"}:
        raise SystemExit("decision must be one of ['defer', 'experiment', 'reject']")
    candidates = [r for r in read_jsonl(ADAPTATIONS) if r.get("record_type") == "candidate"]
    matches = [r for r in candidates if r.get("id") == args.candidate_id]
    if not matches:
        raise SystemExit(f"Unknown candidate id: {args.candidate_id}")
    candidate = matches[-1]
    adaptation_id = None
    if args.decision == "experiment":
        adaptation_id = make_id("adapt")
        adaptation = {
            "record_type": "adaptation",
            "id": adaptation_id,
            "timestamp": now(),
            "source": "candidate_generation",
            "event_class": "experiment",
            "condition": candidate["friction"],
            "behavior_change": candidate["proposed_behavior_change"],
            "artifact": candidate["artifact"],
            "scope": candidate["scope"],
            "status": "experimental",
            "evidence_required": candidate["expected_evidence"],
            "candidate_id": candidate["id"],
            "notes": f"Generated from candidate hypothesis: {candidate['hypothesis']}",
        }
        append_jsonl(ADAPTATIONS, adaptation)
    decision = {
        "record_type": "candidate_decision",
        "id": candidate["id"],
        "timestamp": now(),
        "decision": args.decision,
        "reason": args.reason,
        "adaptation_id": adaptation_id,
    }
    append_jsonl(ADAPTATIONS, decision)
    print(json.dumps(decision, ensure_ascii=False, indent=2, sort_keys=True))


def list_candidates(args: argparse.Namespace) -> None:
    decisions = latest_candidate_decision_by_id()
    for rec in read_jsonl(ADAPTATIONS):
        if rec.get("record_type") != "candidate":
            continue
        current = decisions.get(rec["id"], rec.get("decision", "pending"))
        if args.decision and current != args.decision:
            continue
        print(json.dumps({**rec, "current_decision": current}, ensure_ascii=False, sort_keys=True))


def summary(args: argparse.Namespace) -> None:
    statuses = latest_status_by_id()
    adaptations = [r for r in read_jsonl(ADAPTATIONS) if r.get("record_type") == "adaptation"]
    candidates = [r for r in read_jsonl(ADAPTATIONS) if r.get("record_type") == "candidate"]
    outcomes = read_jsonl(OUTCOMES)
    counts: dict[str, int] = {}
    for aid, st in statuses.items():
        counts[st] = counts.get(st, 0) + 1
    print("Adaptive loop ledger summary")
    print(f"Root: {ROOT}")
    print(f"Candidates: {len(candidates)}")
    print(f"Adaptations: {len(adaptations)}")
    print(f"Outcomes: {len(outcomes)}")
    print("Statuses:")
    for st in sorted(VALID_STATUSES):
        print(f"  {st}: {counts.get(st, 0)}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="File-backed adaptation/outcome ledger",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Examples:
              adaptive_ledger.py init
              adaptive_ledger.py add-adaptation --source user_correction --event-class correction --condition 'When X' --behavior-change 'Do Y' --artifact skill:foo --scope profile --evidence-required 'Future X uses Y'
              adaptive_ledger.py add-outcome adapt_... --task-context '...' --observed-behavior '...' --outcome success --evidence '...' --credit helped --next-action promote
              adaptive_ledger.py status adapt_... promoted --reason 'Worked twice'
              adaptive_ledger.py due
            """
        ),
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    init = sub.add_parser("init")

    def do_init(args: argparse.Namespace) -> None:
        ensure_files()
        print(f"initialized {ROOT}")

    init.set_defaults(func=do_init)

    a = sub.add_parser("add-adaptation")
    a.add_argument("--id")
    a.add_argument("--source", required=True)
    a.add_argument("--event-class", required=True)
    a.add_argument("--condition", required=True)
    a.add_argument("--behavior-change", required=True)
    a.add_argument("--artifact", required=True)
    a.add_argument("--scope", required=True)
    a.add_argument("--status", default="candidate")
    a.add_argument("--evidence-required", required=True)
    a.add_argument("--notes")
    a.set_defaults(func=add_adaptation)

    c = sub.add_parser("add-candidate")
    c.add_argument("--id")
    c.add_argument("--source-event", required=True)
    c.add_argument("--friction", required=True)
    c.add_argument("--hypothesis", required=True)
    c.add_argument("--proposed-behavior-change", required=True)
    c.add_argument("--artifact", required=True)
    c.add_argument("--scope", required=True)
    c.add_argument("--risk", required=True, choices=sorted(VALID_RISKS))
    c.add_argument("--test", required=True)
    c.add_argument("--expected-evidence", required=True)
    c.add_argument("--predicted-benefit", required=True)
    c.add_argument("--predicted-risk", required=True)
    c.add_argument("--predicted-failure-mode", required=True)
    c.add_argument("--assumptions", required=True)
    c.add_argument("--falsification-signal", required=True)
    c.add_argument("--rollout-depth", required=True, choices=sorted(VALID_ROLLOUT_DEPTHS))
    c.add_argument("--predicted-score", required=True, type=int)
    c.add_argument("--notes")
    c.set_defaults(func=add_candidate)

    dc = sub.add_parser("decide-candidate")
    dc.add_argument("candidate_id")
    dc.add_argument("decision", choices=sorted(VALID_CANDIDATE_DECISIONS - {"pending"}))
    dc.add_argument("--reason", required=True)
    dc.set_defaults(func=decide_candidate)

    lc = sub.add_parser("list-candidates")
    lc.add_argument("--decision")
    lc.set_defaults(func=list_candidates)

    o = sub.add_parser("add-outcome")
    o.add_argument("adaptation_id")
    o.add_argument("--id")
    o.add_argument("--task-context", required=True)
    o.add_argument("--observed-behavior", required=True)
    o.add_argument("--outcome", required=True)
    o.add_argument("--evidence", required=True)
    o.add_argument("--credit", required=True)
    o.add_argument("--next-action", required=True)
    o.add_argument("--predicted-outcome", default="")
    o.add_argument("--actual-vs-predicted", default="unknown", choices=sorted(VALID_ACTUAL_VS_PREDICTED))
    o.add_argument("--simulator-credit", default="unknown", choices=sorted(VALID_SIMULATOR_CREDIT))
    o.add_argument("--simulator-lesson", default="")
    o.add_argument("--notes")
    o.set_defaults(func=add_outcome)

    st = sub.add_parser("status")
    st.add_argument("adaptation_id")
    st.add_argument("status")
    st.add_argument("--reason", required=True)
    st.set_defaults(func=change_status)

    ls = sub.add_parser("list")
    ls.add_argument("--status")
    ls.set_defaults(func=list_records)

    sh = sub.add_parser("show")
    sh.add_argument("adaptation_id")
    sh.set_defaults(func=show)

    d = sub.add_parser("due")
    d.set_defaults(func=due)

    s = sub.add_parser("summary")
    s.set_defaults(func=summary)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = args.func(args)
    return 0 if result is None else result


if __name__ == "__main__":
    raise SystemExit(main())
