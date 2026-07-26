# Research OS architecture

## Design objective

Research OS seeks process predictability under uncertain evidence. It does not prescribe one method or one output. It makes each run pass through explicit decisions, evidence states, observable gates, and durable writeback.

## Invocation layers

### User-invoked orchestrators

These skills expose long flows, project setup, durable synthesis, or artifact creation. Codex metadata sets `policy.allow_implicit_invocation: false`. The agent may recommend one through `/ask-research`, but a user-only skill never silently launches another user-only skill.

`develop-research` is the flagship end-to-end orchestrator. It starts from the user's actual seed and chooses one model-invoked primitive at a time according to the live bottleneck. It may establish the workspace contract because invocation explicitly authorizes the scoped local workflow; it still cannot launch a different user-only orchestrator.

### Model-invoked primitives

These skills contain reusable research discipline and rich trigger descriptions. An orchestrator may rely on them without duplicating their rules. Examples include mechanism building, counterfactual design, evidence research, citation entailment, and falsification.

### Router

`ask-research` is the route-only entry point. It names the right human-invoked next step and stops. Most users who already want a finished research artifact should invoke `develop-research`; the router exists for users who only need orientation.

## Durable project contract

`research-workspace-contract` owns initialization and resolution of `.research/config.yaml`; `setup-research-os` is its explicit thin wrapper. The default contract is:

```text
.research/
├── config.yaml
├── CONTEXT.md
├── decisions/
├── evidence/claims.yaml
├── maps/
├── briefs/
├── plans/
├── workpackages/
├── pilots/
├── reviews/
├── papers/
├── proposals/
├── handoffs/
└── templates/
```

Authority is partitioned:

- vocabulary, scope, current question, and current-artifact index → `CONTEXT.md`;
- consequential choices → one Research Decision Record;
- external propositions and source status → `evidence/claims.yaml`;
- approved research contract → a brief;
- executable uncertainty reduction → a workpackage;
- cross-session state → a handoff manifest.

Artifacts link to each other instead of restating each other.

One ready workpackage is executed through `execute-workpackage`. A filesystem-level atomic claim prevents concurrent owners from running the same package; only a sealed, read-back receipt unlocks dependent work.

Canonical conflicts are not resolved by last-writer-wins. `artifact-reconciliation` pins both identities and lineages, separates factual evidence from human choice and schema/execution conflicts, creates one superseding artifact, invalidates stale consumers, and proves one current pointer.

Revision review uses one deterministic comparison packet generated from immutable base and target hashes. Research review axes, citation audit, and destination rendering consume the same changed-section, claim-ID, table, and diff inventory; an empty delta is a verified no-op.

## Research control flow

```text
topic / direction / equation / data / draft / review
    ↓
develop-research
    ↓
current frontier ──→ one narrow primitive ──→ durable readback
    ↑                                           ↓
    └────────────── recompute frontier ← evidence or one decision
                                                ↓
                         falsification + independent review
                                                ↓
                                  repair / reframe / kill
                                                ↓
                                  canonical Research Brief
                                                ↓
                             destination-specific renderer
```

The loop is adaptive: it does not run every primitive or assume a fixed Wave → Diffusion → Equilibrium story, causal claim, method, or journal target. Alternative designs are generated only when anchoring or materially different assumptions justify the cost. Designs compete and may be killed.

## Catalog-driven distribution

`skills/catalog.yaml` is the inventory, stable/core lifecycle default, explicit skill-composition graph, and UI metadata source of truth. `scripts/sync_catalog.py` generates:

- every `agents/openai.yaml`;
- `docs/SKILL_CATALOG.md`.

`scripts/validate_repository.py` checks catalog equality, exact descriptions, invocation policy, UI metadata, local links, placeholders, resource hygiene, workspace contracts, the pinned 41-skill upstream port map, and version alignment. This removes the manual mirror drift observed in the reference repository.

Version 1.0 is Codex-first. OpenAI invocation metadata is generated and enforced; other harnesses require their own generated adapter before cross-harness equivalence can be claimed.

## Mutation boundary

Research work may read local or external sources when needed. External writes—submission, publication, messages, issue creation, purchases, uploads, or remote state changes—remain outside the implied authority of a research skill. A write requires an explicit action request and a receipt/readback.

## Context boundaries

Keep one decision branch in one context. Use a handoff or map when the effort exceeds a session. Workpackages are independent contexts whose inputs and outputs are artifact pointers, not copied conversation history. Their execution envelopes name allowed reads, writes, stop branches, and expected receipts. Parallel agents may explore independent designs or review axes; each writes to a separate artifact before aggregation.

## Lifecycle

Version 1.0 ships only catalogued skills. Future experimental or deprecated buckets must be excluded from installation unless their lifecycle is explicitly represented in the catalog. Deprecation requires a replacement path and a repository-wide ghost-reference check.
