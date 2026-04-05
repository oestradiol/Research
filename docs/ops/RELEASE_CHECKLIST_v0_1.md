# Release checklist v0.2

Before calling the repository current and governed:

1. run `python package_doctor.py`
2. run `python research_launch_gate.py`
3. ensure `governance/AUTHORITATIVE_INDEX_v0_1.md` matches live root entrypoints
4. ensure both root and SUF integrity manifests are current
5. ensure any new root file is in:
   - `ROOT_ALLOWLIST_v0_1.json`
   - `REPOSITORY_FILE_REGISTRY_v0_1.json`
   - `FILE_JUSTIFICATION_REGISTRY_v0_1.json`
6. ensure root docs still route to the correct package surfaces instead of duplicating package state
7. ensure current claim expectations still match the bounded public posture
