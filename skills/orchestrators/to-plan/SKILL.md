---
name: to-plan
description: Convert a verified Research Brief into an executable academic research plan.
---

# To Research Plan

Run `$render-research-deliverable` with:

- destination: `academic research plan`;
- source: the current canonical Research Brief;
- audience, format, institutional template, duration, and language from the user's request.

This wrapper requires a current canonical Research Brief whose readiness is sufficient for planning. If the workspace or brief is missing, stop with the exact prerequisite and recommend `$research-auto` for end-to-end development or `$research-2-brief` when the design is already settled. It never initializes the workspace or synthesizes a missing brief; it does not silently inherit that authority.

Stop after the renderer's readback receipt. Do not submit the plan or invent dates, access, resources, partners, or approvals.
