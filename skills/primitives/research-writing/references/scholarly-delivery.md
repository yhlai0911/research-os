# Scholarly paper and thesis delivery

Apply to a delivered paper blueprint, manuscript or degree thesis. A targeted paragraph edit or planning discussion does not require a whole-paper build. Preserve the requested scope, existing canonical identity, raw evidence and historical versions. Do not rewrite a current case merely because this contract changes.

## Academic completeness

Write professional disciplinary prose with a cumulative argument. Establish the practical/scholarly problem, closest verified knowledge, unresolved issue, mechanism or rationale, question/hypothesis, estimand, data and model choice, estimates with uncertainty, competing explanations, and warranted conclusion. Connect these functions; a heading or a list of citations is not an argument. Use tables, figures and equations where they improve precision, then interpret them in the prose.

Assess literature by coverage of the actual question: foundational theory, closest empirical/design comparisons, current relevant work, local/contextual work where material, conflicting evidence and methodological alternatives. Record search boundary/date, inspected versions and claim-level locators in the existing evidence/audit records. Synthesise agreement, disagreement and the remaining contribution. Do not call a selective or abstract-only search exhaustive. When the core argument requires unavailable text, narrow it or leave the affected section partial/blocked.

No arbitrary word, page or reference quota establishes completeness. Do not pad with tangential works, compress a thesis into slide bullets, or delete warrants/counterevidence to obtain a short style score. Use the verified institution/venue template without claiming approval. For Chinese, adapt clear referents, precise sentences and consistent terminology; ASD-STE100 is an English technical-documentation specification, not a Chinese academic certification. Keep scientific nuance, necessary derivation and established terms. See the source/access limits in [academic-prose.md](academic-prose.md).

For example, “Risk fell; therefore the currency is a safe haven” skips the measurement, uncertainty, adverse cases and distinction between average diversification and stress protection. A defensible passage states the observed comparison and uncertainty, explains the relevant covariance or mechanism, confronts counterexamples, and limits the inference to the supported population and horizon. Adding ten unrelated references or replacing the claim with bullet fragments does not repair that chain. This is an editorial example, not a study result.

## Mathematical exposition

For each substantive displayed equation:

- use an appropriate numbered LaTeX environment and a stable semantic `\label`; refer to it in the prose with `\eqref` or a labelled `\ref`;
- define every symbol, subscript, index, domain, unit/scale and parameter near first use; state the timing and reference category;
- identify whether it is a definition, identity, estimating equation, theoretical relationship or causal assumption;
- provide a derivation, a verified source locator, or explicit reasoning for its introduction; do not present a borrowed model as an original result;
- justify the model relative to the estimand, data structure and serious alternatives; explain assumptions, identification conditions, diagnostics and what would refute the interpretation.

Use cross-references for tables, figures and sections as well. Do not manually type numbers that drift after revision. Distinguish statistical notation from program fields. Introductions should motivate the question in prose; put detailed equations/derivations in the appropriate theory/methods section or appendix. Preserve null/adverse results, failed diagnostics and post-analysis deviations.

## Verified APA bibliography

