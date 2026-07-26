# Academic Research Plan: Finite-Speed or Diffusive?

- ID: PLAN-0001
- Status: partial
- Version: 0.1
- Updated: 2026-07-26
- Source brief: `briefs/financial-wave-diffusion.md` v0.1
- Decision records: `RDR-0001`, `RDR-0002`
- Claim IDs: `C001`–`C005`

## Executive summary

This project asks whether global equity-volatility shocks exhibit finite-speed, inertial propagation that is empirically distinguishable from delayed diffusion and conventional time-series persistence. It compares a constrained graph-diffusion model with a damped graph-telegraph model on the same zero-sum cross-market shock field and ex ante network. The Laplace relation is retained as the long-run boundary of that field, not promoted into a third dynamic regime.

The design is conditional rather than execution-ready. A reproducible literature boundary, an information-time-aligned data panel, and simulation evidence of model separation must pass before a real-market event study. The plan therefore begins with three independent tracer workpackages and kills or reframes the finite-speed claim when delayed diffusion or flexible autoregression reproduces every proposed signature.

## Problem and significance

Financial connectedness models can describe statistical transmission strength and direction, yet these quantities do not by themselves identify how a shock moves through time. A delayed peak may reflect a finite-speed mechanism, non-synchronous trading, ordinary volatility persistence, a common global shock, or a flexible higher-order autoregression. Calling the response “wave-like” without separating these explanations would add metaphor rather than inference.

The practical distinction matters only if it changes a decision. A finite and reproducible arrival interval could support monitoring or timing decisions in markets not yet fully exposed to a shock. If the apparent interval disappears after information alignment, the study instead establishes a useful negative result: diffusion and standard time-series baselines are sufficient for this setting.

## Research questions and objectives

Primary question:

> Does a constrained graph-telegraph model provide distinguishable and out-of-sample useful evidence of finite-speed global equity-volatility transmission relative to graph diffusion and standard time-series baselines?

Objectives:

1. define one economically coherent shock field, graph, and information clock;
2. derive competing diffusion and damped-propagation restrictions on that field;
3. test whether those restrictions are recoverable under realistic simulated calendars and noise;
4. estimate arrival-time and graph-spectral signatures only after data alignment;
5. compare predictive performance under a common out-of-sample window; and
6. retain, repair, or kill the finite-speed interpretation using predeclared thresholds.

## Literature boundary and contribution

The literature boundary spans volatility connectedness, global spillover networks, telegraph-process finance, graph dynamics, and empirical arrival-time measurement. `C005` remains blocked pending the full boundary search. The plan therefore makes no “first” claim.

The candidate contribution is narrower:

> Convert finite-speed versus diffusive transmission into competing spectral, arrival-time, and forecast restrictions, and test whether those restrictions survive information alignment and flexible baselines.

The contribution fails if the closest literature has already established the same empirical restrictions or if the proposed models are observationally indistinguishable.

## Theory, constructs, and hypotheses

Let the observed volatility field be decomposed as

\[
\mathbf u(t)=\boldsymbol\mu(t)+g(t)\mathbf 1+\mathbf z(t),
\qquad \mathbf 1^\top\mathbf z(t)=0,
\]

where \(\boldsymbol\mu(t)\) contains market-specific baselines, \(g(t)\) is the common global mode, and \(\mathbf z(t)\) is the cross-market propagation field. A fixed ex ante graph has Laplacian \(L\).

Diffusion implies

\[
\dot{\mathbf z}(t)=-\kappa L\mathbf z(t)+\mathbf P\boldsymbol\varepsilon(t),
\]

whereas damped propagation implies

\[
\ddot{\mathbf z}(t)+\gamma\dot{\mathbf z}(t)
=-c^2L\mathbf z(t)+\mathbf P\boldsymbol\varepsilon(t).
\]

The primary discriminating hypotheses are:

- arrival timing increases with ex ante distance after information alignment;
- mode-specific response roots cohere with graph eigenvalues under the damped model;
- a delayed-diffusion or flexible VAR baseline cannot reproduce all accepted signatures; and
- any out-of-sample gain survives a common evaluation window and forecast-loss test.

