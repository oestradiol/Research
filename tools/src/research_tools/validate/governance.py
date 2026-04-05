from __future__ import annotations

import json
from pathlib import Path

from research_tools.models.reports import ValidationResult


ROUTING_SURFACES = {
    "root": [
        "README.md",
        "START_HERE.md",
        "docs/frontdoor/PROJECT_PURPOSE_AND_USE_CASES.md",
        "docs/frontdoor/CONTROL_AND_GOVERNANCE_SURFACE.md",
        "governance/AUTHORITATIVE_INDEX_v0_1.md",
    ],
    "suf": [
        "structured-unity-framework/README.md",
        "structured-unity-framework/START_HERE.md",
        "structured-unity-framework/docs/INDEX.md",
        "structured-unity-framework/docs/frontdoor/PROJECT_PURPOSE_AND_USE_CASES.md",
        "structured-unity-framework/docs/frontdoor/CONTROL_AND_GOVERNANCE_SURFACE.md",
        "structured-unity-framework/docs/frontdoor/SCIENTIFIC_GROUNDING_AND_LIMITS.md",
        "structured-unity-framework/governance/AUTHORITATIVE_INDEX_v0_1.md",
    ],
}

MERGED_DOC_EXPECTATIONS = {
    "docs/frontdoor/CONTROL_AND_GOVERNANCE_SURFACE.md": [
        "## Table of contents",
        "## Skeptical audit",
        "## Trust and style",
        "## Provenance",
    ],
    "structured-unity-framework/docs/frontdoor/CONTROL_AND_GOVERNANCE_SURFACE.md": [
        "## Table of contents",
        "## Skeptical audit",
        "## Trust and style",
        "## Provenance",
    ],
    "structured-unity-framework/docs/frontdoor/SCIENTIFIC_GROUNDING_AND_LIMITS.md": [
        "## Table of contents",
        "## Detailed limits surfaces",
        "## Provenance",
    ],
    "structured-unity-framework/docs/orientation/FRAMEWORK_OVERVIEW_AND_READING_GUIDE.md": [
        "## Table of contents",
        "## Reader paths",
        "## Reading and audit paths",
        "## Provenance",
    ],
    "structured-unity-framework/docs/argument/CONTRIBUTION_AND_POSITIONING.md": [
        "## Table of contents",
        "## Locked payoff and contribution candidates",
        "## Bounded rival positioning",
        "## Provenance",
    ],
    "structured-unity-framework/docs/audit/OBJECTIONS_AND_EVIDENCE_STATUS.md": [
        "## Table of contents",
        "## Reviewer objections and current answers",
        "## Evidence-status matrix role",
        "## Provenance",
    ],
    "structured-unity-framework/docs/monograph/MONOGRAPH_SUPPORT_PACKAGE.md": [
        "## Table of contents",
        "## Monograph chapter scaffold",
        "## Bounded closure note",
        "## Provenance",
    ],
}


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _contains_result(check_name: str, path: Path, needle: str, message: str) -> ValidationResult:
    text = path.read_text(encoding="utf-8")
    ok = needle in text
    return ValidationResult(
        check_name=check_name,
        status="pass" if ok else "fail",
        message=message if ok else f"{message} Required fragment missing.",
        path=str(path),
        expected=needle,
        found=needle if ok else "missing",
    )


def _absent_result(check_name: str, path: Path, needle: str, message: str) -> ValidationResult:
    text = path.read_text(encoding="utf-8")
    ok = needle not in text
    return ValidationResult(
        check_name=check_name,
        status="pass" if ok else "fail",
        message=message if ok else f"{message} Forbidden fragment present.",
        path=str(path),
        expected=f"absent: {needle}",
        found="absent" if ok else needle,
    )


def _actual_file_list(repo_root: Path) -> list[str]:
    files: list[str] = []
    for path in sorted(repo_root.rglob('*')):
        if not path.is_file():
            continue
        rel = path.relative_to(repo_root).as_posix()
        if '/__pycache__/' in f'/{rel}/' or '/.pytest_cache/' in f'/{rel}/' or rel.endswith('.pyc'):
            continue
        files.append(rel)
    return files


