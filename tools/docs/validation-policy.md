# Validation Policy

## Core rule

This package validates structure, parseability, consistency, and deterministic route metrics. It does not decide interpretation.

## What tranche 1 validates

- Markdown link integrity in `Research/structured-unity-framework/`
- source-registry shape
- archive-link shape
- event-ledger schema
- route-summary consistency against current published docs

## What tranche 1 does not decide

- whether a theory claim is philosophically correct
- whether a boundary choice is the best one
- whether a reported gain is publishable
- whether a mismatch should overwrite public docs

## Human gate

Every generated report is provisional until a human reviews it.

If tooling output diverges from public docs, the tool reports the mismatch and stops there.

## Escalation rule

Any future move toward auto-suggested doc patches requires:

1. a new ADR
2. explicit human approval
3. a separate implementation tranche

## Status

`strict-gated validation policy`
