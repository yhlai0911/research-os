---
name: research-writing
description: "Write and revise evidence-led academic prose as a cumulative argument. Use for introductions, literature reviews, theory sections, methods, results, discussions, abstracts, reviewer responses, or finance and economics prose that must synthesize rather than list sources."
---

# Research Writing

Build an **argument** in which each paragraph earns the next claim. Write from verified research artifacts rather than from plausible memory.

## Default academic prose

Read [academic-prose.md](references/academic-prose.md) before drafting or revising academic text in any language. Apply it without requiring the user to repeat a style prompt: connected scholarly paragraphs, clear and economical sentences, consistent precise terms, and explicit evidence-to-inference links. Use APA author-date citations by default when no user, institution, or venue style is specified. Preserve necessary tables, equations, hypotheses, method steps, uncertainty, and limitations. Borrow ASD-STE100 clarity principles without imposing its controlled-English vocabulary or word limits, claiming formal compliance, or simplifying an association into causation.

Keep the academic body in the discipline's language. Explain sampling, measurement, transformations, estimators, assumptions and diagnostics without exposing skill names, workflow states, executors, paths, code identifiers or test logs. Put implementation and reproduction details in a separately identified technical appendix or companion. Preserve an appropriate AI-assistance statement; moving operational details must not conceal how the work was produced. Read [body-language-examples.md](references/body-language-examples.md) when revising a mixed academic/operational draft, and run `scripts/check_academic_body.py <manuscript.md>` as a non-mutating leak check. Its findings require located review; a clean result is not proof of scholarly quality or research validity.

For a paper or degree-thesis deliverable, read [scholarly-delivery.md](references/scholarly-delivery.md). Require a developed scholarly argument, verified literature coverage, numbered and explained mathematical displays, managed APA citations, editable LaTeX sources, an actual LaTeX-compiled PDF, first-build evidence, visual QA and a reproducible source package. Markdown may remain an input or review aid; Word-to-PDF, ReportLab or another direct PDF generator cannot satisfy this paper/thesis compilation requirement. A paragraph edit does not by itself authorize rebuilding a whole thesis.

## Load the research contract

1. Resolve `.research/config.yaml` per [writeback-protocol.md](../research-workspace-contract/references/writeback-protocol.md). Stop with `blocked: research_workspace_not_initialized` when it is absent or invalid.
2. Resolve the canonical context, claims, briefs, maps, papers, reviews, and decisions paths from that file. Treat paths such as `.research/CONTEXT.md`, `.research/evidence/claims.yaml`, and `.research/papers/` only as baseline defaults; never probe them before resolution.
3. Read the resolved context and claims registry. Pin the target paper, section, audience, and version under the resolved papers directory, then read the active brief, contribution design, theory, methodology, results, reviews, decisions, and only the evidence linked to the target claims.
4. Stop when the requested section has no declared purpose or verified claim set, or when a required resolved path is missing; request workspace repair instead of inventing a parallel draft location.

Preserve the resolved claims registry's `schema_version`, declared `statuses`, existing claim IDs, status history, and unrelated entries. Use only statuses already declared by that registry; record draft usage pointers without turning prose readiness or section completion into claim statuses.

## Build the argument map

1. State the section's conclusion in one sentence.
2. List the claims required to reach it in logical order.
3. Map each material factual or literature claim to a `verified` entry in the resolved claims registry.
4. Mark interpretation, inference, limitation, and speculation explicitly.
5. Remove claims that do not advance the section's conclusion.

Check the full chain: research problem → closest verified knowledge and unresolved issue → mechanism or research rationale → question/hypothesis → estimand, data and model choice → results and uncertainty → warranted conclusion. Develop warrants, alternatives and counterevidence in prose. Judge completeness by these functions and the actual discipline, not a fixed word count, page count or number of references. If the evidence cannot support the chain, narrow the claim or mark the draft partial; do not pad it.

Choose one interaction mode:

- **Explore:** preserve raw user fragments, source pointers, and acceptance state without forcing them into an outline or upgrading them into verified claims.
- **Shape:** treat the accepted input pile as read-only, establish what the audience must understand, and shape one argumentative block at a time. Offer a small number of meaningful opening or structure choices only when they change the argument.
- **Draft and audit:** render the accepted argument map into a full section, then audit evidence, citations, causality, and internal consistency.

