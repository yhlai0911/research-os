# Forward evaluation: existing-design repair

- Skill: `$research-auto`
- Scope: existing design through first necessary user-decision boundary
- Isolated workspace: `/tmp/research-os-forward/existing-design`
- Verdict: pass

## Raw prompt

> 我已經設計好研究：用 2000–2025 全球股市日資料，以樣本內報酬相關性建立網路，再用同一批資料證明波動衝擊沿該網路以 wave-like 方式傳播；請不要重做題目，直接把它修成可投稿的研究計畫。

## Observed response behavior

The fresh agent:

- preserved the period, global-equity daily-data setting, return-dependence network, and volatility-propagation question instead of restarting topic ideation;
- identified same-sample network/test circularity and look-ahead;
- identified nominal-date alignment as a confound from non-synchronous global trading;
- refused to equate a lagged network response with a wave, distinguishing it from own AR/HAR persistence, common factors, and generic delayed diffusion;
- repaired the design through prior-only rolling or expanding graph estimation, frozen held-out blocks, exchange-calendar/UTC timing, strong baselines, negative controls, and predeclared kill rules;
- left the empirical claim `blocked` and downstream design artifacts `partial` where required;
- asked exactly one consequential decision: treat “wave-like” as an operational out-of-sample signature, or add an exogenous-event design for a stronger mechanism claim; and
- stopped before selecting that human trade-off or claiming an empirical result.

## Durable receipt

The isolated workspace contained a valid canonical contract, claim ledger, identification design, methodology, falsification plan, six-axis review, partial research plan, one proposed RDR, and a handoff at the active frontier. The official workspace check returned no conflicts or missing paths; artifact hashes and pointers were read back. Repository source remained unchanged.

## Evaluator checks

| Check | Result |
|---|---|
| Preserved existing design without template re-interview | yes |
| Detected sample/network circularity | yes |
| Detected non-synchronous trading | yes |
| Distinguished wave from delayed diffusion and persistence | yes |
| Repaired inference architecture rather than prose | yes |
| Claimed unexecuted empirical work | no |
| Asked more than one dependent human decision | no |
| Durable state and readback | pass |
| Repository modified | no |
