# Project purpose and use cases

`Research/` is an umbrella repository for one bounded academic core, one sibling knowledge atlas, and one read-only validation package.

It should be operated as a federation of bounded parts, not as a single flattened surface.

## What the repository contains

- `structured-unity-framework/` — the current academic core and bounded public framework package
- `knowledge/` — the broader Obsidian-first atlas founded on SUF
- `tools/` — the reproducibility, validation, and reporting layer
- `using-this-research-with-human-assistants-and-reasoning-agents.md` — assisted-use guidance

## Primary use cases

- route readers to the correct package without collapsing package roles
- expose root governance and release-hygiene surfaces
- support bounded navigation across SUF, Knowledge, and Tools
- keep assisted reading and validation workflows explicit

## What this repository is not

- not the canonical long-form state surface for SUF
- not a single collapsed monograph file
- not a proof that one demonstrated route settles the full framework
- not a license to treat `knowledge/` as the main academic claim
- not a replacement for human interpretation or domain-native review

## Core navigation rule

Use the package that matches the job:

- framework and current academic posture -> `structured-unity-framework/`
- broader map / study graph -> `knowledge/`
- validation / reports -> `tools/`

Use the governance files before treating any root file as current repository truth. Release history is carried in `CHANGELOG.md` rather than a separate release-notes directory.

## Federation rule

The umbrella repository should keep package roles strong:

- root routes and governs
- `structured-unity-framework/` owns the academic core
- `knowledge/` owns the atlas and study-graph layer
- `tools/` owns read-only validation and reporting

As the system grows, new code, tests, validators, and maintenance routines should prefer the narrowest responsible package instead of accumulating in root by habit. Cross-package coordination should happen through explicit interfaces, current-state surfaces, validation outputs, and file-referenced handoffs.

For the current root protocol, use `governance/FEDERATED_SUBSYSTEM_PROTOCOL_v0_1.md`.
For machine-readable scopes, actor classes, navigation, and trust order, use `governance/SUBSYSTEM_REGISTRY_v0_1.json`.
For stack and language-choice rules plus architecture-decision evidence discipline, use `governance/IMPLEMENTATION_LAYER_POLICY_v0_1.md`.
Durable research deltas should be written back into the owning subsystem rather than left only in chat or ephemeral memory.