Default to Draft and audit when the user requests a complete section and the source contract is ready. Use Explore or Shape when the user explicitly wants co-authoring, when raw author material carries unique intent, or when a large one-shot draft would hide consequential choices.

In interactive modes, re-read the current target before every write so user edits outrank an older in-context copy. Track which concepts have been introduced to the reader; `grounded` means introduced, not empirically verified. Ask at most one dependent structural decision per exchange.

## Draft by section function

- Make the introduction establish problem, closest knowledge, unresolved delta, approach, result, and contribution without suspense.
- Make the literature review synthesize agreements, differences, mechanisms, and the exact opening rather than listing papers.
- Make theory derive mechanisms, boundary conditions, and discriminating predictions.
- Make methods permit a competent researcher to understand the estimand, sample, variables, procedure, assumptions, and evaluation.
- Make results report estimates, uncertainty, diagnostics, and failed tests before interpretation.
- Make discussion calibrate contribution, alternatives, limitations, and generalizability.
- Make reviewer responses quote the concern, state the action, point to evidence, and acknowledge unresolved limits.

Use the canonical terms in the resolved context. Preserve the strength of the evidence: write association as association, estimates as estimates, and causal claims only when identification supports them.

Invoke `$citation-audit` for entailment, `$journal-fit` for audience-specific revision, and the relevant design primitive when writing exposes a research gap. Do not repair research validity with prose.

## Write back

Write or revise the pinned artifact under the resolved papers directory (baseline `.research/papers/<paper-id>/`). Reuse the current registered paper and preserve existing file conventions; never create a parallel duplicate merely because the baseline path differs. In Explore mode, preserve raw input separately and do not mutate it. In Shape mode, save accepted blocks and their source pointers without overwriting user edits. Update resolved claim entries with the draft locations where they are used. Record a hard-to-reverse narrative or scope choice under the resolved decisions directory only when the user confirms it.

Register the current draft or writing outcome in the resolved context per the writeback protocol. Keep `Status: complete|partial|blocked`, `Updated`, and scope in Research OS metadata or the Artifact-index row rather than inserting workflow labels into journal prose.

Set artifact status `complete` only when the requested section is fully supported and internally aligned; use `partial` for an explicitly requested scaffold or unresolved nonfatal passage, and `blocked` when a material claim, target version, or required resolved path cannot be supported.

## Stop conditions

- Stop when a material sentence lacks supported evidence.
- Stop when the requested wording would overstate causality, novelty, precision, or generality.
- Stop when conflicting artifacts leave the intended claim unresolved.
- Stop and ask for material or cut the section when the source pile cannot support the promised argument.
- Stop before overwriting an externally edited target or mutating a declared read-only source pile.
- Use an explicit placeholder only when the user requests a scaffold; never fabricate a result or citation.
- Never add a citation merely because it looks plausible.

## Completion criteria

Finish only when:

- every paragraph has one argumentative job and a clear link to the next;
- every material factual claim maps to a supported claim record and source;
- terminology, estimands, methods, results, and contribution agree across artifacts;
- uncertainty, null results, failed tests, and limitations remain visible;
- citations are placed on the claims they entail;
- the draft path and claim-use pointers are updated;
- no prose substitutes for missing research evidence;
- academic methods and counterevidence survive the removal of implementation language, and the technical companion and AI disclosure remain linked outside the body;
- for a paper/thesis delivery, the scholarly-delivery gates pass: literature and equation coverage, reconciled verified bibliography, actual LaTeX build, clean citation/reference/glyph diagnostics, visual QA and complete source package; missing gates remain partial or blocked, never a completed paper;
- the saved draft, affected claim and decision records, and Artifact-index row are re-read and agree on target identity, IDs, paths, claim strength, and status; and
- interactive-mode source identity, accepted blocks, and user edits are preserved; and
- the run is reported `complete` only after that readback passes, otherwise `partial` or `blocked` according to the status rule above.
