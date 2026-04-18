# Unknown Unknowns Mapping Route

## Purpose

This route maps the **gaps we don't yet know we have** in the SUF/AKS system after the v0.2 governance compression. The goal is to surface hidden brittleness, missing capabilities, and unverified assumptions before they become blockers.

## Current State (Post-v0.2 Refactor)

**Completed:**
- Governance compressed from 13 files → 5 files (62% reduction)
- All v0.1 files archived with `_archived_v0_1` suffix
- Tooling updated to use GOVERNANCE_CORE_v0_2.json as canonical
- v0.1 fallback code removed from validate_clusters.py

**Known Remaining Issues:**
1. Edit scope baseline empty (v0.1 REPOSITORY_EDIT_BASELINE archived, no v0.2 equivalent)
2. SUF contribution note missing required fragment (pre-existing)
3. Validation test failures (non-blocking for research)

## Research Questions

### RQ1: What did we lose in compression?

- [ ] Compare archived v0.1 files against v0.2 consolidation — any field/data loss?
- [ ] Check if SUBSYSTEM_REGISTRY validation_cluster metadata fully migrated
- [ ] Verify actor_classes and scope_classes preserved correctly
- [ ] Audit EDIT_SCOPE_POLICY and REPOSITORY_EDIT_BASELINE — do we need v0.2 equivalents?

### RQ2: What trust assumptions are now unverified?

- [ ] GOVERNANCE_CORE_v0_2.json has no integrity checksum — is this a risk?
- [ ] REGISTRY_MANIFEST_v0_2.json has placeholder SHA256s — when should these be computed?
- [ ] No validation that GOVERNANCE_CORE and REGISTRY_MANIFEST stay synchronized
- [ ] Machine-readable registry is now authoritative — is the human-readable layer sufficient?

### RQ3: What operational workflows are broken/fragile?

- [ ] Edit scope validation returns empty baseline warnings — acceptable or needs fix?
- [ ] How do we update GOVERNANCE_CORE safely? No documented change protocol.
- [ ] Cluster validation has fallback for missing runners — does this mask real errors?
- [ ] SUF package still on v0.1 registries — migration path unclear

### RQ4: What gaps exist in the recursive improvement loop?

- [ ] Promotion states (draft → candidate → grounded → accepted) not validated
- [ ] No automated check that validated outputs feed back into knowledge substrate
- [ ] No metric for "system coverage" vs "unknown gaps"
- [ ] Missing: explicit health indicators for each subsystem

### RQ5: What external dependencies are hidden?

- [ ] Nix environment required for validation — is this a lock-in risk?
- [ ] Git state used as provenance anchor — what if git history is rewritten?
- [ ] Internal/ layer references in public docs — boundary clarity sufficient?

## Methodology

1. **Document Audit**: Read all archived v0.1 files, map each field to v0.2 equivalent
2. **Gap Matrix**: Create explicit table of what moved, what was lost, what was added
3. **Failure Mode Analysis**: For each "unknown" surfaced, trace cascade effects
4. **Fix Prioritization**: Sort by (severity × ease of fix × blocker potential)

## Output Target

A durable knowledge note in `Research/knowledge/map/08-integrative-and-reflexive/` titled:
`unknown-unknowns-post-v0.2-compression.md`

With sections:
- Discovered gaps (unknowns now known)
- Risk assessment (which gaps matter most)
- Proposed fixes (with effort estimates)
- Monitoring plan (how to detect similar gaps in future renewals)

## Status

`in_progress` — research commenced
