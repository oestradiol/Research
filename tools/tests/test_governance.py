from __future__ import annotations

import subprocess
import sys

from research_tools.paths import get_paths
from research_tools.validate.governance import (
    validate_current_claims,
    validate_current_surface_hygiene,
    validate_current_surfaces,
    validate_repository_file_registry,
    validate_repository_minimality,
    validate_routing_surfaces,
    validate_merged_doc_quality,
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
