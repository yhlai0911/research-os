---
name: render-research-deliverable
description: "Render verified research into plans, proposals, manuscript drafts, or local interactive HTML reading companions for existing tables, charts and revision excerpts. Use when the destination is known and evidence must remain traceable; supplementary HTML does not replace scholarly LaTeX/PDF delivery."
---

# Render Research Deliverable

Treat the requested output as an **artifact contract**. Preserve one verified research design while changing audience, section logic, evidence threshold, and format.

Read [output-contracts.md](references/output-contracts.md) after the destination is known. Load only the selected profile and the shared truth rules.

For a supplementary reading view of existing outputs, use [html-reading-views.md](references/html-reading-views.md). This mode actually generates a self-contained HTML file with functioning table sorting/filtering, available charts, highlighted excerpts and real revision comparisons. Resolve the workspace and pin the selected source artifacts first; it is a derived export, not a new design or a claim that the whole manuscript is ready. Do not impose the full-paper acceptance gate on a requested table view. Keep the paper's academic prose and LaTeX/PDF requirements intact.

## User-facing delivery

After generating and inspecting an artifact, give a brief source-supported explanation, its real title with a verified link, and one next step. The reply and link are part of the deliverable. Follow the HTML reference's delivery contract and `scripts/build_reading_reply.py` for reading views. Do not report an artifact as created or supply a placeholder link before it exists. Use the host's supported clickable format, state a local link's device/session scope, and never present a Windows path as a cross-device URL. Failed generation or delivery has no usable link until verified; do not silently host or upload elsewhere. Navigation elements must have real targets/handlers; timed animation is not interaction evidence.

## Resolve the source contract

1. Resolve `.research/config.yaml` and its canonical context, claims, decisions, briefs, plans, workpackages, pilots, reviews, papers, proposals, and templates per [writeback-protocol.md](../research-workspace-contract/references/writeback-protocol.md).
2. For an academic plan, proposal or manuscript, read the current Research Brief and its linked claims, decisions, design artifacts, pilots, and reviews. Pin their IDs or versions. In HTML reading-companion mode, pin the existing selected artifact/table and its relevant sources and verdict instead; this mode is also usable before a brief exists and must not invent or approve one.
3. Resolve the intended audience, use or decision, required format or institutional template, language, and export preference. Preserve supplied values and ask only for a load-bearing missing decision.
4. Stop with `blocked: research_brief_missing` for a plan/proposal/manuscript when there is no canonical brief. For a supplementary HTML reading view, stop with `blocked: reading_source_missing` when the selected existing source cannot be read or pinned; never upgrade its readiness. Stop with `blocked: destination_ambiguous` when the requested artifact type, audience, or decision use remains consequentially unclear.
5. If the requested destination is a Research Brief, stop with `blocked: canonical_writer_mismatch` and return to `$synthesize-research-brief`. This renderer never writes or repairs the canonical brief.
6. Select **new artifact** or **revision** mode. For a revision, pin the current rendered base and intended target source versions, then use `research-workspace-contract/scripts/build_comparison_packet.py` after rendering to produce the exact changed-section, claim-ID, and table packet consumed by citation and research review. An identical base and target is a read-back `no-op`.

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

For academic plans, proposals, blueprints and manuscripts, apply the shared [academic-prose contract](../research-writing/references/academic-prose.md) by default in the requested language. Render the body as a connected scholarly argument, preserve necessary technical structures and claim strength, and use APA unless a supplied citation style takes precedence. Do not turn the ASD-STE100 clarity adaptation into a compliance claim or rigid English-language restrictions.

Use the user's requested language and verified venue conventions. For a paper blueprint, manuscript or degree thesis, apply [scholarly-delivery.md](../research-writing/references/scholarly-delivery.md): deliver editable LaTeX, a PDF actually compiled from that source, bibliography files, build evidence, visual QA and the source package. A Word-converted or directly drawn PDF does not meet this contract. Markdown can be an input/review aid; register an accepted format migration under the same paper identity without erasing prior sources. If a supplied requirement conflicts, resolve it explicitly rather than silently substituting a renderer. Other profiles retain their requested format or default to Markdown. Do not create DOCX, slides, budgets, forms, or submission packages unless requested.

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

Record the artifact ID, status, version, updated date, destination profile, source brief, and claim/decision pointers in the canonical registry or an artifact sidecar. For academic outputs, keep these operational fields out of the body and exported scholarly front matter; use disciplinary prose for methods and a separate technical appendix for implementation. Preserve an existing current artifact when updating the same deliverable; supersede rather than silently fork when its identity changes.

Register it in the resolved context per the writeback protocol.

Re-read the saved canonical artifact, every cited local pointer, the claims registry, the index row, and every requested derived export. Report:

- `complete` when the selected profile, truth gate, citations, and readback all pass, including the paper/thesis LaTeX, bibliography, equation and visual gates when applicable;
- `partial` when a useful labeled artifact exists but a non-load-bearing section, approval, or evidence item remains;
- `blocked` when the source brief, destination, load-bearing evidence, write, or readback fails.

For a revision, also re-read the base, target, packet, citation audit, and research review; all must agree on base hash, target hash, packet ID, changed inventory, and `no-op|changed` status.

Artifact-specific states such as `outline`, `complete-draft`, `submission-ready`, or `funding-ready` stay inside the artifact and never replace the three index statuses.

## Stop branches

- Produce a labeled paper blueprint, not a results manuscript, when analyses are unexecuted.
- Preserve the user's format or funder template; do not substitute a generic structure silently.
- Stop before submission, upload, email, public release, authorship assignment, or spending.
- Return to the Research Brief when rendering reveals a contradiction in the design; do not repair the contract only in downstream prose.
