# Guided workflow delegation

The assistant chooses and transfers work; the receiving skill implements its research obligations. A natural-language research mission can authorize this delegation without the novice typing each workflow name. This is not permission for arbitrary skills to trigger in unrelated conversations.

## Route from inspected state

| Observed need | Receiving skill | Effect and return gate |
|---|---|---|
| Durable workspace absent, additive local setup authorised | `research-setup` | Create/verify only the contract; leave topic and data unresolved |
| No topic, broad idea or unresolved research choice | `research-1-grill` | Ask the first prerequisite question; bounded accepted idea only after actual answers |
| Accepted idea and evidence need one research contract | `research-2-brief` | Traceable canonical brief with honest readiness |
| Ready question lacks failure rules | `research-3-falsify` | Explicit falsifiers and kill/repair/continue rules |
| Accepted design needs bounded executable slices | `research-4-tasks` | Read-back task graph and immutable eligible package |
| One eligible package and its actual authority exist | `research-5-run` | Atomic claim, declared work, checks and sealed receipt |
| Current design/result/draft needs substantive review | `research-6-review` | Pinned target, independent findings and repair gate |
| Verified research needs the requested plan/proposal/paper | `to-plan`, `to-proposal`, `to-paper` | Destination contract, truthful source/readiness gates; required LaTeX still applies |
| A durable continuation is requested | `research-save` | Verified current identities and continuation state |

Do not select a successor solely because the preceding skill wrote a file. Inspect its domain verdict, completion conditions, missing facts and pending decisions. The assistant can remain at the same stage after useful work when a required answer is absent.

## Make a real transfer

Read the selected full SKILL.md and applicable references, then transfer the original user input, objective, scope, accepted choices, unresolved questions, input identities, allowed local operations, stop conditions and expected artifact/readback. A supported independent agent or native skill interface can receive this task. Where no native skill API exists, explicitly execute the loaded receiving discipline as a separate instruction-followthrough phase and retain its actual operations and outputs. Never present that as native invocation. A denied native operation or file read is a stop for that action, not a reason to use this fallback.

`scripts/prepare_workflow_handoff.py` is a non-mutating preflight. Its generated route inventory comes from the catalog. It locates the actual target instructions and checks the workspace contract and local-write grant; `contract_ready` does not mean the research gates passed. Its output is a transfer input, never proof that a skill executed.

The receiving workflow owns substantive research, its decision questions, artifacts and acceptance. Preserve its atomic claims, explicit human choices and terminal branches. It returns control instead of directly launching another mainline. The assistant then reads the returned result and may delegate the next applicable workflow within the same still-valid grant. If required inputs or authority are absent, explain the specific prerequisite and continue only independent guidance.

Do not count a single rewritten response as multiple skill executions. Keep source/target, instruction versions, input, real action, output and gate distinct. The assistant may convey the receiver's exact question without inventing a learner answer. In a teaching role, obtain the role setting from the user/coordinator and label it.

Direct `$research-1-grill` and other named calls remain available. The existing native implicit-selection metadata is not an assistant-delegation allowlist; do not claim it implements one. Retaining explicit native discovery for mainlines prevents unrelated automatic selection, while this bounded, user-requested instruction-followthrough is separately evidenced. `research-help` continues recommending and stopping; it does not inherit this controller role.

## No-topic example

Input: “I want to write a thesis, but I have no topic. Where should I start?”

The assistant identifies a no-topic request and delegates topic clarification to `research-1-grill`, establishing an empty contract first only when the actual grant permits it. The grill skill asks about the learner's background or interest before dependent topic, data or method choices. Do not prewrite a topic list or reuse an old study as a hidden answer. When the learner has not answered, preserve the question and stop the dependent branch. Nothing has become an accepted research idea yet.
