---
name: citation-audit
description: "Verify that citations exist, are primary where appropriate, and entail the claims they support. Use when auditing a manuscript, literature review, novelty claim, dataset statement, quotation, benchmark, reference list, or any draft where fabricated, stale, indirect, or overclaimed citations would be costly."
---

# Citation Audit

Test **entailment** at claim level. A real citation passes only when the cited source supports the exact scope, population, direction, timing, and strength of the sentence.

## Pin the audit target

1. Resolve `.research/config.yaml` per [writeback-protocol.md](../research-workspace-contract/references/writeback-protocol.md). Stop with `blocked: research_workspace_not_initialized` when it is absent or invalid.
2. Resolve the canonical context, claims, briefs, papers, proposals, and reviews paths from that file. Treat paths such as `.research/CONTEXT.md` and `.research/evidence/claims.yaml` only as baseline defaults; never probe them before resolution.
3. Select **full-target** or **comparison** mode. Full-target pins one immutable manuscript, review, proposal, table, or claim set. Comparison pins an immutable base, target, and the deterministic packet produced by `research-workspace-contract/scripts/build_comparison_packet.py`.
4. In comparison mode, stop `no-op` when packet status is `no-op`; otherwise inventory every changed material claim and enough unchanged surrounding text to interpret it. Use the packet's changed-section, claim-ID, and table inventory; do not silently widen or narrow the delta.
5. In full-target mode, inventory every material externally verifiable claim, quotation, numerical result, dataset statement, novelty assertion, and benchmark in the target. Stop when the mode, target, base, packet, or a required resolved path cannot be pinned; request workspace repair instead of inventing a parallel path.

Preserve the resolved claims registry's `schema_version`, declared `statuses`, existing claim IDs, status history, and unrelated entries. Use only statuses already declared by that registry. Keep `entailed`, `partially-entailed`, `not-entailed`, `contradicted`, `unverifiable`, and `citation-missing` as audit-row statuses rather than adding them to the claim-status vocabulary.

## Audit every claim

For each inventory item:

1. Resolve the cited work and verify title, authors, venue, year, version, DOI or stable URL, and retraction or correction status.
2. Open the primary text, dataset documentation, official standard, or first-party record. Treat abstracts, snippets, and secondary citations as discovery aids, not proof.
3. Locate the exact passage, table, figure, equation, or metadata field that bears on the claim.
4. Compare population, setting, construct, method, direction, magnitude, uncertainty, timeframe, and causal strength.
5. Assign one status: `entailed`, `partially-entailed`, `not-entailed`, `contradicted`, `unverifiable`, or `citation-missing`.
6. Check whether a primary source is required and whether the current source is unnecessarily indirect.
7. Verify quotations word-for-word and within their qualifying context.
8. Check reference-list integrity in both directions: every in-text citation resolves, and every listed reference is used.

Invoke `$evidence-research` when a missing or weak claim needs a replacement source. Do not perform a broad literature landscape inside this audit.

## Write back

Reuse the current registered audit for the same target and mode, or create `<target-id>-citation-audit.md` under the resolved reviews directory. Begin it with `Status: complete|partial|blocked`, `Updated`, mode, pinned target identity, base and packet identities when present, and scope. Include one row per in-scope material claim with its location, citation, source locator, audit status, explanation, and required repair. Update matching entries in the resolved claims registry without erasing prior provenance. Add new claim entries only when the target contains material claims not yet registered.

Register the outcome and read it back per the writeback protocol.

Set artifact status `complete` when the pinned target is fully inventoried and every row has an evidence-backed audit status, including explicit negative findings. Use `partial` when a non-load-bearing source gap leaves coverage provisional, and `blocked` when the target or a load-bearing source cannot be inspected well enough to finish the audit.

## Stop conditions

- Mark `unverifiable` when the source cannot be accessed; never pass it from metadata alone.
- Mark `partially-entailed` when only part of a compound claim is supported.
- Mark `not-entailed` when the source is real but answers a different question.
- Stop and flag any retracted, corrected, fabricated, or identity-mismatched source immediately.
- Stop and repin when the base, target, or packet changes during a comparison audit.
- Never silently soften prose or swap citations without recording the repair.

## Completion criteria

Finish only when:

- every material claim in the pinned target has exactly one audit row and status;
- comparison mode uses the same immutable delta packet as the calling review or renderer, and `no-op` exits without findings;
- every passing claim has an exact source locator;
- all quotations, numerical claims, dataset properties, novelty claims, and causal claims are explicitly covered;
- in-text citations and references reconcile bidirectionally;
- every non-passing row has a concrete repair or blocker;
- the resolved claims registry matches the report;
- no inaccessible source is counted as verified;
- the saved audit, comparison packet when present, affected claim records, and Artifact-index row are re-read and agree on base/target identity, packet hash, IDs, paths, audit coverage, and status; and
- the run is reported `complete` only after that readback passes, otherwise `partial` or `blocked` according to the status rule above.
