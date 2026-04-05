from __future__ import annotations

import json
import os
import sys
import shutil
from pathlib import Path

from authoritative_guard import AuthorityError, verify_integrity

BASE = Path(__file__).resolve().parent
TOOLS_SRC = BASE / "tools" / "src"
if str(TOOLS_SRC) not in sys.path:
    sys.path.insert(0, str(TOOLS_SRC))

from research_tools.paths import get_paths  # noqa: E402
from research_tools.validate.governance import (  # noqa: E402
    validate_current_claims,
    validate_current_surfaces,
    validate_repository_file_registry,
    validate_repository_minimality,
    validate_routing_surfaces,
    validate_merged_doc_quality,
)
from research_tools.workflows.validate_all import collect_validation_results  # noqa: E402



def cleanup_transient_artifacts(base: Path) -> tuple[list[str], list[str]]:
    removed_dirs: list[str] = []
    removed_files: list[str] = []
    for pattern in ('__pycache__', '.pytest_cache'):
        for directory in sorted(base.rglob(pattern)):
            if directory.is_dir():
                shutil.rmtree(directory)
                removed_dirs.append(directory.relative_to(base).as_posix())
    for file_path in sorted(base.rglob('*.pyc')):
        if file_path.is_file():
            file_path.unlink()
            removed_files.append(file_path.relative_to(base).as_posix())
    for file_path in sorted(base.rglob('.DS_Store')):
        if file_path.is_file():
            file_path.unlink()
            removed_files.append(file_path.relative_to(base).as_posix())
    return removed_dirs, removed_files

def main() -> None:
    checks = []
    issues = []

    def record(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"check": name, "ok": ok, "detail": detail})
        if not ok:
            issues.append({"check": name, "detail": detail})

    removed_dirs, removed_files = cleanup_transient_artifacts(BASE)
    remaining_transients = [
        p.relative_to(BASE).as_posix()
        for p in BASE.rglob('*')
        if (p.is_dir() and p.name in {'__pycache__', '.pytest_cache'})
        or (p.is_file() and (p.suffix == '.pyc' or p.name == '.DS_Store'))
    ]
    record(
        'layout:transient-artifacts-clean',
        not remaining_transients,
        f'removed_dirs={removed_dirs} removed_files={removed_files} remaining={remaining_transients}',
    )

    try:
        integrity = verify_integrity(strict=True)
        record("integrity:manifest-pass", integrity["status"] == "PASS", f"verified_files={integrity['verified_files']}")
    except AuthorityError as e:
        record("integrity:manifest-pass", False, str(e))

    for rel in [
        "START_HERE.md",
        "docs/frontdoor/PROJECT_PURPOSE_AND_USE_CASES.md",
        "docs/frontdoor/CONTROL_AND_GOVERNANCE_SURFACE.md",
        "governance/AUTHORITATIVE_INDEX_v0_1.md",
        "structured-unity-framework/START_HERE.md",
        "structured-unity-framework/governance/AUTHORITATIVE_INDEX_v0_1.md",
    ]:
        p = BASE / rel
        record(f"exists:{rel}", p.exists(), "present" if p.exists() else f"missing {rel}")

    os.environ.setdefault("PYTHONPATH", str(TOOLS_SRC))
    paths = get_paths()
    validation_results = collect_validation_results(paths)
    failed_validation = [r for r in validation_results if r.status == "fail"]
    record(
        "tools:validate-all-pass",
        not failed_validation,
        "none" if not failed_validation else "; ".join(f"{r.check_name}:{r.message}" for r in failed_validation[:20]),
    )

    for name, results in [
        ("audit:current-surfaces", validate_current_surfaces(BASE)),
        ("audit:file-registry", validate_repository_file_registry(BASE)),
        ("audit:current-claims", validate_current_claims(BASE)),
        ("audit:minimality", validate_repository_minimality(BASE)),
        ("audit:routing", validate_routing_surfaces(BASE)),
        ("audit:merged-doc-quality", validate_merged_doc_quality(BASE)),
    ]:
        failed = [r for r in results if r.status == "fail"]
        record(name, not failed, "none" if not failed else "; ".join(f"{r.check_name}:{r.message}" for r in failed[:20]))

    status = "PASS" if not issues else "FAIL"
    summary = {
        "doctor_version": "0.2.0",
        "status": status,
        "total_checks": len(checks),
        "passed_checks": sum(1 for c in checks if c["ok"]),
        "failed_checks": sum(1 for c in checks if not c["ok"]),
        "issues": issues,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    sys.exit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
