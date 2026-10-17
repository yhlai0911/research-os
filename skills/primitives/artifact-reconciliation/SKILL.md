---
name: artifact-reconciliation
description: "Resolve conflicting canonical research artifacts into one verified current state without erasing either intent or provenance. Use when briefs, decisions, claims, methods, datasets, protocols, handoffs, revisions, or schema versions disagree and a downstream workflow cannot safely choose between them."
---

# Artifact Reconciliation

Lead with **intent**: recover what each artifact was trying to preserve before merging text or asking which file should win.

Read [conflict-types.md](references/conflict-types.md) only after both sides are pinned and the conflict needs classification.

## Pin both sides

1. Resolve `.research/config.yaml` per [writeback-protocol.md](../research-workspace-contract/references/writeback-protocol.md). Stop with `blocked: research_workspace_not_initialized` when it is absent or invalid.
2. Resolve the canonical context, claims, decisions, briefs, plans, workpackages, pilots, reviews, papers, proposals, and handoffs paths from that file. Never probe baseline paths before resolution.
3. Pin both conflicting artifacts by ID, path, version, SHA-256 or equivalent immutable identity. Record their current Artifact-index rows, predecessor and successor links, producing decisions, and every downstream artifact that consumes either side.
4. Read both artifacts in full, then follow their claim, evidence, decision, and execution pointers to primary sources. Do not infer intent from prose style or modification time.
5. Stop with `blocked: conflict_side_unpinned` when either side or its lineage cannot be identified. Do not select the easier-to-read artifact as a fallback.

Preserve the resolved claims registry's schema, status vocabulary, prior status history, and unrelated entries. A conflict verdict belongs in the reconciliation artifact; it is not a new claim status.

## Classify before resolving

Build one conflict packet:

| Element | Side A | Side B | Compatible content | Incompatibility | Authority needed |
|---|---|---|---|---|---|

Classify each incompatibility as:

- **fact conflict** — externally verifiable propositions disagree;
- **human-choice conflict** — two legitimate research objectives, risk tolerances, scopes, or interpretations disagree;
- **schema conflict** — equivalent intent is encoded under incompatible contracts;
- **execution conflict** — planned state and observed execution receipts disagree; or
- **concurrent-edit conflict** — compatible additions were made against the same ancestor.

Invoke `$citation-audit` for load-bearing fact conflicts. For a human-choice conflict, apply the one-question decision discipline: state one prerequisite choice, recommend an option with its cost, wait for the named decision owner, then persist the answer. Never ask the user to decide a fact and never let a later timestamp overrule an accepted decision or execution receipt.

## Reconcile intent, not text

1. Preserve every compatible element and its original provenance.
2. For fact conflicts, retain both propositions until direct evidence supports, contests, or blocks each exact claim.
3. For human-choice conflicts, record the accepted answer in a new Research Decision Record; preserve the rejected branch and rationale.
4. For schema conflicts, map both sources into the currently configured schema without deleting the originals.
5. For execution conflicts, observed receipts control what happened; a plan controls only what was intended.
6. Create one superseding artifact or record. Never edit both parents into apparent agreement and never silently choose a winner.
7. Mark prior Artifact-index rows `superseded`, point them to the new ID, and leave exactly one current pointer for the reconciled subject.
8. Enumerate every downstream artifact, claim, review, export, and workpackage invalidated by the resolution. Re-run or mark each one `partial` or `blocked`; do not leave a stale `complete`.

## Write and prove the resolution

Create `<conflict-id>-reconciliation.md` under the resolved reviews directory. Begin with `Status: complete|partial|blocked`, `Updated`, both pinned identities and hashes, their common ancestor when known, and the exact conflict scope. Include the packet, evidence and decision ownership, preserved content, incompatible choice, superseding artifact, invalidation set, and gate results.

Register the outcome in the resolved context per the writeback protocol. Preserve both parents as superseded rows and create one current row.

Re-read both originals, the reconciliation report, the superseding artifact, affected claims and decisions, every rerun downstream gate, and the Artifact index. Report:

- `complete` only when one verified current pointer remains and every invalidated load-bearing gate has rerun;
- `partial` when a useful superseding artifact exists but a non-load-bearing gate remains open; or
- `blocked` when evidence, human authority, schema mapping, write, or readback cannot establish one current state.

## Stop conditions

- Stop rather than merge when the two inputs do not share the same subject or intended authority.
- Stop at one human-choice question; do not hide several policy choices inside a merge.
- Stop when reconciliation would require deletion, migration, external publication, or another unapproved mutation.
- Never treat conflict-free syntax as proof of semantic agreement.
- Never mark a parent current after its replacement has been verified.

## Completion criteria

Finish only when both immutable inputs and lineage are pinned; every conflict is classified; compatible intent and provenance are preserved; factual and human-choice conflicts use the correct authority; one superseding artifact exists; both parent rows are superseded; all invalidated downstream gates have a current result; and final readback proves exactly one current pointer with no silent loss.
