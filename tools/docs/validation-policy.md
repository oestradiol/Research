# Validation Policy

## Core rule

This package validates structure, parseability, consistency, version-surface alignment, and deterministic route metrics. It does not decide interpretation.

## What the current public tooling validates

- Markdown link integrity in `Research/`
- source-registry shape
- archive-link shape
- event-ledger schema
- route-summary consistency against current SUF published docs
- Knowledge package entry/index integrity
- version, changelog, citation, and package-snapshot consistency
- release-readiness hygiene for public placeholders, internal leakage, and local absolute paths

Recognized fixed archive surfaces in tranche 1 are:

- Wayback fixed captures
- archive.org item pages
- approved source-native fixed archive editions such as `plato.stanford.edu/archives/...`

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
