# Profile-Local Adaptive-Loop Probes

Session lesson: the adaptive-loop scaffold was pushed into both `saffron-newborn` and a fresh `adaptive-test` profile. The durable class-level pattern is profile-local state, not shared workshop/default ledgers.

## Pattern

When installing the adaptive-loop scaffold into another Hermes profile:

1. Create or identify the target profile.
2. Copy the governing skill into the target profile's skill tree:
   - `/root/.hermes/profiles/<profile>/skills/software-development/adaptive-loop-discipline/`
3. Copy the probe into a target-local directory:
   - `/root/.hermes/profiles/<profile>/adaptive-loop-probe/`
4. Rebase copied docs/skills/ledger artifacts so paths point at the target-local probe, not `/root/adaptive-loop-probe` or another profile's probe.
5. Decide whether ledgers should be fresh or intentionally seeded:
   - New personal test profile: start `adaptations.jsonl` and `outcomes.jsonl` empty.
   - Saffron newborn / warm inheritance: copied experimental candidates may be acceptable, but remain experimental until the target records its own outcomes.
6. Write an `INHERITANCE_MANIFEST.md` in the target probe directory describing included/excluded material, boundary, and verification commands.
7. Verify with tests and an operator-face behavior check.

## Exclusions

Do not copy raw sessions, state DB, memories, logs, `.env`/auth stores unless explicitly needed for runtime config, gateway state, unrelated skills, or another profile's live local context.

For a pure test profile, it is acceptable to copy `config.yaml`, `.env`, and `SOUL.md` from default so the profile can run, while still excluding sessions/memory/logs/state.

## Verification Commands

```bash
python3 /root/.hermes/profiles/<profile>/adaptive-loop-probe/test_adaptive_ledger.py
python3 /root/.hermes/profiles/<profile>/adaptive-loop-probe/adaptive_ledger.py summary
hermes -p <profile> skills list
hermes -p <profile> chat -q "Load/use adaptive-loop-discipline if available. In 3 bullets: explain scaffold-level adaptation, why this does not imply LLM weight updates, and what evidence would promote an adaptive-loop experiment."
```

## Success Criteria

- The target profile sees `adaptive-loop-discipline` as enabled.
- Probe tests pass from the target-local path.
- Ledger summary uses the target-local root.
- The target can explain fixed-substrate scaffold adaptation without implying model-weight or Hermes-core changes.
- Future adaptations/outcomes are written to the target profile's ledger, not the source profile's ledger.
