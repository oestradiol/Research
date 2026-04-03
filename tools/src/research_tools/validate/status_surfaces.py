from __future__ import annotations

import re
from pathlib import Path

from research_tools.models.reports import ValidationResult
from research_tools.parse.nz_ledger import parse_nz_ledger
from research_tools.parse.taiwan_ledger import parse_taiwan_ledger
from research_tools.paths import RepoPaths
from research_tools.reports.nz_summary import compute_route_summary

VERSION_RE = re.compile(r'^version:\s*"([^"]+)"\s*$', re.MULTILINE)


def _contains(check_name: str, path: Path, fragment: str, text: str, message: str) -> ValidationResult:
    status = "pass" if fragment in text else "fail"
    return ValidationResult(
        check_name=check_name,
        status=status,
        message=message if status == "pass" else f"{message} Required fragment missing.",
        path=str(path),
        expected=fragment if status == "fail" else None,
        found="missing" if status == "fail" else None,
    )


def _absent(check_name: str, path: Path, fragment: str, text: str, message: str) -> ValidationResult:
    status = "pass" if fragment not in text else "fail"
    return ValidationResult(
        check_name=check_name,
        status=status,
        message=message if status == "pass" else f"{message} Forbidden fragment present.",
        path=str(path),
        expected=f"no '{fragment}'",
        found=fragment if status == "fail" else "none",
    )


def _extract_version(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = VERSION_RE.search(text)
    if not match:
        raise ValueError(f"version not found in {path}")
    return match.group(1)


def validate_status_surfaces(paths: RepoPaths) -> list[ValidationResult]:
    nz_events = parse_nz_ledger(paths.nz_route_root / "event-ledger-seed.md")
    taiwan_events = parse_taiwan_ledger(paths.taiwan_route_root / "taiwan-event-ledger-seed.md")
    nz_summary = compute_route_summary("nz", nz_events)
    taiwan_summary = compute_route_summary("taiwan", taiwan_events)
    hosted_version = f"v{_extract_version(paths.research_root / 'CITATION.cff')}"

    root_readme = paths.research_root / "README.md"
    suf_readme = paths.suf_root / "README.md"
    project_status = paths.suf_root / "docs" / "project-status.md"
    pending_inventory = paths.suf_root / "docs" / "pending-inventory.md"
    contribution_note = paths.suf_root / "docs" / "contribution-and-payoff-note.md"
    v1_bundle = paths.suf_root / "docs" / "v1-academic-bundle.md"
    framework_overview = paths.suf_root / "docs" / "framework-overview.md"
    how_to_read = paths.suf_root / "docs" / "how-to-read-the-framework.md"
    interface_doc = paths.suf_root / "framework" / "framework-interface.md"
    publication_scope = paths.suf_root / "meta" / "publication-scope.md"
    roadmap = paths.suf_root / "ROADMAP.md"
    research_program = paths.suf_root / "framework" / "research-program.md"

    checks = [
        (
            "status-root-readme-main-state",
            root_readme,
            f"Current `main` state: aligned with the hosted `{hosted_version}` New Zealand monograph-baseline release.",
            "Umbrella README keeps the current release-point alignment explicit.",
        ),
        (
            "status-suf-readme-metrics",
            suf_readme,
            f"a `{nz_summary.event_count}`-event New Zealand public ledger with a `{nz_summary.main_interval_count}`-event main interval",
            "SUF README exposes the current New Zealand baseline metrics.",
        ),
        (
            "status-suf-readme-taiwan",
            suf_readme,
            f"a `{taiwan_summary.event_count}`-event bounded Taiwan comparator with one conservative lag pair",
            "SUF README exposes the current Taiwan comparator baseline.",
        ),
        (
            "status-v1-bundle-metrics",
            v1_bundle,
            f"The main empirical anchor is a New Zealand pandemic-coordination route with a `{nz_summary.event_count}`-event public ledger, a `{nz_summary.main_interval_count}`-event main perturbation interval",
            "v1 academic bundle current New Zealand baseline matches the ledger.",
        ),
        (
            "status-v1-bundle-taiwan",
            v1_bundle,
            f"A bounded Taiwan comparator now adds a `{taiwan_summary.event_count}`-event archive-clean tranche under the same source-admission rule.",
            "v1 academic bundle current Taiwan baseline matches the comparator ledger.",
        ),
        (
            "status-interface-bridge-control",
            interface_doc,
            "Framework Interface is the **bridge/control** layer of Structured Unity Framework.",
            "Framework Interface explicitly uses bridge/control wording.",
        ),
        (
            "status-overview-layer-framing",
            framework_overview,
            "three substantive layers plus one bridge/control layer",
            "Framework overview reflects the updated layer framing.",
        ),
        (
            "status-how-to-read-sp-link",
            how_to_read,
            "framework/structural-phenomenology-downstream-role.md",
            "Reading path includes the Structural Phenomenology downstream-role note.",
        ),
        (
            "status-how-to-read-bounded-gain-link",
            how_to_read,
            "bounded-gain-against-simpler-readings.md",
            "Reading path includes the bounded-gain note.",
        ),
        (
            "status-research-program-open-work",
            research_program,
            "- deeper comparative execution beyond the current bounded Taiwan comparator",
            "Research program open-work section reflects the current Taiwan comparator posture.",
        ),
    ]

    forbidden_checks = [
        ("status-readme-no-four-coordinated", suf_readme, "four coordinated theory layers", "SUF README no longer presents four coordinated theory layers."),
        ("status-overview-no-four-theory-layers", framework_overview, "The four theory layers", "Framework overview no longer presents four peer theory layers."),
        ("status-v1-no-four-coordinated", v1_bundle, "four coordinated theory layers", "v1 academic bundle no longer presents four coordinated theory layers."),
    ]

    results: list[ValidationResult] = []
    for check_name, path, fragment, message in checks:
        text = path.read_text(encoding="utf-8")
        results.append(_contains(check_name, path, fragment, text, message))
    for check_name, path, fragment, message in forbidden_checks:
        text = path.read_text(encoding="utf-8")
        results.append(_absent(check_name, path, fragment, text, message))
    return results
