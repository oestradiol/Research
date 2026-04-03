from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from research_tools.parse.nz_ledger import parse_nz_ledger
from research_tools.parse.source_registry import parse_source_registry, source_registry_index
from research_tools.parse.taiwan_ledger import parse_taiwan_ledger
from research_tools.paths import get_paths
from research_tools.reports.nz_summary import (
    compare_nz_summary_to_docs,
    compute_nz_window_summaries,
    compute_route_summary,
    render_nz_summary_report,
    render_nz_window_report,
)
from research_tools.reports.nz_taiwan_summary import (
    compare_nz_taiwan_summary_to_docs,
    render_nz_taiwan_report,
)
from research_tools.validate.archives import validate_archive_links
from research_tools.validate.links import validate_markdown_links
from research_tools.validate.route_consistency import validate_nz_route, validate_taiwan_route
from research_tools.validate.sources import validate_source_registry
from research_tools.workflows.validate_all import render_validation_report


def _generated_at() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _write_output(filename: str, content: str) -> Path:
    paths = get_paths()
    paths.out_root.mkdir(parents=True, exist_ok=True)
    output_path = paths.out_root / filename
    output_path.write_text(content, encoding="utf-8")
    return output_path


def _results_exit_code(results: list) -> int:
    return 1 if any(result.status == "fail" for result in results) else 0


def _render_simple_results(
    title: str,
    generated_at: str,
    results: list,
    source_files: list[Path],
) -> str:
    files = "\n".join(f"- `{path}`" for path in source_files)
    body = "\n".join(
        f"- `{result.check_name}` [{result.status}] {result.message}"
        + (f" Expected `{result.expected}`." if result.expected else "")
        + (f" Found `{result.found}`." if result.found else "")
        + (f" Path `{result.path}`." if result.path else "")
        for result in results
    )
    return f"""# {title}

Generated: `{generated_at}`

## Source files

{files}

## Results

{body}

## Human validation required

This output is read-only and provisional until a human reviews it.
"""


def handle_validate_links(_: argparse.Namespace) -> int:
    paths = get_paths()
    results = validate_markdown_links(paths.suf_root)
    output = _render_simple_results(
        "Validate Links",
        _generated_at(),
        results,
        [paths.suf_root],
    )
    output_path = _write_output("validate-links.md", output)
    print(output_path)
    return _results_exit_code(results)


def handle_validate_archives(_: argparse.Namespace) -> int:
    paths = get_paths()
    entries = parse_source_registry(paths.source_registry)
    results = validate_archive_links(entries)
    output = _render_simple_results(
        "Validate Archives",
        _generated_at(),
        results,
        [paths.source_registry],
    )
    output_path = _write_output("validate-archives.md", output)
    print(output_path)
    return _results_exit_code(results)


def handle_validate_source_registry(_: argparse.Namespace) -> int:
    paths = get_paths()
    entries = parse_source_registry(paths.source_registry)
    results = validate_source_registry(entries)
    output = _render_simple_results(
        "Validate Source Registry",
        _generated_at(),
        results,
        [paths.source_registry],
    )
    output_path = _write_output("validate-source-registry.md", output)
    print(output_path)
    return _results_exit_code(results)


def handle_validate_route(args: argparse.Namespace) -> int:
    paths = get_paths()
    entries = parse_source_registry(paths.source_registry)
    index = source_registry_index(entries)
    if args.route == "nz":
        results = validate_nz_route(paths.nz_route_root, index)
        source_files = [
            paths.nz_route_root / "event-ledger-seed.md",
            paths.nz_route_root / "first-pass-i-summary.md",
            paths.nz_route_root / "first-pass-window-comparison.md",
            paths.suf_root / "docs" / "project-status.md",
        ]
        filename = "validate-route-nz.md"
        title = "Validate Route NZ"
    else:
        results = validate_taiwan_route(paths.taiwan_route_root, index)
        source_files = [
            paths.taiwan_route_root / "taiwan-event-ledger-seed.md",
            paths.taiwan_route_root / "first-nz-taiwan-comparison-note.md",
        ]
        filename = "validate-route-taiwan.md"
        title = "Validate Route Taiwan"
    output = _render_simple_results(title, _generated_at(), results, source_files)
    output_path = _write_output(filename, output)
    print(output_path)
    return _results_exit_code(results)


def handle_validate_all(_: argparse.Namespace) -> int:
    paths = get_paths()
    entries = parse_source_registry(paths.source_registry)
    index = source_registry_index(entries)
    results = []
    results.extend(validate_markdown_links(paths.suf_root))
    results.extend(validate_source_registry(entries))
    results.extend(validate_archive_links(entries))
    results.extend(validate_nz_route(paths.nz_route_root, index))
    results.extend(validate_taiwan_route(paths.taiwan_route_root, index))
    output = render_validation_report(
        generated_at=_generated_at(),
        results=results,
        source_files=[
            paths.suf_root,
            paths.source_registry,
            paths.nz_route_root / "event-ledger-seed.md",
            paths.taiwan_route_root / "taiwan-event-ledger-seed.md",
        ],
    )
    output_path = _write_output("validation-report.md", output)
    print(output_path)
    return _results_exit_code(results)


