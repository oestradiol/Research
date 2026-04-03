# Architecture

## Purpose

`Research/tools/` is a read-only tooling layer for validating and summarizing research artifacts in `Research/`.

The current public scope still centers on the SUF route work, but now also includes Knowledge package checks, version-surface validation, and release-readiness reporting for the full public repo.

## Module boundaries

- `models/`: typed data structures for sources, ledgers, summaries, and validation results
- `parse/`: Markdown parsers for source registry entries, ledger events, and links
- `validate/`: pure validation checks that return structured results
- `reports/`: deterministic read-only summary generation
- `workflows/`: command-level orchestration for combined checks

## Data flow

1. path resolution from `paths.py`
2. Markdown parsing into typed models
3. validation and metric computation
4. read-only report rendering to `out/`

## Current route assumptions

- New Zealand is the primary validated route
- Taiwan is the current starter comparator
- route metrics are derived from public Markdown, not an external database
- Taiwan comparator files currently live inside the same case directory as the New Zealand route package

## Output rule

The tooling may compute, compare, and report. It may not rewrite public docs.

## Status

`architecture locked for tranche 1`
