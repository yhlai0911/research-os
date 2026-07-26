# WP-03: Model-separation simulation

- Status: ready
- Blocked by: none

## Decision or uncertainty reduced

Test whether proposed diagnostics distinguish diffusion, damped propagation, delayed diffusion, and flexible autoregression under realistic noise.

## End-to-end slice

Simulate all four data-generating processes on the same fixed graph and missing-market calendar. Estimate all candidate models blind to the generator and evaluate classification, parameter recovery, and false positives.

## Deliverables

- deterministic simulation code and seeds;
- recovery and confusion matrices;
- modal, arrival-time, and forecast diagnostics;
- minimum sampling and signal conditions;
- revised empirical acceptance thresholds.

## Acceptance criteria

The finite-speed classifier controls false positives against delayed diffusion and flexible VAR at a predeclared rate and recovers a useful fraction of true telegraph cases.

## Falsifier and stop rule

Kill or redesign the empirical mechanism claim if observably equivalent baselines cannot be separated under plausible data conditions.
