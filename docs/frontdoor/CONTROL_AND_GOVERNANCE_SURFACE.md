# Control and governance surface

This is the shortest current map of how the root repository stays bounded, current, hard to drift by accident, and readable without inflating package claims.

## Table of contents
- [Core rule](#core-rule)
- [Current truth surfaces](#current-truth-surfaces)
- [Checks before use](#checks-before-use)
- [How the repository resists sprawl](#how-the-repository-resists-sprawl)
- [Skeptical audit](#skeptical-audit)
- [Trust and style](#trust-and-style)
- [Honest limit](#honest-limit)
- [Provenance](#provenance)

## Core rule

No repository-level claim should be stronger than the current package boundaries, current governance files, and current validation surfaces.

## Current truth surfaces

Use these to see what is current and authoritative:
- `../../governance/AUTHORITATIVE_INDEX_v0_1.md`
- `../../governance/AUTHORITATIVE_SOURCES_v0_1.json`
- `../../governance/CURRENT_SURFACES_REGISTRY_v0_1.json`
- `../../governance/AUTHORITATIVE_INTEGRITY_MANIFEST_v0_1.json`
- `../../governance/PACKAGE_STATE_SUMMARY_v0_1.json`
- `../../structured-unity-framework/START_HERE.md`

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
- `python tools/audit_edit_scope.py`

## How the repository resists sprawl

- `../../governance/PACKAGE_MINIMIZATION_POLICY_v0_1.md`
- `../../governance/AGENT_EDIT_SCOPE_POLICY_v0_1.json`
- `../../governance/REPOSITORY_EDIT_BASELINE_v0_1.json`
- `../../governance/ROOT_ALLOWLIST_v0_1.json`
- `../../governance/FILE_JUSTIFICATION_REGISTRY_v0_1.json`
- `../../governance/REPOSITORY_FILE_REGISTRY_v0_1.json`

Rule: no root file without a clear routing, governance, licensing, citation, or operational job. Agent edits outside current surfaces and designated work surfaces should fail review unless explicitly declared.

## Skeptical audit

### Main risks that still matter
1. A current root file can still be subtly misleading even if it passes routing checks.
2. Governance can prove file roles without proving that package claims are scientifically correct.
3. `knowledge/` can still drift toward SUF-overforegrounding if note discipline weakens.
4. Validation tooling can prove consistency and release hygiene without proving truth.
5. Future changes can still introduce new failure modes not yet tracked by current audits.

### What is already in place against those risks
- current-vs-supportive file roles are explicit
- current repository surfaces are indexed and hashed
- file-registry and root-allowlist checks exist
- SUF remains the academic core instead of being flattened into the umbrella
- read-only validation remains separate from substantive research claims
- root state duplication has been minimized so package truth stays package-local

### What remains true anyway
- repository governance is not scientific truth adjudication
- package-local academic claims still belong primarily to SUF
- human review remains necessary

## Trust and style

Root front-door writing should:
- route clearly between packages
- avoid duplicate long-form SUF state
- stay specific and bounded
- avoid hype, overclaiming, and generic assistant-like filler

## Honest limit

These controls increase coherence, traceability, and release hygiene. They do not guarantee scientific truth and they do not replace careful human judgment.

## Provenance

This current file consolidates the roles previously carried by:
- `COHERENCE_AND_CONTROL_SURFACE.md`
- `SKEPTICAL_AUDIT_AND_HARDENING.md`
- `TRUST_AND_STYLE_POLICY.md`
