# Research Context

## Mission

Determine whether cross-market equity volatility shocks exhibit empirically distinguishable finite-speed, inertial propagation rather than only delayed diffusion.

## Artifact index

| Kind | Topic | Current artifact or claim IDs | Status | Updated | Supersedes |
|---|---|---|---|---|---|
| research brief | finite-speed versus diffusion | `briefs/financial-wave-diffusion.md` | partial | 2026-07-26 | — |
| research decisions | core comparison and ex ante distance | `RDR-0001`, `RDR-0002` | complete | 2026-07-26 | — |
| evidence task | closest literature and novelty boundary | `C001`, `C002`, `C003`, `C004`, `C005` | blocked | 2026-07-26 | — |
| pilot protocol | model separation before market interpretation | `pilots/model-separation-protocol.md` | complete | 2026-07-26 | — |
| review | referee pre-mortem | `reviews/referee-pre-mortem.md` | complete | 2026-07-26 | — |
| workpackage map | four tracer studies | `workpackages/INDEX.md`, `WP-01`, `WP-02`, `WP-03`, `WP-04` | partial | 2026-07-26 | — |
| academic research plan | finite-speed versus diffusion | `plans/PLAN-0001-financial-wave-diffusion.md` | partial | 2026-07-26 | — |

## Research question

Does a constrained graph telegraph model provide distinguishable and out-of-sample useful evidence of finite-speed global equity volatility transmission relative to graph diffusion and standard time-series baselines?

## Unit of analysis and scope

- Unit: major national equity index by aligned trading interval.
- Primary outcome: deviation of log volatility from a market-specific baseline.
- Frequency: not yet fixed; daily data are a feasibility baseline, while intraday or session-decomposed data may be required for arrival-time claims.
- Excluded: order books, Maxwell–Boltzmann distributions, direct price-direction forecasting, and literal physical-law claims.

## Constructs and measures

| Construct | Meaning | Proposed measure | Status |
|---|---|---|---|
| Shock field | Cross-market risk deviation after market baselines and the common global mode | Zero-sum projection of residualized log range or realized volatility | proposed |
| Financial distance | Ex ante path along which timing should vary | Closing-time or time-zone distance; trade distance as robustness | proposed |
| Inertia | Persistence in the change of the shock field | Constrained lagged first difference | proposed |
| Finite-speed evidence | Later response at greater ex ante distance | First-significant and peak-response timing after alignment | unresolved |
| Equilibrium boundary | Dissipation of cross-market residual differences | Norm of the zero-sum propagation field and graph-gradient decay; common mode modeled separately | proposed |

## Mechanism and rival explanations

Candidate mechanism: information and risk re-pricing propagate through market-opening opportunities and cross-market linkages with inertia and damping.

Rivals:

1. non-synchronous trading mechanically creates lags;
2. a higher-order VAR mimics oscillation without finite-speed propagation;
3. common global news creates simultaneous responses;
4. volatility persistence creates delayed peaks;
5. a misspecified or endogenous graph manufactures distance effects.

## Estimand or prediction target

Primary estimands are the damping parameter, graph propagation parameter, mode-specific response roots, and distance-arrival relation. Primary prediction targets are next-session volatility and peak-arrival bins.

## Identification

Identification is unresolved. Required discriminators include ex ante distance, explicit information-availability alignment, simulation recovery, spectral restrictions, and comparisons against delayed-diffusion and flexible VAR baselines.

## Contribution claim

Candidate contribution: convert the diffusion-versus-inertial-propagation distinction into competing, rejectable restrictions for cross-market volatility transmission. Novelty claim C005 is blocked until the full boundary search is executed.

## Glossary

| Canonical term | Definition | Avoid |
|---|---|---|
| Wave-like | Evidence consistent with finite-speed inertial graph dynamics | markets obey waves |
| Diffusion-like | Evidence consistent with first-order graph smoothing | heat moves through markets |
| Telegraph model | Damped second-order graph dynamics | pure wave equation |
| Equilibrium boundary | Long-run dissipation of the zero-sum cross-market field, with the common mode modeled separately | all market volatilities become equal |

## Open decisions

- Select a sampling frequency that can identify arrival timing.
- Fix a primary ex ante graph before observing outcome propagation.
- Define a shock source and event protocol without outcome-based event selection.
- Verify the claimed literature delta.

## Reviewer concerns

- Physics analogy may relabel a second-order autoregression.
- Daily data may make propagation speed observationally inseparable from market hours.
- The graph may be endogenous.
- Laplace equilibrium may be economically empty.
- Flexible baselines may dominate out of sample.
