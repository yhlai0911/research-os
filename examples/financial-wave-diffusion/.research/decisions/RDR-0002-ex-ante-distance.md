# RDR-0002: Use an ex ante primary graph

- Status: proposed
- Date: 2026-07-26
- Supersedes: none

## Context

A graph estimated from the same volatility outcomes used to test propagation would make the result partly circular.

## Decision

Use market closing-time or information-availability distance as the primary graph. Treat return correlation and volatility correlation graphs as robustness specifications only.

## Alternatives

- Outcome correlation graph: flexible but endogenous to the phenomenon being explained.
- Geographic distance: exogenous but economically incomplete.
- Trade-weight graph: plausible and ex ante, but lower-frequency and potentially slow moving.

## Consequences

The empirical design must align trading intervals in UTC and separate overnight from intraday responses. The final graph choice remains conditional on data feasibility.

## Revisit when

Revisit after the data pilot measures coverage and temporal resolution for all candidate markets.
