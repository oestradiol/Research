from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from research_tools.models.reports import ValidationResult
from research_tools.parse.subsystems import parse_subsystem_registry
from research_tools.repo_files import iter_truth_files


SUPPORT_SURFACE_BOUNDARY_EXPECTATIONS = {
    "structured-unity-framework/framework/research-program.md": {
        "contains": [
            "It does not replace the theory stack, prove phenomenology from metrics, or claim that one case confirms the whole framework.",
            "It does not freeze one threshold system, one weighting scheme, or one aggregation formula across all future domains.",
            "The package should not imply that current route-local estimators already yield objective cross-domain measurement or mature high-fit prediction.",
        ],
        "absent_patterns": [
            {
                "label": "conclusive-proof-across-all-domains",
                "pattern": r"(?i)\b(?:is|was|has been|already is|already been)\s+conclusively\s+proven\s+across\s+all\s+domains\b",
            },
            {
                "label": "empirically-closed-across-all-future-domains",
                "pattern": r"(?i)\ball\s+future\s+domains\s+(?:are|were|remain|seem|look)\s+already\s+empirically\s+closed\b",
            },
        ],
    },
    "structured-unity-framework/applications/README.md": {
        "contains": [
            "does **not** imply that SUF is already validated across every mapped area.",
            "demonstrated routes",
            "research map",
        ],
        "absent_patterns": [
            {
                "label": "all-applications-empirically-closed",
                "pattern": r"(?i)\ball\s+applications\s+(?:are|were|remain|seem|look)\s+already\s+empirically\s+closed\b",
            },
            {
                "label": "layer-proves-suf-universally",
                "pattern": r"(?i)\bthis\s+layer\s+proves\s+SUF\s+universally\b",
            },
        ],
    },
    "structured-unity-framework/meta/publication-scope.md": {
        "contains": [
            "The package is active, but not empirically closed.",
            "that one demonstrated route proves the framework universally",
            "that the current package already yields objectively settled cross-domain measurement or strong predictive closure",
        ],
        "absent_patterns": [],
    },
}


EDIT_SCOPE_CURRENT_SURFACE_REGISTRIES = [
    "governance/CURRENT_SURFACES_REGISTRY_v0_1.json",
    "structured-unity-framework/governance/CURRENT_SURFACES_REGISTRY_v0_1.json",
]


def _sha256(path: Path) -> str:
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def _safe_read_text(path: Path) -> tuple[str | None, str | None]:
    if not path.exists():
        return None, f"missing file: {path}"
    if not path.is_file():
        return None, f"not a regular file: {path}"
    return path.read_text(encoding="utf-8"), None


def _contains_result(check_name: str, path: Path, needle: str, message: str) -> ValidationResult:
    text, error = _safe_read_text(path)
    if error is not None:
        return ValidationResult(
            check_name=check_name,
            status="fail",
            message=f"{message} Required fragment could not be checked because the file is unavailable.",
            path=str(path),
            expected=needle,
            found=error,
        )
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
    text, error = _safe_read_text(path)
    if error is not None:
        return ValidationResult(
            check_name=check_name,
            status="fail",
            message=f"{message} Forbidden-fragment check could not run because the file is unavailable.",
            path=str(path),
            expected=f"absent: {needle}",
            found=error,
        )
    ok = needle.casefold() not in text.casefold()
    return ValidationResult(
        check_name=check_name,
        status="pass" if ok else "fail",
        message=message if ok else f"{message} Forbidden fragment present.",
        path=str(path),
        expected=f"absent: {needle}",
        found="absent" if ok else needle,
    )


def _absent_pattern_result(check_name: str, path: Path, pattern: str, label: str, message: str) -> ValidationResult:
    text, error = _safe_read_text(path)
    if error is not None:
        return ValidationResult(
            check_name=check_name,
            status="fail",
            message=f"{message} Forbidden-pattern check could not run because the file is unavailable.",
            path=str(path),
            expected=f"absent pattern: {label}",
            found=error,
        )
    match = re.search(pattern, text)
    ok = match is None
    return ValidationResult(
        check_name=check_name,
        status="pass" if ok else "fail",
        message=message if ok else f"{message} Forbidden pattern present.",
        path=str(path),
        expected=f"absent pattern: {label}",
        found="absent" if ok else match.group(0),
    )


