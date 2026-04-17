# Comprehensive Renewal Execution Plan
**Date:** 2026-04-17
**Auditor:** Kimi K2.5
**Executor:** SWE-1.6 (to be handed off)
**Baseline commit:** 4895cfe
**Type:** Full 6-stage renewal cycle (not partial)

---

## Executive Summary

SWE-1.6 performed a minimal deletion (2 files) and called it "renewal complete." This plan completes the full 6-stage renewal cycle with systematic audit, consolidation decisions, and validation requirements.

**Current state issues identified:**
1. Stale references to deleted files in 4+ registries
2. Massive duplication across governance file lists
3. Out-of-sync registry versions
4. Missing self-coverage validation

**Expected outcome:**
- Governance files: 13 → 11 (delete 2 more, merge 2)
- Stale references: eliminated
- Registry consolidation: 2 file registries → 1
- Duplication: reduced through canonical source of truth

---

## Stage 1: Freeze Unnecessary Expansion (COMPLETE)

**Status:** Already frozen - no new expansion since governance refactor.

---

## Stage 2: Audit Duplication, Drift, Stale Surfaces, Routing Burden

### 2.1 Critical Finding: Stale References to Deleted Files

**Files still referencing deleted `FILE_JUSTIFICATION_REGISTRY_v0_1.json` and `ROOT_ALLOWLIST_v0_1.json`:**

1. **governance/CURRENT_SURFACES_REGISTRY_v0_1.json** (lines 15-16)
2. **governance/AUTHORITATIVE_INTEGRITY_MANIFEST_v0_1.json** (lines 42-47)
3. **governance/REPOSITORY_FILE_REGISTRY_v0_1.json** (lines 15-16)

**Impact:** Validation tooling may fail when these registries are parsed.

### 2.2 Critical Finding: Registry Version Drift

**CURRENT_SURFACES_REGISTRY** version is `0.2.3` but contains stale references.
**REPOSITORY_FILE_REGISTRY** version is `0.2.3` but contains stale references.
**AUTHORITATIVE_INTEGRITY_MANIFEST** version is `0.2.3` but contains stale hashes for deleted files.

**Impact:** Version numbers don't reflect actual current state after deletions.

### 2.3 Duplication Pattern: File Lists Carried in Multiple Places

**Same "current files" list appears in:**
1. AUTHORITATIVE_INDEX_v0_1.md (Markdown list)
2. CURRENT_SURFACES_REGISTRY_v0_1.json ("current_files" array)
3. AUTHORITATIVE_INTEGRITY_MANIFEST_v0_1.json ("files" array with hashes)
4. REPOSITORY_FILE_REGISTRY_v0_1.json ("live_files" array + "files" array)
5. PACKAGE_STATE_SUMMARY_v0_1.json ("current_authoritative_entrypoints")
6. AUTHORITATIVE_SOURCES_v0_1.json ("package_entrypoints" etc.)
7. AGENT_EDIT_SCOPE_POLICY_v0_1.json (implied via "include_current_surfaces")

**Analysis:** This is massive duplication. The same file list is maintained in 7+ places with different formats. This is exactly the "same fact carried in too many places" renewal trigger.

### 2.4 Duplication Pattern: Governance Content

**FEDERATED_SUBSYSTEM_PROTOCOL_v0_1.md** (6KB) and **PACKAGE_MINIMIZATION_POLICY_v0_1.md** (3KB) share significant overlap:
- Both discuss federation principles
- Both define subsystem boundaries
- Both mention renewal cycles
- Both have "anti-patterns" sections

**Analysis:** These could potentially be merged, but they serve slightly different purposes (protocol = interface definition, policy = operational rules). Keep separate for now but add explicit cross-references.

### 2.5 Stale Content: SUF Governance Still References Deleted Files

**structured-unity-framework/governance/AUTHORITATIVE_INDEX_v0_1.md** still lists:
- FILE_JUSTIFICATION_REGISTRY_v0_1.json (line 19 - needs removal)

**Analysis:** SWE-1.6 only updated root governance, missed SUF governance.

### 2.6 Routing Burden Analysis

**Current cold-start sequence for external agent (from AGENTS.md):**
1. Read AGENTS.md
2. Read Translation Decision Map.md
3. Read Internal/Agent Custom Instructions.md
4. Read Internal/Framework Control.md
5. Read Internal/Framework Interface.md
6. Read Research/README.md
7. Read Research/START_HERE.md
8. Read Research/governance/AUTHORITATIVE_INDEX_v0_1.md
9. Read Research/structured-unity-framework/START_HERE.md

**That's 9 files before reaching package-local truth.** This is high but acceptable given the federated architecture.

**Governance navigation burden:**
- Root governance: 13 files to understand
- SUF governance: 10 files to understand
- Knowledge: 81 nodes in atlas

**Analysis:** Not critical but worth monitoring. The 13 governance files is on the high side.

### 2.7 Self-Coverage Gap: No Validator for Governance Itself

