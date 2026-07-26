---
name: to-workpackages
description: Split a research brief into dependency-aware tracer workpackages.
---

# To Workpackages

Use **tracer study** as the leading concept. Decompose a ready research brief into small, end-to-end workpackages that reduce uncertainty and leave independently verifiable artifacts.

## Workspace resolution

- Read only `.research/config.yaml` first. If it is absent, stop and recommend that the user invoke `setup-research-os`; do not invoke it yourself.
- Before reading any other workspace artifact, resolve `canonical.context`, `canonical.briefs`, `canonical.decisions`, `canonical.pilots`, `canonical.reviews`, `canonical.claims`, and `canonical.workpackages` from the config. Resolve relative values against the repository root and preserve absolute values.
- Bind the resolved paths as `CONTEXT`, `BRIEFS`, `DECISIONS`, `PILOTS`, `REVIEWS`, `CLAIMS`, and `WORKPACKAGES`. Read and write only through these bindings.
- Treat the setup baseline paths as defaults only, never as fallback targets. If a required key is missing, invalid, or has a file/directory type collision, stop as `blocked`; do not probe or write a default path.

## Guardrails

- After path resolution, read `CONTEXT`, `CLAIMS`, the canonical brief in `BRIEFS`, and relevant records in `DECISIONS`, `PILOTS`, and `REVIEWS`.
- Refuse to decompose a brief whose status is `blocked` or whose load-bearing decisions are unresolved.
- Verify technical and factual dependencies yourself. Ask the user to decide priorities, acceptable risk, resource commitments, and package boundaries.
- Never invoke another user-invoked skill.
- Write the package index and package records only in `WORKPACKAGES`.

## Stage 1 — Trace obligations

Extract every obligation from the brief: claim, evidence requirement, dataset, construct, estimand, method, falsifier, ethical control, reproducibility artifact, and output. Give each a stable identifier and link it to its canonical source.

**Complete when:** every brief obligation is represented exactly once and missing prerequisites are explicit.

## Stage 2 — Design the first tracer

Make the first workpackage the smallest end-to-end study that can traverse:

```text
question → evidence/data → construct → method → result → falsifier → recorded verdict
```

Prefer a package that can expose fatal data, measurement, identification, or execution problems before expensive scale-up.

**Complete when:** the tracer has observable output, a reproducible procedure, and predeclared kill/repair/continue criteria.

## Stage 3 — Slice the remaining work

Create vertical workpackages rather than separate literature, data, coding, and writing silos. For each package specify:

- identifier, objective, and research uncertainty reduced;
- canonical inputs and outputs;
- blocking edges and external dependencies;
- method, checks, and reproducibility requirements;
- acceptance criteria and failure threshold;
- claim and brief obligations covered;
- status and responsible decision owner;
- a context envelope containing immutable input pointers, allowed reads and writes, completion criterion, stop branches, and expected receipt.

Size each package to fit one focused agent session when practical. Use staged expand–migrate–contract packages for a cross-cutting infrastructure change that cannot remain valid as a vertical slice.

**Complete when:** every package is independently verifiable, its mutation boundary is explicit, and every dependency edge reflects a real prerequisite.

## Stage 4 — Confirm the graph

Present the proposed frontier, package granularity, critical path, parallel opportunities, and highest-risk dependency. Investigate factual objections; ask the user to approve priorities and resource commitments.

Reject cycles, orphan packages, duplicated obligations, and packages that produce activity without a decision-relevant result.

**Complete when:** the user approves the graph and every brief obligation maps to at least one package output.

## Stage 5 — Write the execution set

Write one canonical package index plus one record per package in `WORKPACKAGES`. Use this lifecycle:

```text
proposed → ready → claimed externally → sealed receipt
              ↘ blocked
```

After graph approval, mark a package `ready` only when its blockers, immutable inputs, context envelope, acceptance checks, falsifier, and expected receipt are complete. Keep it `proposed` while a design choice remains and `blocked` when an external prerequisite is unavailable.

A ready package record is immutable execution input. If its question, procedure, input versions, authority, or thresholds change, supersede it with a new version and hash instead of editing it in place. Claim and outcome state live in atomic claims and sealed receipts; do not rewrite the package merely to say `claimed` or `complete`.

**Complete when:** the unblocked frontier can be computed entirely from immutable ready package versions and sealed blocker receipts.

## Register and verify

For every terminal outcome reached with a readable workspace, write or update the canonical package index and package records through `WORKPACKAGES`, then register every created or updated current artifact or outcome in the single `## Artifact index` table in `CONTEXT`:

`| Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes |`

Keep package substance and graph state in `WORKPACKAGES`; the index contains only identity, current state, timestamp, and lineage. Upsert one current row per `Kind` and `Topic`. When an ID changes, preserve the former row as `superseded` and put its ID in the replacement row's `Supersedes`; never create a second index or two current rows for the same subject.

Read back the package index, every package record created or updated by this workflow, and `CONTEXT`; then verify every row's ID, status, timestamp, and lineage. Use only these index statuses:

- `complete` only when every skill completion gate passes and the package set and all of its rows read back successfully;
- `partial` when a usable, read-back package set exists but a non-load-bearing decision or verification remains, or only an index update or index readback cannot be sealed;
- `blocked` when no usable current package set can be produced because the brief is not ready or a load-bearing resource, permission, resolved path, package write, or package readback fails.

If the config or `CONTEXT` cannot be read, report `blocked` and state that registration did not occur. Keep package readiness and stop states in `WORKPACKAGES`; they do not replace the three index statuses.

## Stop branches

- Stop as `brief-not-ready` when decomposition would encode unresolved research choices.
- Stop as `blocked` when a required resource, permission, or dataset is unavailable.
- Stop as `needs-decision` when multiple valid package graphs imply materially different cost or risk.
- Never start a package or invoke another user workflow as part of decomposition.
