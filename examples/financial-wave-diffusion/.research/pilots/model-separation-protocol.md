# Pilot protocol: Model separation before market data

## Purpose

Prove that the proposed diagnostics can tell the claimed mechanisms apart before interpreting financial observations.

## Generators

1. graph diffusion;
2. damped graph telegraph;
3. delayed diffusion;
4. unrestricted stable graph VAR.

Use identical graph, innovations, missing-market calendar, and signal-to-noise grid where possible.

## Blind evaluation

Separate generator code from estimator selection. Record the generator label only after classification and parameter estimation finish.

## Primary metrics

- false telegraph classification under non-telegraph generators;
- recovery of \(\gamma\), \(c\), and relevant modal roots;
- slope and coverage of distance-arrival relations;
- out-of-sample QLIKE and MSE;
- sensitivity to non-synchronous missingness.

## Go/no-go rule

Proceed to the event pilot only if the classifier has a predeclared false-positive ceiling and useful power over a plausible region. Otherwise repair the diagnostic or narrow the research claim.
