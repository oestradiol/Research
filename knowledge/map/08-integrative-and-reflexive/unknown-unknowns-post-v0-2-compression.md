# Unknown Unknowns: Post-v0.2 Compression Analysis

## Research Date
2026-04-18

## Executive Summary

Governance compression from 13 v0.1 files → 5 v0.2 files achieved 62% reduction but **three conceptual structures were lost**, not migrated.

---

## Discovered Gap #1: Scope Classes Missing

**What was lost:**
```json
// From SUBSYSTEM_REGISTRY_v0_1.json
"scope_classes": [
  {"id": "local-file", "description": "single file, note, or module scope"},
  {"id": "subsystem", "description": "one bounded package or operating layer"},
  {"id": "cross-subsystem", "description": "coordination layer spanning more than one bounded part"},
  {"id": "root-governance", "description": "umbrella routing, policy, and release hygiene"},
  {"id": "private-internal", "description": "non-public operator and agent delta surfaces"}
]
```

**Impact:** Navigation by scope class is no longer machine-verifiable. Agents must infer scope from path patterns.

**Severity:** Medium — affects automated scope checking in `validate_edit_scope()`

---

## Discovered Gap #2: Durable Writeback Packet Structure Lost

**What was lost:**
```json
// From SUBSYSTEM_REGISTRY_v0_1.json
"durable_writeback_packet": [
  "provenance_or_source_anchor",
  "short_summary",
  "target_subsystem",
  "target_file_reference",
  "status_candidate_working_or_accepted",
  "change_class_governance_architecture_knowledge_or_local_execution"
]
```

**Impact:** No machine-readable schema for handoff packets. Cross-subsystem coordination relies on prose conventions.

**Severity:** Medium — affects agent-to-agent handoff reliability

---

## Discovered Gap #3: Governance Meta Missing

**What was lost:**
```json
// From SUBSYSTEM_REGISTRY_v0_1.json
"governance_meta": {
  "heterogeneous_agent_assumption": true,
  "self_reference_required_in_renewal_cycles": true,
  "guided_convergence_target": "increase coherence, auditability, and self-coverage while resisting drift, stale legacy growth, and meta-inflation"
}
```

**Impact:** Explicit commitment to heterogeneous-agent support and self-coverage is no longer machine-readable.

**Severity:** Low-Medium — affects trustworthiness signaling to external auditors

---

## Discovered Gap #4: Validation Cluster Source Files Not Migrated

**v0.1 SUBSYSTEM_REGISTRY** specified explicit `validation_cluster.source_files` for each subsystem.

**v0.2 GOVERNANCE_CORE** derives clusters dynamically from `subsystems.*.entry`, `state_surface`, `validation_policy`, and `surfaces`.

**Risk:** Derivation logic in `derive_subsystem_validation_cluster()` could drift from original intent without explicit source file lists to compare against.

**Severity:** Low — current derivation appears correct but is implicit

---

## Risk Assessment Matrix

| Gap | Severity | Ease of Fix | Priority |
|-----|----------|-------------|----------|
| Scope classes missing | Medium | Easy (add to GOVERNANCE_CORE) | 2 |
| Writeback packet lost | Medium | Easy (add to GOVERNANCE_CORE) | 2 |
| Governance meta missing | Low-Medium | Easy (add to GOVERNANCE_CORE) | 3 |
| Validation cluster derivation implicit | Low | Hard (requires logic change) | 4 |

---

## Proposed Fixes

### Option A: Minimal (Recommended)
Add three fields to GOVERNANCE_CORE_v0_2.json:
- `scope_classes`: restore from v0.1
- `durable_writeback_packet`: restore from v0.1  
- `governance_meta`: restore from v0.1

Version bump to v0.2.1. No code changes needed — fields are advisory.

### Option B: Integration
- Merge `scope_classes` into `actor_classes` (each actor has default scope)
- Merge `durable_writeback_packet` into `edit_scope_policy`
- Merge `governance_meta` into `principles`

More elegant but requires documentation updates and semantic mapping.

### Option C: Accept Loss
Document that v0.2 prioritizes operational clarity over explicit metadata. Add prose explanations to `FEDERATION_AND_LAYERS_v0_2.md`.

---

## Monitoring Plan

During future renewal cycles, check:
1. Any field present in archived v0.1 but not in v0.2+ is flagged
2. Validation tests include "no conceptual loss without explicit acceptance" check
3. Compression migration plan template includes "semantic preservation audit" step

---

## Status

`research_complete` — awaiting decision on fix approach
