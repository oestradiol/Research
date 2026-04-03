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
    locked_payoff_sentence = (
        "SUF shows that the New Zealand response should not be read only as centralized executive command, "
        "because public-information coordination is structurally central to the working coordination architecture."
    )

    root_readme = paths.research_root / "README.md"
    suf_readme = paths.suf_root / "README.md"
    project_status = paths.suf_root / "docs" / "project-status.md"
    pending_inventory = paths.suf_root / "docs" / "pending-inventory.md"
    contribution_note = paths.suf_root / "docs" / "contribution-and-payoff-note.md"
    v1_bundle = paths.suf_root / "docs" / "v1-academic-bundle.md"
    framework_overview = paths.suf_root / "docs" / "framework-overview.md"
    how_to_read = paths.suf_root / "docs" / "how-to-read-the-framework.md"
    index_doc = paths.suf_root / "docs" / "INDEX.md"
    reviewer_doc = paths.suf_root / "docs" / "reviewer-objections-and-current-answers.md"
    evidence_doc = paths.suf_root / "docs" / "evidence-status-matrix.md"
    interface_doc = paths.suf_root / "framework" / "framework-interface.md"
    publication_scope = paths.suf_root / "meta" / "publication-scope.md"
    roadmap = paths.suf_root / "ROADMAP.md"
    research_program = paths.suf_root / "framework" / "research-program.md"
    bounded_gain_note = (
        paths.suf_root
        / "applications"
        / "demonstrated-routes"
        / "states-and-societies"
        / "institutional-coordination-under-perturbation"
        / "bounded-gain-against-simpler-readings.md"
    )

    checks = [
        ("status-root-readme-main-state", root_readme, f"Current `main` state: aligned with the hosted `{hosted_version}` New Zealand monograph-baseline release.", "Umbrella README keeps the current release-point alignment explicit."),
        ("status-suf-readme-bounded-release", suf_readme, "publication-ready bounded public release", "SUF README keeps the bounded public release wording explicit."),
        ("status-suf-readme-no-proof-whole-stack", suf_readme, "treat the New Zealand route as proof of the whole stack", "SUF README explicitly blocks treating the New Zealand route as proof of the whole stack."),
        ("status-suf-readme-metrics", suf_readme, f"a `{nz_summary.event_count}`-event New Zealand public ledger with a `{nz_summary.main_interval_count}`-event main interval", "SUF README exposes the current New Zealand baseline metrics."),
        ("status-suf-readme-taiwan", suf_readme, f"a `{taiwan_summary.event_count}`-event bounded Taiwan comparator with one conservative lag pair", "SUF README exposes the current Taiwan comparator baseline."),
        ("status-v1-bundle-metrics", v1_bundle, f"The main empirical anchor is a New Zealand pandemic-coordination route with a `{nz_summary.event_count}`-event public ledger, a `{nz_summary.main_interval_count}`-event main perturbation interval", "v1 academic bundle current New Zealand baseline matches the ledger."),
        ("status-v1-bundle-taiwan", v1_bundle, f"A bounded Taiwan comparator now adds a `{taiwan_summary.event_count}`-event archive-clean tranche under the same source-admission rule.", "v1 academic bundle current Taiwan baseline matches the comparator ledger."),
        ("status-interface-bridge-control", interface_doc, "Framework Interface is the **bridge/control** layer of Structured Unity Framework.", "Framework Interface explicitly uses bridge/control wording."),
        ("status-overview-layer-framing", framework_overview, "three substantive layers plus one bridge/control layer", "Framework overview reflects the updated layer framing."),
        ("status-how-to-read-sp-link", how_to_read, "framework/structural-phenomenology-downstream-role.md", "Reading path includes the Structural Phenomenology downstream-role note."),
        ("status-how-to-read-bounded-gain-link", how_to_read, "bounded-gain-against-simpler-readings.md", "Reading path includes the bounded-gain note."),
        ("status-index-reviewer-doc", index_doc, "reviewer-objections-and-current-answers.md", "Index includes the reviewer-objections doc."),
        ("status-index-evidence-doc", index_doc, "evidence-status-matrix.md", "Index includes the evidence-status matrix."),
        ("status-project-status-reviewer-doc", project_status, "reviewer-objections-and-current-answers.md", "Project status links the reviewer-objections doc."),
        ("status-project-status-evidence-doc", project_status, "evidence-status-matrix.md", "Project status links the evidence-status matrix."),
        ("status-v1-reviewer-doc", v1_bundle, "reviewer-objections-and-current-answers.md", "v1 bundle links the reviewer-objections doc."),
        ("status-v1-evidence-doc", v1_bundle, "evidence-status-matrix.md", "v1 bundle links the evidence-status matrix."),
        ("status-reviewer-purpose", reviewer_doc, "This file collects the strongest foreseeable academic objections", "Reviewer-objections doc has its intended purpose text."),
        ("status-evidence-purpose", evidence_doc, "This file maps the major current public claims", "Evidence-status matrix has its intended purpose text."),
        ("status-reviewer-doc-evidence-mapping", reviewer_doc, "stronger evidence-to-claim mapping", "Reviewer-objections doc keeps the remaining evidence-to-claim mapping burden explicit."),
        ("status-publication-scope-no-universal-proof", publication_scope, "that one demonstrated route proves the framework universally", "Publication scope explicitly blocks one-route universal proof language."),
        ("status-publication-scope-no-closure", publication_scope, "that the current package already yields objectively settled cross-domain measurement or strong predictive closure", "Publication scope explicitly blocks settled measurement and predictive closure claims."),
        ("status-contribution-note-locked-payoff", contribution_note, locked_payoff_sentence, "Contribution note keeps the locked public payoff sentence explicit."),
        ("status-project-status-locked-payoff", project_status, locked_payoff_sentence, "Project status matches the locked public payoff sentence."),
        ("status-bounded-gain-locked-payoff", bounded_gain_note, locked_payoff_sentence, "Bounded-gain note matches the locked public payoff sentence."),
        ("status-evidence-payoff-row", evidence_doc, locked_payoff_sentence, "Evidence-status matrix includes the locked payoff claim."),
        ("status-evidence-payoff-modeled-locked", evidence_doc, "modeled / provisional but publicly locked", "Evidence-status matrix marks the locked payoff sentence as modeled / provisional but publicly locked."),
        ("status-evidence-no-predictive-closure", evidence_doc, "| The current package demonstrates high-fit predictive closure. | not established |", "Evidence-status matrix keeps predictive closure as not established."),
        ("status-evidence-no-cross-domain-measurement", evidence_doc, "| The current package has objectively settled cross-domain measurement for `I`, `C`, `L`, and `U`. | not established |", "Evidence-status matrix keeps settled cross-domain measurement as not established."),
        ("status-evidence-no-strong-consciousness", evidence_doc, "| The current package justifies strong consciousness attribution to states or institutions. | not established |", "Evidence-status matrix keeps strong institutional consciousness attribution as not established."),
        ("status-research-program-open-work", research_program, "- deeper comparative execution beyond the current bounded Taiwan comparator", "Research program open-work section reflects the current Taiwan comparator posture."),
        ("status-publication-scope-layer-framing", publication_scope, "three substantive framework layers plus one bridge/control layer", "Publication scope reflects the updated layer framing."),
    ]

    forbidden_checks = [
        ("status-readme-no-four-coordinated", suf_readme, "four coordinated theory layers", "SUF README no longer presents four coordinated theory layers."),
        ("status-overview-no-four-theory-layers", framework_overview, "The four theory layers", "Framework overview no longer presents four peer theory layers."),
        ("status-v1-no-four-coordinated", v1_bundle, "four coordinated theory layers", "v1 academic bundle no longer presents four coordinated theory layers."),
        ("status-publication-scope-no-four-layer", publication_scope, "the four-layer framework", "Publication scope no longer presents the four-layer framework wording."),
        ("status-project-status-no-four-layer", project_status, "the four-layer framework structure", "Project status no longer presents the four-layer framework wording."),
        ("status-reviewer-doc-no-indexing-missing", reviewer_doc, "stronger completeness in reviewer-facing indexing", "Reviewer-objections doc no longer describes reviewer-facing indexing as missing or incomplete."),
        ("status-readme-no-nz-proves-stack", suf_readme, "proves the whole stack", "SUF README does not imply that the New Zealand route proves the whole stack."),
        ("status-project-status-no-high-fit-closure", project_status, "high-fit predictive closure", "Project status does not imply high-fit predictive closure."),
        ("status-readme-no-human-like-consciousness", suf_readme, "human-like consciousness", "SUF README does not imply human-like consciousness attribution."),
        ("status-project-status-no-human-like-consciousness", project_status, "human-like consciousness", "Project status does not imply human-like consciousness attribution."),
    ]

    results: list[ValidationResult] = []
    for check_name, path, fragment, message in checks:
        text = path.read_text(encoding="utf-8")
        results.append(_contains(check_name, path, fragment, text, message))
    for check_name, path, fragment, message in forbidden_checks:
        text = path.read_text(encoding="utf-8")
        results.append(_absent(check_name, path, fragment, text, message))
    return results
