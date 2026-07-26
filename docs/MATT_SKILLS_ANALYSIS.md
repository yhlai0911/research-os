# Matt Pocock Skills: file-level design analysis

## Scope and method

The source was cloned from [mattpocock/skills](https://github.com/mattpocock/skills) at commit [`ed37663cc5fbef691ddfecd080dff42f7e7e350d`](https://github.com/mattpocock/skills/commit/ed37663cc5fbef691ddfecd080dff42f7e7e350d). The audit covered all 167 tracked files at that commit, including all 41 `SKILL.md` files, their direct references and scripts, repository invocation rules, plugin manifests, install scripts, docs mirrors, lifecycle buckets, and release metadata.

The aim was to learn behavioral architecture, not to rewrite upstream prose. Each row below records the main mechanism and its Research OS implication.

The machine-verifiable, one-row-per-upstream-skill disposition is in [`MATT_PORT_MAP.yaml`](MATT_PORT_MAP.yaml). Prompt-level evidence and retained/rejected mechanics are expanded under [`port-audit/`](port-audit/).
The final implementation response to audit findings is tracked in [`PORT_REMEDIATION.md`](PORT_REMEDIATION.md).

## Engineering skills

| Upstream skill | Prompt or architecture mechanism | Research OS decision |
|---|---|---|
| `ask-matt` | Human-only router over a main flow, on-ramps, and standalone tools | Adopt one remembered router; keep it advisory rather than a hidden dispatcher |
| `code-review` | Parallel, independent review axes prevent one kind of quality from masking another | Expand to six research-review axes and aggregate without halo effects |
| `codebase-design` | Shared vocabulary plus branch-specific disclosed references | Use model primitives as vocabulary authorities; disclose specialized branches |
| `diagnosing-bugs` | No hypothesis work before a tight red-capable feedback loop | Research diagnosis starts from an observable bottleneck and discriminating probe |
| `domain-modeling` | Inline glossary maintenance; difficult decisions become ADRs | Use `CONTEXT.md` and Research Decision Records as separate authorities |
| `grill-with-docs` | Thin human wrapper composes grilling with durable domain writeback | `grill-research-idea` composes decision interviewing with `.research/` state |
| `implement` | Spec/ticket drives TDD and independent review before commit | Workpackages drive tracer execution and review; commit remains separately authorized |
| `improve-codebase-architecture` | Survey candidates before selecting and designing one | Separate research-system diagnosis from design execution |
| `prototype` | Throwaway artifact answers one question; result survives, prototype does not become product | Pilot studies reduce one uncertainty and end in a go/no-go decision |
| `research` | Background primary-source investigation writes a cited memo | Add claim-level entailment, source version, conflict, freshness, and ledger status |
| `resolving-merge-conflicts` | Recover both intents from primary sources | Preserve conflicting protocols or datasets when intent cannot be safely reconciled |
| `setup-matt-pocock-skills` | Explore, confirm, then write per-repo adapter configuration | Initialize an additive `.research/` contract with preview and readback |
| `tdd` | Red-green vertical slices at pre-agreed public seams | Use testable analysis contracts where appropriate; do not force TDD on open exploration |
| `to-spec` | Synthesize current context; do not restart the interview | Produce a research brief from verified artifacts and unresolved decisions |
| `to-tickets` | Tracer bullets plus explicit blocking edges | Workpackages are end-to-end tracer studies, not horizontal literature/method silos |
| `triage` | Category and exactly one state; verify before recommending transition | Triage ideas and reviewer requests into kill, repair, pilot, or advance |
| `wayfinder` | Destination, fog, frontier, and one decision ticket per session | Use a durable research decision map for genuinely multi-session uncertainty |

## Productivity skills

| Upstream skill | Prompt or architecture mechanism | Research OS decision |
|---|---|---|
| `grill-me` | Very thin explicit wrapper around an implicit primitive | Keep human entry points thin and rules in model-invoked primitives |
| `grilling` | One dependent decision at a time; agent finds facts, human makes decisions | Adopt directly as the decision-authority split |
| `handoff` | Compact context and point to artifacts instead of copying them | Add artifact hashes, current status, next authorized action, and acceptance receipt |
| `teach` | Mission, resources, learning records, and supersession create durable state | Reuse the state discipline, not the pedagogical renderer |
| `writing-great-skills` | Predictability, invocation load, hierarchy, leading words, pruning | Make these the meta-skill and machine-enforce inventory drift |

## In-progress skills

| Upstream skill | Experimental mechanism | Research OS decision |
|---|---|---|
| `batch-grill-me` | Ask all currently independent frontier questions in a round | Use only when independence is explicit; default to one dependent question |
| `claude-handoff` | Compact and directly launch a Claude background session | Reject platform binding and no-ack dispatch; use portable handoff manifests |
| `loop-me` | Discover workflows and write specs without implementation | Adapt the trigger-input-state-retry-receipt lens to research operations |
| `setup-ts-deep-modules` | Prove guardrails through pass-fail-pass negative testing | Adopt negative tests for validators and workspace setup |
| `to-questionnaire` | Convert knowledge gaps into one-recipient questions | Keep as a future branch, not a core skill |
| `wizard` | Stable runtime template plus variable procedure stages | Adopt declarative contract plus runner separation; reject unreceipted external steps |
| `writing-beats` | Select one reachable narrative beat at a time | Use only as an optional writing strategy, not the core research argument contract |
| `writing-fragments` | Explore raw material before structure | Preserve provenance and acceptance state if later added |
| `writing-shape` | Exploit a source pile paragraph by paragraph with grounding | Research writing instead follows verified argument claims and section functions |

## Deprecated skills

| Upstream skill | Why the evolution matters | Research OS decision |
|---|---|---|
| `design-an-interface` | Became a disclosed branch of a broader design vocabulary | Do not create a skill for every branch; split only for independent invocation |
| `qa` | Moved toward verified, configured triage instead of direct issue creation | No unreviewed external writes; evidence precedes state transition |
| `request-refactor-plan` | God skill decomposed into interview, spec, tickets, and implementation | Keep research ideation, contract, execution, and writing as separate phases |
| `ubiquitous-language` | One-time extraction became active domain modeling | Maintain constructs and vocabulary during work, not as a one-off export |

## Miscellaneous and personal skills

| Upstream skill | Mechanism or limitation | Research OS decision |
|---|---|---|
| `git-guardrails-claude-code` | Regex hook blocks selected commands but is harness-specific | Do not treat hooks as authorization or security boundaries |
| `migrate-to-shoehorn` | Narrow repeatable transformation with explicit patterns | Keep domain-specific migration skills out of the core |
| `scaffold-exercises` | Concrete filesystem contract and lint rules | Reuse deterministic scaffolding only where output schema is stable |
| `setup-pre-commit` | Detect environment, install, wire, then verify | Adopt environment detection and proof, but use `uv` and no automatic commit |
| `edit-article` | Personal editing preference with incomplete gates | Reject as a universal academic writing contract |
| `obsidian-vault` | Useful workflows but hard-coded personal path and tools | Keep storage adapters configurable and project-local |

## Cross-cutting findings

### Adopt

- human-only orchestrators and model-invoked reusable disciplines;
- one router to offset human cognitive load;
- leading concepts that anchor both invocation and execution;
- checkable, demanding completion criteria;
- one-level progressive disclosure;
- shared vocabulary and durable decision records;
- parallel independent alternatives and review axes;
- real context boundaries for long work.

### Repair

The upstream repository manually mirrors promoted skills across README files, docs pages, plugin lists, and metadata. At the pinned commit, those surfaces already contain version, renamed-skill, deprecated-reference, and behavioral drift. Research OS generates its inventory and UI metadata from one catalog and fails CI when any surface differs.

### Reject

- destructive all-skill symlink installation;
- GitHub- or Claude-specific behavior in the research core;
- implicit issue creation, commit, push, or publication;
- hard-coded context-window sizes, labels, paths, or personal tooling;
- forcing every research question into a predetermined lifecycle;
- treating fluent prose as evidence or completion.
