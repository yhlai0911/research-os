# Workpackage execution contract

## State machine

```text
proposed → ready → claimed → complete | partial | blocked
                       ↘ released
```

`claimed` is a concurrency lock, not evidence of work. Claim IDs include package ID, version, source-hash prefix, and attempt ID. `complete`, `partial`, and `blocked` require a sealed receipt for that exact immutable version and attempt. A research-domain verdict such as `continue`, `repair`, or `kill` is carried inside that receipt and must not be confused with execution status.

## Immutable execution envelope

Pin before claiming:

- package ID and SHA-256;
- source brief and decision versions;
- input artifact and dataset versions;
- allowed reads and writes;
- explicit external actions not authorized;
- procedure;
- package-local acceptance criterion;
- falsifier and stop thresholds;
- required project-level integration check;
- expected outputs and receipt path.

A material envelope change invalidates the claim. Stop, supersede the package through the planning workflow, and claim the replacement instead of editing the active target around a failure.

## Stale claims

Elapsed time alone does not prove abandonment. Inspect the owner or task, package state, output paths, and logs. Prefer an acknowledged release. The owner may use `atomic_claim.py release` with a reason; the helper atomically fixes `released` as the only terminal state, moves the claim into history, and writes a release receipt. A later attempt uses a new attempt ID. When the owner cannot be reached, record the recovery decision, preserve the former claim in history, and use a new package version or explicit administrative recovery; never silently delete the lock.

## Receipt minimum

- package, versioned claim ID, owner, start and end timestamps;
- pinned hashes and actual input versions;
- commands or procedures and environment;
- outputs with paths, IDs, versions, and hashes;
- failure and retry history;
- package-local and project-level gate results;
- falsifier result and research-domain verdict;
- external actions and authorization receipts, if any;
- claim, decision, and Artifact-index updates;
- final `complete|partial|blocked` and readback evidence.

The seal helper requires JSON fields `claim_id`, `owner`, `status`, `source_sha256`, `domain_verdict`, `outputs`, `checks`, and `readback`; it recomputes the source hash and matches identity and result before sealing.
