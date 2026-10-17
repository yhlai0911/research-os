---
name: journal-fit
description: "Match a research contribution, evidence standard, method, and narrative to a journal audience. Use when selecting target journals, comparing outlet fit, reverse-designing a submission, diagnosing desk-reject risk, or deciding whether a project is finance, economics, management, methods, or interdisciplinary work."
---

# Journal Fit

Choose an **audience**, not a prestige label. Match what the project changes, how it knows, and who must care.

## Load the research contract

1. Resolve `.research/config.yaml` per [writeback-protocol.md](../research-workspace-contract/references/writeback-protocol.md). Stop with `blocked: research_workspace_not_initialized` when it is absent or invalid.
2. Resolve the canonical context, claims, briefs, papers, reviews, and decisions paths from that file. Treat paths such as `.research/CONTEXT.md` and `.research/evidence/claims.yaml` only as baseline defaults; never probe them before resolution.
3. Read the resolved context and claims registry, followed by the active paper, brief, contribution design, methodology, reviews, and submission decisions at their resolved paths.
4. State the contribution delta, method, evidence strength, field conversation, and intended reader in one paragraph. Stop when the contribution, target manuscript version, or a required resolved path is unresolved; request workspace repair instead of inventing a parallel path.

Preserve the resolved claims registry's `schema_version`, declared `statuses`, existing claim IDs, status history, and unrelated entries. Use only statuses already declared by that registry; keep journal rankings, fit judgments, and readiness outcomes in the fit review rather than adding them as claim statuses.

## Build the outlet set

1. Identify three to five plausible journals spanning the real disciplinary boundary. Include a safer fit when appropriate.
2. Verify current aims and scope, article types, author instructions, data and code policies, ethics requirements, fees, and submission constraints from official journal or publisher pages.
3. Inspect recent relevant articles or official issue contents to test revealed audience fit. Do not rely on scope prose alone.
4. Record the date of every volatile fact.
5. Compare each outlet on audience, contribution type, theoretical expectation, identification standard, data standard, method tolerance, narrative style, length, reproducibility policy, and desk-reject risk.
6. Separate verified facts from inference. Treat rankings, acceptance rates, and turnaround claims as unverified unless a primary current source supports them.
7. Specify the smallest manuscript changes required for each outlet. Do not propose changing the research claim merely to imitate a journal.

Invoke `$research-review` for validity risk and `$research-writing` only after the audience decision is made.

## Recommend and write back

Rank the outlets by substantive fit and readiness, not prestige alone. Give one primary recommendation, one credible alternative, and one fallback, each with disqualifiers.

Reuse the current registered fit review for the same paper, or create `<paper-id>-journal-fit.md` under the resolved reviews directory. Begin it with `Status: complete|partial|blocked`, `Updated`, pinned paper identity, and scope. Include the dated evidence matrix, inference labels, required changes, and ranked recommendation. Record a target-journal choice under the resolved decisions directory only after the user confirms it. Do not rewrite the paper or config during fit analysis.

Register the outcome and read it back per the writeback protocol.

Set artifact status `complete` only when the shortlist and ranking have current primary-source support; use `partial` when nonfatal volatile facts or outlet comparisons remain unresolved, and `blocked` when the paper, contribution, official requirements, or required resolved path cannot be verified.

## Stop conditions

- Stop at `blocked` when official scope or submission requirements cannot be verified.
- Exclude an outlet when article type, ethics, data policy, or contribution scope is incompatible.
- Stop and warn when the shortlist contains suspected predatory or identity-confused journals.
- Never claim acceptance probability from fit alone.
- Never treat an old journal policy as current without verification.

## Completion criteria

Finish only when:

- three to five plausible outlets have current primary-source evidence;
- every outlet is assessed on all substantive and operational dimensions;
- facts and inferences are visibly separated and dated;
- each recommendation names required changes and disqualifiers;
- the ranking follows the declared audience and evidence standard;
- any confirmed target decision points to the saved fit review;
- the saved fit review, affected claim and decision records, and Artifact-index row are re-read and agree on target identity, IDs, paths, evidence dates, recommendation, and status; and
- the run is reported `complete` only after that readback passes, otherwise `partial` or `blocked` according to the status rule above.
