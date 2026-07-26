# WP-02: Aligned data tracer

- Status: ready
- Blocked by: none

## Decision or uncertainty reduced

Determine whether available observations can distinguish reaction time from trading-hour mechanics.

## End-to-end slice

Acquire a small panel for three markets with different trading hours. Build UTC session labels, separate overnight and intraday volatility, record holidays and stale prices, and estimate simple event responses.

## Deliverables

- raw-source manifest and license notes;
- UTC alignment table;
- missingness and common-window report;
- three-market volatility panel;
- recommendation on daily, session, hourly, or higher-frequency scope.

## Acceptance criteria

Every observation has an information-availability interval, source version, and missingness status. The pilot can state what “arrival after \(h\)” means without calendar ambiguity.

## Falsifier and stop rule

Stop the arrival-speed claim if the feasible data frequency cannot separate propagation from market opening.
