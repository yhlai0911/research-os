# Research assistant: a guide throughout the project

[繁體中文](RESEARCH_ASSISTANT.zh-TW.md) · [Quickstart](QUICKSTART.en.md) · [All 43 skills](SKILL_CATALOG.md)

`research-assistant` is included in the core on `main`. It reads current project evidence, selects and delegates to the applicable skill, checks that skill's real output, then guides the next step. The receiving skill performs the research. You need not learn every skill name before asking for help.

## Start from what you actually have

| Your situation | What to say | First useful effect |
|---|---|---|
| No topic | “I want to write a thesis, but I have no topic. Where should I start?” | The assistant selects `research-1-grill`; grill asks the first background or interest question before dependent topic choices. |
| Existing data | “Inspect this project's data provenance and feasibility before suggesting a question. Preserve the originals.” | A receiving data/design skill checks what the data can support. |
| Existing draft | “Read the current draft and accepted design. Recommend the next repair; do not restart topic selection.” | Review/revision targets the actual gap and pinned draft. |
| Continuation | “Continue this project from its current artifacts and handoff.” | Readback recovers decisions and unfinished gates instead of trusting an old completion claim. |

In Codex you can explicitly name `$research-assistant`. In Claude Code this model-invoked primitive is hidden from the slash-command menu; describe the research need in conversation. Host discovery and actual selection still need verification in the intended project. Installed files or manually read instructions are not proof of native invocation.

With no durable workspace, the assistant can still explain the next step. Additive setup goes to `research-setup` only within an actual local-write grant. Multiple plausible projects require a target choice before their contents are inspected.

## Choose the kind of help

- **Guidance:** explain the stage, missing prerequisite and next useful action.
- **Recommendation:** compare options and explain a preferred next step; a recommendation is not execution.
- **Delegated technical choice:** inside explicit bounds, the receiving skill can choose reversible implementation details and record why.
- **Authorized execution:** transfer the bounded task to its owning skill, then read back its artifact, checks and verdict. Additional authority is required for new costs or external actions.

Research questions, hypotheses, exclusions, inferential meaning and failure rules remain consequential research choices. The assistant conveys the receiving skill's question rather than inventing your agreement. Standalone translation, proofreading and formatting should stay within that request.

## How progression works

| Need or stage | Receiving skill | What makes progress observable |
|---|---|---|
| Missing authorized workspace | `research-setup` | Valid canonical paths with existing work preserved |
| Unclear topic or research choice | `research-1-grill` | Bounded question, alternatives and feasibility; no hidden preset topic |
| Decisions/evidence need one contract | `research-2-brief` | Traceable brief with readiness and open issues |
| Failure conditions missing | `research-3-falsify` | Falsifiers and kill/repair/continue rules recorded before results |
| Executable slices needed | `research-4-tasks` | Bounded task graph, inputs, authority and acceptance checks |
| One eligible task is ready | `research-5-run` | Actual execution, verified output and sealed receipt |
| Design/results/draft need challenge | `research-6-review` | Pinned-target findings, repairs and review verdict |
| Research supports the requested output | `to-plan`, `to-proposal`, `to-paper` | Destination requirements met without upgrading planned work into results |
| A continuation is needed | `research-save` | Durable current identities and next gate |

This is a route map, not an instruction to run every skill for every study. The assistant may stay at a stage after useful work when a required answer or evidence is still missing. It reads the returned artifact and domain verdict before advancing. One invocation of `research-5-run` executes one eligible package, not the entire project.

Direct mainline calls remain available. `research-help` only recommends an entry point and stops. Explicit `research-auto` is a separate adaptive workflow. With no native skill interface, a fully read, distinct delegated instruction-followthrough phase can be recorded as such; it must not be labelled native invocation or used to bypass a denied operation.

## Open real outputs

When a reading view helps, the assistant delegates its production to `render-research-deliverable`. The reply briefly explains the output, links its real title and names the next research step. Generation and target verification happen before the link is returned. A local file or localhost link is local to that computer; cross-device access needs a supported, authorized attachment route.

See [reading views and scholarly delivery](DELIVERABLES.en.md) for tables/charts/revisions, academic prose, APA references, equations and actual LaTeX PDF requirements. See [verification](RESEARCH_ASSISTANT_TESTING.md) for the difference between distribution tests, browser interaction, model behavior and native invocation.
