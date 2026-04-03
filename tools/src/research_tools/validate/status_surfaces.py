from __future__ import annotations

import re
from pathlib import Path

from research_tools.models.reports import ValidationResult
from research_tools.parse.nz_ledger import parse_nz_ledger
from research_tools.parse.taiwan_ledger import parse_taiwan_ledger
from research_tools.paths import RepoPaths
from research_tools.reports.nz_summary import compute_route_summary

VERSION_RE = re.compile(r'^version:\s*"([^"]+)"\s*$', re.MULTILINE)


def _contains(
    check_name: str,
    path: Path,
    fragment: str,
    text: str,
    message: str,
) -> ValidationResult:
    status = "pass" if fragment in text else "fail"
    return ValidationResult(
        check_name=check_name,
        status=status,
        message=message if status == "pass" else f"{message} Required fragment missing.",
        path=str(path),
        expected=fragment if status == "fail" else None,
        found="missing" if status == "fail" else None,
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
    publication_scope = paths.suf_root / "meta" / "publication-scope.md"
    roadmap = paths.suf_root / "ROADMAP.md"
    research_program = paths.suf_root / "framework" / "research-program.md"

    checks = [
        (
            "status-root-readme-main-state",
            root_readme,
            (
                f"Current `main` state: aligned with the hosted `{hosted_version}` "
                "New Zealand monograph-baseline release."
            ),
            "Umbrella README keeps the current release-point alignment explicit.",
        ),
        (
            "status-root-readme-metrics",
            root_readme,
            (
                f"The hosted `{hosted_version}` tag anchors the public citation, changelog, "
                "and release-note surfaces. Current `main` is aligned with that same release "
                f"point: a `{nz_summary.event_count}`-event New Zealand monograph-baseline "
                f"route with a `{nz_summary.main_interval_count}`-event main interval, a "
                f"`{taiwan_summary.event_count}`-event bounded Taiwan comparator, and the "
                "same read-only validation layer carried forward under the new release line."
            ),
            "Umbrella README release-point metrics match the current package baseline.",
        ),
        (
            "status-suf-readme-metrics",
            suf_readme,
            (
                f"a `{nz_summary.event_count}`-event New Zealand public ledger with a "
                f"`{nz_summary.main_interval_count}`-event main interval"
            ),
            "SUF README exposes the current New Zealand baseline metrics.",
        ),
        (
            "status-suf-readme-taiwan",
            suf_readme,
            (
                f"a `{taiwan_summary.event_count}`-event bounded Taiwan comparator "
                "with one conservative lag pair"
            ),
            "SUF README exposes the current Taiwan comparator baseline.",
        ),
        (
            "status-project-status-main-state",
            project_status,
            (
                f"Current `main` is aligned with the hosted `{hosted_version}` "
                "New Zealand monograph-baseline release for the public package."
            ),
            "Project status keeps the current release-point alignment explicit.",
        ),
        (
            "status-project-status-metrics",
            project_status,
            (
                f"The framework core is in place, the New Zealand route now includes a "
                f"`{nz_summary.event_count}`-event public ledger with a "
                f"`{nz_summary.main_interval_count}`-event main perturbation interval"
            ),
            "Project status metrics match the current route and comparator baseline.",
        ),
        (
            "status-pending-inventory-metrics",
            pending_inventory,
            (
                f"- a `{nz_summary.event_count}`-event New Zealand route with a "
                f"`{nz_summary.main_interval_count}`-event main interval"
            ),
            "Pending inventory current-main summary matches the current New Zealand baseline.",
        ),
        (
            "status-pending-inventory-taiwan",
            pending_inventory,
            f"- a `{taiwan_summary.event_count}`-event bounded Taiwan comparator",
            "Pending inventory current-main summary matches the current Taiwan baseline.",
        ),
        (
            "status-contribution-note-pi",
            contribution_note,
            (
                "- public-information coordination receives "
                f"`{nz_summary.public_information_receiving_count} / "
                f"{nz_summary.event_count}` coded events"
            ),
            "Contribution note current public-information share matches the New Zealand ledger.",
        ),
        (
            "status-contribution-note-taiwan",
            contribution_note,
            (
                "- the current Taiwan bounded comparator also keeps "
                "public-information coordination central rather than peripheral"
            ),
            "Contribution note reflects the current Taiwan comparator posture.",
        ),
        (
            "status-v1-bundle-metrics",
            v1_bundle,
            (
                f"The main empirical anchor is a New Zealand pandemic-coordination route with a "
                f"`{nz_summary.event_count}`-event public ledger, a "
                f"`{nz_summary.main_interval_count}`-event main perturbation interval"
            ),
            "v1 academic bundle current New Zealand baseline matches the ledger.",
        ),
        (
            "status-v1-bundle-taiwan",
            v1_bundle,
            (
                "A bounded Taiwan comparator now adds a "
                f"`{taiwan_summary.event_count}`-event archive-clean tranche under "
                "the same source-admission rule."
            ),
            "v1 academic bundle current Taiwan baseline matches the comparator ledger.",
        ),
        (
            "status-publication-scope-nz",
            publication_scope,
            (
                "- the New Zealand demonstrated route with a "
                f"`{nz_summary.event_count}`-event public ledger, "
                f"a `{nz_summary.main_interval_count}`-event main interval, "
                "a chapter-ready monograph baseline, "
                "first bounded readouts, "
                "and a `14`-check robustness note"
            ),
            "Publication scope current New Zealand baseline matches the ledger.",
        ),
        (
            "status-publication-scope-taiwan",
            publication_scope,
            (
                f"- the bounded Taiwan comparator with a "
                f"`{taiwan_summary.event_count}`-event ledger and one conservative "
                "lag pair"
            ),
            "Publication scope current Taiwan baseline matches the comparator ledger.",
        ),
        (
            "status-roadmap-main-state",
            roadmap,
            (
                f"Current `main` is aligned with the hosted `{hosted_version}` "
                "New Zealand monograph-baseline release for the same public package line."
            ),
            (
                "Roadmap keeps the current release-point status synchronized with the "
                "repo-complete state."
            ),
        ),
        (
            "status-research-program-open-work",
            research_program,
            "- deeper comparative execution beyond the current bounded Taiwan comparator",
            "Research program open-work section reflects the current Taiwan comparator posture.",
        ),
    ]

    results: list[ValidationResult] = []
    for check_name, path, fragment, message in checks:
        text = path.read_text(encoding="utf-8")
        results.append(_contains(check_name, path, fragment, text, message))
    return results
