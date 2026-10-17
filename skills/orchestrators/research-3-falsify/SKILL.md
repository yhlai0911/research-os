---
name: research-3-falsify
description: Predeclare what evidence would kill the current research design before any expensive work begins.
---

# Step 3 - Try to Kill It

> **Mainline step 3 of 6.** Open the first response by telling the user where they are: previous step `research-2-brief`, next step `research-4-tasks`.

Lead with **kill**. A design that cannot fail cannot be tested, and a threshold chosen after seeing the result proves nothing. This step runs before task decomposition so that no expensive work is committed to an unfalsifiable claim.

Resolve `.research/config.yaml` and register every outcome per [writeback-protocol.md](../../primitives/research-workspace-contract/references/writeback-protocol.md).

Run `$falsification-first` against the central claims of the current canonical Research Brief.

## Prerequisite

This wrapper requires a current canonical Research Brief. When the workspace or the brief is missing, stop with the exact prerequisite and recommend `research-2-brief`, or `research-auto` for end-to-end development. It never initializes the workspace, synthesizes a missing brief, or invokes another user-invoked skill.

## Report to the user

State, in plain language: which claims are now falsifiable, what result would kill each one, which decisive test is cheapest, and whether any claim survived only because no falsifier could be found. A claim with no conceivable falsifier is a stop condition, not a finding.

Stop after the falsification plan and its readback receipt. Do not run the tests here, and never revise a predeclared threshold after an outcome is known.
