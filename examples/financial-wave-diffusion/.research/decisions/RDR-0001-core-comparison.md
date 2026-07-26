# RDR-0001: Compare diffusion with damped graph propagation

- Status: accepted
- Date: 2026-07-26
- Supersedes: none

## Context

The seed idea treated the heat, wave, and Laplace equations as three financial regimes. A separate observable Laplace regime would require all connected-node residuals to be harmonic and risks becoming an empty relabeling.

## Decision

Make the empirical competition graph diffusion versus a damped graph telegraph model. Decompose log volatility into market-specific baselines, a separately modeled global common mode, and a zero-sum cross-market propagation field. Treat the Laplace relation only as a long-run boundary on that projected field.

## Alternatives

- Three-state Wave–Heat–Laplace switching model: rejected as overidentified by narrative and weakly distinguished in daily data.
- Pure wave equation: rejected because financial responses plausibly exhibit damping.
- Standard VAR only: retained as a baseline, not the focal mechanism.

## Consequences

The paper has one sharp model-separation question. It must establish evidence beyond a generic second lag and must not advertise a novel “three PDE theory.” For a connected graph, the Laplace boundary implies that the projected field vanishes because it is orthogonal to the graph's constant zero mode; it does not require the global factor or raw volatilities to vanish.

## Revisit when

Revisit only if simulation and data reveal a separately identified, economically meaningful harmonic state.
