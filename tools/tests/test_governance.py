from __future__ import annotations

import subprocess
import sys

from research_tools.paths import get_paths
from research_tools.validate.governance import (
    _authorize_edit_path,
    _canonicalize_repo_relative_path,
    validate_current_claims,
    validate_current_surface_hygiene,
    validate_current_surfaces,
    validate_support_surface_boundaries,
    validate_repository_file_registry,
    validate_repository_minimality,
    validate_routing_surfaces,
    validate_merged_doc_quality,
    validate_edit_scope,
)


def _cleanup_transients(repo_root):
    for path in sorted(repo_root.rglob('*')):
        if path.is_dir() and path.name in {'__pycache__', '.pytest_cache'}:
            import shutil; shutil.rmtree(path)
    for path in sorted(repo_root.rglob('*.pyc')):
        path.unlink()


def test_governance_validations_pass() -> None:
    repo_root = get_paths().research_root
    _cleanup_transients(repo_root)
    results = []
    results.extend(validate_current_surfaces(repo_root))
    results.extend(validate_repository_file_registry(repo_root))
    results.extend(validate_current_claims(repo_root))
    results.extend(validate_repository_minimality(repo_root))
    results.extend(validate_routing_surfaces(repo_root))
    results.extend(validate_merged_doc_quality(repo_root))
    results.extend(validate_edit_scope(repo_root))
    assert not [result for result in results if result.status == 'fail']


def test_package_doctor_passes() -> None:
    repo_root = get_paths().research_root
    _cleanup_transients(repo_root)
    run = subprocess.run([sys.executable, str(repo_root / 'package_doctor.py')], capture_output=True, text=True)
    assert run.returncode == 0, run.stdout + run.stderr


def test_current_surface_hygiene_catches_stale_wrapper_fragment(tmp_path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "governance").mkdir(parents=True)
    (repo / "structured-unity-framework" / "governance").mkdir(parents=True)
    bad = repo / "bad.md"
    bad.write_text("see docs/state/PROJECT_STATUS.md\n", encoding="utf-8")
    root_registry = {"current_files": ["bad.md"], "live_entrypoints": ["bad.md"]}
    suf_registry = {"current_files": [], "live_entrypoints": []}
    import json
    (repo / "governance" / "CURRENT_SURFACES_REGISTRY_v0_1.json").write_text(json.dumps(root_registry), encoding="utf-8")
    (repo / "structured-unity-framework" / "governance" / "CURRENT_SURFACES_REGISTRY_v0_1.json").write_text(json.dumps(suf_registry), encoding="utf-8")

    results = validate_current_surface_hygiene(repo)

    assert any(result.status == "fail" for result in results)


def test_routing_surfaces_catch_orphan(tmp_path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "governance").mkdir(parents=True)
    (repo / "structured-unity-framework" / "governance").mkdir(parents=True)
    (repo / "README.md").write_text("root only\n", encoding="utf-8")
    (repo / "START_HERE.md").write_text("root only\n", encoding="utf-8")
    (repo / "docs" / "frontdoor").mkdir(parents=True)
    (repo / "docs" / "frontdoor" / "PROJECT_PURPOSE_AND_USE_CASES.md").write_text("purpose\n", encoding="utf-8")
    (repo / "docs" / "frontdoor" / "CONTROL_AND_GOVERNANCE_SURFACE.md").write_text("control\n", encoding="utf-8")
    (repo / "governance" / "AUTHORITATIVE_INDEX_v0_1.md").write_text("index\n", encoding="utf-8")
    (repo / "orphan.md").write_text("current but unreachable\n", encoding="utf-8")
    import json
    (repo / "governance" / "CURRENT_SURFACES_REGISTRY_v0_1.json").write_text(json.dumps({"current_files": ["README.md", "START_HERE.md", "docs/frontdoor/PROJECT_PURPOSE_AND_USE_CASES.md", "docs/frontdoor/CONTROL_AND_GOVERNANCE_SURFACE.md", "governance/AUTHORITATIVE_INDEX_v0_1.md", "orphan.md"], "live_entrypoints": ["README.md"]}), encoding="utf-8")
    (repo / "structured-unity-framework" / "governance" / "CURRENT_SURFACES_REGISTRY_v0_1.json").write_text(json.dumps({"current_files": [], "live_entrypoints": []}), encoding="utf-8")

    results = validate_routing_surfaces(repo)

    assert any(result.status == "fail" for result in results)


