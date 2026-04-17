# Package minimization policy v0.2

Rules:

- no root file without a routing, governance, licensing, citation, or operational job
- no current surface without explicit inclusion in the current-surfaces registry
- no supportive file should silently pretend to be current truth
- root docs should route to package-local truth instead of duplicating package state where routing will do
- historical or migration-only meta should not remain in live root pathways once the port is complete
- new files should prefer existing package structure over ad hoc root growth
- growth phases should be followed by deliberate recompression and rebirth passes rather than indefinite additive accumulation
- recompression and rebirth must also search for stale assumptions, missing self-reference, missing self-tests, and hidden legacy drift in governance or tooling
- maintenance is part of operational correctness here, not cosmetic aftercare
- the umbrella repository should remain federated: each major part should own its local structure, validation, and maintenance instead of collapsing into one central dumping ground

## Renewal-cycle rule

When the system starts accumulating stale, duplicate, weakly routed, or hard-to-navigate material, pause expansion work long enough to run a bounded renewal cycle.

Typical triggers:

- current or supportive files begin duplicating each other
- agent startup or retrieval cost rises because too many surfaces must be scanned
- stale notes, support docs, or legacy routing survive after newer current surfaces exist
- validators pass but navigation quality, legibility, or edit safety is degrading
- more effort is being spent remembering the structure than using it

Renewal-cycle stages:

1. freeze unnecessary expansion
2. audit duplication, drift, stale surfaces, and routing burden
3. recompress by deleting, merging, archiving, shortening, or externalizing redundant material
4. refactor names, locations, and interfaces so the current truth becomes simpler to find and harder to misuse
5. rebuild indexes, registries, manifests, and handoff surfaces
6. reopen normal work only after validation passes again

Guardrail:

Do not let maintenance become permanent self-referential meta-work. The cycle is complete only when the repository is simpler, clearer, and easier to operate than before.

Optimization requirement:

A serious renewal cycle should check whether the system can still inspect, validate, and improve its own critical parts. If a validator can inspect others but not itself, if scaffolding coordinates work but cannot surface its own drift, or if a subsystem has no path for recursive review, that gap should be treated as design debt rather than as optional polish.

Self-reference is therefore allowed here only as disciplined recursion: bounded, evidence-seeking, and aimed at convergence rather than inflation.

## Federation rule

The repository should grow as a federation of bounded parts rather than as one ever-flatter structure.

That means:

- new logic should land in the narrowest responsible package or subsystem
- root surfaces should route, govern, and summarize, not absorb local package truth
- each subsystem should keep its own entrypoint, local interfaces, and local maintenance posture
- future test, validation, and automation clusters should live near the package they protect whenever possible
- cross-subsystem coordination should happen through explicit shared protocol surfaces rather than hidden assumptions

Minimum shared protocol between parts:

- a clear purpose and boundary
- a stable entry surface
- explicit current-state or authoritative surfaces where relevant
- local validation or review path
- human-readable file references for handoff and traceability
- explicit change-scope and handoff discipline for cross-part edits

Anti-patterns:

- one folder becoming the default home for unrelated logic
- root governance quietly replacing package-local ownership
- shared utilities expanding until subsystem boundaries stop meaning anything
- agents editing across parts by convenience rather than by declared interface
