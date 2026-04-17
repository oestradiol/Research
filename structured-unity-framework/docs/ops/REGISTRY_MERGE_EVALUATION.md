# Registry Merge Evaluation

## Question
Should REPOSITORY_FILE_REGISTRY_v0_1.json and REPOSITORY_EDIT_BASELINE_v0_1.json be merged?

## Analysis

### REPOSITORY_FILE_REGISTRY_v0_1.json
- Purpose: File metadata and categorization
- Contains:
  - `live_files`: array of 22 "live" governance files
  - `files`: array of all files with metadata (path, category, extension)
- Role: Knows which files exist and what kind they are
- Use case: File discovery, categorization, "what files are live?"

### REPOSITORY_EDIT_BASELINE_v0_1.json
- Purpose: Integrity baseline for all repository files
- Contains: path + sha256 hash pairs for ALL files
- Role: Knows what files should exist and their expected hash
- Use case: Integrity checking, change detection

### AUTHORITATIVE_INTEGRITY_MANIFEST_v0_1.json
- Purpose: Integrity manifest for CURRENT files only
- Contains: path + sha256 hash for `current_files` subset
- Role: Integrity for canonical current surfaces
- Use case: Validate current surfaces haven't drifted

## Overlap Analysis

**REPOSITORY_EDIT_BASELINE vs AUTHORITATIVE_INTEGRITY_MANIFEST:**
- Both contain sha256 hashes
- EDIT_BASELINE covers ALL files
- INTEGRITY_MANIFEST covers CURRENT files (subset)
- Similar structure, different scope

**REPOSITORY_FILE_REGISTRY:**
- Contains metadata (category, extension)
- Contains `live_files` array (which files are "live")
- No hashes
- Different purpose from both EDIT_BASELINE and INTEGRITY_MANIFEST

## Recommendation

### Keep REPOSITORY_FILE_REGISTRY separate
**Reasons:**
1. Different purpose: metadata vs integrity
2. Contains `live_files` array which is governance-critical
3. Category/extension data useful for file discovery
4. No structural overlap with hash-based registries

### Evaluate merging REPOSITORY_EDIT_BASELINE into AUTHORITATIVE_INTEGRITY_MANIFEST
**Option A: Keep separate**
- EDIT_BASELINE: full repo integrity
- INTEGRITY_MANIFEST: current surfaces integrity
- Clear separation of concerns
- But: duplication of hash data

**Option B: Merge**
- Single integrity registry with flags for "current" vs "all"
- Reduces duplication
- But: blurs scope distinction

**Recommendation: Keep separate**
- Full repo integrity (EDIT_BASELINE) is different from current surfaces integrity (INTEGRITY_MANIFEST)
- Different update cadences:
  - EDIT_BASELINE: update when ANY file changes
  - INTEGRITY_MANIFEST: update when CURRENT_SURFACES_REGISTRY changes
- Clearer audit trail with separate files

## Conclusion
- **REPOSITORY_FILE_REGISTRY**: Keep (metadata purpose, no overlap)
- **REPOSITORY_EDIT_BASELINE**: Keep separate from AUTHORITATIVE_INTEGRITY_MANIFEST (different scope and update cadence)

No merge recommended. Current separation is justified by distinct purposes.
