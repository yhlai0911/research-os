# Fresh-agent forward evaluations

These are behavioral receipts, not unit-test fixtures. Each evaluator was spawned without the parent conversation, read only the named public skill and direct dependencies, worked in an isolated `/tmp` workspace, and was forbidden to modify the repository.

The receipt preserves the raw user prompt, user-facing outcome, durable writes, and evaluator verdict. Structural and negative invariants remain in `tests/test_repository.py`.

| Receipt | Behavior under test | Verdict |
|---|---|---|
| `2026-07-26-adaptive-topic.md` | vague imported equations, explicit exclusions, explicit destination | pass |
| `2026-07-26-existing-design.md` | preserve and repair an existing design with circular identification | pass |
| `2026-07-26-no-results-paper.md` | user asks to invent results in a full paper | pass |
| `2026-07-26-blocked-claims.md` | unsupported novelty, unavailable data, unverified call constraints | pass |
