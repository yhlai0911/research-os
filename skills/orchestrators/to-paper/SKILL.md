---
name: to-paper
description: Draft an academic paper from verified research artifacts.
---

# To Paper

Run `$render-research-deliverable` with:

- destination: `paper blueprint` when required analyses or results are missing;
- destination: `manuscript draft` only when completed results and provenance exist;
- source: the current canonical Research Brief and registered result artifacts;
- journal, language, format, and style from the user's request.

For paper/thesis delivery, require the renderer's scholarly-delivery contract: developed academic prose and verified literature, explained numbered equations, managed APA citations, editable LaTeX, an actual LaTeX-compiled PDF, first-build evidence, visual QA and a source package. Missing compilation or evidence means partial/blocked delivery, not permission to substitute Word-to-PDF or invent sources. A blueprint remains a blueprint even when its PDF compiles.

This wrapper requires a current canonical Research Brief. If the workspace or brief is missing, stop and recommend `$research-auto` or `$research-2-brief`; do not silently create the prerequisite here.

Stop after readback. Never fill a results section with expected, simulated, or plausible findings unless they are explicitly labeled as such and the requested artifact permits them.
