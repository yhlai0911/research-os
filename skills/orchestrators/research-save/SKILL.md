---
name: research-save
description: Create a verifiable handoff that preserves research continuity across sessions.
---

# Save Progress

Use **continuity** as the leading concept. Hand over the live research state through verified pointers to canonical artifacts, not through a rewritten version of the project.

## Workspace resolution

- Resolve `.research/config.yaml` per [writeback-protocol.md](../../primitives/research-workspace-contract/references/writeback-protocol.md). If it is absent, stop and recommend that the user invoke `research-setup`; do not invoke it yourself.
- Before reading any other workspace artifact, resolve `canonical.context`, `canonical.decisions`, `canonical.claims`, `canonical.maps`, `canonical.briefs`, `canonical.workpackages`, `canonical.pilots`, `canonical.papers`, `canonical.proposals`, `canonical.reviews`, and `canonical.handoffs` from the config. Resolve relative values against the repository root and preserve absolute values.
- Bind the resolved paths as `CONTEXT`, `DECISIONS`, `CLAIMS`, `MAPS`, `BRIEFS`, `WORKPACKAGES`, `PILOTS`, `PAPERS`, `PROPOSALS`, `REVIEWS`, and `HANDOFFS`. Read and write only through these bindings, except when updating an existing pointer field in the config itself.
- Treat the setup baseline paths as defaults only, never as fallback targets. If a required key is missing, invalid, or has a file/directory type collision, stop as `blocked`; do not probe or write a default path.

## Guardrails

- After path resolution, read `CONTEXT`, `CLAIMS`, and the active records in `DECISIONS`, `MAPS`, `BRIEFS`, `WORKPACKAGES`, `PILOTS`, `PAPERS`, `PROPOSALS`, and `REVIEWS`.
- Verify artifact existence, status, and readback yourself. Ask the user only to decide the intended recipient, next objective, priority, and acceptable unresolved risk.
- Never invoke another user-invoked skill.
- Write the handoff only in `HANDOFFS`. Reference canonical artifacts; do not copy their full content.
- Redact credentials, personal data, confidential reviewer material, and unnecessary sensitive content.

## Stage 1 — Pin the handoff target

Establish who or what will resume the work, the next session's objective, and the point at which the handoff should be considered consumed.

**Complete when:** the user confirms one recipient context and one next objective.

## Stage 2 — Verify the live state

Inspect and classify:

- last verified objective and current status;
- settled decisions and their owners;
- evidence claims and unresolved entailment gaps;
- active map frontier or workpackage frontier;
- completed outputs and their acceptance evidence;
- blockers, failed attempts, and external dependencies;
- pending user decisions;
- exact checks, commands, or readbacks needed to continue.

Distinguish verified fact, user decision, assumption, and inference. Use `partial` or `blocked` when evidence is incomplete.

**Complete when:** every status statement points to a readable canonical artifact or is labeled as an unresolved assertion.

## Stage 3 — Compress by reference

Create a concise handoff containing:

- objective and why it matters now;
- current verified state;
- decisions already closed;
- unresolved facts and decisions;
- canonical artifact links;
- frontier and recommended next action;
- blockers and stop conditions;
- verification commands or acceptance checks;
- provenance timestamp and repository revision when available.
- a context envelope: objective, immutable or canonical input pointers, allowed reads and writes, completion criterion, stop branches, and expected output receipt;
- recipient or child task identifier when known, acknowledgement state, and the source versions it accepted.

Do not duplicate briefs, maps, results, or draft prose. Link to them.

**Complete when:** the handoff contains only the live thread that is not already represented by its references.

## Stage 4 — Read back and seal

Write the handoff in `HANDOFFS`, read it back, and verify every local reference. Update an existing handoff only when it represents the same transfer; otherwise create a timestamped record.

If the config already defines an active-handoff pointer, update that field in the config and read it back. Do not invent a parallel pointer schema.

**Complete when:** a fresh agent can identify the next safe action, its inputs, allowed mutation boundary, completion criterion, expected receipt, and stop branches without the prior conversation.

## Register and verify

For every terminal outcome reached with a readable workspace, write or update its canonical record through `HANDOFFS`, then register every created or updated current artifact or outcome in `CONTEXT` per the writeback protocol.

Read back the handoff, every referenced local artifact needed to support its status, any updated config pointer, and `CONTEXT`.

Resolve the index status against the handoff: `complete` when the handoff, its supporting references, and its row read back; `partial` when a usable handoff exists but external state or non-load-bearing verification remains; `blocked` when a load-bearing input, permission, path, or write fails. Domain-specific states stay in the handoff.

## Stop branches

- Stop as `blocked` when canonical artifacts contradict each other or cannot be read. Recommend `$artifact-reconciliation` with both pinned artifact IDs; a handoff never chooses a winner or presents unresolved conflict as continuity.
- Stop as `partial` when external state, results, or receipts cannot be verified.
- Stop as `needs-decision` when no next objective or recipient context is agreed.
- Never describe unverified work as complete, and never use the handoff itself as evidence that upstream work succeeded.
