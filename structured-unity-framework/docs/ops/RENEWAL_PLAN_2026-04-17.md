# Renewal Plan: Governance Layer Consolidation
**Date:** 2026-04-17
**Agent:** SWE-1.6
**Trigger:** User-initiated renewal after governance refactor expansion
**Commit baseline:** 08642f7

## Renewal Triggers Detected

From PACKAGE_MINIMIZATION_POLICY:
- "current or supportive files begin duplicating each other" ✓
- "agent startup or retrieval cost rises because too many surfaces must be scanned" ✓
- "more effort is being spent remembering the structure than using it" ✓

## Duplication Analysis

### File Registry Duplication (223KB total)

Three separate file registries tracking the same files:

1. **FILE_JUSTIFICATION_REGISTRY_v0_1.json** (107KB)
   - Purpose: Justifies why each file exists
   - Structure: Array of file paths with justifications

2. **REPOSITORY_FILE_REGISTRY_v0_1.json** (57KB)
   - Purpose: File metadata (path, category, extension)
   - Structure: Array of file objects with metadata

3. **REPOSITORY_EDIT_BASELINE_v0_1.json** (59KB)
   - Purpose: SHA256 hashes for integrity checking
   - Structure: Array of file objects with hashes

**Problem:** Same file list carried three times with different metadata fields.

**Impact:** 223KB of JSON for what could be one consolidated registry.

### Governance File Proliferation (14 files total)

Governance directory now contains 14 files:
- AGENT_EDIT_SCOPE_POLICY_v0_1.json
- AUTHORITATIVE_INDEX_v0_1.md
- AUTHORITATIVE_INTEGRITY_MANIFEST_v0_1.json
- AUTHORITATIVE_SOURCES_v0_1.json
- CURRENT_CLAIM_EXPECTATIONS_v0_1.json
- CURRENT_SURFACES_REGISTRY_v0_1.json
- FEDERATED_SUBSYSTEM_PROTOCOL_v0_1.md (NEW)
- FILE_JUSTIFICATION_REGISTRY_v0_1.json
- IMPLEMENTATION_LAYER_POLICY_v0_1.md (NEW)
- PACKAGE_MINIMIZATION_POLICY_v0_1.md
- PACKAGE_STATE_SUMMARY_v0_1.json
- REPOSITORY_EDIT_BASELINE_v0_1.json
- REPOSITORY_FILE_REGISTRY_v0_1.json
- ROOT_ALLOWLIST_v0_1.json
- SUBSYSTEM_REGISTRY_v0_1.json (NEW)

**Problem:** 14 governance files is high cognitive load for navigation.

## Renewal Actions

### Action 1: Consolidate File Registries

**Merge into:** `REPOSITORY_FILE_REGISTRY_v0_1.json`

**New structure:**
```json
{
  "version": "0.3.0",
  "files": [
    {
      "path": "README.md",
      "category": "README.md",
      "extension": ".md",
      "justification": "Repository routing surface",
      "sha256": "hash"
    }
  ]
}
```

**Delete:**
- FILE_JUSTIFICATION_REGISTRY_v0_1.json
- REPOSITORY_EDIT_BASELINE_v0_1.json

**Update references:**
- AUTHORITATIVE_INDEX_v0_1.md
- CONTROL_AND_GOVERNANCE_SURFACE.md
- RELEASE_CHECKLIST_v0_1.md
- Validation tooling

### Action 2: Consolidate New Governance Files

**Question:** Do FEDERATED_SUBSYSTEM_PROTOCOL, IMPLEMENTATION_LAYER_POLICY, and SUBSYSTEM_REGISTRY need to be separate?

**Analysis:**
- FEDERATED_SUBSYSTEM_PROTOCOL points to the other two as "machine-readable companion surfaces"
- This suggests intentional separation (prose + JSON)
- However, the protocol is 6KB and could potentially absorb the policy

**Decision:** Keep separate for now (protocol = prose, policy = prose, registry = JSON), but add cross-references to make the relationship explicit.

### Action 3: Review Governance File Count

**Question:** Can any of the 14 governance files be merged?

**Analysis:**
- Most serve distinct purposes (index, sources, surfaces, integrity, minimization, etc.)
- PACKAGE_STATE_SUMMARY_v0_1.json (694 bytes) is small - could potentially be merged into another registry
- ROOT_ALLOWLIST_v0_1.json (325 bytes) is tiny - could be inlined

**Decision:** Merge ROOT_ALLOWLIST into CURRENT_SURFACES_REGISTRY as a field. Keep PACKAGE_STATE_SUMMARY separate for now (used by tooling).

## Expected Outcome

**Before renewal:**
- 14 governance files
- 3 file registries (223KB)
- 3 new governance files (protocol, policy, registry)

**After renewal:**
- 12 governance files (merge ROOT_ALLOWLIST)
- 1 file registry (consolidated, ~80KB)
- 3 new governance files (with explicit cross-references)

**Reduction:** 2 files, ~143KB

## Validation Plan

After consolidation:
1. Update all references to deleted files
2. Run validation tooling to ensure no broken references
3. Test that tooling can read consolidated registry
4. Verify AUTHORITATIVE_INDEX accuracy
5. Check release checklist completeness

## Guardrail

Do not let renewal become permanent meta-work. Stop when:
- File registry consolidation is complete
- References are updated
- Validation passes
- System is simpler and clearer than before
