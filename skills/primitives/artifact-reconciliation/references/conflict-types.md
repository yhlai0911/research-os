# Research artifact conflict types

Load this reference only after two immutable conflict sides and their lineages are pinned.

| Type | Authority | Required proof | Invalid resolution |
|---|---|---|---|
| Fact | Primary evidence and claim-level entailment | source locator, scope comparison, status history | asking the user which fact is true |
| Human choice | Researcher or named decision owner | one accepted decision and rationale | choosing from model preference |
| Schema | Current configured contract plus preserved source | explicit field map and loss audit | deleting or silently coercing fields |
| Execution | Immutable receipt and readback | command/action identity, output, status | letting planned prose override observation |
| Concurrent edit | Common ancestor and both diffs | compatible-intent inventory | last-writer-wins |

For mixed conflicts, resolve in this order: schema identity, execution truth, externally verifiable facts, then human choices. A later step must not rewrite an earlier authority.
