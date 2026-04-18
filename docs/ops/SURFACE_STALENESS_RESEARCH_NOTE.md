# Research Note: Solving Surface Staleness Systematically

**Date:** 2026-04-18  
**Status:** Active research problem  
**Priority:** High (recurring friction source)  

---

## The Problem

Surface staleness is a **documented, recurring failure mode** that persists despite multiple interventions:

```
Empirical phases complete → surfaces not auto-synced → validators compute from actual data 
while docs show stale values → validation failures accumulate → manual fixes required
```

**Documented incidents:**
- 2026-04-18: Taiwan 15→20 event drift, v1.2.0→v1.5.0 version drift, 71→76 event count drift
- Earlier: current-execution-order.md became stale after v1.2-v1.4 completion

**Current state:** Staleness sweep added to prepare-handoff protocol as manual check.

---

## Why Current Solutions Fail

### 1. Validation Layer is Consistency-Only

The 191-check validation suite ensures **syntactic consistency** (doc A matches doc B) but not **semantic correctness** (docs match reality).

**Example failure:**
```
Status surface: "71 events"
Ledger (old): "71 events coded"
Validator: ✅ MATCH (passes)
Reality (new): 76 events coded
Result: Validation passes, claim is FALSE
```

**Root cause:** Validators compare surfaces to each other, not to ground truth (ledgers).

### 2. Manual Synchronization Burden

Current process requires humans to:
1. Remember to check all status surfaces after ledger updates
2. Manually propagate version numbers across 10+ files
3. Verify CITATION.cff, README.md, CHANGELOG.md, project-status.md stay aligned

**Friction:** This is error-prone and creates cognitive load that scales with repository complexity.

### 3. No Automated Ground-Truth Validation

There is no validator that checks:
- Does project-status.md event count match actual ledger count?
- Does README.md version match CITATION.cff version?
- Does CHANGELOG.md date match release date?

---

## Research Questions

### Q1: Can We Build Ground-Truth Validators?

**Hypothesis:** Add validators that parse ledgers and compare to status surface claims.

**Approach:**
```python
def validate_ground_truth():
    ledger_count = parse_ledger().event_count  # e.g., 76
    status_claim = parse_project_status().event_count  # e.g., 71
    assert ledger_count == status_claim, f"Drift: ledger {ledger_count} vs status {status_claim}"
```

**Challenges:**
- Natural language parsing for "76 verified events" in prose
- Distinguishing historical claims from current claims
- Handling intentional discrepancies (e.g., phased reporting)

### Q2: Should We Derive Status from Single Source of Truth?

**Hypothesis:** Instead of 10 files claiming version, derive all from `GOVERNANCE_CORE_v0_2.json`.

**Approach:**
```json
{
  "current_version": "1.5.0",
  "release_date": "2026-04-18",
  "event_counts": {
    "nz": 38,
    "taiwan": 20,
    "australia": 18,
    "total": 76
  }
}
```

All Markdown files use template syntax: `{{current_version}}` rendered at build time.

**Challenges:**
- Requires build step (currently repo is source-only)
- Templates reduce human readability
- Version control becomes more complex

### Q3: Can We Automate Propagation?

**Hypothesis:** Tooling can auto-update version references across files.

**Approach:**
```bash
research-tools release bump 1.5.0
# Auto-updates:
# - CITATION.cff version and date
# - README.md version references
# - CHANGELOG.md (adds new section)
# - project-status.md version claim
```

**Challenges:**
- Requires structured editing (not just text replacement)
- Must preserve human nuance in prose
- Risk of over-automation (changes without human review)

### Q4: Is the Problem Organizational or Technical?

**Organizational hypothesis:** The issue is process, not tooling. We need:
- Explicit "surface synchronization" step in every phase exit criteria
- Owner assigned for version coordination
- Checklist enforcement

**Technical hypothesis:** The issue is tooling. We need:
- Automated drift detection
- Single source of truth
- Generated surfaces rather than hand-maintained

**Mixed hypothesis:** Both. Organizational process for now, technical automation as repository scales.

---

## Proposed Solutions (Ranked by Effort/Impact)

### Option 1: Enhanced Validators (Low Effort, Medium Impact)

Add ground-truth validators to existing suite:

```python
# New validation checks
- `ground_truth-event-count`: Parse ledgers, compare to status claims
- `ground_truth-version-alignment`: CITATION.cff vs README.md vs CHANGELOG.md
- `ground_truth-date-consistency`: Release dates across all surfaces
```

**Pros:** Uses existing infrastructure, catches drift early  
**Cons:** Still reactive (fails after drift occurs), doesn't prevent staleness

### Option 2: SSOT with Runtime Derivation (Medium Effort, High Impact)

Make `GOVERNANCE_CORE_v0_2.json` the single source of truth:

```json
{
  "release": {
    "version": "1.5.0",
    "date": "2026-04-18"
  },
  "empirical": {
    "nz": {"events": 38, "main_interval": 29},
    "taiwan": {"events": 20},
    "australia": {"events": 18}
  }
}
```

Validators derive all claims from this file. Status surfaces include explicit derivation markers.

**Pros:** One update propagates everywhere, unambiguous truth  
**Cons:** Requires migration, adds dependency on JSON for prose files

### Option 3: Automated Propagation Tool (Medium Effort, Medium Impact)

Build `research-tools release sync` command:

```bash
# Updates all version references atomically
research-tools release sync --version 1.6.0 --date 2026-04-25
```

**Pros:** Reduces manual burden, consistent updates  
**Cons:** Complex to build safely, still requires human trigger

### Option 4: Template-Based Generation (High Effort, High Impact)

Convert all status surfaces to templates:

```markdown
# project-status.md.template

**`{{release.version}}`** names the dated hosted snapshot (**{{release.date}}**).

Current `main` represents a **monograph-{{quality.level}} repository** with 
{{empirical.total}} verified events.
```

Render at commit time or CI time.

**Pros:** Eliminates manual synchronization entirely  
**Cons:** Major architectural change, requires build pipeline, loses "readable source" property

---

## Recommended Path Forward

**Phase 1 (Immediate):** Enhanced Validators
- Add `ground_truth-*` validation checks
- Run in `prepare-handoff` and pre-commit
- Catches drift before it accumulates

**Phase 2 (Short-term):** SSOT Enforcement
- Strengthen `GOVERNANCE_CORE_v0_2.json` as canonical
- Derive surface claims from SSOT where possible
- Document which claims are derived vs hand-authored

**Phase 3 (Long-term):** Evaluate Templates
- If staleness persists despite Phases 1-2, consider template generation
- Requires significant architectural investment

---

## Open Questions for Research

1. **Parser robustness:** Can we reliably extract event counts from natural language status surfaces?

2. **Intentional drift:** Are there legitimate cases where surfaces should diverge from ground truth temporarily?

3. **Scale threshold:** At what repository size does manual synchronization become unsustainable?

4. **Human factors:** Does automation reduce or increase cognitive load for maintainers?

5. **Version migration:** How do we migrate to SSOT without breaking existing handoff protocols?

---

## Related Documentation

- `Research/tools/docs/validation-policy.md` — current validation scope
- `Research/structured-unity-framework/docs/current-execution-order.md` — "Tooling-stage discipline" section

---

## Status

`active research problem - solutions prototyped, implementation pending`
