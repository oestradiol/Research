from __future__ import annotations

import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _actual_files(repo_root: Path, scope_prefix: str) -> list[str]:
    files = []
    for path in sorted(repo_root.rglob('*')):
        if not path.is_file():
            continue
        rel = path.relative_to(repo_root).as_posix()
        if '/__pycache__/' in f'/{rel}/' or '/.pytest_cache/' in f'/{rel}/' or rel.endswith('.pyc') or rel.endswith('.DS_Store'):
            continue
        if scope_prefix and not rel.startswith(scope_prefix):
            continue
        files.append(rel)
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


def main() -> None:
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
    print('Synced repository file registries and integrity manifests.')


if __name__ == '__main__':
    main()
