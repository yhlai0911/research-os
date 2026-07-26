---
name: data-feasibility
description: "Verify data obtainability, timing, coverage, licensing, alignment, missingness, and fitness for the estimand. Use when a research design depends on a dataset, API, archive, index, panel, event window, frequency, or merge whose real availability and semantics must be checked."
---

# Data Feasibility

Treat **obtainability** as an empirical claim. Verify that the required observations can be lawfully acquired, aligned, and interpreted before calling a design feasible.

## Load the research contract

1. Read only `.research/config.yaml` first. Stop with `blocked: research_workspace_not_initialized` when it is absent or invalid.
2. Resolve the canonical context, claims, briefs, reviews, proposals, workpackages, and decisions paths from that file. Treat paths such as `.research/CONTEXT.md` and `.research/evidence/claims.yaml` only as baseline defaults; never probe them before resolution.
3. Read the resolved context and claims registry, followed by the active brief, identification design, proposal, workpackages, and prior data decisions at their resolved paths.
4. Extract the required population, units, variables, identifiers, geography, frequency, horizon, release timing, and merge keys. Stop when the target estimand or a required resolved path is missing; request workspace repair instead of inventing a parallel path.

Preserve the resolved claims registry's `schema_version`, declared `statuses`, existing claim IDs, status history, and unrelated entries. Use only statuses already declared by that registry; keep data-feasibility verdicts in the review rather than adding them as claim statuses.

## Verify the data

1. Build a requirement-to-source matrix. Include every variable and every observation window required by the design.
2. Verify existence and semantics from primary sources: provider documentation, data dictionaries, schemas, sample files, release calendars, licenses, and API responses.
3. Test access with the smallest safe read when credentials and authorization already exist. Never purchase access, accept a license, or request personal data without explicit user authority.
4. Audit coverage by entity, geography, date, frequency, and revision vintage. Distinguish advertised coverage from observed coverage.
5. Audit timing for publication lag, restatements, backfills, timezone, event timestamp, observation timestamp, and availability-to-researcher timestamp.
6. Audit joins for identifier stability, one-to-many expansion, survivorship, entity changes, duplicates, and unmatched rates.
7. Measure missingness and sample loss when data are available. Otherwise specify the exact pilot needed to measure them.
8. Test fitness against the estimand and construct. A field with the right name but the wrong meaning does not pass.
9. Record licensing, privacy, retention, redistribution, and replication-package constraints.

Delegate source verification to `$evidence-research`, construct validity to `$construct-design`, and a minimum acquisition test to `$pilot-study` when full access is premature.

## Decide and write back

Assign one verdict: `feasible`, `feasible-with-repair`, `pilot-required`, `infeasible`, or `blocked`.

Reuse the current registered review for the same topic, or create `<artifact-id>-data-feasibility.md` under the resolved reviews directory (baseline `.research/reviews/`). Begin it with `Status: complete|partial|blocked`, `Updated`, and scope, then include the requirement matrix, primary-source evidence, observed tests, risks, and feasibility verdict. Update every affected data premise in the resolved claims registry with its support status and report pointer. Record durable access, licensing, or dataset choices under the resolved decisions directory.

Register the outcome in the single `## Artifact index` table in the resolved context with columns `Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes`. Update the current row for the same kind and topic when its artifact ID is unchanged. When replacing an artifact, preserve the prior row as `superseded`, add the new current row, and name the prior ID in `Supersedes`.

Map verdicts to artifact status mechanically: `feasible` is `complete`; `feasible-with-repair` and `pilot-required` are `partial`; `infeasible` is `complete` as a diagnostic outcome but blocks a dependent design; and `blocked` is `blocked`.

## Stop conditions

- Stop at `blocked` when access, credentials, legal terms, or source documentation cannot be verified.
- Stop at `infeasible` when a load-bearing variable, window, population, or lawful use is unavailable.
- Stop and escalate when human-subject, personal, sensitive, or licensed data lack approval.
- Never infer historical availability from present-day API output.
- Never reuse a stale sample as proof of current coverage.

## Completion criteria

Finish only when:

- every required variable and window maps to a verified source or explicit blocker;
- access, semantics, timing, coverage, joins, missingness, licensing, and replication constraints are each classified;
- observed checks are separated from provider claims and assumptions;
- the verdict follows from the weakest load-bearing requirement;
- affected claim entries and durable decisions are updated;
- no unavailable or unverified data are represented as feasible;
- the saved review, affected claim and decision records, and Artifact-index row are re-read and agree on IDs, paths, verdict, and status; and
- the run is reported `complete` only after that readback passes, `partial` for unresolved nonfatal requirements, and `blocked` when a load-bearing requirement or required resolved path is unavailable.
