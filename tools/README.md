# Research Tools

## Purpose

This package provides reproducible, read-only research-support tooling for the `Research/` repository.

The first tranche is scoped to Structured Unity Framework (SUF) route and source work while also covering repository-wide Markdown link validation across `Research/`. It validates current public research surfaces and generates deterministic read-only reports for human review.

This package does **not**:

- rewrite public docs automatically
- make interpretation decisions for the research
- bypass human validation

## Current scope

Tranche 1 supports:

- Markdown link validation across `Research/`
- source-registry shape and archive validation
- New Zealand route parsing and consistency checks
- Taiwan starter-route parsing and consistency checks
- deterministic read-only report generation

## Workflow model

- Nix provides the interpreter and base toolchain.
- `.venv` lives inside this directory and is local-only.
- Generated outputs live under `out/`.
- Public docs remain human-authored.

## Setup

```bash
cd Research/tools
nix develop
python -m venv --system-site-packages .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --no-build-isolation -e .[dev]
ruff check .
pytest
```

## Commands

```bash
research-tools validate links
research-tools validate archives
research-tools validate source-registry
research-tools validate route --route nz
research-tools validate route --route taiwan
research-tools validate all

research-tools report nz-summary
research-tools report nz-window-comparison
research-tools report nz-taiwan-summary
```

## Output policy

- validation commands are read-only with respect to repo-tracked Research docs
- report commands write Markdown under `out/`
- generated outputs are provisional and require human review
- mismatches are reported, not auto-applied

## Governance

Important tooling decisions are tracked in:

- `docs/architecture.md`
- `docs/validation-policy.md`
- `docs/backlog.md`
- `docs/sprint-log.md`
- `docs/adr/`

## Status

`tranche-1 tooling active`
