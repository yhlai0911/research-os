---
name: data-feasibility
description: "Verify data obtainability, timing, coverage, licensing, alignment, missingness, and fitness for the estimand. Use when a research design depends on a dataset, API, archive, index, panel, event window, frequency, or merge whose real availability and semantics must be checked."
---

# Data Feasibility

Treat **obtainability** as an empirical claim. Verify that the required observations can be lawfully acquired, aligned, and interpreted before calling a design feasible.

## Load the research contract

1. Resolve `.research/config.yaml` per [writeback-protocol.md](../research-workspace-contract/references/writeback-protocol.md). Stop with `blocked: research_workspace_not_initialized` when it is absent or invalid.
2. Resolve the canonical context, claims, briefs, reviews, proposals, workpackages, and decisions paths from that file. Treat paths such as `.research/CONTEXT.md` and `.research/evidence/claims.yaml` only as baseline defaults; never probe them before resolution.
3. Read the resolved context and claims registry, followed by the active brief, identification design, proposal, workpackages, and prior data decisions at their resolved paths.
4. Choose **source preflight** when the user has data but no settled question, or **design fitness** when a target question/estimand exists. In source preflight, inspect actual columns, units, coverage, access and limitations without selecting a question for the user; record target-specific fitness as pending. In design fitness, extract the required population, units, variables, identifiers, geography, frequency, horizon, release timing, and merge keys. A missing research choice is a research frontier, not a broken workspace. Stop when a required resolved path is missing; request workspace repair instead of inventing a parallel path.

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
   In source preflight, state which descriptive or inferential uses are supported, excluded, or still unassessed instead of inventing an estimand.
9. Record licensing, privacy, retention, redistribution, and replication-package constraints.

Delegate source verification to `$evidence-research`, construct validity to `$construct-design`, and a minimum acquisition test to `$pilot-study` when full access is premature.

## Decide and write back

Assign one verdict: `feasible`, `feasible-with-repair`, `pilot-required`, `infeasible`, or `blocked`.

Reuse the current registered review for the same topic, or create `<artifact-id>-data-feasibility.md` under the resolved reviews directory. Begin it with `Status: complete|partial|blocked`, `Updated`, and scope, then include the requirement matrix, primary-source evidence, observed tests, risks, and feasibility verdict. Update every affected data premise in the resolved claims registry with its support status and report pointer. Record durable access, licensing, or dataset choices under the resolved decisions directory.

Register the outcome and read it back per the writeback protocol.

Keep factual feasibility findings in the report and claims registry. A provider's refusal, unavailable dataset, existing user restriction, or routine stop does not by itself create a new research decision. Create a decision record only for a substantive user-confirmed access, licensing, or dataset choice that passes the research-grilling admission tests; then use the configured decision-record template and naming rule (otherwise the next RDR-NNNN). Do not invent DDR/DATA-decision schemas or mark a source fact as an accepted human choice. When no such choice is made, leave decisions unchanged and name the unresolved choice in the report.

Map verdicts to artifact status mechanically: `feasible` is `complete`; `feasible-with-repair` and `pilot-required` are `partial`; `infeasible` is `complete` as a diagnostic outcome but blocks a dependent design; and `blocked` is `blocked`.

## Resolve unit and validation disagreements

Pin the exact field, provider version/locator, units and transformation formula. Compare documented semantics to observed samples and any independent reference on matching dates, aggregation and scale. A magnitude range, median cutoff, variable name, or familiar-looking sample is a diagnostic heuristic, not unit proof. Test the conversion algebra and alignment; do not tune a threshold or overwrite raw data merely to make a validator pass. When documentation and a heuristic disagree, diagnose the check and preserve the failed receipt. When primary evidence itself conflicts, retain the ambiguity and block only the dependent inference. Bound attempts to distinct evidence routes; after repeated checks add no information, record the unresolved alternatives and the exact source needed instead of looping.

For source preflight, a fully observed source inventory may be `complete` while design fitness remains explicitly pending; it does not license a `feasible` design verdict. Record source observations, undecided target, and the next research choice separately. Infeasibility can complete a diagnosis while blocking its dependent design.

## Stop conditions

- Stop at `blocked` when access, credentials, legal terms, or source documentation cannot be verified.
- Stop at `infeasible` when a load-bearing variable, window, population, or lawful use is unavailable.
- Stop and escalate when human-subject, personal, sensitive, or licensed data lack approval.
- Never infer historical availability from present-day API output.
- Never reuse a stale sample as proof of current coverage.

## Completion criteria

Finish only when:

Apply target-specific requirements below only in design-fitness mode. In source preflight, complete the observed source inventory and explicitly leave target fitness undecided; do not request workspace repair merely because that research decision is still open.

- every required variable and window maps to a verified source or explicit blocker;
- access, semantics, timing, coverage, joins, missingness, licensing, and replication constraints are each classified;
- observed checks are separated from provider claims and assumptions;
- the verdict follows from the weakest load-bearing requirement;
- affected claim entries and durable decisions are updated;
- no unavailable or unverified data are represented as feasible;
- the saved review, affected claim and decision records, and Artifact-index row are re-read and agree on IDs, paths, verdict, and status; and
- the run is reported `complete` only after that readback passes, `partial` for unresolved nonfatal requirements, and `blocked` when a load-bearing requirement or required resolved path is unavailable.
