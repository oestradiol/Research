# Devil's Advocate Audit Report

**Generated**: 2026-04-18
**Scope**: Complete session review with self-red-team
**Status**: FAILURES FOUND — requires remediation

---

## Critical Finding 1: Unverified Source Citations (HIDDEN FAILURE)

**Issue**: The 5 added Australia events cite sources NOT in official corpus

### Affected Events:
- `au-b-013`: cites `src-australia-ahppc-anzac-2020-03-17` — NOT IN REGISTRY
- `au-b-014`: cites `src-australia-ahppc-transition-2020-04-21` — NOT IN REGISTRY  
- `au-a-015`: cites `src-australia-national-cabinet-maritime-2020-04-24` — NOT IN REGISTRY
- `au-a-016`: cites `src-australia-national-cabinet-may-2020-05-15` — NOT IN REGISTRY
- `au-a-017`: cites `src-australia-national-cabinet-reopening-2020-05-29` — NOT IN REGISTRY

### Evidence:
```bash
$ grep -r "src-australia-ahppc-anzac" references/source-registry.md
# No results

$ grep -r "src-australia-national-cabinet-may" references/source-registry.md  
# No results
```

### Why This Matters:
- Australia official corpus inventory only lists 9 admitted sources
- The cited sources appear in summary table but lack:
  - Verified live official URLs
  - Verified fixed archive URLs  
  - Admission to official corpus via discovery log
- This creates phantom evidentiary base — events exist but sources don't

### Remediation Required:
1. EITHER: Remove 5 events from ledger, revert to 13 detailed events
2. OR: Discover and admit 5 missing sources to corpus with live+archive URLs
3. OR: Mark 5 events as `status: discovery-needed` with explicit provenance gap

---

## Finding 2: Tooling Edge Cases (ACCEPTABLE RISK)

### validate-closure-note.py
- **Gap**: Implementation marker counts differ from closure note prose claims
- **Impact**: Validator correctly detects discrepancy — this is FEATURE not bug
- **Risk**: Low — prose claims may need revision to match actual markers

### validate-all.py  
- **Gap**: Hardcodes Python path to venv location
- **Impact**: Fails if venv moved or not present
- **Risk**: Medium — needs env var fallback or auto-detection

### ledger-to-json.py
- **Gap**: Regex parsing fragile for multiline action_type fields
- **Impact**: May truncate or misparse complex action descriptions
- **Risk**: Low — current corpus validates successfully

---

## Finding 3: Handoff Protocol Failure Modes

### Protocol: `.windsurf/workflows/prepare-handoff.md`

**Failure Mode 1: // turbo annotation untested**
- Claim: Auto-executes without explicit permission
- Reality: Not verified if Cascade actually respects // turbo
- Risk: User may still need to explicitly approve each step

**Failure Mode 2: Agent-instructions may not propagate**
- Changes made to `Internal/active/agent-instructions.md`
- No guarantee future agents load this file vs cached version
- Risk: Protocol change may not persist across sessions

**Failure Mode 3: No rollback mechanism**
- If handoff protocol triggers inappropriately (false positive completion)
- No documented way to abort or revise
- Risk: Premature commits of incomplete work

---

## Finding 4: Groundedness Audit of Decisions

| Decision | Grounded? | Issue |
|----------|-----------|-------|
| Add 5 Australia events | ⚠️ PARTIAL | Sources not in corpus (unverified) |
| Update corpus spec to 76 | ❌ NO | Based on unverified events |
| Mark v1.5 complete | ⚠️ PARTIAL | Depends on 76-event claim |
| Create handoff workflow | ✅ YES | Response to explicit user friction |
| Add // turbo annotation | ⚠️ UNTESTED | Unknown if actually works |

### Root Cause: Source Verification Gap

The Australia events were added based on summary table in ledger, NOT based on:
- `australia-official-corpus-inventory.md` (only 9 sources admitted)
- `australia-source-discovery-log.md` (unstable candidates)
- `references/source-registry.md` (master source registry)

**Assumption made**: "If event ID in summary table, source must exist"
**Reality**: Summary table ≠ verified corpus admission

---

## Remediation Status

### P0 (COMPLETED 2026-04-18):
1. ✅ **Fixed unverified sources**: Removed 5 events (au-b-013, au-b-014, au-a-015, au-a-016, au-a-017)
2. ✅ **Reverted corpus spec**: 71 verified events (38+20+13)
3. ✅ **Updated project-status.md**: Now reflects actual verified event count
4. ✅ **Updated current-execution-order.md**: Phase table corrected
5. ✅ **Regenerated exports**: corpus.json, corpus.csv, metrics.json with 71 events
6. ✅ **Updated Australia ledger**: Readout cues and status reflect 13 verified events + 5 pending discovery

### P1 (Pending next session):
- Add source-registry validation to `ledger-to-json.py`
- Create source discovery backlog for missing 5 sources
- Test // turbo annotation behavior

---

## Open Questions

1. Should unverified events be removed or sources expedited?
2. Does // turbo actually auto-execute in Cascade?
3. Will agent-instructions changes persist across sessions?
4. Is 71-event corpus (verified) acceptable vs 76-event (partially unverified)?

---

## Validation Status (V?)

V? — Audit reveals groundedness failures requiring remediation before v1.5 can be marked complete

**Recommendation**: DO NOT proceed to v1.6 workstreams until P0 remediations complete.
