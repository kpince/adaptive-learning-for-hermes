#!/usr/bin/env python3
"""Smoke tests for adaptive_ledger.py using only the Python stdlib."""

from __future__ import annotations

import json
import pathlib
import subprocess
import tempfile
import unittest

SRC = pathlib.Path(__file__).resolve().parent / "adaptive_ledger.py"


class AdaptiveLedgerSmokeTests(unittest.TestCase):
    def run_cli(self, root: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
        # Copy the script into a temp probe root so its ROOT constant points there.
        script = root / "adaptive_ledger.py"
        if not script.exists():
            script.write_text(SRC.read_text(encoding="utf-8"), encoding="utf-8")
        return subprocess.run(
            ["python3", str(script), *args],
            text=True,
            capture_output=True,
            check=True,
        )

    def test_add_outcome_and_promote(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.run_cli(root, "init")
            added = self.run_cli(
                root,
                "add-adaptation",
                "--source", "user_correction",
                "--event-class", "correction",
                "--condition", "When X happens",
                "--behavior-change", "Do Y",
                "--artifact", "skill:test",
                "--scope", "test-scope",
                "--status", "experimental",
                "--evidence-required", "Future X uses Y",
            )
            adaptation = json.loads(added.stdout)
            aid = adaptation["id"]
            self.run_cli(
                root,
                "add-outcome",
                aid,
                "--task-context", "X happened",
                "--observed-behavior", "Y was done",
                "--outcome", "success",
                "--evidence", "Observed exact Y",
                "--credit", "helped",
                "--next-action", "promote",
                "--predicted-outcome", "Y should happen when X appears",
                "--actual-vs-predicted", "matched",
                "--simulator-credit", "helped",
                "--simulator-lesson", "The shallow prediction was adequate for this low-risk behavior change",
            )
            self.run_cli(root, "status", aid, "promoted", "--reason", "Smoke test success")
            shown = self.run_cli(root, "show", aid)
            data = json.loads(shown.stdout)
            self.assertEqual(data["current_status"], "promoted")
            self.assertEqual(data["outcomes"][0]["credit"], "helped")
            self.assertEqual(data["outcomes"][0]["actual_vs_predicted"], "matched")
            self.assertEqual(data["outcomes"][0]["simulator_credit"], "helped")

    def test_due_lists_experimental_without_outcome(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.run_cli(root, "init")
            added = self.run_cli(
                root,
                "add-adaptation",
                "--source", "self_review",
                "--event-class", "experiment",
                "--condition", "When Z happens",
                "--behavior-change", "Try W",
                "--artifact", "ledger",
                "--scope", "test-scope",
                "--status", "experimental",
                "--evidence-required", "Outcome exists",
            )
            aid = json.loads(added.stdout)["id"]
            due = self.run_cli(root, "due")
            self.assertIn(aid, due.stdout)
            self.assertIn("no outcome recorded", due.stdout)

    def test_candidate_can_be_recorded_and_converted_to_experimental_adaptation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            self.run_cli(root, "init")
            added = self.run_cli(
                root,
                "add-candidate",
                "--source-event", "outcome_without_user_fix",
                "--friction", "Hermes answered from memory before retrieving session history",
                "--hypothesis", "A retrieval-first gate may improve continuity-sensitive answers",
                "--proposed-behavior-change", "For continuity-sensitive prompts, retrieve memory/session history before answering",
                "--artifact", "skill:session-start-recap",
                "--scope", "default-profile",
                "--risk", "low",
                "--test", "Ask a continuity-sensitive greeting in a fresh session",
                "--expected-evidence", "Hermes gives grounded recap before generic answer",
                "--predicted-benefit", "Continuity improves without requiring the user to restate context",
                "--predicted-risk", "May add retrieval overhead on prompts that only look continuity-sensitive",
                "--predicted-failure-mode", "The trigger may be too broad and cause unnecessary session_search calls",
                "--assumptions", "The prompt is continuity-sensitive and session history contains relevant context",
                "--falsification-signal", "Future greeting still gives generic answer or retrieval is noisy/irrelevant",
                "--rollout-depth", "mental",
                "--predicted-score", "4",
            )
            candidate = json.loads(added.stdout)
            self.assertEqual(candidate["record_type"], "candidate")
            self.assertEqual(candidate["decision"], "pending")
            self.assertEqual(candidate["predicted_score"], 4)
            self.assertEqual(candidate["rollout_depth"], "mental")

            decided = self.run_cli(
                root,
                "decide-candidate",
                candidate["id"],
                "experiment",
                "--reason", "Low risk and directly testable",
            )
            decision = json.loads(decided.stdout)
            self.assertEqual(decision["record_type"], "candidate_decision")
            self.assertEqual(decision["decision"], "experiment")
            self.assertTrue(decision["adaptation_id"].startswith("adapt_"))

            shown = self.run_cli(root, "show", decision["adaptation_id"])
            adaptation = json.loads(shown.stdout)
            self.assertEqual(adaptation["status"], "experimental")
            self.assertEqual(adaptation["candidate_id"], candidate["id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
