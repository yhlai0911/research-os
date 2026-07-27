---
name: ethics-reproducibility
description: "Design ethical, reproducible, and auditable research. Use when a study involves human participants, personal or licensed data, model-assisted analysis, preregistration, provenance, computational reproducibility, conflicts of interest, disclosure, consent, or a replication package."
---

# Ethics and Reproducibility

Build an **audit trail** that lets another qualified researcher determine what was authorized, what ran, what changed, and whether the result can be reproduced.

## Load the research contract

1. Resolve `.research/config.yaml` per [writeback-protocol.md](../research-workspace-contract/references/writeback-protocol.md). Stop with `blocked: research_workspace_not_initialized` when it is absent or invalid.
2. Resolve the canonical context, claims, briefs, proposals, reviews, pilots, workpackages, papers, and decisions paths from that file. Treat paths such as `.research/CONTEXT.md` and `.research/evidence/claims.yaml` only as baseline defaults; never probe them before resolution.
3. Read the resolved context and claims registry, followed by the active brief, proposal, methodology, data-feasibility review, pilots, workpackages, papers, disclosures, and relevant decisions at their resolved paths.
4. Identify the jurisdiction, institution, funder, venue, data provider, participant population, and collaboration obligations that govern the work. Stop when the governing context or a required resolved path is unknown; request workspace repair instead of inventing a parallel path.

Preserve the resolved claims registry's `schema_version`, declared `statuses`, existing claim IDs, status history, and unrelated entries. Use only statuses already declared by that registry; keep ethics-gate and reproducibility outcomes in the review rather than adding `pass` or `not-applicable` as claim statuses.

## Apply the ethics gate

Classify each item as `pass`, `not-applicable`, or `blocked`, with evidence:

1. Human-participant review, exemption, consent, recruitment, compensation, withdrawal, and vulnerable populations.
2. Personal, sensitive, licensed, proprietary, or indigenous data; purpose limitation; minimization; retention; access; transfer; and deletion.
3. Intervention risk, dual use, foreseeable harm, deception, and downstream misuse.
4. Authorship, contributor roles, conflicts of interest, funding, data ownership, and community obligations.
5. Model-assisted work, automation, generated content, and required disclosures.

Treat missing approval as `blocked`, never as implied permission.

## Build reproducibility

1. Pin protocols, preregistrations, deviations, input identities, source versions, licenses, code commits, environments, dependencies, seeds, hardware-sensitive settings, and execution timestamps.
2. Separate raw, derived, and publishable artifacts; preserve lineage without copying restricted data into the repo.
3. Require deterministic commands or a documented stochastic replication procedure.
4. Capture failed, null, excluded, and rerun analyses with reasons.
5. Specify what a replication package may contain, what must remain restricted, and how an authorized researcher can reconstruct it.
6. Verify that tables, figures, claims, and manuscript versions point to the exact generating artifacts.
7. Record deviations from preregistration before interpreting their outcomes.

Invoke `$data-feasibility` for license and access semantics, `$citation-audit` for disclosure claims, and `$research-diagnosis` when reproduction fails.

## Write back

Reuse the current registered review for the same artifact, or create `<artifact-id>-ethics-reproducibility.md` under the resolved reviews directory. Begin it with `Status: complete|partial|blocked`, `Updated`, target identity, and scope. Include the gate matrix, evidence pointers, blockers, reproducibility manifest, and release plan. Record approvals, exemptions, licenses, preregistration choices, deviations, and disclosure decisions under the resolved decisions directory. Update `.research/config.yaml` only after user confirmation and without deleting prior policy. Update affected entries in the resolved claims registry when reproducibility changes their support status.

Register the outcome and read it back per the writeback protocol.

Set artifact status `complete` only when every applicable ethics gate passes or is justified as not applicable and the required audit trail is reproducible. Use `partial` only for non-safety reproducibility gaps that do not authorize a blocked action, and `blocked` whenever a required ethics, license, approval, governing-context, or resolved-path gate is blocked.

## Stop conditions

- Stop before collection, contact, upload, sharing, or analysis when a required ethics or license gate is blocked.
- Stop before public release when restricted data, credentials, personal information, or prohibited derivatives would leak.
- Stop when an approval, consent, exemption, preregistration, or disclosure cannot be verified.
- Never fabricate compliance, anonymization, permission, or reproducibility.
- Never overwrite the record of a deviation or failed run.

## Completion criteria

Finish only when:

- every applicable ethics, governance, authorship, conflict, and disclosure item has evidence and a status;
- every blocked item names the authority and action required to clear it;
- inputs, code, environment, randomness, commands, outputs, and deviations form an unbroken provenance chain;
- restricted and releasable artifacts are separated;
- the replication package has an executable reconstruction path or an explicit justified limitation;
- the saved review, decisions, config, and affected claims agree;
- no blocked action is described as approved or complete;
- the saved review, affected claim and decision records, any confirmed config change, and Artifact-index row are re-read and agree on IDs, paths, approvals, blockers, and status; and
- the run is reported `complete` only after that readback passes, otherwise `partial` or `blocked` according to the status rule above.
