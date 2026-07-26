---
name: grill-research-idea
description: Interrogate a research idea one decision at a time until it is researchable.
---

# Grill Research Idea

Use a **decision tree** as the leading concept. Resolve one consequential branch at a time until the idea has a bounded question, a defensible mechanism, observable evidence, and a way to fail.

## Workspace resolution

- Read only `.research/config.yaml` first. If it is absent, stop and recommend that the user invoke `setup-research-os`; do not invoke it yourself.
- Before reading any other workspace artifact, resolve `canonical.context`, `canonical.decisions`, and `canonical.claims` from the config. Resolve relative values against the repository root and preserve absolute values.
- Bind the resolved paths as `CONTEXT`, `DECISIONS`, and `CLAIMS`. Read and write only through these bindings.
- Treat the setup baseline paths as defaults only, never as fallback targets. If a required key is missing, invalid, or has a file/directory type collision, stop as `blocked`; do not probe or write a default path.

## Guardrails

- After path resolution, read `CONTEXT`, relevant records in `DECISIONS`, and `CLAIMS`.
- Investigate facts with the appropriate model-invoked research primitives. Do not ask the user to recall facts the agent can verify.
- Put choices, interpretations, priorities, and trade-offs to the user one at a time. Include a recommendation and its cost.
- Never invoke another user-invoked skill.
- Update `CONTEXT`, `DECISIONS`, and `CLAIMS` as understanding changes. Do not leave settled knowledge only in chat.

## Stage 1 — Fix the root

Establish the phenomenon, decision problem, target audience, desired contribution, and practical constraint that motivate the study. Separate the user's desired outcome from claims about the world.

**Complete when:** the user confirms one sentence describing what the study must explain, estimate, predict, design, or decide.

## Stage 2 — Walk the tree

Resolve dependent decisions in order:

1. research question and unit of analysis;
2. constructs, outcomes, treatments, mechanisms, or theoretical objects;
3. target population, setting, period, and boundary conditions;
4. estimand or prediction target;
5. contribution relative to the closest literature;
6. data obtainability and measurement;
7. identification or inferential logic;
8. discriminating predictions, falsifiers, and kill thresholds;
9. ethics, reproducibility, scope, and explicit non-goals.

Use `research-grilling` for the interview discipline and `research-domain-modeling` when terms or relations change. Resolve prerequisite branches before their dependents.

**Complete when:** every live branch is either resolved, backed by a named evidence task, or explicitly ruled out.

## Stage 3 — Stress-test researchability

Try to break the idea with the closest prior work, data constraints, rival mechanisms, identification threats, measurement failure, and ethical constraints. Convert each surviving uncertainty into a testable question rather than optimistic prose.

**Complete when:** the idea has at least one credible failure condition and no hidden assumption that would invalidate the whole design.

## Stage 4 — Write the resolved idea

Write or update one canonical decision record in `DECISIONS`. Record:

- confirmed research question and intended contribution;
- construct and mechanism definitions;
- unit, population, setting, and scope;
- required evidence and current claim-chain links;
- proposed design direction;
- falsifiers and kill thresholds;
- unresolved facts and user decisions;
- status: `researchable`, `blocked`, `repair`, or `needs-map`.

Write canonical terms to `CONTEXT` and factual claims to `CLAIMS`.

**Complete when:** the user confirms the record and a fresh researcher can understand why the idea is or is not researchable.

## Register and verify

For every terminal outcome reached with a readable workspace, write or update its canonical record through the resolved output path, then register every created or updated current artifact or outcome in the single `## Artifact index` table in `CONTEXT`:

`| Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes |`

Keep substantive content in its canonical artifact; the index contains only identity, current state, timestamp, and lineage. Upsert one current row per `Kind` and `Topic`. When an ID changes, preserve the former row as `superseded` and put its ID in the replacement row's `Supersedes`; never create a second index or two current rows for the same subject. A claim-only outcome uses its claim IDs in the artifact-or-claim-ID column.

Read back the resolved artifact or outcome and `CONTEXT`, then verify the row's ID, status, timestamp, and lineage. Use only these index statuses:

- `complete` only when every skill completion gate passes and both the artifact or outcome and its row read back successfully;
- `partial` when a usable, read-back durable result exists but remains incomplete, or only the index update or index readback cannot be sealed;
- `blocked` when no usable current result can be produced because a load-bearing input, permission, resolved path, artifact write, or artifact readback fails.

If the config or `CONTEXT` cannot be read, report `blocked` and state that registration did not occur. Keep domain-specific states in the canonical artifact; they do not replace the three index statuses.

## Stop branches

- Stop as `blocked` when a load-bearing factual premise cannot be verified.
- Stop as `repair` when the idea can survive only after a named change.
- Stop as `needs-map` when the unresolved decision graph will not fit one session; recommend `research-wayfinder` and yield.
- Stop as `kill-candidate` when evidence makes the central claim infeasible, non-distinct, unethical, or unfalsifiable; record the reason and ask the user for the final decision.
