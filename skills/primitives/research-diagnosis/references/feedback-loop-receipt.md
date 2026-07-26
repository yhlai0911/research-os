# Feedback-loop receipt

Use this packet when a failure is stochastic, long-running, or observable only through a human action.

## Phase-1 loop receipt

```yaml
diagnosis_id: DIAG-...
expected:
observed_exact_symptom:
pinned_inputs:
invocation_or_protocol:
raw_output_pointer:
exact_symptom_red_capable: pass|fail
reproduction:
  mode: deterministic|stochastic
  attempts:
  exact_symptom_count:
  rate:
runtime_seconds:
agent_runnable: pass|fail|hitl
hitl_capture_pointer:
verdict: red|green|inconclusive
```

All four gates must be evidenced. `inconclusive` is not red.

## Stochastic escalation

Choose the initial attempt count before running. Increase it only when another bounded batch can distinguish named predictions. Record cumulative attempts and failures. Stop at the predeclared time, compute, paid-resource, or human-effort limit and report `blocked` or `partial`; never keep rerunning until the symptom disappears.

## Structured HITL capture

Give the human one action sequence and one observation form. Capture:

- environment and artifact identity;
- start and end timestamps;
- numbered actions;
- expected marker;
- actual marker, screenshot, trace, or exact text;
- whether the exact symptom occurred;
- ambiguous or interrupted steps.

The human supplies observation, not diagnosis. Store the capture under the diagnosis ID and replay it when possible.

## Instrumentation cleanup

Prefix every temporary trace, log, column, flag, and file with the same unique diagnosis ID. After the final run, remove it and save the command or search that returned zero remaining matches.