def test_merged_doc_quality_catches_residue(tmp_path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    from research_tools.validate.governance import MERGED_DOC_EXPECTATIONS
    for rel in MERGED_DOC_EXPECTATIONS:
        p2 = repo / rel
        p2.parent.mkdir(parents=True, exist_ok=True)
        p2.write_text("# placeholder\n## Table of contents\n## Provenance\n", encoding="utf-8")
    bad = repo / "structured-unity-framework" / "docs" / "argument" / "CONTRIBUTION_AND_POSITIONING.md"
    bad.write_text("# Contribution\n## Source surfaces preserved here\n", encoding="utf-8")

    results = validate_merged_doc_quality(repo)

    assert any(result.status == "fail" for result in results)


def test_support_surface_boundaries_catch_overclaim(tmp_path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    target = repo / "structured-unity-framework" / "framework" / "research-program.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        "# Research Program\nThis package is conclusively proven across all domains.\n",
        encoding="utf-8",
    )
    (repo / "structured-unity-framework" / "applications").mkdir(parents=True, exist_ok=True)
    (repo / "structured-unity-framework" / "applications" / "README.md").write_text(
        "# Applications Atlas\nThis layer does **not** imply that SUF is already validated across every mapped area.\n demonstrated routes\n research map\n",
        encoding="utf-8",
    )
    (repo / "structured-unity-framework" / "meta").mkdir(parents=True, exist_ok=True)
    (repo / "structured-unity-framework" / "meta" / "publication-scope.md").write_text(
        "# Publication Scope\nThe package is active, but not empirically closed.\nthat one demonstrated route proves the framework universally\nthat the current package already yields objectively settled cross-domain measurement or strong predictive closure\n",
        encoding="utf-8",
    )

    results = validate_support_surface_boundaries(repo)

    assert any(result.status == "fail" for result in results)


def test_merged_doc_quality_missing_file_fails_cleanly(tmp_path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()

    results = validate_merged_doc_quality(repo)

    assert all(result.status == "fail" for result in results)
    assert all("unavailable" in result.message for result in results)


def test_support_surface_boundary_regex_avoids_negation_false_positive(tmp_path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    target = repo / "structured-unity-framework" / "framework" / "research-program.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        """# Research Program
It does not replace the theory stack, prove phenomenology from metrics, or claim that one case confirms the whole framework.
It does not freeze one threshold system, one weighting scheme, or one aggregation formula across all future domains.
The package should not imply that current route-local estimators already yield objective cross-domain measurement or mature high-fit prediction.
It is not ready for broad deployment, and this does not generalize broadly.
""",
        encoding="utf-8",
    )
    (repo / "structured-unity-framework" / "applications").mkdir(parents=True, exist_ok=True)
    (repo / "structured-unity-framework" / "applications" / "README.md").write_text(
        """# Applications Atlas
This layer does **not** imply that SUF is already validated across every mapped area.
demonstrated routes
research map
""",
        encoding="utf-8",
    )
    (repo / "structured-unity-framework" / "meta").mkdir(parents=True, exist_ok=True)
    (repo / "structured-unity-framework" / "meta" / "publication-scope.md").write_text(
        """# Publication Scope
The package is active, but not empirically closed.
that one demonstrated route proves the framework universally
that the current package already yields objectively settled cross-domain measurement or strong predictive closure
""",
        encoding="utf-8",
    )

    results = validate_support_surface_boundaries(repo)

    assert not [result for result in results if result.status == "fail"]


def test_edit_scope_catches_out_of_scope_existing_file_change(tmp_path) -> None:
    import shutil
    import json
    import hashlib

    source = get_paths().research_root
    repo = tmp_path / "repo"
    shutil.copytree(source, repo)
    target = repo / "structured-unity-framework" / "meta" / "weak-naturalization.md"
    target.write_text(target.read_text(encoding="utf-8") + "\nThis proves SUF universally.\n", encoding="utf-8")

    results = validate_edit_scope(repo)

    assert any(result.check_name == "edit-scope-changes-within-policy" and result.status == "fail" for result in results)


def test_edit_scope_allows_current_surface_change(tmp_path) -> None:
    import shutil

    source = get_paths().research_root
    repo = tmp_path / "repo"
    shutil.copytree(source, repo)
    target = repo / "README.md"
    target.write_text(target.read_text(encoding="utf-8") + "\nTemporary current-surface wording update.\n", encoding="utf-8")

    results = validate_edit_scope(repo)

    assert not any(result.check_name == "edit-scope-changes-within-policy" and result.status == "fail" for result in results)


def test_edit_scope_allows_designated_tooling_change(tmp_path) -> None:
    import shutil

    source = get_paths().research_root
    repo = tmp_path / "repo"
    shutil.copytree(source, repo)
    target = repo / "tools" / "README.md"
    target.write_text(target.read_text(encoding="utf-8") + "\nTemporary tooling note.\n", encoding="utf-8")

    results = validate_edit_scope(repo)

    assert not any(result.check_name == "edit-scope-changes-within-policy" and result.status == "fail" for result in results)


def test_canonicalize_repo_relative_path_normalizes_aliases() -> None:
    assert _canonicalize_repo_relative_path('./tools//../tools/README.md') == 'tools/README.md'
    assert _canonicalize_repo_relative_path('governance/./CURRENT_SURFACES_REGISTRY_v0_1.json') == 'governance/CURRENT_SURFACES_REGISTRY_v0_1.json'


def test_canonicalize_repo_relative_path_rejects_escape() -> None:
    assert _canonicalize_repo_relative_path('../README.md') is None
    assert _canonicalize_repo_relative_path('../../tools/README.md') is None


def test_authorize_edit_path_uses_canonical_aliases_consistently() -> None:
    decision = _authorize_edit_path(
        './tools//../tools/README.md',
        always_files=set(),
        declared_files=set(),
        always_prefixes=('tools/',),
        declared_prefixes=(),
    )

    assert decision['editable'] is True
    assert decision['canonical_path'] == 'tools/README.md'
    assert decision['reason'] == 'always-prefix'


def test_authorize_edit_path_rejects_prefix_near_miss() -> None:
    decision = _authorize_edit_path(
        'toolshed/README.md',
        always_files=set(),
        declared_files=set(),
        always_prefixes=('tools/',),
        declared_prefixes=(),
    )

    assert decision['editable'] is False
    assert decision['reason'] == 'out-of-scope'