These are hypotheses, not observed findings.

## Data and identification

The unit is a major national equity index observed on aligned trading intervals. Daily high–low range volatility is the feasibility baseline. Session-decomposed or intraday measures may be necessary if daily data cannot distinguish information availability from response time.

The primary graph must be fixed before outcome propagation is inspected. Candidate ex ante distances include market-closing-time or time-zone distance, with trade distance reserved for robustness. Correlation-based distance cannot serve as the primary graph because it would use the outcome relationship to define the path later claimed to transmit the outcome.

Identification threats include non-synchronous trading, common news, volatility persistence, endogenous graph construction, outcome-selected events, and flexible lag dynamics. The design addresses them through UTC alignment, explicit common-mode modeling, ex ante distance, simulation recovery, delayed-diffusion and VAR rivals, and a predeclared event protocol.

## Methods, baselines, and evaluation

The methods sequence is:

1. derive discrete-time estimable restrictions from both graph models;
2. test parameter and model recovery under synthetic diffusion, damped propagation, delayed diffusion, and flexible VAR data-generating processes;
3. build the aligned market panel and document calendar coverage;
4. estimate local or model-based shock responses without outcome-selected timing;
5. test distance–arrival and spectral restrictions;
6. compare graph diffusion, damped propagation, graph autoregression, and flexible VAR forecasts; and
7. report uncertainty, null results, failed diagnostics, and sensitivity to graph and frequency.

Forecast evaluation must use a common sample, common information set, and losses appropriate to volatility. No model receives a favorable window chosen after results are observed.

## Work plan and milestones

Work is organized by decision gates rather than invented calendar dates:

| Gate | Workpackage | Pass condition | Failure action |
|---|---|---|---|
| G1 | WP-01 literature boundary | contribution delta survives a reproducible closest-work search | kill or reposition contribution |
| G2 | WP-02 aligned data tracer | one feasible panel supports arrival-time measurement | weaken target or change frequency |
| G3 | WP-03 model-separation simulation | proposed signatures separate serious data-generating rivals | redesign restrictions or kill mechanism claim |
| G4 | WP-04 event-study pilot | G1–G3 sealed receipts and real-data pilot passes declared checks | report negative result or stop scale-up |

The first three packages may run independently. G4 remains blocked until their exact-version receipts are accepted.

## Falsifiers, risks, and contingencies

The finite-speed claim is killed or radically reframed when:

- information alignment removes the distance–arrival relation;
- delayed diffusion or an unrestricted VAR reproduces all proposed signatures;
- modal frequencies do not relate to graph eigenvalues;
- parameter recovery fails under realistic noise and missing-market calendars;
- forecast gains disappear under a common evaluation window; or
- the literature boundary finds the same empirical test already established.

Failure is a research outcome, not permission to weaken thresholds after inspection.

## Ethics and reproducibility

The design uses market data and does not currently involve human participants. Licensing, redistribution, and source terms must be verified for every dataset before acquisition or release. Code, environment, graph construction, event definitions, calendar alignment, sample versions, model specifications, seeds, and all negative diagnostics must be captured in reproducible workpackage receipts.

No paid data acquisition, submission, publication, or third-party commitment is authorized by this plan.

## Expected outputs and value

Conditional outputs are:

- a verified literature-boundary memo and claim ledger;
- an aligned-data feasibility receipt;
- a simulation-based model-separation report;
- an event-pilot report only if prior gates pass;
- a paper blueprint or manuscript whose status matches executed evidence; and
- reusable code and provenance sufficient for replication, subject to data licenses.

The scholarly value is either a credible finite-speed distinction or a rigorous demonstration that ordinary alternatives explain the apparent propagation.

## References

Material external references are intentionally represented by claim IDs until `C005` and the citation audit are complete. This plan does not convert provisional source notes into a polished bibliography.

## Open decisions

- sampling frequency capable of identifying arrival timing;
- primary ex ante graph;
- shock source and event protocol;
- target journal audience after the contribution delta is verified.

## Acceptance

- Owner: unresolved
- Accepted at: unresolved
- Readback: complete for this partial plan; execution readiness remains conditional