def handle_report_nz_summary(_: argparse.Namespace) -> int:
    paths = get_paths()
    events = parse_nz_ledger(paths.nz_route_root / "event-ledger-seed.md")
    summary = compute_route_summary("nz", events)
    window_summaries = compute_nz_window_summaries(events)
    validations = compare_nz_summary_to_docs(
        summary=summary,
        window_summary=window_summaries["Main perturbation interval"],
        project_status_path=paths.suf_root / "docs" / "project-status.md",
        i_summary_path=paths.nz_route_root / "first-pass-i-summary.md",
        seed_readout_path=paths.nz_route_root / "first-pass-seed-readout.md",
        window_comparison_path=paths.nz_route_root / "first-pass-window-comparison.md",
    )
    output = render_nz_summary_report(
        summary=summary,
        window_summary=window_summaries["Main perturbation interval"],
        validations=validations,
        source_files=[
            paths.nz_route_root / "event-ledger-seed.md",
            paths.nz_route_root / "first-pass-i-summary.md",
            paths.nz_route_root / "first-pass-seed-readout.md",
            paths.nz_route_root / "first-pass-window-comparison.md",
            paths.suf_root / "docs" / "project-status.md",
        ],
        generated_at=_generated_at(),
    )
    output_path = _write_output("nz-summary.md", output)
    print(output_path)
    return _results_exit_code(validations)


def handle_report_nz_window_comparison(_: argparse.Namespace) -> int:
    paths = get_paths()
    events = parse_nz_ledger(paths.nz_route_root / "event-ledger-seed.md")
    output = render_nz_window_report(
        compute_nz_window_summaries(events),
        _generated_at(),
        [
            paths.nz_route_root / "event-ledger-seed.md",
            paths.nz_route_root / "first-pass-window-comparison.md",
        ],
    )
    output_path = _write_output("nz-window-comparison.md", output)
    print(output_path)
    return 0


def handle_report_nz_taiwan_summary(_: argparse.Namespace) -> int:
    paths = get_paths()
    nz_events = parse_nz_ledger(paths.nz_route_root / "event-ledger-seed.md")
    taiwan_events = parse_taiwan_ledger(paths.taiwan_route_root / "taiwan-event-ledger-seed.md")
    nz_summary = compute_route_summary("nz", nz_events)
    taiwan_summary = compute_route_summary("taiwan", taiwan_events)
    validations = compare_nz_taiwan_summary_to_docs(
        nz_summary=nz_summary,
        taiwan_summary=taiwan_summary,
        comparison_note_path=paths.taiwan_route_root / "first-nz-taiwan-comparison-note.md",
    )
    output = render_nz_taiwan_report(
        nz_summary=nz_summary,
        taiwan_summary=taiwan_summary,
        validations=validations,
        source_files=[
            paths.nz_route_root / "event-ledger-seed.md",
            paths.taiwan_route_root / "taiwan-event-ledger-seed.md",
            paths.taiwan_route_root / "first-nz-taiwan-comparison-note.md",
        ],
        generated_at=_generated_at(),
    )
    output_path = _write_output("nz-taiwan-summary.md", output)
    print(output_path)
    return _results_exit_code(validations)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="research-tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate")
    validate_subparsers = validate_parser.add_subparsers(dest="validate_command", required=True)

    validate_subparsers.add_parser("links").set_defaults(func=handle_validate_links)
    validate_subparsers.add_parser("archives").set_defaults(func=handle_validate_archives)
    validate_subparsers.add_parser("source-registry").set_defaults(
        func=handle_validate_source_registry
    )
    validate_route_parser = validate_subparsers.add_parser("route")
    validate_route_parser.add_argument("--route", choices=("nz", "taiwan"), required=True)
    validate_route_parser.set_defaults(func=handle_validate_route)
    validate_subparsers.add_parser("all").set_defaults(func=handle_validate_all)

    report_parser = subparsers.add_parser("report")
    report_subparsers = report_parser.add_subparsers(dest="report_command", required=True)
    report_subparsers.add_parser("nz-summary").set_defaults(func=handle_report_nz_summary)
    report_subparsers.add_parser("nz-window-comparison").set_defaults(
        func=handle_report_nz_window_comparison
    )
    report_subparsers.add_parser("nz-taiwan-summary").set_defaults(
        func=handle_report_nz_taiwan_summary
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    func: Callable[[argparse.Namespace], int] = args.func
    return func(args)


if __name__ == "__main__":
    raise SystemExit(main())
