# Implementation Layer Policy v0.1

## Purpose

This file explains which implementation layers should be used for which jobs in the public repository and how to decide between them.

It exists to stop stack choices from collapsing into habit.

## Core rule

Choose the narrowest adequate layer for the job. Keep durable truth, machine coordination, environment control, orchestration logic, and performance-critical code in different layers unless there is a clear reason to merge them.

## Current layer stack

### Layer 1: human-readable truth surfaces

Primary media:

- Markdown

Use for:

- package truth
- argument, route, and boundary prose
- handoff surfaces for humans and agents

Do not use for:

- executable orchestration logic
- machine-only coordination state that must be parsed deterministically every run

### Layer 2: machine-readable protocol and registry surfaces

Primary media:

- JSON

Use for:

- current-surface registries
- integrity manifests
- machine-readable subsystem ownership and scope
- explicit policy or protocol data that tools should consume directly

Do not use for:

- human-facing explanation that needs nuance and legibility

### Layer 3: environment and toolchain skeleton

Primary media:

- Nix

Use for:

- reproducible environments
- language/runtime availability
- shared system skeleton for multi-language tooling

Do not use for:

- application logic
- research truth surfaces

### Layer 4: orchestration, parsing, validation, and glue

Primary media:

- Python

Use for:

- parsing Markdown and registries
- validation and reporting
- read-only workflows
- fast-turnaround tooling and prototypes

Do not use for:

- pretending to be the environment layer
- hiding durable governance state that should live in explicit registries

### Layer 5: shell entrypoints

Primary media:

- shell scripts or one-line commands

Use for:

- thin wrappers
- operator convenience
- command composition at the edge

Do not use for:

- durable core logic
- complex branching business rules

### Layer 6: compiled systems components

Candidate media:

- Rust or another compiled language when justified

Use for:

- long-lived or safety-critical operators
- concurrency-heavy services
- correctness- or performance-sensitive subsystems
- agent runtimes that outgrow scripting ergonomics

Do not use for:

- fashionable overreach
- code that still benefits more from iteration speed than from compilation

## Decision rules

1. If the job is human truth, use Markdown first.
2. If the job is machine coordination metadata, use JSON first.
3. If the job is environment reproducibility or toolchain skeleton, use Nix first.
4. If the job is parsing, validation, reporting, or glue, use Python first.
5. If the job is only an operator wrapper, keep shell thin.
6. Only promote work into a compiled language when safety, concurrency, runtime, or performance pressures clearly justify it.

## Promotion triggers for compiled components

Promotion from Python or shell toward Rust-like layers should require at least one of:

- repeated correctness failures that stronger typing or ownership discipline would materially reduce
- concurrency or async complexity that has become central rather than incidental
- long-running processes where operational robustness matters more than iteration speed
- performance bottlenecks shown by actual profiling rather than intuition

## Architecture evidence policy

Every durable layer or stack decision should carry a minimal evidence packet.

Minimum decision packet:

- decision being made
- job to be done
- alternatives considered
- why the chosen layer fits better now
- main objections or risks
- promotion or revisit triggers
- file references or source anchors when external guidance informed the choice

This can live in an ADR, policy note, or bounded design note, but the reasoning should be externalized instead of remaining only in agent memory.

## Anti-patterns

- using shell as a permanent logic layer
- using Python as an implicit source of governance truth
- using Nix to encode application behavior that belongs in tooling code
- using compiled languages before the problem has stabilized enough to justify them
- storing human-meaning-bearing truth primarily in machine-oriented formats

## Status

`current root policy for choosing implementation layers in the public repo`

## Architecture evidence packet

When introducing or promoting a layer choice, record at least:

- problem being solved
- why this layer is the narrowest adequate one
- alternatives considered
- reasons rejected or deferred
- validation surface or success criterion
- what future pressure would justify promotion to a stronger or lower-level layer

Do not let habit, model preference, or local convenience silently become architecture.

## Skeptical implementation stance

Implementation choices should default to doubt. A persuasive proposal is not enough. The question is what grounds the choice, what failure mode it closes, what new failure mode it introduces, and how the system will notice if that choice later becomes stale or legacy baggage.
