---
name: falsification-first
description: "Try to kill a research claim before reviewers do. Use when a hypothesis, mechanism, novelty claim, empirical design, or model needs falsifiers, rival explanations, placebo tests, negative controls, failure thresholds, or a predeclared kill-repair-continue rule."
---

# Falsification First

Lead with **kill**: define what evidence would make the project abandon or materially weaken its central claim before designing evidence that could support it.

## Load the research contract

1. Resolve `.research/config.yaml` per [writeback-protocol.md](../research-workspace-contract/references/writeback-protocol.md). Stop with `blocked: research_workspace_not_initialized` when it is absent or invalid.
2. Resolve the canonical context, claims, briefs, maps, pilots, and decisions paths from that file. Treat paths such as `.research/CONTEXT.md` and `.research/evidence/claims.yaml` only as baseline defaults; never probe them before resolution.
3. Read the resolved context and claims registry, followed by the active brief, literature map, identification design, methodology, pilot results, and relevant decisions at their resolved paths.
4. Select the smallest set of claims whose failure would change the paper's contribution. Stop when no central claim can be named or a required resolved path is missing; request workspace repair instead of inventing a parallel path.

Preserve the resolved claims registry's `schema_version`, declared `statuses`, existing claim IDs, status history, and unrelated entries. Use only statuses already declared by that registry; keep falsification-plan state and `kill`, `repair`, or `continue` actions out of the claim-status field.

## Design the attack

For each central claim:

1. State the strongest rival explanation or null model.
2. State the observation that should differ under the claim and the rival.
3. Design discriminating tests, not generic robustness volume.
4. Include applicable placebo outcomes, placebo treatments, negative controls, pre-trends, alternative measurements, alternative samples, sensitivity bounds, out-of-sample tests, and independent replication.
5. Specify the required data, statistic, direction, uncertainty, and threshold for each test.
6. State what each possible result means. Prevent an ambiguous failure from being redescribed as support.
7. Predeclare one action: `kill`, `repair`, or `continue`. Define the repair boundary so a repair cannot silently change the estimand, construct, population, or contribution.
8. Rank tests by information gained per unit of cost. Put the cheapest decisive test first.

Delegate missing data checks to `$data-feasibility`, design validity to `$identification-design`, and a low-cost execution to `$pilot-study`.

## Write back

Reuse the current registered falsification plan for the same topic, or create `<artifact-id>-falsification.md` under the resolved briefs directory. Begin it with `Status: complete|partial|blocked`, `Updated`, and scope, then include the complete claim-to-falsifier matrix and predeclared action rules. Update each affected entry in the resolved claims registry with its falsifier, threshold, and plan pointer. Record any later repair that changes a hard-to-reverse choice under the resolved decisions directory; never overwrite the original threshold after outcomes are known.

Register the outcome and read it back per the writeback protocol.

Set artifact status `complete` only when every central claim has a predeclared discriminating plan; use `partial` when a nonfatal branch remains unresolved or a decisive test is `pilot-required`, and `blocked` when no central claim, falsifier, or required resolved path can be established.

## Stop conditions

- Stop and reframe or kill a claim that has no conceivable falsifier.
- Stop at `pilot-required` when a decisive test depends on unknown data behavior.
- Stop when thresholds are chosen after inspecting the confirmatory result.
- Stop when a robustness test cannot distinguish the claim from its strongest rival.
- Never convert a failed predeclared test into a successful exploratory result without relabeling the claim.

## Completion criteria

Finish only when:

- every central claim has at least one discriminating falsifier and strongest rival;
- every falsifier specifies data, expected contrast, threshold, interpretation, and action;
- all applicable placebo, negative-control, timing, measurement, and sensitivity branches are addressed or marked non-applicable with reasons;
- kill, repair, and continue boundaries cannot overlap;
- claim records point to the immutable plan;
- no confirmatory threshold depends on already-observed confirmatory outcomes;
- the saved plan, affected claim and decision records, and Artifact-index row are re-read and agree on IDs, paths, thresholds, and status; and
- the run is reported `complete` only after that readback passes, otherwise `partial` or `blocked` according to the status rule above.
