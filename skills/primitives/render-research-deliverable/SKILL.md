---
name: render-research-deliverable
description: "Render a verified Research Brief into a fit-for-purpose academic research plan, grant proposal, project proposal, paper blueprint, or manuscript draft. Use when the destination artifact is known and its claims, decisions, methods, and evidence must be assembled without inventing missing work."
---

# Render Research Deliverable

Treat the requested output as an **artifact contract**. Preserve one verified research design while changing audience, section logic, evidence threshold, and format.

Read [output-contracts.md](references/output-contracts.md) after the destination is known. Load only the selected profile and the shared truth rules.

## Resolve the source contract

1. Read only `.research/config.yaml` first.
2. Resolve context, claims, decisions, briefs, plans, workpackages, pilots, reviews, papers, proposals, and templates from its canonical entries.
3. Read the current Research Brief and its linked claims, decisions, design artifacts, pilots, and reviews. Pin their IDs or versions.
4. Resolve the intended audience, use or decision, required format or institutional template, language, and export preference. Preserve supplied values and ask only for a load-bearing missing decision.
5. Stop with `blocked: research_brief_missing` when there is no canonical brief. Stop with `blocked: destination_ambiguous` when the requested artifact type, audience, or decision use remains consequentially unclear.
6. If the requested destination is a Research Brief, stop with `blocked: canonical_writer_mismatch` and return to `$synthesize-research-brief`. This renderer never writes or repairs the canonical brief.
7. Select **new artifact** or **revision** mode. For a revision, pin the current rendered base and intended target source versions, then use `research-workspace-contract/scripts/build_comparison_packet.py` after rendering to produce the exact changed-section, claim-ID, and table packet consumed by citation and research review. An identical base and target is a read-back `no-op`.

Treat the baseline `.research/...` paths as documentation only. Never write through them when the configuration resolves an adapter.

## Pass the truth gate

Build a source matrix for every section:

| Needed statement | Source artifact or claim ID | Evidence state | Allowed wording |
|---|---|---|---|

Distinguish discovered facts, accepted decisions, proposed methods, executed procedures, observed results, interpretations, forecasts, and speculation. A polished sentence cannot upgrade any state.

Apply these gates:

- a novelty statement requires a surviving gap audit and inspected sources;
- a causal or mechanism-effect statement requires a current identification verdict;
- a data or implementation promise requires a feasibility receipt;
- a result section requires executed outputs, uncertainty, and provenance;
- a budget, duration, institutional commitment, authorship claim, or submission promise requires user authority.

Mark a missing non-load-bearing element visibly. Stop when a load-bearing element would have to be invented.

## Render for the destination

Use the selected output profile. Keep the Research Brief's question, constructs, estimand, mechanism, scope, and evidence strength unchanged unless an accepted Research Decision Record supersedes them.

Invoke `$research-writing` for evidence-led academic prose. Invoke `$citation-audit` before finalizing factual claims and references. Invoke `$research-review` when the artifact claims submission, funding, or decision readiness. In revision mode, pass the identical frozen comparison packet to both; never let separate reviewers reconstruct different deltas.

Use the user's requested language and venue conventions. Default to Markdown. Use LaTeX for an equation-heavy academic artifact when requested; compile PDF only when requested and a supported local document workflow is available. Do not create DOCX, slides, budgets, forms, or submission packages unless requested.

Write the canonical artifact to the resolved destination:

- academic research plan → plans;
- grant, institutional, or project proposal → proposals;
- paper blueprint or manuscript draft → papers.

When the user requests a copy outside the canonical workspace, treat it as a derived export:

1. write and read back the canonical artifact first;
2. generate the requested Markdown, LaTeX, PDF, DOCX, or other supported copy from that pinned version;
3. record the export path, format, source artifact ID and version, SHA-256 when locally available, generation time, and readback status in the canonical artifact;
4. verify the exported file independently; and
5. never use an export as a competing source of truth.

If the requested renderer is unavailable, keep the canonical artifact and report the export as `partial`; do not substitute another format silently.

## Register and verify

Begin the artifact with its ID, artifact-specific status, version, updated date, destination profile, source brief, and claim/decision pointers. Preserve an existing current artifact when updating the same deliverable; supersede rather than silently fork when its identity changes.

Register it in the one resolved-context `## Artifact index`:

`| Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes |`

Re-read the saved canonical artifact, every cited local pointer, the claims registry, the index row, and every requested derived export. Report:

- `complete` when the selected profile, truth gate, citations, and readback all pass;
- `partial` when a useful labeled artifact exists but a non-load-bearing section, approval, or evidence item remains;
- `blocked` when the source brief, destination, load-bearing evidence, write, or readback fails.

For a revision, also re-read the base, target, packet, citation audit, and research review; all must agree on base hash, target hash, packet ID, changed inventory, and `no-op|changed` status.

Artifact-specific states such as `outline`, `complete-draft`, `submission-ready`, or `funding-ready` stay inside the artifact and never replace the three index statuses.

## Stop branches

- Produce a labeled paper blueprint, not a results manuscript, when analyses are unexecuted.
- Preserve the user's format or funder template; do not substitute a generic structure silently.
- Stop before submission, upload, email, public release, authorship assignment, or spending.
- Return to the Research Brief when rendering reveals a contradiction in the design; do not repair the contract only in downstream prose.
