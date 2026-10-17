---
name: research-6-review
description: Attack the current research design or draft as a skeptical journal panel and record every finding.
---

# Step 6 - Review

> **Mainline step 6 of 6.** Open the first response by telling the user where they are. After review, the next step is a named repair gate or, only when readiness passes, a deliverable (`to-plan`, `to-proposal`, or `to-paper`).

Lead with **reject**. The purpose is to surface the reasons a referee would decline, while repair is still cheap.

Resolve `.research/config.yaml` and register every outcome per [writeback-protocol.md](../../primitives/research-workspace-contract/references/writeback-protocol.md).

Run `$research-review` over the current canonical artifact. Keep contribution, theory, identification, measurement and data, evidence, and execution axes independent, and let the worst load-bearing axis control the verdict.

## Prerequisite

This wrapper requires a current canonical artifact to review — a brief, plan, workpackage receipt, or draft. When none exists, stop with the exact prerequisite and recommend `research-2-brief`. It never repairs the design itself and never invokes another user-invoked skill.

## Report to the user

For every major or fatal finding, give the axis, the reason a referee would raise it, and the smallest repair that would change the failed inference. Separate findings the user must decide on (scope, contribution, commitment) from findings the agent can repair without a decision.

Return finding IDs, target locations, repair owner, evidence needed, acceptance test, and one concrete return route. Recommend `research-auto` for authorized integrated repair, `research-4-tasks` for bounded repair packages when a ready brief exists, or the named primitive for a narrow defect. Do not recommend paper production while an open load-bearing finding invalidates it. A completed review is not an accepted research design.

Stop after the review report and its readback receipt. Do not rewrite the artifact to make findings disappear, and never let writing quality conceal a rejection reason.
