# Research OS architecture

## Design objective

Research OS seeks process predictability under uncertain evidence. It does not prescribe one method or one output. It makes each run pass through explicit decisions, evidence states, observable gates, and durable writeback.

## Invocation layers

### User-invoked orchestrators

These skills expose long flows, project setup, durable synthesis, or artifact creation. Codex metadata sets `policy.allow_implicit_invocation: false` for their direct discovery. They can also receive a bounded delegation from `research-assistant` under the user's actual research mission. A mainline does not recursively launch another mainline; `research-help` still recommends and stops. Native explicit-selection metadata is not a per-caller delegation implementation.

Six of them form the **mainline**, `research-1-grill` through `research-6-review`. The numbering is load-bearing rather than cosmetic: the pipeline's order is the first thing a user sees in the skill list, and each mainline skill states its own position and names its successor on reaching a completion gate. Handing off is not the same as launching — a mainline skill names the next step and stops. `research-3-falsify` precedes decomposition so that no execution cost is committed to a claim with no predeclared way to fail.

`research-auto` is the adaptive alternative to walking the mainline by hand. It starts from the user's actual seed and chooses one model-invoked primitive at a time according to the live bottleneck. It may establish the workspace contract because invocation explicitly authorizes the scoped local workflow; it still cannot launch a different user-only orchestrator.

`research-status` is read-only. It reports mainline position, current artifacts, and unresolved claims from the Artifact index and the claim registry, and never advances or repairs anything.

### Model-invoked primitives

`research-assistant` is the guide/controller in this layer. It reads actual state, selects the applicable skill, transfers the bounded task, and checks the receiving skill's output before guiding the next step. The novice need not type every name. The assistant does not replace the receiving skill with an embedded research pipeline. Missing setup can be delegated to `research-setup` only inside an actual additive local-write grant; other missing facts or research choices remain gates. With no native skill interface, fully read delegated instruction-followthrough is a separate, honestly labelled execution mode, never a native-invocation claim or a fallback around denial. The non-mutating handoff helper reports contract prerequisites, not research readiness. `research-help` retains its route-only contract.

These skills contain reusable research discipline and rich trigger descriptions. An orchestrator may rely on them without duplicating their rules. Examples include mechanism building, counterfactual design, evidence research, citation entailment, and falsification.

### Router

`research-help` is the route-only entry point. It names the right human-invoked next step and stops. The numbered mainline already answers "what comes next" for anyone inside the pipeline, so the router now serves the narrower case of a user who does not yet know which entry point applies.

## Durable project contract

`research-workspace-contract` owns initialization and resolution of `.research/config.yaml`; `research-setup` is its explicit thin wrapper. The default contract is:

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

`research-workspace-contract/references/writeback-protocol.md` is the single definition of the resolution procedure, the Artifact index contract, and the three index statuses. Skills bind to it by link and state only what is specific to their own artifact. `validate_repository.py` enforces the link rather than the literal table header; the earlier string check produced the same bookkeeping in 33 files and would have propagated it to every new skill.

Authority is partitioned:

- vocabulary, scope, current question, and current-artifact index → `CONTEXT.md`;
- consequential choices → one Research Decision Record;
- external propositions and source status → `evidence/claims.yaml`;
- approved research contract → a brief;
- executable uncertainty reduction → a workpackage;
- cross-session state → a handoff manifest.

Artifacts link to each other instead of restating each other.

One ready workpackage is executed through `research-5-run`. A filesystem-level atomic claim prevents concurrent owners from running the same package; only a sealed, read-back receipt unlocks dependent work.

Canonical conflicts are not resolved by last-writer-wins. `artifact-reconciliation` pins both identities and lineages, separates factual evidence from human choice and schema/execution conflicts, creates one superseding artifact, invalidates stale consumers, and proves one current pointer.

Revision review uses one deterministic comparison packet generated from immutable base and target hashes. Research review axes, citation audit, and destination rendering consume the same changed-section, claim-ID, table, and diff inventory; an empty delta is a verified no-op.

## Research control flow

Three entry routes share the same durable state: assistant-guided delegation, direct mainline invocation, and explicit `research-auto`. The assistant is a selector/controller; receiving skills own research work and gates. In the direct, user-paced mainline:

