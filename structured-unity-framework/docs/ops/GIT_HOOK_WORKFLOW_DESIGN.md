# Git Hook Workflow Design

## Purpose
Design for pre-commit hook that runs governance consistency validation.

## Trigger Conditions
Hook should run when:
- Any governance file changes
- CURRENT_SURFACES_REGISTRY changes
- AUTHORITATIVE_INTEGRITY_MANIFEST changes
- SUBSYSTEM_REGISTRY changes

## Implementation Options

### Option A: Pre-commit hook (local)
**Pros:**
- Catches issues before push
- Immediate feedback
- No CI dependency

**Cons:**
- Requires local setup
- Can be bypassed with `--no-verify`
- Not enforced in CI

### Option B: CI workflow (GitHub Actions, GitLab CI, etc.)
**Pros:**
- Enforced on all PRs
- Consistent across all contributors
- Can't be bypassed

**Cons:**
- No local feedback (push then fail)
- Requires CI infrastructure
- Slower feedback loop

### Option C: Both (recommended)
- Pre-commit hook for local feedback
- CI workflow for enforcement
- Best of both worlds

## Recommended Implementation

### Pre-commit Hook (Option A + C)
Location: `.git/hooks/pre-commit`

```bash
#!/bin/bash
# Pre-commit hook for governance consistency

# Check if governance files changed
if git diff --cached --name-only | grep -q "governance/\|CURRENT_SURFACES_REGISTRY_v0_1.json\|AUTHORITATIVE_INTEGRITY_MANIFEST_v0_1.json\|SUBSYSTEM_REGISTRY_v0_1.json"; then
    echo "Governance files changed. Running validation..."
    
    # Activate Nix environment and run validation
    nix develop ./tools -c python tools/src/research_tools/validate/governance_consistency.py
    
    if [ $? -ne 0 ]; then
        echo "Governance validation failed. Please fix errors before committing."
        exit 1
    fi
    
    echo "Governance validation passed."
fi

exit 0
```

### CI Workflow (Option B + C)
Location: `.github/workflows/governance-validation.yml` (or equivalent)

```yaml
name: Governance Validation

on:
  pull_request:
    paths:
      - 'governance/**'
      - 'CURRENT_SURFACES_REGISTRY_v0_1.json'
      - 'AUTHORITATIVE_INTEGRITY_MANIFEST_v0_1.json'
      - 'SUBSYSTEM_REGISTRY_v0_1.json'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Nix
        uses: cachix/install-nix-action@v20
      - name: Run governance validation
        run: nix develop ./tools -c python tools/src/research_tools/validate/governance_consistency.py
```

## Integration with Auto-Generation

When auto-generation commands are implemented (from INTEGRITY_MANIFEST_AUTO_GENERATION_DESIGN):

### Option 1: Auto-generate in hook
- Hook runs validation
- If validation fails due to stale hashes, auto-generate
- Add generated file to commit

**Pros:** Seamless
**Cons:** Auto-modification can be surprising

### Option 2: Warn in hook, manual fix
- Hook runs validation
- If validation fails, warn with command to fix
- User runs `research-tools generate integrity-manifest` manually
- User adds generated file to commit

**Pros:** Explicit, no surprises
**Cons:** Extra step for user

**Recommendation:** Option 2 (warn, don't auto-fix)

## Installation

### Pre-commit hook
```bash
# Copy hook to .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Or use pre-commit framework:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: governance-validation
        name: Governance validation
        entry: nix develop ./tools -c python tools/src/research_tools/validate/governance_consistency.py
        files: 'governance/.*\.json|.*_REGISTRY.*\.json|.*_MANIFEST.*\.json'
```

## Testing
1. Modify a governance file
2. Try to commit
3. Hook should run validation
4. If validation passes, commit succeeds
5. If validation fails, commit blocked with error message

## Recommendation
**Start with pre-commit hook only (Option A)**
- Immediate feedback
- No CI infrastructure needed yet
- Can add CI enforcement later if needed

**Use warn-don't-autofix approach**
- Explicit is better than implicit
- User controls when to run generation commands