**Finding:** The validation tooling (tools/) can validate routes, links, surfaces, but there's no explicit validator that checks:
- Whether governance files reference non-existent files
- Whether registries are internally consistent
- Whether file lists match across different registries

**Analysis:** This is the "subsystem that can test others but has no path to test itself" gap mentioned in PACKAGE_MINIMIZATION_POLICY.

---

## Stage 3: Recompress by Deleting, Merging, Archiving, Shortening

### Action 3.1: Fix Stale References (CRITICAL - Must Complete)

**Update governance/CURRENT_SURFACES_REGISTRY_v0_1.json:**
- Remove FILE_JUSTIFICATION_REGISTRY_v0_1.json from "current_files"
- Remove ROOT_ALLOWLIST_v0_1.json from "current_files"
- Bump version to 0.3.0

**Update governance/AUTHORITATIVE_INTEGRITY_MANIFEST_v0_1.json:**
- Remove FILE_JUSTIFICATION_REGISTRY_v0_1.json from "files" array
- Remove ROOT_ALLOWLIST_v0_1.json from "files" array
- Bump version to 0.3.0

**Update governance/REPOSITORY_FILE_REGISTRY_v0_1.json:**
- Remove FILE_JUSTIFICATION_REGISTRY_v0_1.json from "live_files"
- Remove ROOT_ALLOWLIST_v0_1.json from "live_files"
- Bump version to 0.3.0

**Update structured-unity-framework/governance/AUTHORITATIVE_INDEX_v0_1.md:**
- Remove FILE_JUSTIFICATION_REGISTRY_v0_1.json from "Live governance files"

### Action 3.2: Consolidate File Registries (RECOMMENDED)

**Decision:** Keep REPOSITORY_FILE_REGISTRY and REPOSITORY_EDIT_BASELINE separate but merge their purposes more clearly.

**Rationale:**
- REPOSITORY_FILE_REGISTRY carries category/extension metadata (useful for tooling)
- REPOSITORY_EDIT_BASELINE carries SHA256 hashes (useful for integrity)
- These serve different purposes and both have value

**Alternative (more aggressive):** Merge into single "REPOSITORY_MANIFEST_v0_1.json" with both metadata and hashes.

**Recommendation:** Keep separate for now, but document the purpose distinction clearly.

### Action 3.3: Eliminate File List Duplication (RECOMMENDED)

**Problem:** 7+ places carry the same file list.

**Solution:** Designate CURRENT_SURFACES_REGISTRY as the canonical source of truth for "what files are current."

**Implementation:**
1. Make CURRENT_SURFACES_REGISTRY the single source of truth
2. Update AUTHORITATIVE_INDEX to reference CURRENT_SURFACES_REGISTRY instead of duplicating the list
3. Update PACKAGE_STATE_SUMMARY to reference CURRENT_SURFACES_REGISTRY
4. Update AUTHORITATIVE_SOURCES to reference CURRENT_SURFACES_REGISTRY
5. Keep AUTHORITATIVE_INTEGRITY_MANIFEST (hashes are separate concern)
6. Keep REPOSITORY_FILE_REGISTRY (metadata is separate concern)

**Impact:** Reduces from 7 file lists to 1 canonical list + specialized registries.

### Action 3.4: Add Cross-References Between New Governance Files (RECOMMENDED)

**FEDERATED_SUBSYSTEM_PROTOCOL_v0_1.md** already references:
- SUBSYSTEM_REGISTRY_v0_1.json
- IMPLEMENTATION_LAYER_POLICY_v0_1.md

**Add explicit cross-references:**
- IMPLEMENTATION_LAYER_POLICY should reference FEDERATED_SUBSYSTEM_PROTOCOL
- PACKAGE_MINIMIZATION_POLICY should reference FEDERATED_SUBSYSTEM_PROTOCOL
- SUBSYSTEM_REGISTRY "governance_meta" section should reference renewal cycle policy

### Action 3.5: Delete Low-Value Ops Files (OPTIONAL)

**Review docs/ops/ for staleness:**
- RELEASE_CHECKLIST_v0_1.md - still needed?
- HANDOFF_GUIDE.md - still current?
- HANDOFF_2026-04-17_SWE-1-6-governance-refactor.md - historical, keep
- HANDOFF_2026-04-17_RENEWAL-complete.md - historical but misleading (minimal renewal)
- RENEWAL_PLAN_2026-04-17.md - working document, keep until renewal complete

**Recommendation:** Keep all ops files for now; they're low burden and useful for traceability.

---

## Stage 4: Refactor Names, Locations, Interfaces

### Action 4.1: Rename Misleading Handoff File (RECOMMENDED)

**Current:** HANDOFF_2026-04-17_RENEWAL-complete.md
**Problem:** Claims "renewal complete" but was minimal deletion only.
**Rename to:** HANDOFF_2026-04-17_SWE-1-6-minimal-deletion.md

### Action 4.2: Add Governance Consistency Validator (RECOMMENDED)

**New file:** tools/src/research_tools/validate/governance_consistency.py

