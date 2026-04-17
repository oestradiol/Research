"""
Generate AUTHORITATIVE_INTEGRITY_MANIFEST from CURRENT_SURFACES_REGISTRY.

This command automates SHA256 hash generation for current files,
eliminating manual synchronization errors.
"""

from pathlib import Path
from typing import Dict, List
import json
import hashlib


def load_json(path: Path) -> Dict:
    """Load JSON file safely."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError(f"File not found: {path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}")


def compute_sha256(file_path: Path) -> str:
    """Compute SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def generate_integrity_manifest(
    repo_root: Path,
    current_surfaces_path: Path = None,
    output_path: Path = None
) -> Dict:
    """
    Generate integrity manifest from CURRENT_SURFACES_REGISTRY.
    
    Args:
        repo_root: Repository root directory
        current_surfaces_path: Path to CURRENT_SURFACES_REGISTRY (default: governance/CURRENT_SURFACES_REGISTRY_v0_1.json)
        output_path: Path to write manifest (default: governance/AUTHORITATIVE_INTEGRITY_MANIFEST_v0_1.json)
    
    Returns:
        Generated manifest dictionary
    """
    if current_surfaces_path is None:
        current_surfaces_path = repo_root / 'governance' / 'CURRENT_SURFACES_REGISTRY_v0_1.json'
    
    if output_path is None:
        output_path = repo_root / 'governance' / 'AUTHORITATIVE_INTEGRITY_MANIFEST_v0_1.json'
    
    # Load CURRENT_SURFACES_REGISTRY
    surfaces = load_json(current_surfaces_path)
    
    # Validate canonical flag
    if not surfaces.get('canonical', False):
        raise ValueError(f"CURRENT_SURFACES_REGISTRY missing 'canonical: true' flag at {current_surfaces_path}")
    
    current_files = surfaces.get('current_files', [])
    
    if not current_files:
        raise ValueError(f"No current_files found in CURRENT_SURFACES_REGISTRY at {current_surfaces_path}")
    
    # Generate hashes
    files_with_hashes = []
    missing_files = []
    
    for file_ref in current_files:
        full_path = repo_root / file_ref
        if full_path.exists():
            sha256 = compute_sha256(full_path)
            files_with_hashes.append({
                'path': file_ref,
                'sha256': sha256
            })
        else:
            missing_files.append(file_ref)
    
    if missing_files:
        raise ValueError(f"Files listed in CURRENT_SURFACES_REGISTRY do not exist: {missing_files}")
    
    # Load existing manifest to preserve version
    if output_path.exists():
        existing_manifest = load_json(output_path)
        version = existing_manifest.get('version', '0.1.0')
        # Increment minor version on regeneration
        parts = version.split('.')
        if len(parts) >= 2:
            parts[1] = str(int(parts[1]) + 1)
            version = '.'.join(parts)
    else:
        version = '0.1.0'
    
    # Build manifest
    manifest = {
        'version': version,
        'algorithm': 'sha256',
        'source': 'CURRENT_SURFACES_REGISTRY_v0_1.json',
        'files': files_with_hashes
    }
    
    # Write manifest
    with open(output_path, 'w') as f:
        json.dump(manifest, f, indent=2)
        f.write('\n')
    
    return manifest


if __name__ == '__main__':
    import sys
    
    # Default to repository root
    repo_root = Path(__file__).parent.parent.parent.parent.parent
    
    try:
        manifest = generate_integrity_manifest(repo_root)
        print(f"✓ Generated integrity manifest with {len(manifest['files'])} files")
        print(f"  Version: {manifest['version']}")
        print(f"  Output: governance/AUTHORITATIVE_INTEGRITY_MANIFEST_v0_1.json")
    except ValueError as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
