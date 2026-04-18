# SUF Analysis-Ready Tooling

## Purpose

This directory contains v1.5 analysis-ready tooling for the Structured Unity Framework.

Tools are **read-only** — they derive from canonical Markdown docs and do not rewrite public prose.

## Tool Categories

### `exports/`
Structured data exports from canonical Markdown sources.

- `ledger-to-json.py` — Convert event ledgers to JSON
- `source-registry-to-csv.py` — Export source registry to CSV
- `cross-case-metrics.json` — Generated three-case summary metrics

### `validators/`
Deterministic validation of claims against canonical docs.

- `validate-ledger-counts.py` — Verify event counts match claims
- `validate-archive-urls.py` — Check Wayback archive reachability
- `validate-closure-note.py` — Verify cross-case claims against ledgers
- `validate-monograph-integrity.py` — Check chapter-to-artifact mapping

### `generators/`
Deterministic table/figure generation for monograph-facing docs.

- `generate-event-table.py` — Create summary tables from ledgers
- `generate-source-family-chart.py` — Source distribution visualization data
- `generate-comparison-matrix.py` — Cross-case metric matrices

## Usage

All tools read from `../` (canonical docs) and write to `./outputs/` (derived artifacts).

```bash
# Export ledgers to JSON
python3 tools/exports/ledger-to-json.py \
  --input applications/demonstrated-routes/.../event-ledger-seed.md \
  --output tools/outputs/nz-ledger.json

# Validate closure note claims
python3 tools/validators/validate-closure-note.py \
  --closure-note applications/.../nz-taiwan-australia-closure-note.md \
  --ledgers tools/outputs/*-ledger.json

# Generate comparison table
python3 tools/generators/generate-comparison-matrix.py \
  --ledgers tools/outputs/*-ledger.json \
  --output tools/outputs/comparison-matrix.md
```

**Environment**: Python 3.8+ required. No external dependencies (standard library only).

## Status

`v1.5 analysis-ready tooling — initial structure established`