Default to APA 7 unless verified user/institution/venue requirements specify another edition or style. Use BibLaTeX with `biblatex-apa` and Biber, or a BibTeX workflow verified to match the required edition. The [CTAN biblatex-apa record](https://ctan.org/pkg/biblatex-apa) documents APA 7 and the Biber dependency; [apacite](https://ctan.org/pkg/apacite) implements APA 6 and must not be silently substituted for APA 7 (records checked 2026-10-24). Keep references in `.bib`; use citation commands and generated reference lists, not a separately retyped list. Protect corporate authors and proper-name capitalisation where required; check author ordering, year suffixes, versions, quotation locators and language conventions in the PDF.

Resolve each cited work against the publisher/DOI record or authoritative repository/catalogue. Verify author names/order, year, title, venue and DOI as a single identity; a resolving DOI alone is insufficient. Do not invent a DOI or infer one from a similar title. A work with no DOI is legitimate when that absence/status and a stable source are verified. Unresolved metadata remains an explicit audit gap, not a polished invented entry. Keep source existence, metadata accuracy and support for the cited sentence as separate checks. Abstract-only access permits only what the inspected abstract supports, not claims about unseen methods/results.

Reconcile text citation keys ↔ `.bib` entries ↔ generated references in both directions. Explain any institution-required uncited bibliography rather than hiding it with blanket `\nocite{*}`. Run `$citation-audit` on the pinned current version and resolve material negative findings; an audit being complete does not mean its findings passed. Recheck after any bibliographic/source change.

## Actual LaTeX production

Deliver the editable `.tex` sources, `.bib`, necessary styles/classes and permitted figures, plus the PDF genuinely compiled from those sources. A Word-exported or directly drawn PDF cannot stand in for a LaTeX build. Preserve Markdown as source history/review aid if useful; make an accepted source-format change under the same paper identity and update its pointers.

Choose a supported engine (normally XeLaTeX or LuaLaTeX for Chinese) and available fonts with the required glyphs. Record engine/version and bibliography backend. Use a reproducible build recipe such as `latexmk` or the documented engine → Biber/BibTeX → engine rerun sequence. Use existing authorised tools; do not install packages/fonts, enable shell escape, change security settings or purchase services merely to make a build pass. Report a missing compiler/backend/font exactly and preserve the sources.

The first actual compile is mandatory for each new deliverable, and compile again after changes affecting the output. Save the real command/tool result, exit status, diagnostic logs and hashes of source inputs and resulting PDF. Complete the bibliography and cross-reference reruns. A compile attempt, an older PDF, synthetic test log or successful source lint is not a successful build. The final run must have no undefined citation/reference, unresolved bibliography rerun, duplicate label or missing-glyph diagnostic. Repair errors without changing substantive research choices; report remaining blockers rather than claiming success.

Inspect all rendered pages on first delivery. After revision, inspect every changed page plus pagination/cross-reference effects. Check equations, labels, superscripts, Chinese characters, APA citations/reference list, tables, captions, figure resolution, page breaks, margins and clipping. Compilation alone does not detect a cramped or unreadable argument. Fix layout, recompile and reinspect. Pin the visual-QA record to the exact PDF hash; an earlier review does not transfer automatically.

Package all permitted inputs needed to rebuild: main and included TeX, bibliography, custom classes/styles, figure assets, build instructions and dependency/font versions. Include provenance/build/QA records as companions outside the academic body. Do not redistribute third-party full-text PDFs or restricted data just because they were read. Check the package inventory and source hashes against the delivered build. Keep a current artifact sidecar pointing to the canonical source and derived PDF/package, rather than creating another research registry.

## Acceptance and mechanical preflight

Completion requires three distinct kinds of evidence:

1. Academic review: the argument/literature/equation/interpretation functions above are developed, supported and internally aligned; material findings are repaired or remain clearly blocking.
2. Citation review: identities, locators, entailment, bibliography and bidirectional citation mapping are verified on the current version.
3. Production: a real LaTeX build, clean final diagnostics, current visual QA and a rebuildable source package.

Use `scripts/check_latex_delivery.py <project-root> <receipt.json>` to check mechanical provenance and fatal diagnostic patterns. The receipt contains `schema_version: 1`, `main`, `pdf`, `inputs` (project-relative file → SHA256), `build` (`engine`, `command`, `exit_code`, `logs` file → SHA256, `pdf_sha256`), `source_package` (`path`, `sha256`), and `reviews`. Reviews `academic`, `citations` and `visual` each name `path`, `sha256`, `status: complete`, `unresolved_material_findings: 0`; academic/citation reviews pin `input_hashes`, and visual QA pins `pdf_sha256`. Source packages use the same relative input paths at archive root. Never construct a receipt that says a missing check ran.

The checker validates hashes, package inputs, a recognised compiler log, and selected warnings; it cannot prove a log is authentic, assess prose depth, verify a DOI online, fully parse TeX macros or certify academic/degree readiness. Synthetic unit fixtures test this checker only. Supported compiler-tool evidence may be preserved directly when its log format differs; document that limitation and manually verify every gate rather than fabricating a recognised log. Missing evidence prevents a `complete` paper delivery. Report `partial` for usable sources/draft with unfinished nonfatal work, and `blocked` when a required source, compiler, bibliography backend or critical evidence cannot be obtained.
