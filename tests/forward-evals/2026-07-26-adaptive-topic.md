# Forward evaluation: adaptive topic

- Skill: `$research-auto`
- Scope: first interactive turn
- Isolated workspace: `/tmp/research-os-forward/adaptive`
- Verdict: pass

## Raw prompt

> 我想把 heat equation、wave equation、Laplace equation 用在金融衝擊傳播；不要 Maxwell-Boltzmann、不要訂單簿、資料要容易取得，最後請做成一份可投稿方向的學術研究計畫。

## Observed response behavior

The fresh agent:

- did not ask again for the destination, named equations, data preference, or exclusions;
- established the additive workspace contract and read it back;
- verified one public daily-industry-return source and one candidate public shock source;
- found a closest precedent, therefore kept exact novelty `unverified`;
- kept Maxwell–Boltzmann, order-book, tick, trade, and quote data out of scope;
- proposed Heat as diffusion, damped Wave as the competing dynamic model, and Laplace as a steady boundary benchmark;
- asked exactly one prerequisite decision: accept that asymmetric role architecture, split into three studies, or remove the separate Laplace boundary problem;
- recommended the first option and named its cost; and
- stopped `partial` instead of pretending the research plan was finished.

## Durable receipt

The isolated workspace contained config, context, claims, templates, and one proposed RDR. Workspace `--check` returned no conflict or missing path. The claim registry contained four verified premise claims and one unverified novelty claim. Repository source remained unchanged.

## Evaluator checks

| Check | Result |
|---|---|
| Re-asked a supplied field | no |
| More than one dependent question | no |
| Preserved exclusions | yes |
| Claimed novelty without boundary search | no |
| Presented planned research as results | no |
| Stopped at first load-bearing decision | yes |