def validate_current_surfaces(repo_root: Path) -> list[ValidationResult]:
    results: list[ValidationResult] = []
    root_registry_path = repo_root / 'governance' / 'CURRENT_SURFACES_REGISTRY_v0_1.json'
    suf_registry_path = repo_root / 'structured-unity-framework' / 'governance' / 'CURRENT_SURFACES_REGISTRY_v0_1.json'
    for registry_path, prefix in ((root_registry_path, 'root'), (suf_registry_path, 'suf')):
        registry = _read_json(registry_path)
        current_files = registry.get('current_files', [])
        missing = [rel for rel in current_files if not (repo_root / rel).exists()]
        results.append(ValidationResult(
            check_name=f'{prefix}-current-surfaces-exist',
            status='pass' if not missing else 'fail',
            message='All current surfaces listed in the registry exist.' if not missing else 'Current surfaces registry references missing files.',
            path=str(registry_path),
            expected='all listed current files exist',
            found='none missing' if not missing else ', '.join(missing),
        ))
        live_entrypoints = registry.get('live_entrypoints', [])
        missing_entrypoints = [rel for rel in live_entrypoints if rel not in current_files]
        results.append(ValidationResult(
            check_name=f'{prefix}-entrypoints-subset-of-current',
            status='pass' if not missing_entrypoints else 'fail',
            message='Live entrypoints are also marked current.' if not missing_entrypoints else 'Some live entrypoints are not marked current.',
            path=str(registry_path),
            expected='live_entrypoints subset of current_files',
            found='ok' if not missing_entrypoints else ', '.join(missing_entrypoints),
        ))
    return results


def validate_repository_file_registry(repo_root: Path) -> list[ValidationResult]:
    results: list[ValidationResult] = []
    for registry_path, prefix in ((repo_root / 'governance' / 'REPOSITORY_FILE_REGISTRY_v0_1.json', 'root'), (repo_root / 'structured-unity-framework' / 'governance' / 'REPOSITORY_FILE_REGISTRY_v0_1.json', 'suf')):
        registry = _read_json(registry_path)
        scope_prefix = registry['scope_prefix']
        actual = [rel for rel in _actual_file_list(repo_root) if rel.startswith(scope_prefix)]
        registered = sorted(entry['path'] for entry in registry['files'])
        missing = sorted(set(actual) - set(registered))
        extra = sorted(set(registered) - set(actual))
        results.append(ValidationResult(
            check_name=f'{prefix}-file-registry-coverage',
            status='pass' if not missing and not extra else 'fail',
            message='Repository file registry matches the actual file set in scope.' if not missing and not extra else 'Repository file registry does not match the actual file set in scope.',
            path=str(registry_path),
            expected='full coverage with no extras',
            found=('ok' if not missing and not extra else f'missing={missing}; extra={extra}'),
        ))
    return results


def validate_repository_minimality(repo_root: Path) -> list[ValidationResult]:
    allow = _read_json(repo_root / 'governance' / 'ROOT_ALLOWLIST_v0_1.json')
    allowed = set(allow['allowed_root_files'])
    actual_root_files = sorted(p.name for p in repo_root.iterdir() if p.is_file())
    forbidden = [name for name in actual_root_files if name not in allowed]

    transient_dirs = sorted(
        path.relative_to(repo_root).as_posix()
        for path in repo_root.rglob('*')
        if path.is_dir() and path.name in {'__pycache__', '.pytest_cache'}
    )
    transient_files = sorted(
        path.relative_to(repo_root).as_posix()
        for path in repo_root.rglob('*')
        if path.is_file() and (path.suffix == '.pyc' or path.name == '.DS_Store')
    )

    return [
        ValidationResult(
            check_name='root-allowlist',
            status='pass' if not forbidden else 'fail',
            message='Root file set respects the explicit allowlist.' if not forbidden else 'Root contains files outside the explicit allowlist.',
            path=str(repo_root / 'governance' / 'ROOT_ALLOWLIST_v0_1.json'),
            expected='all root files allowlisted',
            found='ok' if not forbidden else ', '.join(forbidden),
        ),
        ValidationResult(
            check_name='transient-artifacts-absent',
            status='pass' if not transient_dirs and not transient_files else 'fail',
            message='Transient cache artifacts are absent from the repository tree.' if not transient_dirs and not transient_files else 'Transient cache artifacts are present in the repository tree.',
            path=str(repo_root),
            expected='no __pycache__, .pytest_cache, .pyc, or .DS_Store artifacts',
            found='ok' if not transient_dirs and not transient_files else f'dirs={transient_dirs}; files={transient_files}',
        ),
    ]


