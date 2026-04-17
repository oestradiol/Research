from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "tools" / "src"))

from research_tools.repo_files import iter_truth_files


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _actual_files(repo_root: Path, scope_prefix: str) -> list[str]:
    files = iter_truth_files(repo_root)
    if scope_prefix:
        files = [rel for rel in files if rel.startswith(scope_prefix)]
    return files


def _category(path: str) -> str:
    name = Path(path).name
    return name if name else path


def _write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sync_registry(registry_path: Path) -> None:
    repo_root = BASE
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    scope_prefix = registry['scope_prefix']
    files = _actual_files(repo_root, scope_prefix)
    registry['files'] = [
        {'path': rel, 'category': _category(rel), 'extension': Path(rel).suffix or '[none]'}
        for rel in files
    ]
    _write_json(registry_path, registry)


def sync_manifest(manifest_path: Path) -> None:
    repo_root = BASE
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest['files'] = [
        {'path': entry['path'], 'sha256': _sha(repo_root / entry['path'])}
        for entry in manifest['files']
    ]
    _write_json(manifest_path, manifest)


def sync_edit_baseline(baseline_path: Path) -> None:
    baseline_rel = baseline_path.relative_to(BASE).as_posix()
    files = [rel for rel in _actual_files(BASE, "") if rel != baseline_rel]
    baseline = {"version": "0.1.0", "files": [{"path": rel, "sha256": _sha(BASE / rel)} for rel in files]}
    _write_json(baseline_path, baseline)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-edit-baseline", action="store_true")
    args = parser.parse_args()

    for rel in [
        'governance/REPOSITORY_FILE_REGISTRY_v0_1.json',
        'structured-unity-framework/governance/REPOSITORY_FILE_REGISTRY_v0_1.json',
    ]:
        sync_registry(BASE / rel)
    for rel in [
        'governance/AUTHORITATIVE_INTEGRITY_MANIFEST_v0_1.json',
        'structured-unity-framework/governance/AUTHORITATIVE_INTEGRITY_MANIFEST_v0_1.json',
    ]:
        sync_manifest(BASE / rel)
    if args.include_edit_baseline:
        sync_edit_baseline(BASE / 'governance/REPOSITORY_EDIT_BASELINE_v0_1.json')
        print('Synced repository file registries, integrity manifests, and edit baseline.')
    else:
        print('Synced repository file registries and integrity manifests.')


if __name__ == '__main__':
    main()
