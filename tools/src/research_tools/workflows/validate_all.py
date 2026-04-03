from __future__ import annotations

from pathlib import Path

from research_tools.models.reports import ValidationResult


def summarize_validation_results(results: list[ValidationResult]) -> tuple[int, int, int]:
    passed = sum(1 for result in results if result.status == "pass")
    failed = sum(1 for result in results if result.status == "fail")
    warned = sum(1 for result in results if result.status == "warn")
    return passed, failed, warned


def render_validation_report(
    generated_at: str,
    results: list[ValidationResult],
    source_files: list[Path],
) -> str:
    passed, failed, warned = summarize_validation_results(results)
    files = "\n".join(f"- `{path}`" for path in source_files)
    body = "\n".join(
        f"- `{result.check_name}` [{result.status}] {result.message}"
        + (f" Expected `{result.expected}`." if result.expected else "")
        + (f" Found `{result.found}`." if result.found else "")
        + (f" Path `{result.path}`." if result.path else "")
        for result in results
    )
    return f"""# Validation Report

Generated: `{generated_at}`

## Source files

{files}

## Summary

- passed: `{passed}`
- failed: `{failed}`
- warned: `{warned}`

## Results

{body}

## Human validation required

This output is read-only and provisional until a human reviews it.
"""
