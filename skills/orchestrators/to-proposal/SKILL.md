---
name: to-proposal
description: Turn a research design into a grant, institutional, or project proposal.
---

# To Proposal

Determine whether the requested destination is a `grant proposal`, `institutional proposal`, or `project proposal`. When that choice changes required evidence or structure and is not explicit, use `$research-grilling` to ask exactly one decision question.

Then run `$render-research-deliverable` with the selected proposal profile, current canonical Research Brief, audience or call, format, language, constraints, and requested decision.

This wrapper requires a current canonical Research Brief. If the workspace or brief is missing, stop and recommend `$research-auto` or `$research-2-brief`; do not silently create the prerequisite here.

Stop after readback. Do not invent budget, eligibility, team commitments, partnerships, approvals, facilities, deadlines, or submission status.
