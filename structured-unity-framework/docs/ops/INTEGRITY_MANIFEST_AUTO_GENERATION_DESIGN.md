# Auto-Generate Integrity Manifest Design

## Purpose
Design for automating AUTHORITATIVE_INTEGRITY_MANIFEST_v0_1.json generation from CURRENT_SURFACES_REGISTRY_v0_1.json.

## Current State
- CURRENT_SURFACES_REGISTRY_v0_1.json is canonical source of truth for current files
- AUTHORITATIVE_INTEGRITY_MANIFEST_v0_1.json currently manually maintained
- SHA256 hashes must be regenerated whenever files change
- Manual synchronization is error-prone (renewal cycle revealed this)

## Proposed Design

### CLI Command
```bash
nix develop ./tools -c research-tools generate integrity-manifest
```

### Implementation

1. **Read CURRENT_SURFACES_REGISTRY_v0_1.json**
   - Parse JSON
   - Extract `current_files` array
   - Validate `canonical: true` flag

2. **Generate SHA256 hashes**
   - For each file in `current_files`:
     - Read file bytes
     - Compute SHA256 hash
     - Store as `{"path": file_path, "sha256": hash}`

3. **Write AUTHORITATIVE_INTEGRITY_MANIFEST_v0_1.json**
   - Preserve `version` (increment if needed)
   - Preserve `algorithm` ("sha256")
   - Replace `files` array with generated hashes
   - Format with proper indentation

### Validation Checks
- All files in `current_files` must exist
- No files in manifest that aren't in registry (stale detection)
- No files in registry that aren't in manifest (missing detection)

### Error Handling
- Fail if CURRENT_SURFACES_REGISTRY not found
- Fail if canonical flag missing or false
- Fail if any file in registry doesn't exist
- Warn on stale/missing file mismatches

## Integration Points

### Pre-commit Hook
Run auto-generation before commit if:
- CURRENT_SURFACES_REGISTRY changed
- Any file in current_files changed
- AUTHORITATIVE_INTEGRITY_MANIFEST changed

### CI Workflow
Run in CI to ensure integrity manifest stays synchronized with registry.

## Benefits
- Eliminates manual synchronization errors
- Ensures hashes always match current files
- Reduces maintenance burden
- Makes CURRENT_SURFACES_REGISTRY truly canonical

## Risks
- Auto-generation could overwrite manual edits (mitigation: only auto-generate via explicit command)
- Version bumping needs policy (mitigation: auto-increment minor version on generation)

## Recommendation
Implement as `research-tools generate integrity-manifest` with explicit invocation (not automatic). Add to pre-commit hook as optional check that warns rather than auto-fixes.
