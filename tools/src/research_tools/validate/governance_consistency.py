"""
Governance consistency validator.

Checks that governance files are internally consistent and reference only existing files.
This closes the self-coverage gap where the system can validate others but not itself.
"""

from pathlib import Path
from typing import List, Dict, Set, Tuple
import json


def load_json(path: Path) -> Dict:
    """Load JSON file safely."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError(f"File not found: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}")


def check_file_exists(path: Path, repo_root: Path) -> Tuple[bool, str]:
    """Check if a file exists in the repository."""
    full_path = repo_root / path
    exists = full_path.exists()
    return exists, str(full_path)


def check_current_surfaces_registry(registry_path: Path, repo_root: Path) -> List[Tuple[str, str]]:
    """
    Check CURRENT_SURFACES_REGISTRY for:
    - All listed files actually exist
    - No stale references to deleted files
    """
    issues = []
    registry = load_json(registry_path)
    
    current_files = registry.get('current_files', [])
    
    for file_ref in current_files:
        exists, full_path = check_file_exists(file_ref, repo_root)
        if not exists:
            issues.append(('missing_file', f"File listed in CURRENT_SURFACES_REGISTRY does not exist: {file_ref}"))
    
    return issues


def check_integrity_manifest(manifest_path: Path, repo_root: Path) -> List[Tuple[str, str]]:
    """
    Check AUTHORITATIVE_INTEGRITY_MANIFEST for:
    - All listed files actually exist
    - No stale references to deleted files
    """
    issues = []
    manifest = load_json(manifest_path)
    
    files = manifest.get('files', [])
    
    for entry in files:
        file_path = entry.get('path')
        if file_path:
            exists, full_path = check_file_exists(file_path, repo_root)
            if not exists:
                issues.append(('missing_file', f"File listed in INTEGRITY_MANIFEST does not exist: {file_path}"))
    
    return issues


def check_repository_file_registry(registry_path: Path, repo_root: Path) -> List[Tuple[str, str]]:
    """
    Check REPOSITORY_FILE_REGISTRY for:
    - All live_files actually exist
    - No stale references to deleted files
    """
    issues = []
    registry = load_json(registry_path)
    
    live_files = registry.get('live_files', [])
    
    for file_ref in live_files:
        exists, full_path = check_file_exists(file_ref, repo_root)
        if not exists:
            issues.append(('missing_file', f"File listed in REPOSITORY_FILE_REGISTRY live_files does not exist: {file_ref}"))
    
    return issues


def check_version_consistency(
    surfaces_path: Path,
    integrity_path: Path,
    file_registry_path: Path
) -> List[Tuple[str, str]]:
    """
    Check that registry versions are consistent.
    After changes, all registries should have matching version numbers.
    """
    issues = []
    
    surfaces = load_json(surfaces_path)
    integrity = load_json(integrity_path)
    file_registry = load_json(file_registry_path)
    
    surfaces_version = surfaces.get('registry_version')
    integrity_version = integrity.get('version')
    file_registry_version = file_registry.get('version')
    
    versions = {
        'CURRENT_SURFACES_REGISTRY': surfaces_version,
        'AUTHORITATIVE_INTEGRITY_MANIFEST': integrity_version,
        'REPOSITORY_FILE_REGISTRY': file_registry_version
    }
    
    # Check if all versions match
    unique_versions = set(v for v in versions.values() if v is not None)
    
    if len(unique_versions) > 1:
        issues.append((
            'version_mismatch',
            f"Registry versions are inconsistent: {versions}"
        ))
    
    return issues


def validate_governance_consistency(repo_root: Path) -> Dict[str, List[Tuple[str, str]]]:
    """
    Run all governance consistency checks.
    
    Returns dict with check names as keys and lists of (issue_type, message) tuples as values.
    """
    results = {}
    
    governance_dir = repo_root / 'governance'
    
    # Check CURRENT_SURFACES_REGISTRY
    surfaces_path = governance_dir / 'CURRENT_SURFACES_REGISTRY_v0_1.json'
    if surfaces_path.exists():
        results['current_surfaces_registry'] = check_current_surfaces_registry(surfaces_path, repo_root)
    else:
        results['current_surfaces_registry'] = [('missing_file', f'CURRENT_SURFACES_REGISTRY not found at {surfaces_path}')]
    
    # Check AUTHORITATIVE_INTEGRITY_MANIFEST
    integrity_path = governance_dir / 'AUTHORITATIVE_INTEGRITY_MANIFEST_v0_1.json'
    if integrity_path.exists():
        results['integrity_manifest'] = check_integrity_manifest(integrity_path, repo_root)
    else:
        results['integrity_manifest'] = [('missing_file', f'INTEGRITY_MANIFEST not found at {integrity_path}')]
    
    # Check REPOSITORY_FILE_REGISTRY
    file_registry_path = governance_dir / 'REPOSITORY_FILE_REGISTRY_v0_1.json'
    if file_registry_path.exists():
        results['file_registry'] = check_repository_file_registry(file_registry_path, repo_root)
    else:
        results['file_registry'] = [('missing_file', f'REPOSITORY_FILE_REGISTRY not found at {file_registry_path}')]
    
    # Check version consistency
    if all([
        surfaces_path.exists(),
        integrity_path.exists(),
        file_registry_path.exists()
    ]):
        results['version_consistency'] = check_version_consistency(
            surfaces_path,
            integrity_path,
            file_registry_path
        )
    else:
        results['version_consistency'] = [('skip', 'Skipped due to missing registry files')]
    
    return results


def format_results(results: Dict[str, List[Tuple[str, str]]]) -> str:
    """Format validation results for human reading."""
    lines = []
    
    total_issues = 0
    for check_name, issues in results.items():
        if issues:
            lines.append(f"\n{check_name}:")
            for issue_type, message in issues:
                lines.append(f"  [{issue_type}] {message}")
                total_issues += 1
    
    if total_issues == 0:
        lines.append("✓ All governance consistency checks passed.")
    else:
        lines.insert(0, f"✗ Found {total_issues} governance consistency issue(s):")
    
    return '\n'.join(lines)


if __name__ == '__main__':
    import sys
    
    # Default to repository root
    repo_root = Path(__file__).parent.parent.parent.parent.parent
    
    results = validate_governance_consistency(repo_root)
    output = format_results(results)
    print(output)
    
    # Exit with error if any issues found
    total_issues = sum(len(issues) for issues in results.values())
    sys.exit(1 if total_issues > 0 else 0)
