# Workspace contract

Load this reference only when initializing or adapting a research workspace.

## Canonical artifacts

| Path | Authority |
|---|---|
| `.research/config.yaml` | Contract version and canonical path registry |
| `.research/CONTEXT.md` | Research vocabulary, current question, scope, unresolved decisions, and the current-artifact index |
| `.research/decisions/` | One Research Decision Record per admitted consequential choice |
| `.research/evidence/claims.yaml` | Claim-to-source status ledger |
| `.research/maps/` | Multi-session decision maps |
| `.research/briefs/` | Approved research contracts |
| `.research/plans/` | Executable academic research plans |
| `.research/workpackages/` | Dependency-aware tracer studies |
| `.research/papers/` | Manuscript artifacts |
| `.research/proposals/` | Proposal artifacts |
| `.research/handoffs/` | Cross-session continuity manifests |
| `.research/reviews/` | Independent review reports and repair receipts |
| `.research/pilots/` | Pilot protocols, outputs, and go/no-go decisions |
| `.research/templates/` | Copyable artifact formats; never project evidence |

## Authority rules

1. Keep each meaning in one place. Link to an artifact instead of restating it.
2. Treat the evidence ledger as status, not proof. A source becomes evidence only after direct inspection and claim-level entailment.
3. Record a choice as a decision only when all four tests pass: costly to reverse, surprising or unsafe without rationale, a genuine trade-off, and necessary to prevent downstream ambiguity. Keep routine routing, formatting, and progress out.
4. Preserve prior decisions. Supersede with a new record instead of silently rewriting history.
5. Mark unsupported fields `unresolved`, `unverified`, `partial`, or `blocked`.
6. Register every current artifact or evidence-task outcome in the single `## Artifact index` table in `CONTEXT.md`. Preserve superseded rows so another session can resolve the active artifact without guessing from filenames.

## Adapting an existing workspace

Prefer an adapter decision over migration when an established project already has equivalent artifacts. Update `config.yaml` so every Research OS skill resolves the same canonical paths. Migrate only after the user accepts a path map and every source file has a destination and readback check.
