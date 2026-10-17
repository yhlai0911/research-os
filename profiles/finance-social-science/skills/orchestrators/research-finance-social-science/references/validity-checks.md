# Conditional validity checks

Use only sections relevant to the design. These are design prompts, not evidence that a method's assumptions hold.

## Finance and market data

- Record dataset provenance, license/access limits, observation timestamps and what was knowable at the decision date. Distinguish publication date, reporting period, release lag, and later revisions.
- Check survivorship, delistings, universe reconstitution, corporate actions, stale prices, currency/unit conventions, and missingness before estimating returns or factors.
- For prediction/backtests, split chronologically; prevent future information leaking into preprocessing, feature choice, tuning, and evaluation. Specify overlapping labels and whether purge/embargo is needed. Lock the test set before model selection.
- Separate in-sample fit from out-of-sample evidence. Include appropriate benchmarks, turnover, transaction costs, liquidity/capacity assumptions, and sensitivity where relevant. Correct for repeated model searching; never portray a favorable backtest as a guaranteed future return.
- For event studies, state event-time definition, anticipation/leakage risk, concurrent events, estimation window, dependence across units/dates, and inference strategy.

## Quantitative social science and causal designs

- Distinguish descriptive association, prediction, and causation. Name target population, treatment/exposure, outcome, unit, estimand, interference risks, and selection process.
- Separate identification assumptions from estimator choice. For experiments check assignment, attrition, noncompliance, spillovers and analysis population. For observational designs state plausible confounding and what evidence can challenge the identifying assumptions.
- For difference-in-differences inspect treatment timing, comparison groups, anticipation, parallel trends and heterogeneous effects; a non-significant pretrend test alone does not establish identification. For instruments address relevance, exclusion, independence and whose effect is identified. For discontinuity designs address assignment, manipulation, bandwidth and continuity.
- Justify uncertainty estimates for clustering, repeated observations, small cluster counts, sampling weights and multiple testing as applicable. Separate prespecified primary outcomes from exploratory ones. Do not choose significance thresholds after seeing results.
- Define constructs and measurement validity, translation/cultural comparability, missing-data assumptions and sensitivity. A convenient proxy is not automatically the intended construct.

## Qualitative and mixed methods

- Match sampling, recruitment, positionality and analytic approach to the interpretive question. Preserve negative cases and rival explanations; avoid numerical saturation thresholds without methodological justification.
- Distinguish participant accounts, researcher interpretations and triangulated findings. Keep coding decisions and revisions auditable; do not invent interviews, consent, quotes or inter-rater agreement.
- For mixed methods, state how strands connect, where disagreement is retained, and what each strand can and cannot support.

## People, permissions and reproducibility

- Identify consent, ethics review, vulnerable populations, reidentification risks and data-use restrictions before collection or release. Approval requirements depend on institution, jurisdiction and project; mark unresolved requirements rather than asserting blanket exemptions.
- Minimize personal data. Keep restricted/raw data outside public repositories; share only authorized derivatives. Record data availability without exposing credentials or participant information.
- Retain a reproducible transformation trail, software/environment versions, random seeds where meaningful, and an analysis decision log. Distinguish a runnable pipeline from independently reproduced results.