def _actual_file_list(repo_root: Path) -> list[str]:
    return iter_truth_files(repo_root)


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


def validate_subsystem_registry(repo_root: Path) -> list[ValidationResult]:
    registry_path = repo_root / "governance" / "SUBSYSTEM_REGISTRY_v0_1.json"
    try:
        subsystems = parse_subsystem_registry(registry_path)
    except Exception as exc:
        return [
            ValidationResult(
                check_name="subsystem-registry-parse",
                status="fail",
                message="Subsystem registry could not be parsed.",
                path=str(registry_path),
                expected="valid subsystem registry JSON",
                found=str(exc),
            )
        ]

    results: list[ValidationResult] = []
    subsystem_ids = [subsystem.subsystem_id for subsystem in subsystems]
    duplicate_subsystems = sorted(
        subsystem_id
        for subsystem_id, count in Counter(subsystem_ids).items()
        if count > 1
    )
    results.append(
        ValidationResult(
            check_name="subsystem-ids-unique",
            status="pass" if not duplicate_subsystems else "fail",
            message=(
                "Subsystem registry uses unique subsystem ids."
                if not duplicate_subsystems
                else "Subsystem registry reuses subsystem ids."
            ),
            path=str(registry_path),
            expected="unique subsystem ids",
            found="ok" if not duplicate_subsystems else ", ".join(duplicate_subsystems),
        )
    )

    cluster_ids = [
        subsystem.validation_cluster.cluster_id
        for subsystem in subsystems
        if subsystem.validation_cluster is not None
    ]
    duplicate_clusters = sorted(
        cluster_id for cluster_id, count in Counter(cluster_ids).items() if count > 1
    )
    results.append(
        ValidationResult(
            check_name="subsystem-cluster-ids-unique",
            status="pass" if not duplicate_clusters else "fail",
            message=(
                "Subsystem registry uses unique validation cluster ids."
                if not duplicate_clusters
                else "Subsystem registry reuses validation cluster ids."
            ),
            path=str(registry_path),
            expected="unique cluster ids",
            found="ok" if not duplicate_clusters else ", ".join(duplicate_clusters),
        )
    )

    missing_entry_surfaces = [
        subsystem.entry_surface
        for subsystem in subsystems
        if not (repo_root / subsystem.entry_surface).exists()
    ]
    results.append(
        ValidationResult(
            check_name="subsystem-entry-surfaces-exist",
            status="pass" if not missing_entry_surfaces else "fail",
            message=(
                "Subsystem entry surfaces exist."
                if not missing_entry_surfaces
                else "Subsystem registry references missing entry surfaces."
            ),
            path=str(registry_path),
            expected="all entry surfaces exist",
            found="ok" if not missing_entry_surfaces else ", ".join(missing_entry_surfaces),
        )
    )

    missing_authoritative_surfaces = [
        subsystem.authoritative_surface
        for subsystem in subsystems
        if not (repo_root / subsystem.authoritative_surface).exists()
    ]
    results.append(
        ValidationResult(
            check_name="subsystem-authoritative-surfaces-exist",
            status="pass" if not missing_authoritative_surfaces else "fail",
            message=(
                "Subsystem authoritative surfaces exist."
                if not missing_authoritative_surfaces
                else "Subsystem registry references missing authoritative surfaces."
            ),
            path=str(registry_path),
            expected="all authoritative surfaces exist",
            found=(
                "ok"
                if not missing_authoritative_surfaces
                else ", ".join(missing_authoritative_surfaces)
            ),
        )
    )

    entry_scope_mismatches = [
        f"{subsystem.subsystem_id}:{subsystem.entry_surface}"
        for subsystem in subsystems
        if not any(
            subsystem.entry_surface.startswith(prefix)
            for prefix in subsystem.scope_prefixes
        )
    ]
    results.append(
        ValidationResult(
            check_name="subsystem-entry-surfaces-in-scope",
            status="pass" if not entry_scope_mismatches else "fail",
            message=(
                "Subsystem entry surfaces stay within declared scope prefixes."
                if not entry_scope_mismatches
                else "Some subsystem entry surfaces fall outside their declared scope."
            ),
            path=str(registry_path),
            expected="entry surfaces within scope prefixes",
            found="ok" if not entry_scope_mismatches else ", ".join(entry_scope_mismatches),
        )
    )

    authoritative_scope_mismatches = [
        f"{subsystem.subsystem_id}:{subsystem.authoritative_surface}"
        for subsystem in subsystems
        if not any(
            subsystem.authoritative_surface.startswith(prefix)
            for prefix in subsystem.scope_prefixes
        )
    ]
    results.append(
        ValidationResult(
            check_name="subsystem-authoritative-surfaces-in-scope",
            status="pass" if not authoritative_scope_mismatches else "fail",
            message=(
                "Subsystem authoritative surfaces stay within declared scope prefixes."
                if not authoritative_scope_mismatches
                else "Some subsystem authoritative surfaces fall outside their declared scope."
            ),
            path=str(registry_path),
            expected="authoritative surfaces within scope prefixes",
            found=(
                "ok"
                if not authoritative_scope_mismatches
                else ", ".join(authoritative_scope_mismatches)
            ),
        )
    )

    missing_cluster_sources = sorted(
        {
            rel
            for subsystem in subsystems
            if subsystem.validation_cluster is not None
            for rel in subsystem.validation_cluster.source_files
            if not (repo_root / rel).exists()
        }
    )
    results.append(
        ValidationResult(
            check_name="subsystem-cluster-source-files-exist",
            status="pass" if not missing_cluster_sources else "fail",
            message=(
                "Subsystem validation-cluster source files exist."
                if not missing_cluster_sources
                else "Subsystem registry references missing validation-cluster source files."
            ),
            path=str(registry_path),
            expected="all validation-cluster source files exist",
            found="ok" if not missing_cluster_sources else ", ".join(missing_cluster_sources),
        )
    )

    nonlocal_cluster_sources = [
        subsystem.subsystem_id
        for subsystem in subsystems
        if subsystem.validation_cluster is not None
        and not any(
            any(rel.startswith(prefix) for prefix in subsystem.scope_prefixes)
            for rel in subsystem.validation_cluster.source_files
        )
    ]
    results.append(
        ValidationResult(
            check_name="subsystem-clusters-include-local-sources",
            status="pass" if not nonlocal_cluster_sources else "fail",
            message=(
                "Each subsystem validation cluster includes at least one local-scope source file."
                if not nonlocal_cluster_sources
                else "Some subsystem validation clusters do not include any local-scope source files."
            ),
            path=str(registry_path),
            expected="each cluster includes at least one source file in local scope",
            found="ok" if not nonlocal_cluster_sources else ", ".join(nonlocal_cluster_sources),
        )
    )

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
        if path.is_dir() and path.name in {'__pycache__', '.mypy_cache', '.pytest_cache', '.ruff_cache'}
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
            check_name='operational-artifacts-ignored',
            status='pass',
            message='Operational cache artifacts are excluded from repository-truth minimality checks.' if transient_dirs or transient_files else 'No operational cache artifacts detected during minimality checks.',
            path=str(repo_root),
            expected='operational artifacts are ignored or absent',
            found='none detected' if not transient_dirs and not transient_files else f'ignored dirs={transient_dirs}; ignored files={transient_files}',
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
    results.extend(validate_support_surface_boundaries(repo_root))
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
            text, error = _safe_read_text(path)
            if error is not None:
                results.append(ValidationResult(
                    check_name=f'{prefix}-surface-hygiene:{rel}',
                    status='fail',
                    message='Current surface hygiene could not be checked because the file is unavailable.',
                    path=str(path),
                    expected='no stale wrapper fragments',
                    found=error,
                ))
                continue
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


