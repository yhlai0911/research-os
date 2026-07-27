---
name: research-5-run
description: Claim and execute one eligible research workpackage with bounded authority, falsification gates, receipts, and readback.
---

# Step 5 - Run a Task

> **Mainline step 5 of 6.** Open the first response by telling the user where they are: previous step `research-4-tasks`, next step `research-6-review`.

Use **claim** as the leading concept. Execute exactly one unblocked vertical research slice, prove its result, and update the frontier without letting two agents perform the same package.

Read [execution-contract.md](references/execution-contract.md) before claiming, recovering, or sealing a package.

## Resolve and select

Resolve `.research/config.yaml` per [writeback-protocol.md](../../primitives/research-workspace-contract/references/writeback-protocol.md). Resolve context, briefs, workpackages, claims, decisions, pilots, reviews, papers, proposals, and handoffs from the canonical entries. Read the current package index and the minimum artifacts needed to verify blockers.

Use the package named by the user. Otherwise select the first current package whose blockers have read-back complete receipts. Do not infer readiness from ordering alone. If multiple eligible packages imply materially different cost, risk, or external authority, recommend one and ask exactly one decision.

Pin the package ID, file SHA-256, brief version, input versions, completion criterion, falsifier, allowed reads and writes, and expected receipt.

**Complete when:** one current eligible package and its immutable execution envelope are explicit.

## Claim before work

Use the bundled claim helper, or an equivalent atomic compare-and-set primitive:

```bash
uv run --no-project python <research-workspace-contract>/scripts/atomic_claim.py claim \
  --state-root <resolved-workpackages-directory> \
  --claim-id <package-id>-v<version>-<sha256-prefix>-a<attempt> \
  --source <absolute-package-path> \
  --expected-sha256 <pinned-sha256> \
  --owner <agent-or-task-id>
```

Read the receipt. Continue only on `claimed`. On `already-claimed`, stop or select another eligible package. On `already-sealed`, verify the sealed receipt and return `no-op`. Never delete or steal a stale claim automatically; recover it only after the owner, timeout, and current package state are inspected and the user authorizes the recovery when another actor may still be running.

Keep the ready package byte-for-byte immutable while it is claimed. The atomic claim is the sole ownership record. Re-read both the claim and the still-pinned package.

**Complete when:** this execution owns one read-back claim for the pinned package hash.

## Execute the declared slice

Perform only the package procedure and writes allowed by its context envelope. Verify inputs before use and record commands, source versions, sample or fixture identity, environment, failures, outputs, and zero-cost local transformations needed for reproduction.

Use the narrow model primitives required by the package. For empirical or computational work, establish an independent observable failure before repair when practical. For literature or evidence work, write claim chains rather than uncited summaries. For human-subject, licensed-data, paid, messaging, submission, publication, or other external mutations, stop for the exact missing authority; the package invocation does not imply it.

Do not silently broaden scope. A newly discovered design decision stops execution, persists the decision frontier, and leaves the package `partial` or `blocked`.

**Complete when:** the declared procedure has either produced its expected outputs or reached a named stop condition with preserved evidence.

## Test the package and the project

Run the package-local acceptance checks and its predeclared falsifier. Then run the project-level integration, reproducibility, or consistency check named in the package. Invoke `$research-review` when the package changes a load-bearing contribution, theory, identification, measurement, result, or destination-readiness claim.

Classify the domain result:

- `continue` when the acceptance gate passes and no kill condition fires;
- `repair` when a bounded, predeclared repair can change the failed inference;
- `kill` when the central package obligation is falsified or infeasible;
- `blocked` when required evidence, authority, or access is unavailable.

Do not average away a fatal axis or relabel a failed threshold as a limitation.

## Seal and advance

Keep the ready package immutable. Write a JSON execution receipt containing at least `claim_id`, `owner`, `status`, `source_sha256`, `domain_verdict`, `outputs`, `checks`, and `readback`, plus pinned inputs, actual operations, output hashes, failed attempts, acceptance and falsifier results, costs when any, claim or artifact IDs, and authorization receipts.

Before sealing, update claims, dependent artifacts, the package index, and the single current `## Artifact index` row through their resolved paths, then read them back and include their hashes or IDs in the execution receipt:

Seal the atomic claim:

```bash
uv run --no-project python <research-workspace-contract>/scripts/atomic_claim.py seal \
  --state-root <resolved-workpackages-directory> \
  --claim-id <package-id>-v<version>-<sha256-prefix>-a<attempt> \
  --owner <agent-or-task-id> \
  --result complete \
  --receipt <absolute-receipt-path>
```

Use `complete`, `partial`, or `blocked` for the execution receipt independently of the domain verdict. The helper refuses to seal if the ready package changed, the receipt schema or identity differs, or the receipt result differs from `--result`. Re-read the sealed claim receipt, immutable package, outputs, claims, project-level checks, and Artifact-index row. Recompute the unblocked frontier from immutable packages and exact-version sealed receipts; no post-seal mutation is needed to make a dependent eligible.

If execution stops before sealing, preserve the active claim and exact continuation state unless safe release is explicitly warranted. An acknowledged owner may run the helper's `release` command with an explicit reason; it archives rather than deletes the claim. Never report completion merely because a package file says `Status: complete`.

## Finish only when

- exactly one package was claimed and no concurrent owner was displaced;
- the executed work matches the pinned envelope and source versions;
- every result, failure, and cost has provenance;
- package and project acceptance gates ran;
- claims and downstream readiness were updated without inflation;
- the claim was sealed with a readable receipt;
- the next frontier was recomputed; and
- no commit, push, submission, upload, purchase, message, or institutional commitment occurred without separate authority.

Then hand off explicitly: when the recomputed frontier still holds an eligible package, name `research-5-run` again for that package; when none remains eligible, name `research-6-review` as the next step. Never run either yourself.
