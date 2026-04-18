# Current Execution Order

## Purpose

This file states the shortest live execution order for the current `v1.x` phase.

Use it when the question is not "what is the whole long-range program?" but "what do we do next without drifting?"

**Updated:** 2026-04-18 — phases v1.2-v1.4 now complete; v1.5 tooling phase active

For current package posture, use [project-status.md](project-status.md). For the canonical long-range phase ladder, use [monograph-and-closure-program.md](monograph-and-closure-program.md). For the compressed roadmap, use [../ROADMAP.md](../ROADMAP.md).

## Phase completion status

| Phase | Status | Deliverable |
|-------|--------|-------------|
| v1.2 Taiwan chapter-ready | ✅ **COMPLETE** | 20-event ledger, chapter-ready threshold met |
| v1.3 Australia federal comparator | ✅ **COMPLETE** | 18-event federal-only ledger, AHPPC + National Cabinet |
| v1.4 Bounded pandemic-governance closure | ✅ **COMPLETE** | 76-event 3-case synthesis, rival-framework positioning |
| v1.5 Analysis-ready tooling | **ACTIVE** | Structured exports, enhanced validators |
| v1.6 Research-ops tooling | pending | Maintenance helpers (post-pain) |

## Live execution rule

Do now:

- stop major boundary rewriting
- trust the current three-case synthesis
- treat `v1.5` analysis-ready tooling as the active workstream
- keep tooling read-only posture (docs canonical, tools validate)

### v1.5 tooling scope (analysis-ready)

- **Structured exports:** JSON/CSV route and comparison data for external analysis
- **Enhanced validators:** Cross-case consistency checks, ledger integrity, metric companions
- **Export surfaces:** Human- and machine-readable evidence organization

### v1.5 exit criteria

- [ ] Route export validates against current 76-event corpus
- [ ] Comparison export includes all three cases with metadata
- [ ] Metric companions auto-generated from ledger
- [ ] Validator coverage extended to cross-case patterns

Do not spend current work on:

- further public boundary rewrites not forced by tooling needs
- optional atlas growth
- v1.6 research-ops work before v1.5 analysis-ready is validated
- frontier branches of any kind

## Operational interpretation

The main constraint is now **tooling correctness**, not empirical expansion.

Current public surfaces provide:

- a bounded v1.2.0 release frame
- a stable New Zealand monograph-baseline core (38 events)
- a chapter-ready Taiwan comparator (20 events)
- a bounded Australia federal comparator (18 events)
- a three-case pandemic-governance synthesis (76 events)
- a read-only validation layer preventing silent drift

That means v1.5 work should focus on **export correctness and validator coverage** rather than corpus expansion. Tooling must honor the current empirical base without requiring new data.

## Stale surface warning

`current-execution-order.md` became stale because v1.2-v1.4 completion was not propagated here immediately. This is a documented failure mode. Post-v1.4 tooling stages must include **surface freshness checks** in the definition of "analysis-ready."

## Non-priority rule

Do not spend current work on:

- further public boundary rewrites that are not forced by tooling needs
- optional atlas growth
- v1.6 research-ops before v1.5 analysis-ready validates
- corpus expansion beyond current 76-event base
- frontier branches of any kind

## Tooling-stage discipline

v1.5 must explicitly prevent the stale-surface failure mode that persisted here. Include in exit criteria:

- [ ] All status surfaces (this file, project-status.md, pending-inventory.md) synchronized
- [ ] ROADMAP.md phase markers match actual completion
- [ ] Automated or manual freshness check documented

## Status

`live execution-order surface`