def validate_support_surface_boundaries(repo_root: Path) -> list[ValidationResult]:
    results: list[ValidationResult] = []
    for rel, expectations in SUPPORT_SURFACE_BOUNDARY_EXPECTATIONS.items():
        path = repo_root / rel
        for needle in expectations.get('contains', []):
            results.append(_contains_result(
                f'support-boundary-present:{rel}:{needle[:32]}',
                path,
                needle,
                'Support surface preserves an explicit bounded-scope boundary anchor.',
            ))
        for needle in expectations.get('absent', []):
            results.append(_absent_result(
                f'support-boundary-absent:{rel}:{needle[:32]}',
                path,
                needle,
                'Support surface stays free of known absolute-closure or universal-proof overclaims.',
            ))
        for item in expectations.get('absent_patterns', []):
            results.append(_absent_pattern_result(
                f"support-boundary-absent-pattern:{rel}:{item['label']}",
                path,
                item['pattern'],
                item['label'],
                'Support surface stays free of known absolute-closure or universal-proof overclaims.',
            ))
    return results



def _canonicalize_repo_relative_path(path: str) -> str | None:
    candidate = Path(path)
    if candidate.is_absolute():
        return None

    parts: list[str] = []
    for part in candidate.parts:
        if part in ('', '.'):
            continue
        if part == '..':
            if not parts:
                return None
            parts.pop()
            continue
        parts.append(part)

    if not parts:
        return None
    return Path(*parts).as_posix()



