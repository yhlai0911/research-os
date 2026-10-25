# Academic prose and clarity across languages

Use this contract by default for academic drafting, revision, rendering and manuscript-style review. Apply the user's language and verified venue or institution requirements. It governs the academic body, not the skill's operational checklist or the research registry schema.

## Argument in connected paragraphs

Write introductions, literature synthesis, theory, results, discussion and conclusions as connected scholarly prose. Give each paragraph one argumentative job: state the point, present its evidence or reasoning, and explain the inference or boundary that advances the next point. Do not substitute slide headings, fragments, slogans, an author-by-author list, or repeated bullet summaries for that argument. A shorter passage still needs the reasoning that makes its conclusion defensible.

Professional concision removes redundancy, not intellectual work. Develop the closest literature, the unresolved issue, the warrant for each inference, serious alternatives and the conditions under which the conclusion could fail. A literature matrix and argument map are working aids; turn their substantive comparisons into analytical prose. Do not meet a perceived academic standard by adding a quota of words or references. A short but complete argument can pass; a long source list with no synthesis cannot.

Keep a table when comparison is clearer in rows, an equation when precision requires it, explicit hypotheses, and numbered method steps when sequence matters. Define symbols and connect those elements to the prose. Preserve actionable finding IDs, repair tables and checklists in review reports; present their substantive assessment in coherent prose. Do not convert required structures into paragraphs merely to satisfy a blanket ban on lists.

## Adopt clarity principles, preserve scholarly meaning

- Choose direct, economical sentences with an explicit subject, referent and logical relationship. Split a sentence when doing so resolves ambiguity; use length as a diagnostic, not a fixed cutoff.
- Use the same defined term for the same construct, measure or procedure. Define necessary technical terms, abbreviations and symbols; retain established disciplinary terms and distinguish concepts that differ. Do not replace precision with a simpler but inaccurate synonym.
- Prefer active voice when the actor matters and is known. Retain justified passive constructions, modality, qualifications, quotations and technical forms when changing them would misstate the research.
- Separate observed results, interpretation, proposed mechanisms and speculation. Preserve signs, units, uncertainty, null/adverse results, scope and limitations. An association stays an association; clearer prose cannot supply missing identification or make a nonsignificant result prove no effect.
- Remove filler and repetition without deleting counterevidence, caveats or inferential steps. Explain what each source supports rather than adding decorative citations.

These are cross-language adaptations of useful ASD-STE100 principles. Do not enforce its English approved-word dictionary, restrictions on grammatical forms, or procedural sentence/paragraph limits as academic rules. Do not label a Chinese text or an academic paper ASD-STE100-compliant or certified on this basis. Scientific nuance and technical accuracy control the adaptation.

## Separate disciplinary exposition from implementation

Write the academic body for a researcher in the relevant discipline. Retain the research question, sample, variable definitions, mathematical notation, data transformations, estimators, uncertainty, diagnostics and deviations from the analytical design. Explain those choices in disciplinary terms rather than substituting software field names, functions, command lines or internal workflow vocabulary for the method.

Keep skill names and invocation examples, canonical registries, artifact states, workpackages, executors, receipts, hashes, filesystem paths, implementation identifiers, test frameworks and operation logs out of the body. Put necessary reproduction information in a separately identified technical appendix or companion; keep tool-operation tutorials separate from the research manuscript. Research OS metadata stays in its owning registry or sidecar, not in scholarly paragraphs. Software or AI systems that are themselves the study's objects may be discussed as defined research constructs; this exception does not authorize unrelated project internals.

Do not remove methodological substance to satisfy this boundary. For example, replace a code call with the transformation, formula, sampling rule and missing-data treatment it implements. Distinguish mathematical symbols and established terms such as OLS, HAC, covariance and bootstrap from program identifiers. Include AI assistance, tools and responsibility in an appropriate acknowledgment or disclosure under the applicable institution/venue rules. If those rules are unknown, label the disclosure provisional in the production metadata and preserve the factual assistance record; do not invent compliance or hide assistance.

Use [body-language-examples.md](body-language-examples.md) for positive/negative examples and [check_academic_body.py](../scripts/check_academic_body.py) for a non-mutating Markdown preflight. Review each located hit against the actual discipline and scope. The checker is a targeted leak detector, not an automatic style or validity certificate. Read the rendered body as well as the source; mathematical symbols, table labels and figure captions must follow the same boundary.

## Citations and final readback

Use APA author-date citations and matching reference entries by default; a supplied user, institution or journal style takes precedence. Preserve verified author names, years, locators and bibliographic metadata. Do not invent or silently complete a reference to make its formatting look finished. Keep direct quotations distinguishable and exact.

For full paper/thesis outputs, apply [scholarly-delivery.md](scholarly-delivery.md): BibTeX/BibLaTeX manages the verified bibliography; LaTeX labels and cross-references connect equations, tables and figures to the argument; actual compilation and visual review are required. Mathematical precision includes symbol definitions, units, assumptions, derivation or source, and the reason for selecting a model. Typesetting cannot replace these explanations.

Before delivery, read the saved body to check paragraph progression, terminology and clear referents; compare every changed factual sentence, number, qualifier and citation with the pinned evidence. Confirm that necessary tables, equations and procedures survived and that concise wording did not strengthen a claim. Reviewers should identify located defects and the smallest repair, not certify a text from sentence counts, a style score or a label. Keep writing quality separate from research-validity and publication-readiness judgments.

## Source and scope of this adaptation

The official ASD Simplified Technical English Maintenance Group [overview](https://www.asd-ste100.org/) and [FAQ](https://www.asd-ste100.org/STE_faq.html) identify STE as a controlled language for technical documentation, developed for English-language maintenance documentation. Their official indexed descriptions were checked on 2026-10-24; page/PDF retrieval returned HTTP 403, so this revision does not claim to have inspected the full standard. The earlier reference recorded a public overview/FAQ check on 2026-10-18. Use the scope statement conservatively: Chinese academic prose may adapt clarity, precision and terminology consistency, but is not formally ASD-STE100-compliant, certified or controlled English. The scholarly argument, citation and inference requirements are this workflow's academic contract, not provisions attributed to STE. Do not reproduce the standard or infer a prescribed Chinese vocabulary, sentence length or academic-paper format from it.
