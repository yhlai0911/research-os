---
name: research-review
description: "Review research as a skeptical journal panel across contribution, theory, identification, measurement and data, evidence, and execution. Use when the user asks for peer review, referee comments, pre-submission audit, red-team review, major-revision risks, or an independent assessment of a paper, brief, model, or proposal."
---

# Research Review

Ask what would make a skeptical reviewer **reject** the work. Keep the six review axes independent so strength on one axis cannot hide failure on another.

## Pin the review target

1. Read only `.research/config.yaml` first. Stop with `blocked: research_workspace_not_initialized` when it is absent or invalid.
2. Resolve the canonical context, claims, briefs, maps, papers, proposals, reviews, pilots, and decisions paths from that file. Treat paths such as `.research/CONTEXT.md` and `.research/evidence/claims.yaml` only as baseline defaults; never probe them before resolution.
3. Select one review mode:
   - **full-target** for a first review of one immutable paper, proposal, brief, model, or result set; or
   - **comparison** for a revision, response-to-review, or any request to review changes.
4. In full-target mode, pin one target by path, version, commit, or hash and read it in full. In comparison mode, pin both base and target identities and run `research-workspace-contract/scripts/build_comparison_packet.py` to create one deterministic packet containing both hashes, changed sections, changed claim IDs, changed tables, and the unified diff.
5. If the packet status is `no-op`, register and report a read-back `no-op`; do not invent review findings. Otherwise freeze the packet hash and give the exact same packet plus linked evidence to every axis.
6. Load only the evidence, decisions, pilots, and prior reviews needed to test the full target or packet. Stop when the mode, target, base, packet, or a required resolved path is ambiguous; request workspace repair instead of inventing a parallel path.

Preserve the resolved claims registry's `schema_version`, declared `statuses`, existing claim IDs, status history, and unrelated entries. Use only statuses already declared by that registry; keep axis and overall review verdicts in the review rather than adding them as claim statuses.

## Run six independent attacks

Review these axes in separate contexts or parallel subagents when available. In comparison mode, every axis must acknowledge the same packet ID and hash and may inspect unchanged context only to understand a changed item:

1. **Contribution** — test novelty, material delta, importance, and the closest competing work.
2. **Theory** — test mechanism, actors, incentives, boundary conditions, and discriminating predictions.
3. **Identification** — test estimand, counterfactual, timing, assumptions, rival explanations, and causal language.
4. **Measurement and data** — test construct validity, provenance, coverage, missingness, alignment, and licensing.
5. **Evidence** — test whether results, citations, robustness, and uncertainty support every material claim.
6. **Execution** — test reproducibility, internal consistency, completeness, ethics, and whether the promised study was actually run.

Require each axis to report:

- one verdict: `pass`, `minor-revision`, `major-revision`, `reject`, or `blocked`;
- findings tied to exact claims, sections, tables, equations, or artifacts;
- why each finding matters;
- the smallest evidence or change that would resolve it; and
- what was checked when no issue was found.

Invoke `$citation-audit`, `$identification-design`, `$data-feasibility`, or `$ethics-reproducibility` only when an axis needs their deeper procedure.

## Aggregate without masking

Present all six reports separately. Do not average scores or discard minority findings. Derive the overall verdict from the worst load-bearing axis, then distinguish fatal defects from repairable work.

Reuse the current registered review for the same target and mode, or create `<target-id>-research-review.md` under the resolved reviews directory (baseline `.research/reviews/`). Begin it with `Status: complete|partial|blocked`, `Updated`, review mode, pinned target identity, base identity and comparison-packet identity when applicable, and scope. Update affected claims in the resolved claims registry to reflect newly verified contradictions or blockers without erasing provenance or prior status history. Do not rewrite the reviewed target.

Register the outcome in the single `## Artifact index` table in the resolved context with columns `Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes`. Update the current row for the same kind and topic when its artifact ID is unchanged. When replacing an artifact, preserve the prior row as `superseded`, add the new current row, and name the prior ID in `Supersedes`.

Set artifact status `complete` for a fully executed `pass`, `minor-revision`, `major-revision`, or `reject` review; these verdicts describe the target, not task completeness. Use `partial` when a non-load-bearing check remains open and `blocked` when a missing target, source, or load-bearing axis prevents a defensible overall verdict.

## Stop conditions

- Stop an axis at `blocked` when its evidence or source artifact is unavailable.
- Stop and repin when the target, base, or comparison packet changes during review.
- Stop `no-op` when base and target hashes are identical.
- Never infer that an omitted check passed.
- Never let stylistic polish lower the severity of a validity failure.

## Completion criteria

Finish only when:

- all six axes have independent verdicts and coverage statements;
- full-target or comparison mode is explicit; comparison reviews pin base, target, one delta packet, and matching acknowledgements from every axis;
- every material target claim is covered by at least one axis;
- every finding has a precise target, consequence, evidence, and repair test;
- conflicts between axes remain visible;
- the overall verdict follows from the worst load-bearing failure;
- the saved review and all affected claim records cross-reference the pinned target;
- the saved review, comparison packet when present, affected claim records, and Artifact-index row are re-read and agree on base/target identity, packet hash, IDs, paths, verdict, and status; and
- the run is reported `complete` only after that readback passes, otherwise `partial` or `blocked` according to the status rule above.