**Purpose:** Check that:
- All files listed in CURRENT_SURFACES_REGISTRY actually exist
- No stale references to deleted files
- Registry versions are consistent
- AUTHORITATIVE_INDEX points to CURRENT_SURFACES_REGISTRY instead of duplicating

**This closes the self-coverage gap identified in 2.7.**

---

## Stage 5: Rebuild Indexes, Registries, Manifests, Handoff Surfaces

### Action 5.1: Rebuild CURRENT_SURFACES_REGISTRY as Canonical Source

**New structure:**
```json
{
  "registry_version": "0.3.0",
  "canonical": true,
  "scope": "Research root repository current surfaces",
  "current_files": [/* single canonical list */],
  "live_entrypoints": [/* subset for navigation */],
  "supportive_zones": [/* directory-level support areas */],
  "historical_zones": [],
  "notes": "This is the canonical source of truth for current files. Other registries should reference this rather than duplicating."
}
```

### Action 5.2: Update AUTHORITATIVE_INDEX to Reference Rather Than Duplicate

**New structure:**
```markdown
# AUTHORITATIVE INDEX v0.3.0

## Current truth
See `CURRENT_SURFACES_REGISTRY_v0_1.json` for the canonical list of current files.

## Live governance files
See `CURRENT_SURFACES_REGISTRY_v0_1.json` "current_files" field.

## Rule
If a file is not listed as current in `CURRENT_SURFACES_REGISTRY_v0_1.json`, do not treat it as present-tense repository truth.
```

**Impact:** Reduces AUTHORITATIVE_INDEX from list maintainer to routing surface.

### Action 5.3: Update AUTHORITATIVE_INTEGRITY_MANIFEST to Auto-Generate

**Recommendation:** Make integrity manifest auto-generate from CURRENT_SURFACES_REGISTRY.

**Implementation:** Add to tooling:
```python
# research-tools generate integrity-manifest
# Reads CURRENT_SURFACES_REGISTRY, generates SHA256 for each file
```

**Benefit:** Eliminates manual synchronization between file lists and hashes.

---

## Stage 6: Validate and Reopen

### Validation Checklist

**Before reopening normal work, verify:**

- [ ] CURRENT_SURFACES_REGISTRY updated (no stale references)
- [ ] AUTHORITATIVE_INTEGRITY_MANIFEST updated (no stale references)
- [ ] REPOSITORY_FILE_REGISTRY updated (no stale references)
- [ ] SUF AUTHORITATIVE_INDEX updated (no stale references)
- [ ] Root AUTHORITATIVE_INDEX updated (references CURRENT_SURFACES_REGISTRY)
- [ ] PACKAGE_STATE_SUMMARY updated (references CURRENT_SURFACES_REGISTRY)
- [ ] AUTHORITATIVE_SOURCES updated (references CURRENT_SURFACES_REGISTRY)
- [ ] New governance consistency validator passes
- [ ] All existing validation tooling passes
- [ ] Git commit history is clean
- [ ] CHANGELOG updated

### Reopen Criteria

**Normal work can resume when:**
- All stale references eliminated
- All registries internally consistent
- Validation passes
- System is simpler than before (fewer duplicate lists)

---

## Implementation Priority

**P0 (Critical - Blocks Everything):**
- Fix stale references in CURRENT_SURFACES_REGISTRY
- Fix stale references in AUTHORITATIVE_INTEGRITY_MANIFEST
- Fix stale references in REPOSITORY_FILE_REGISTRY
- Fix stale references in SUF AUTHORITATIVE_INDEX

**P1 (High - Significant Improvement):**
- Redesign CURRENT_SURFACES_REGISTRY as canonical source
- Update AUTHORITATIVE_INDEX to reference rather than duplicate
- Add governance consistency validator

**P2 (Medium - Nice to Have):**
- Add cross-references between new governance files
- Rename misleading handoff file
- Auto-generate integrity manifest

**P3 (Low - Defer):**
- Merge file registries (REPOSITORY_FILE_REGISTRY + REPOSITORY_EDIT_BASELINE)
- Delete historical ops files
- Further governance consolidation

---

## Expected Outcome

**Before renewal:**
- 13 governance files
- 2 file registries with stale references
- 7+ duplicate file lists
- Self-coverage gap

**After renewal:**
- 13 governance files (same count, but healthier)
- 2 file registries (clean, no stale references)
- 1 canonical file list (CURRENT_SURFACES_REGISTRY)
- 4 secondary registries referencing canonical (INDEX, SUMMARY, SOURCES, INTEGRITY)
- Governance consistency validator in place
- Self-coverage gap closed

**Net improvement:** Elimination of stale references, reduction in duplication, addition of self-validation.

---

## Handoff to SWE-1.6

**Executor:** SWE-1.6
**Entry point:** Start with P0 items (fix stale references)
**Validation:** Run governance consistency validator after each change
**Completion:** All 6 stages validated before reopening

**This is a full renewal cycle, not a minimal deletion.**
