# Matt port remediation ledger

This ledger records the final Research OS disposition of prompt- and repository-level findings in `docs/port-audit/`. The audit files preserve what each upstream skill actually did and what was missing at inspection time; this file is the current implementation readback.

## Closed for v1.0

| Finding | Final Research OS mechanism | Mechanical proof |
|---|---|---|
| No adaptive topic-to-output flow | `develop-research` recomputes one load-bearing frontier, separates facts from decisions, preserves exclusions, and stops at destination readiness | fresh-agent adaptive evaluation |
| Source contract mixed with rendered output | `synthesize-research-brief` is the only Research Brief writer; `render-research-deliverable` owns destination profiles and derived-export provenance | validator plus no-results paper evaluation |
| No academic research-plan output | `to-research-plan`, a canonical plans path, template, and renderer profile | workspace and catalog tests |
| Workpackage graph had no executor | `execute-workpackage` claims and executes one immutable ready package, runs package/project gates, and seals a receipt | atomic competition/idempotence tests |
| Wayfinder charting could collapse into work | explicit `chart` and `work` modes; chart stops after create-then-wire; work claims before reading or asking | prompt audit plus shared atomic helper |
| Concurrent nodes could double-run | versioned atomic directory claim with owner, source hash, `already-claimed`, `already-sealed`, release history, and sealed-version conflict | claim race, release, mutation, and no-op tests |
| Claim sealing trusted mutable source or prose receipt | source hash is recomputed; JSON receipt schema, owner, claim ID, source hash, and result must match | negative seal tests |
| Workspace setup could green-light malformed state | preflight and check validate canonical keys, baseline-vs-adapter boundary, Artifact index, claims statuses, template markers, and path types while allowing mutable context prose | pass-fail-repair and adapter tests |
| Routine choices inflated decision history | four-part RDR admission test: costly reversal, surprising without rationale, genuine trade-off, and downstream ambiguity | prompt contract and catalog composition check |
| Skill dependencies existed only in prose | catalog `composition` graph must exactly match every `$skill` reference; unknown or ghost references fail validation | repository validator |
| Lifecycle and distribution were implicit | catalog defaults declare stable/core/no replacement; v1 installs the complete catalog | repository validator and installer |
| Installer could overwrite its marker or leave a half-copy | marker ownership preflight, staging, hash verification, atomic promotion, rollback, provenance receipt, and idempotent copy/symlink modes | installer conflict, marker, and symlink tests |
| Release packaging ran too few gates | release runs catalog sync, repository validation, pytest, deterministic archive construction, manifest/CRC/hash readback, and dirty-tree attestation | release script and release-time double build |
| Writing had only one-shot drafting | `research-writing` has evidence-safe Explore, Shape, and Draft/Audit modes, immutable raw input, and edit-aware reread | prompt-level audit |
| Diagnosis could proceed without a fully evidenced loop | `research-diagnosis` requires exact-symptom, reproducibility, runtime, and agent/HITL receipts; stochastic escalation; pre-repair red/post-repair green; and tagged cleanup | prompt regression test plus receipt reference |
| Revision axes could inspect different changes | one deterministic Markdown-aware comparison packet pins base/target hashes and changed sections, claim IDs, tables, and diff; review, citation, and renderer share it and stop on `no-op` | comparison-packet deterministic/no-op test |
| Canonical conflicts could stop but not recover | `artifact-reconciliation` classifies authority, preserves both lineages, supersedes parents, invalidates stale consumers, and proves exactly one current pointer | validator, composition graph, and prompt regression test |
| Triage could restart renamed ideas | concept signatures, aliases, evidence-frontier `checked_at`, discover/resume queues, dedup, reason codes, and verified `no-op` | prompt regression test |
| Interaction uncertainty did not fit an empirical pilot | `pilot-study` selects an empirical tracer or quarantined interaction prototype with actors, states, variants, observations, thresholds, and separate promotion authority | prompt regression test |
| Research Brief writer and plan prerequisite authority could drift | `synthesize-research-brief` is the sole canonical writer; renderer rejects Brief destinations; `to-research-plan` never initializes or synthesizes missing prerequisites | unique-writer and wrapper-authority regression test |
| Cross-harness enforcement was ambiguous | catalog generates Codex metadata in-repo and Claude Code invocation frontmatter at install time; each harness has an independent verifier path | Codex/Claude install integration tests, README, and architecture contract |

## Deliberately outside the v1 core

- Claude Marketplace plugin distribution plus Cursor- or other vendor-specific invocation adapters;
- receipt-aware managed upgrade and uninstall;
- cryptographic release signing or automatic GitHub Release publication;
- recurring research-operation automation;
- harness-mandated background scheduling for every evidence lookup;
- sequential one-at-a-time presentation of alternative designs and its optional disclosed recommendation;
- an exhaustive success/near-miss/blocked equivalence matrix for every thin wrapper and primitive pair;
- the upstream package-graph three-question quiz where v1 already applies stronger structural graph gates;
- a standalone recipient-questionnaire system;
- generic execution of paid, licensed, human-subject, submission, messaging, or institutional actions.

These are not silently “supported.” They require separate design, authority, and forward tests before promotion.

## Behavioral port boundary

The port is intentionally not a word-for-word rewrite. Research OS retains control mechanics that change reliability—invocation boundaries, leading concepts, adaptive routing, feedback loops, independent reviews, completion gates, context boundaries, writeback, and stop branches—while replacing code-specific objects with research contracts, evidence claims, estimands, falsifiers, workpackages, proposals, and manuscripts.
