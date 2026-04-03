from research_tools.parse.nz_ledger import parse_nz_ledger
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


def test_nz_summary_report_renders_current_metrics() -> None:
    paths = get_paths()
    events = parse_nz_ledger(paths.nz_route_root / "event-ledger-seed.md")
    summary = compute_route_summary("nz", events)
    windows = compute_nz_window_summaries(events)
    validations = compare_nz_summary_to_docs(
        summary=summary,
        window_summary=windows["Main perturbation interval"],
        project_status_path=paths.suf_root / "docs" / "project-status.md",
        i_summary_path=paths.nz_route_root / "first-pass-i-summary.md",
        seed_readout_path=paths.nz_route_root / "first-pass-seed-readout.md",
        window_comparison_path=paths.nz_route_root / "first-pass-window-comparison.md",
    )

    output = render_nz_summary_report(
        summary=summary,
        window_summary=windows["Main perturbation interval"],
        validations=validations,
        source_files=[paths.nz_route_root / "event-ledger-seed.md"],
        generated_at="2026-04-02T00:00:00+00:00",
    )

    assert "`30`" in output
    assert "`23`" in output
    assert "- none" in output


def test_nz_window_comparison_report_renders_expected_rows() -> None:
    paths = get_paths()
    events = parse_nz_ledger(paths.nz_route_root / "event-ledger-seed.md")

    output = render_nz_window_report(
        compute_nz_window_summaries(events),
        "2026-04-02T00:00:00+00:00",
        [paths.nz_route_root / "event-ledger-seed.md"],
    )

    assert "Main perturbation interval" in output
    assert "`23`" in output


def test_nz_taiwan_summary_report_renders_expected_rows() -> None:
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
        source_files=[paths.taiwan_route_root / "first-nz-taiwan-comparison-note.md"],
        generated_at="2026-04-02T00:00:00+00:00",
    )

    assert "`6`" in output
    assert "public-information receiving share" in output
    assert "- none" in output
