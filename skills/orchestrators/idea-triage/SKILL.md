---
name: idea-triage
description: Classify research ideas as kill, repair, pilot, or advance.
---

# Idea Triage

Use **verdict** as the leading concept. Test each idea against evidence and recommend exactly one of `kill`, `repair`, `pilot`, or `advance`; let the user make the final decision. Preserve a concept-level memory so renamed duplicates and newly changed evidence resume the prior case instead of restarting it.

## Workspace resolution

- Read only `.research/config.yaml` first. If it is absent, stop and recommend that the user invoke `setup-research-os`; do not invoke it yourself.
- Before reading any other workspace artifact, resolve `canonical.context`, `canonical.decisions`, `canonical.claims`, `canonical.briefs`, and `canonical.pilots` from the config. Resolve relative values against the repository root and preserve absolute values.
- Bind the resolved paths as `CONTEXT`, `DECISIONS`, `CLAIMS`, `BRIEFS`, and `PILOTS`. Read and write only through these bindings.
- Treat the setup baseline paths as defaults only, never as fallback targets. If a required key is missing, invalid, or has a file/directory type collision, stop as `blocked`; do not probe or write a default path.

## Guardrails

- After path resolution, read `CONTEXT`, relevant records in `DECISIONS`, `BRIEFS`, `PILOTS`, and `CLAIMS`.
- Verify literature, data, method, and feasibility facts with model-invoked primitives. Ask the user only for priorities, acceptable risk, interpretation, and the final verdict.
- Never invoke another user-invoked skill.
- Keep one canonical verdict record per idea in `DECISIONS`; update it rather than creating competing summaries.

## Choose triage mode

- **named idea** — evaluate one supplied idea;
- **discover** — inventory registered proposed ideas and place them in `new`, `changed-evidence`, `unchanged-current`, or `blocked-input` queues; or
- **resume** — continue one prior verdict whose load-bearing evidence frontier changed.

For every candidate, derive a concept signature from the canonical question, population, unit, mechanism, estimand or prediction target, and core data requirement. Compare the signature and accepted aliases against existing verdict records before allocating an ID. A renamed or reworded match resumes the existing idea and preserves its lineage; lexical difference alone never creates a new verdict.

Each verdict record must store `checked_at` and an evidence frontier: load-bearing claim IDs, source versions or access states, relevant decision IDs, and their hashes or updated timestamps. Discover and resume mode recompute only candidates whose frontier changed. An unchanged current frontier is a verified `no-op`, not a new review.

## Stage 1 — Establish the gate

State the idea in one sentence and identify its load-bearing claims. Evaluate:

- materiality of the question;
- closest literature and defensible contribution delta;
- theory or mechanism coherence;
- construct and measurement validity;
- data obtainability;
- identification or inferential credibility;
- falsifiability, ethics, execution cost, and opportunity cost.

Mark every premise as verified, contradicted, or unresolved in the claim chain.

**Complete when:** the evidence needed to distinguish the four verdicts is explicit and no factual gap is disguised as a preference.

## Stage 2 — Recommend one verdict

Apply these meanings:

- **Kill:** a load-bearing premise is false, the contribution is immaterial, the design is irreparably invalid, the study is unethical, or the opportunity cost is unjustifiable.
- **Repair:** the question remains valuable but named, correctable defects block execution.
- **Pilot:** one or more pivotal uncertainties can be resolved cheaply by a smallest end-to-end tracer study with a predeclared kill threshold.
- **Advance:** the question, contribution, feasible evidence, inferential path, and falsification plan are sufficiently supported for a research brief.

Attach one reason code without creating extra top-level verdict states:

- `already-established` — the proposed delta is already answered by inspected evidence;
- `out-of-scope` — the idea is valid but outside the accepted mission or resource boundary;
- `invalid` — a load-bearing premise is contradicted or the design cannot support the claim;
- `superseded` — another registered idea or decision now owns the same contribution;
- `evidence-changed` — a prior verdict is being resumed because its frontier materially changed; or
- `ready` — no negative reason applies.

Present the recommended verdict, strongest evidence for it, strongest counterargument, and the minimum condition for changing it.

**Complete when:** the user accepts or overrides the recommendation and states why.

## Stage 3 — Write the verdict

Update the idea's canonical decision record in `DECISIONS` with:

- canonical idea ID, concept signature, accepted aliases, verdict, reason code, `checked_at`, and decision owner;
- the exact evidence frontier and what changed since the prior check;
- evidence and claim-chain links;
- rejected alternatives;
- conditions and risks;
- required repair, pilot specification, or advancement readiness;
- next user-invoked workflow as a recommendation only.

For `pilot`, write the approved tracer specification in `PILOTS` with its observable outcome and kill/continue threshold.

**Complete when:** the verdict and its consequences are recoverable from the resolved canonical workspace without this conversation.

## Register and verify

For every terminal outcome reached with a readable workspace, write or update its canonical record through the resolved output path, then register every created or updated current artifact or outcome in the single `## Artifact index` table in `CONTEXT`. A `pilot` registers both the verdict record and the tracer specification:

`| Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes |`

Keep substantive content in its canonical artifact; the index contains only identity, current state, timestamp, and lineage. Upsert one current row per `Kind` and `Topic`. When an ID changes, preserve the former row as `superseded` and put its ID in the replacement row's `Supersedes`; never create a second index or two current rows for the same subject. A claim-only outcome uses its claim IDs in the artifact-or-claim-ID column.

Read back each resolved artifact or outcome and `CONTEXT`, then verify every row's ID, status, timestamp, and lineage. Use only these index statuses:

- `complete` only when every skill completion gate passes and all artifacts or outcomes and their rows read back successfully;
- `partial` when a usable, read-back durable result exists but remains incomplete, or only an index update or index readback cannot be sealed;
- `blocked` when no usable current result can be produced because a load-bearing input, permission, resolved path, artifact write, or artifact readback fails.

If the config or `CONTEXT` cannot be read, report `blocked` and state that registration did not occur. A `no-op` must read back the already-current row instead of adding one. Keep domain-specific states in the canonical artifact; they do not replace the three index statuses.

## Stop branches

- Stop as `blocked` rather than forcing a verdict when pivotal facts remain unverifiable.
- Stop as `conflict` when canonical artifacts disagree; surface the contradiction for the user to resolve.
- Stop as `no-op` when the same concept already has a current verdict supported by an unchanged evidence frontier; read back the existing record and update no timestamp merely to manufacture activity.
- Stop discovery after producing the four queue buckets; do not silently triage every idea or launch its next workflow.
- Never silently promote an idea or launch the recommended next workflow.
