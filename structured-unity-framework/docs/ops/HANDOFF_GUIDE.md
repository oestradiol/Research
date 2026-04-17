# Handoff guide

If you are handing off the current SUF package state to a future operator:

1. start with `../../README.md` and `../../START_HERE.md`
2. use `../../governance/AUTHORITATIVE_INDEX_v0_1.md` before trusting any file as current
3. read `../project-status.md`
4. read `../current-execution-order.md`
5. read `../pending-inventory.md`
6. use `../../framework/research-program.md` and `../../references/source-registry.md` for methods and sources
7. capture the current repo commit and working-tree state before describing the package as current
8. from the repository root, run the package doctor through the `tools` environment before treating the package as clean current state

Preferred validation path from the `Research/` root:

- `nix develop ./tools -c python package_doctor.py`

Equivalent supported environments may use the Python setup documented in `tools/README.md`.

Minimal handoff packet:

- current objective or open question
- touched current surfaces
- validation status
- residual risks or open decisions
- the best next starting point

Do not silently merge current truth, supportive context, and historical trace into one undifferentiated surface.
