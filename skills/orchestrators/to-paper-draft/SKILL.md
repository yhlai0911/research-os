---
name: to-paper-draft
description: Draft an academic paper from verified research artifacts.
---

# To Paper Draft

Run `$render-research-deliverable` with:

- destination: `paper blueprint` when required analyses or results are missing;
- destination: `manuscript draft` only when completed results and provenance exist;
- source: the current canonical Research Brief and registered result artifacts;
- journal, language, format, and style from the user's request.

This wrapper requires a current canonical Research Brief. If the workspace or brief is missing, stop and recommend `$develop-research` or `$to-research-brief`; do not silently create the prerequisite here.

Stop after readback. Never fill a results section with expected, simulated, or plausible findings unless they are explicitly labeled as such and the requested artifact permits them.
