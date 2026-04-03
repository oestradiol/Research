# Sprint Log

## 2026-04-02 - Tranche 1 scaffold

### Target

Create the first strict-gated tooling package for SUF validation and read-only reporting.

### Commands added

- `research-tools validate links`
- `research-tools validate archives`
- `research-tools validate source-registry`
- `research-tools validate route --route nz`
- `research-tools validate route --route taiwan`
- `research-tools validate all`
- `research-tools report nz-summary`
- `research-tools report nz-window-comparison`
- `research-tools report nz-taiwan-summary`

### Validations added

- Markdown link checks
- source-registry checks
- archive-shape checks
- NZ route schema and consistency checks
- Taiwan route schema and consistency checks

### Tests added

- link validation
- source-registry parsing
- NZ ledger parsing
- Taiwan ledger parsing
- route consistency
- report generation

### Known gaps

- no lag-pair recomputation yet
- no Knowledge validation yet
- no doc-patch workflow

### Next tasks

- extend validation beyond SUF route surfaces where that adds real value
- add Knowledge-specific validators and graph checks
- extend Taiwan support when the comparator branch deepens
- decide when to add richer report exports

### Verified outcomes

- `nix develop` + local `.venv` workflow confirmed
- editable install confirmed with `--system-site-packages` and `--no-build-isolation`
- `ruff check .` passing
- `pytest` passing
- report and validation commands generating outputs under `out/`

## Status

`sprint log active`
