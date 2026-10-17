---
name: research-2-brief
description: Collapse the current discussion and evidence into a rigorous research brief.
---

# Step 2 - Lock the Design

> **Mainline step 2 of 6.** Open the first response by telling the user where they are: previous step `research-1-grill`, next step `research-3-falsify`.

Run `$research-workspace-contract` if the project contract is absent, then run `$synthesize-research-brief` with this explicit destination:

> Produce or update the one canonical, audience-neutral Research Brief from current verified research state.

Stop after its readback receipt. Return the brief path, readiness status, unresolved blockers, and the next smallest decision or evidence task.

When the brief reads `ready`, name `research-3-falsify` as the next step. When it reads `conditional` or `blocked`, name the gate that must clear first instead. Never run the next step yourself.
