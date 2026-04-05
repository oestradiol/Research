# Control and governance surface

This is the shortest current map of how the SUF package keeps its academic core legible while also staying bounded, current, and harder to drift by accident.

## Table of contents
- [Core rule](#core-rule)
- [Current truth surfaces](#current-truth-surfaces)
- [Checks before use](#checks-before-use)
- [How the package resists drift](#how-the-package-resists-drift)
- [Skeptical audit](#skeptical-audit)
- [Trust and style](#trust-and-style)
- [Honest limit](#honest-limit)
- [Provenance](#provenance)

## Core rule

Governance exists here to protect the academic object, not to replace it. No package claim should be stronger than the current evidence, current route state, and current audit surfaces.

## Current truth surfaces

Use these to see what is current and authoritative:
- `../../governance/AUTHORITATIVE_INDEX_v0_1.md`
- `../../governance/AUTHORITATIVE_SOURCES_v0_1.json`
- `../../governance/CURRENT_SURFACES_REGISTRY_v0_1.json`
- `../../governance/AUTHORITATIVE_INTEGRITY_MANIFEST_v0_1.json`
- `../project-status.md`
- `../current-execution-order.md`

## Checks before use

Run these from the repository root:
- `python package_doctor.py`
- `python research_launch_gate.py`

Supporting audits:
- `python tools/audit_current_surfaces.py`
- `python tools/audit_repository_file_registry.py`
- `python tools/audit_current_claims.py`
- `python tools/audit_repository_minimality.py`
- `python tools/audit_routing_surfaces.py`
- `python tools/audit_merged_docs.py`

## How the package resists drift

- current files are listed explicitly
- integrity hashes are tracked for the current authoritative set
- package status and execution-order surfaces are separated
- merged docs are checked for navigation headers and provenance
- historical or supportive material is not treated as present-tense truth by default
- the package routes readers back to canonical academic surfaces instead of letting control docs silently take over

## Skeptical audit

### Main risks that still matter
1. Current files can still be conceptually weak even if their governance metadata is correct.
2. Route-local empirical support is stronger than whole-framework proof.
3. The package can still drift through wording inflation if current surfaces are not audited.
4. Read-only validators can prove consistency without proving truth.
5. Future reopening can still introduce new failure modes not tracked by current checks.

### What is already in place against those risks
- package status and execution-order surfaces are explicit
- reviewer-objection and evidence-status surfaces are current
- current files are indexed and hashed
- route/state/version surfaces are checked by the tooling package
- current-claim expectations keep bounded posture explicit

### What remains true anyway
- one demonstrated route is not whole-framework proof
- route-local metrics are not closed predictive theory
- human judgment remains necessary

## Trust and style

Current front-door writing should:
- say plainly what the package is
- say plainly what it does not yet prove
- point to concrete files rather than vague gestures
- prefer clarity over defensive jargon or hype
- avoid using structure as a substitute for evidence

## Honest limit

These controls are strong against many governance and hygiene failures. They do not replace human judgment, and they do not prove scientific truth by themselves. They are here to keep the package honest enough that the real intellectual work stays visible.

## Provenance

This current file consolidates the roles previously carried by:
- `COHERENCE_AND_CONTROL_SURFACE.md`
- `SKEPTICAL_AUDIT_AND_HARDENING.md`
- `TRUST_AND_STYLE_POLICY.md`
