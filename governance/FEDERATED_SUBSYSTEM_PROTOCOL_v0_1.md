# Federated Subsystem Protocol v0.1

## Purpose

This file defines how the root repository should operate as a federation of bounded parts rather than as one flattened surface.

It exists to keep growth modular, local ownership explicit, and cross-part coordination legible.

Machine-readable companion surfaces:

- `SUBSYSTEM_REGISTRY_v0_1.json`
- `IMPLEMENTATION_LAYER_POLICY_v0_1.md`

## Core rule

Each major part should own its local truth, local maintenance, and local validation posture. Umbrella governance should coordinate those parts, not absorb them.

## Current public subsystem map

For machine-readable ownership, scopes, entry surfaces, and cluster metadata, use `SUBSYSTEM_REGISTRY_v0_1.json`.

Tooling should consume that registry instead of re-encoding subsystem ownership or cluster metadata in code whenever a machine-readable field is already present.

### Root governance layer

Owns:

- umbrella routing
- package-role clarity
- current-surface governance
- release hygiene

Does not own:

- SUF package-local academic truth
- Knowledge atlas-local structure
- tools-local implementation detail

### `structured-unity-framework/`

Owns:

- academic-core truth
- package-local current state
- package-local route and evidence posture

Primary entry and control surfaces:

- `structured-unity-framework/START_HERE.md`
- `structured-unity-framework/governance/AUTHORITATIVE_INDEX_v0_1.md`
- `structured-unity-framework/docs/project-status.md`
- `structured-unity-framework/docs/current-execution-order.md`

### `knowledge/`

Owns:

- atlas structure
- study routes
- typed relations
- domain-native versus SUF-supported role discipline

Primary entry and control surfaces:

- `knowledge/README.md`
- `knowledge/_indexes/knowledge-index.md`
- `knowledge/_indexes/node-index.md`
- `knowledge/study-routes/README.md`

### `tools/`

Owns:

- read-only validation
- deterministic reporting
- workflow orchestration over public artifacts

Primary entry and control surfaces:

- `tools/README.md`
- `tools/docs/architecture.md`
- `tools/docs/validation-policy.md`

## Minimum shared protocol

Every subsystem should make these visible:

1. purpose and boundary
2. stable entry surface
3. current-state or authoritative surfaces where relevant
4. local validation or review path
5. human-readable handoff path using file references
6. explicit edit-scope discipline when cross-subsystem changes are needed
7. machine-readable scope and navigation data when tooling or multiple agents need to share the same map
8. durable write-back rules for research deltas, decisions, and promotion state

## Navigation and trust

Actors should navigate by scope, not by convenience.

Use the owning subsystem's authoritative and current surfaces first, then the machine-readable registry, then validation outputs, and only then supportive prose or prompt-local memory.

Default actor classes and scope classes are defined in `SUBSYSTEM_REGISTRY_v0_1.json`.

## Cross-subsystem change procedure

When work crosses subsystem boundaries:

1. identify the owning subsystem for the primary change
2. make the smallest effective local change there first
3. update a neighboring subsystem only if coordination, routing, validation, or handoff really changed
4. validate locally first
5. validate at umbrella level when the cross-part interface changed
6. leave a handoff trail through file references rather than implicit memory
7. write durable research deltas back into the owning subsystem with provenance, short summary, status, and target file reference

## Placement rules for future code, tests, and validators

- new code should land in the narrowest responsible subsystem
- package-local tests or validators should live near the package or module they protect when possible
- umbrella orchestration may compose subsystem outputs, but should not erase local ownership
- root should not become the default location for unrelated helpers just because it is convenient

## Renewal relationship

Federation and renewal support each other.

- good local ownership makes recompression easier
- renewal cycles should first simplify locally before centralizing globally
- if boundaries stop earning their cost, renewal work may merge, reroute, or shrink them

## Anti-patterns

- one package or folder becoming the default home for unrelated logic
- root governance drifting into package-local truth maintenance
- shared helpers expanding until every subsystem depends on one hidden center
- cross-subsystem edits happening by convenience rather than by explicit protocol
- local validation being skipped in favor of only umbrella checks

## Adding a new subsystem

A new bounded subsystem should earn its place by showing:

- a distinct job that existing parts do not already own well
- a stable entry surface
- a local validation or review path
- a clear relationship to current root governance and the other packages
- enough expected future growth to justify bounded ownership

If those conditions are not met, prefer extending an existing subsystem instead.

## Status

`current root governance protocol for federated subsystem ownership`

## Heterogeneous-agent rule

The federation should assume from the start that different agents, proto-agents, humans, and tools will have different capacities, blind spots, costs, and context limits.

Therefore:

- subsystem interfaces should be explicit enough that weaker or narrower agents can still operate safely
- validation should not depend on one model family or one reasoning style
- critical paths should prefer inspectable files, small protocols, and tool-grounded checks over charisma or apparent confidence
- cross-subsystem cooperation should preserve coherence by protocol, not by assuming shared cognition

## Self-coverage rule

When possible, each subsystem should eventually expose a path for inspecting its own freshness, drift, or blind spots. If full self-validation is not yet possible, the gap should be documented as known debt and revisited during renewal cycles.