def validate_current_claims(repo_root: Path) -> list[ValidationResult]:
    results: list[ValidationResult] = []
    for expectations_path in (
        repo_root / 'governance' / 'CURRENT_CLAIM_EXPECTATIONS_v0_1.json',
        repo_root / 'structured-unity-framework' / 'governance' / 'CURRENT_CLAIM_EXPECTATIONS_v0_1.json',
    ):
        data = _read_json(expectations_path)
        for item in data.get('contains', []):
            path = repo_root / item['path']
            results.append(_contains_result(item['check_name'], path, item['needle'], item['message']))
        for item in data.get('absent', []):
            path = repo_root / item['path']
            results.append(_absent_result(item['check_name'], path, item['needle'], item['message']))
    results.extend(validate_current_surface_hygiene(repo_root))
    return results


def validate_current_surface_hygiene(repo_root: Path) -> list[ValidationResult]:
    forbidden_fragments = [
        'docs/state/PROJECT_STATUS.md',
        'docs/state/CURRENT_EXECUTION_ORDER.md',
        'docs/state/PENDING_INVENTORY.md',
        'CURRENT_OPERATOR_START_HERE.md',
        'PACKAGE_ENFORCEMENT_LAYER_v0_1.md',
    ]
    results: list[ValidationResult] = []
    seen: set[str] = set()
    for registry_path, prefix in (
        (repo_root / 'governance' / 'CURRENT_SURFACES_REGISTRY_v0_1.json', 'root'),
        (repo_root / 'structured-unity-framework' / 'governance' / 'CURRENT_SURFACES_REGISTRY_v0_1.json', 'suf'),
    ):
        registry = _read_json(registry_path)
        for rel in registry.get('current_files', []):
            if rel in seen:
                continue
            seen.add(rel)
            path = repo_root / rel
            if not path.exists() or path.suffix not in {'.md', '.json', '.py'}:
                continue
            text = path.read_text(encoding='utf-8')
            bad = [frag for frag in forbidden_fragments if frag in text]
            results.append(ValidationResult(
                check_name=f'{prefix}-surface-hygiene:{rel}',
                status='pass' if not bad else 'fail',
                message='Current surface is free of known stale wrapper fragments.' if not bad else 'Current surface still contains stale wrapper fragments.',
                path=str(path),
                expected='no stale wrapper fragments',
                found='ok' if not bad else ', '.join(bad),
            ))
    return results


def validate_routing_surfaces(repo_root: Path) -> list[ValidationResult]:
    results: list[ValidationResult] = []
    registries = {
        'root': _read_json(repo_root / 'governance' / 'CURRENT_SURFACES_REGISTRY_v0_1.json'),
        'suf': _read_json(repo_root / 'structured-unity-framework' / 'governance' / 'CURRENT_SURFACES_REGISTRY_v0_1.json'),
    }
    for scope, registry in registries.items():
        routing_paths = [repo_root / rel for rel in ROUTING_SURFACES[scope]]
        routing_text = '\n'.join(path.read_text(encoding='utf-8') for path in routing_paths if path.exists())
        scope_prefix = 'structured-unity-framework/' if scope == 'suf' else ''
        orphans = []
        for rel in registry.get('current_files', []):
            if rel in ROUTING_SURFACES[scope]:
                continue
            candidates = {rel, Path(rel).name}
            if scope_prefix and rel.startswith(scope_prefix):
                candidates.add(rel[len(scope_prefix):])
            if not any(candidate in routing_text for candidate in candidates):
                orphans.append(rel)
        results.append(ValidationResult(
            check_name=f'{scope}-routing-coverage',
            status='pass' if not orphans else 'fail',
            message='Every current file is reachable from at least one current routing surface.' if not orphans else 'Some current files are orphaned from current routing surfaces.',
            path=', '.join(str(p) for p in routing_paths),
            expected='all current files referenced by current routing surfaces',
            found='ok' if not orphans else ', '.join(orphans),
        ))
    return results


def validate_merged_doc_quality(repo_root: Path) -> list[ValidationResult]:
    results: list[ValidationResult] = []
    forbidden_fragments = [
        '## Source surfaces preserved here',
        '## Preserved source:',
        'This file preserves and consolidates the material from the source surfaces listed below.',
    ]
    for rel, required in MERGED_DOC_EXPECTATIONS.items():
        path = repo_root / rel
        text = path.read_text(encoding='utf-8')
        missing = [frag for frag in required if frag not in text]
        bad = [frag for frag in forbidden_fragments if frag in text]
        results.append(ValidationResult(
            check_name=f'merged-doc-quality:{rel}',
            status='pass' if not missing and not bad else 'fail',
            message='Merged document keeps navigation headings and clean consolidation prose.' if not missing and not bad else 'Merged document is missing navigation headings or still contains consolidation residue.',
            path=str(path),
            expected='required headings present; no consolidation residue',
            found='ok' if not missing and not bad else f'missing={missing}; residue={bad}',
        ))
    return results