def _canonicalize_repo_relative_paths(paths: set[str] | list[str]) -> set[str]:
    canonical: set[str] = set()
    for path in paths:
        normalized = _canonicalize_repo_relative_path(path)
        if normalized is not None:
            canonical.add(normalized)
    return canonical



def _load_current_surface_paths(repo_root: Path) -> set[str]:
    current: set[str] = set()
    for rel in EDIT_SCOPE_CURRENT_SURFACE_REGISTRIES:
        registry = _read_json(repo_root / rel)
        current.update(registry.get("current_files", []))
    return _canonicalize_repo_relative_paths(current)



def _normalize_scope_prefixes(prefixes: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    normalized: list[str] = []
    for prefix in prefixes:
        canonical = _canonicalize_repo_relative_path(prefix)
        if canonical is None:
            continue
        normalized.append(canonical.rstrip('/') + '/')
    return tuple(sorted(set(normalized)))



def _path_matches_prefix(path: str, prefix: str) -> bool:
    return path == prefix[:-1] or path.startswith(prefix)



def _authorize_edit_path(
    path: str,
    *,
    always_files: set[str],
    declared_files: set[str],
    always_prefixes: tuple[str, ...],
    declared_prefixes: tuple[str, ...],
) -> dict[str, str | bool]:
    canonical_path = _canonicalize_repo_relative_path(path)
    if canonical_path is None:
        return {
            'raw_path': path,
            'canonical_path': '',
            'editable': False,
            'reason': 'invalid-path',
            'matched_scope': '',
        }

    if canonical_path in always_files:
        return {
            'raw_path': path,
            'canonical_path': canonical_path,
            'editable': True,
            'reason': 'always-file',
            'matched_scope': canonical_path,
        }
    if canonical_path in declared_files:
        return {
            'raw_path': path,
            'canonical_path': canonical_path,
            'editable': True,
            'reason': 'declared-file',
            'matched_scope': canonical_path,
        }
    for prefix in always_prefixes:
        if _path_matches_prefix(canonical_path, prefix):
            return {
                'raw_path': path,
                'canonical_path': canonical_path,
                'editable': True,
                'reason': 'always-prefix',
                'matched_scope': prefix,
            }
    for prefix in declared_prefixes:
        if _path_matches_prefix(canonical_path, prefix):
            return {
                'raw_path': path,
                'canonical_path': canonical_path,
                'editable': True,
                'reason': 'declared-prefix',
                'matched_scope': prefix,
            }
    return {
        'raw_path': path,
        'canonical_path': canonical_path,
        'editable': False,
        'reason': 'out-of-scope',
        'matched_scope': '',
    }



def validate_edit_scope(repo_root: Path) -> list[ValidationResult]:
    policy_path = repo_root / 'governance' / 'AGENT_EDIT_SCOPE_POLICY_v0_1.json'
    baseline_path = repo_root / 'governance' / 'REPOSITORY_EDIT_BASELINE_v0_1.json'

    policy = _read_json(policy_path)
    baseline = _read_json(baseline_path)

    excluded_from_baseline = set(policy.get('excluded_from_baseline', [])) | {baseline_path.relative_to(repo_root).as_posix()}
    baseline_entries = {entry['path']: entry['sha256'] for entry in baseline.get('files', []) if entry['path'] not in excluded_from_baseline}
    actual_files = [rel for rel in _actual_file_list(repo_root) if rel not in excluded_from_baseline]
    actual_hashes = {rel: _sha256(repo_root / rel) for rel in actual_files}

    current_surface_files = _load_current_surface_paths(repo_root) if policy.get('include_current_surfaces', False) else set()
    always_files = current_surface_files | _canonicalize_repo_relative_paths(policy.get('always_allowed_files', []))
    declared_files = _canonicalize_repo_relative_paths(policy.get('declared_allowed_files', []))
    always_prefixes = _normalize_scope_prefixes(policy.get('always_allowed_prefixes', []))
    declared_prefixes = _normalize_scope_prefixes(policy.get('declared_allowed_prefixes', []))

    changed_entries: list[dict[str, str]] = []
    for rel, sha in sorted(actual_hashes.items()):
        baseline_sha = baseline_entries.get(rel)
        if baseline_sha is None:
            changed_entries.append({'path': rel, 'change': 'new-file'})
        elif baseline_sha != sha:
            changed_entries.append({'path': rel, 'change': 'modified'})
    for rel in sorted(set(baseline_entries) - set(actual_hashes)):
        changed_entries.append({'path': rel, 'change': 'removed'})

    out_of_scope = []
    for entry in changed_entries:
        decision = _authorize_edit_path(
            entry['path'],
            always_files=always_files,
            declared_files=declared_files,
            always_prefixes=always_prefixes,
            declared_prefixes=declared_prefixes,
        )
        if not decision['editable']:
            canonical = decision['canonical_path'] or entry['path']
            out_of_scope.append(f"{entry['change']}:{canonical}")

    declared_targets = sorted(declared_files) + sorted(declared_prefixes)
    results = [
        ValidationResult(
            check_name='edit-scope-baseline-readable',
            status='pass' if baseline_entries else 'fail',
            message='Repository edit baseline is present and readable.' if baseline_entries else 'Repository edit baseline is missing or empty.',
            path=str(baseline_path),
            expected='baseline file entries available',
            found=str(len(baseline_entries)),
        ),
        ValidationResult(
            check_name='edit-scope-policy-readable',
            status='pass',
            message='Agent edit scope policy is present and readable.',
            path=str(policy_path),
            expected='policy file readable',
            found='ok',
        ),
        ValidationResult(
            check_name='edit-scope-changes-within-policy',
            status='pass' if not out_of_scope else 'fail',
            message='All files changed relative to the review baseline stay within current surfaces, designated work surfaces, or declared scope.' if not out_of_scope else 'Some files changed relative to the review baseline fall outside current surfaces, designated work surfaces, and declared scope.',
            path=str(policy_path),
            expected='all changed files within allowed scope',
            found='ok' if not out_of_scope else '; '.join(out_of_scope[:50]),
        ),
        ValidationResult(
            check_name='edit-scope-declared-scope-empty-or-explicit',
            status='pass',
            message='Declared edit scope remains explicit; empty means no exceptional paths are currently authorized.',
            path=str(policy_path),
            expected='explicit exceptional scope declaration',
            found='none' if not declared_targets else '; '.join(declared_targets),
        ),
    ]
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
        text, error = _safe_read_text(path)
        if error is not None:
            results.append(ValidationResult(
                check_name=f'merged-doc-quality:{rel}',
                status='fail',
                message='Merged document quality could not be checked because the file is unavailable.',
                path=str(path),
                expected='required headings present; no consolidation residue',
                found=error,
            ))
            continue
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