```text
research-setup
    ↓
1 grill ──→ 2 brief ──→ 3 falsify ──→ 4 tasks ──→ 5 run ──→ 6 review
    │          │            │            │          │          │
    └──────────┴────────────┴────────────┴──────────┴──────────┘
         each step registers its artifact, names the next step, and stops
                                    ↓
                    to-plan / to-proposal / to-paper
```

`research-status` reads that state at any point without advancing it. The adaptive route collapses the same gates into one loop:

```text
topic / direction / equation / data / draft / review
    ↓
research-auto
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

Codex metadata is generated in the repository. Claude Code metadata is generated at installation time so canonical `SKILL.md` frontmatter remains limited to `name` and `description`. Other harnesses require their own generated and verified adapter before cross-harness equivalence can be claimed.

### Codex installation contract

Research OS is distributed as one catalogued suite of 43 skills, not as one root skill. A bare GitHub repository URL is therefore not a valid input to Codex's single-skill installer, which requires one or more internal skill paths.

The repository-owned installer is the suite authority:

1. honor an explicit target, preferably a project `.agents/skills`; the installer's existing personal default remains `$CODEX_HOME/skills` or `~/.codex/skills`, which is not a current-host discovery guarantee;
2. preflight every catalogued destination and the ownership marker before any write;
3. stage and hash every pending skill;
4. promote the complete set or roll back;
5. write `.research-os-install.json` with catalog version, source commit, mode, and per-skill hashes;
6. run `scripts/verify_install.py` to read back all 43 core directories, required Codex metadata, hashes, receipt and readable local Markdown dependencies; copy mode rewrites source-bucket links for the flattened installation. Host discovery/loading and actual workflow execution are separate validation layers.

Claude plugin manifests are outside this Codex-first contract. Adding one cannot prove a complete Codex installation.

### Claude Code installation contract

Claude Code discovers standalone personal skills at `~/.claude/skills/<name>/SKILL.md` and project skills at `.claude/skills/<name>/SKILL.md`. `scripts/install_skills.py --harness claude-code` materializes all 43 catalogued skills into one of those standard locations.

The adapter is deterministic and catalog-driven:

- `invocation: user` generates `disable-model-invocation: true`;
- `invocation: model` generates `user-invocable: false`;
- source `SKILL.md` files remain unchanged;
- copy mode is required because the installed frontmatter differs from source;
- the receipt records `harness: claude-code`, source hashes, and installed hashes;
- `scripts/verify_install.py --harness claude-code` verifies paths, frontmatter policy, hashes, and receipt.

This standalone-skills contract does not require `.claude-plugin/plugin.json`. A future marketplace plugin would be a separate generated distribution surface with namespaced commands and its own add, install, reload, version, and validation gates.

## Mutation boundary

Research work may read local or external sources when needed. External writes—submission, publication, messages, issue creation, purchases, uploads, or remote state changes—remain outside the implied authority of a research skill. A write requires an explicit action request and a receipt/readback.

## Context boundaries

Keep one decision branch in one context. Use a handoff or map when the effort exceeds a session. Workpackages are independent contexts whose inputs and outputs are artifact pointers, not copied conversation history. Their execution envelopes name allowed reads, writes, stop branches, and expected receipts. Parallel agents may explore independent designs or review axes; each writes to a separate artifact before aggregation.

## Lifecycle

The current core ships only catalogued skills. Future experimental or deprecated buckets must be excluded from installation unless their lifecycle is explicitly represented in the catalog. Deprecation requires a replacement path and a repository-wide ghost-reference check.

## Presentation and scholarly production

`render-research-deliverable` owns derived reading views; `research-assistant` forwards only verified result links. The HTML renderer and reply builder are standard-library Python mechanics, not a research engine or native-chat invocation implementation. Pages preserve actual values, units, missingness and available revision versions. Device/session scope belongs in the reply; a presentation request does not authorize hosting or upload.

Academic manuscripts retain disciplinary prose and managed citations. The shared writing contract requires numbered/referenced equations, defined symbols, real LaTeX and bibliography production, clean final citation/reference/glyph diagnostics, exact-source packaging and current visual QA. HTML is a companion; tool records remain outside the academic body. See [delivery requirements](DELIVERABLES.en.md).
