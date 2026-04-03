from __future__ import annotations

from pathlib import Path

from research_tools.models.reports import ValidationResult
from research_tools.validate.links import validate_markdown_links

REQUIRED_KNOWLEDGE_FILES = (
    "README.md",
    "knowledge-package-spec.md",
    "suf-relationship.md",
    "studying-and-teaching-with-suf.md",
    "_indexes/knowledge-index.md",
    "_indexes/cluster-index.md",
    "_indexes/node-index.md",
    "_indexes/study-routes-index.md",
    "_indexes/relation-tags-index.md",
    "study-routes/README.md",
)


def _contains_check(
    path: Path,
    needle: str,
    check_name: str,
    message: str,
) -> ValidationResult:
    text = path.read_text(encoding="utf-8")
    status = "pass" if needle in text else "fail"
    return ValidationResult(
        check_name=check_name,
        status=status,
        message=message if status == "pass" else f"{message} Missing expected reference.",
        path=str(path),
        expected=needle,
        found=needle if status == "pass" else "missing",
    )


def validate_knowledge_package(knowledge_root: Path) -> list[ValidationResult]:
    results: list[ValidationResult] = []
    results.extend(validate_markdown_links(knowledge_root))

    for relative_path in REQUIRED_KNOWLEDGE_FILES:
        full_path = knowledge_root / relative_path
        status = "pass" if full_path.exists() else "fail"
        results.append(
            ValidationResult(
                check_name="knowledge-required-file",
                status=status,
                message="Required Knowledge surface exists."
                if status == "pass"
                else "Required Knowledge surface is missing.",
                path=str(full_path),
                expected=relative_path,
                found=relative_path if status == "pass" else "missing",
            )
        )

    readme_path = knowledge_root / "README.md"
    index_path = knowledge_root / "_indexes" / "knowledge-index.md"
    spec_path = knowledge_root / "knowledge-package-spec.md"
    contributing_path = knowledge_root / "CONTRIBUTING.md"

    if readme_path.exists():
        results.append(
            _contains_check(
                readme_path,
                "_indexes/knowledge-index.md",
                "knowledge-readme-entry-link",
                "Knowledge README references the main index.",
            )
        )
        results.append(
            _contains_check(
                readme_path,
                "../structured-unity-framework/README.md",
                "knowledge-readme-suf-link",
                "Knowledge README references the sibling SUF package.",
            )
        )

    if index_path.exists():
        for needle, check_name, message in (
            (
                "../knowledge-package-spec.md",
                "knowledge-index-spec-link",
                "Knowledge index references the live spec filename.",
            ),
            (
                "../README.md",
                "knowledge-index-readme-link",
                "Knowledge index references the package README.",
            ),
            (
                "cluster-index.md",
                "knowledge-index-cluster-link",
                "Knowledge index references the cluster index.",
            ),
            (
                "node-index.md",
                "knowledge-index-node-link",
                "Knowledge index references the node index.",
            ),
            (
                "study-routes-index.md",
                "knowledge-index-routes-link",
                "Knowledge index references the study-routes index.",
            ),
            (
                "relation-tags-index.md",
                "knowledge-index-relations-link",
                "Knowledge index references the relation-tags index.",
            ),
        ):
            results.append(_contains_check(index_path, needle, check_name, message))

    if spec_path.exists():
        results.append(
            _contains_check(
                spec_path,
                "knowledge-package-spec.md",
                "knowledge-spec-self-reference",
                "Knowledge package spec uses the normalized live filename.",
            )
        )

    if contributing_path.exists():
        results.append(
            _contains_check(
                contributing_path,
                "knowledge-package-spec.md",
                "knowledge-contributing-spec-link",
                "Knowledge contributing guide references the normalized spec filename.",
            )
        )

    legacy_hits: list[str] = []
    for markdown_file in knowledge_root.rglob("*.md"):
        text = markdown_file.read_text(encoding="utf-8")
        if "Knowledge Package Spec.md" in text:
            legacy_hits.append(str(markdown_file))
    results.append(
        ValidationResult(
            check_name="knowledge-legacy-filename",
            status="pass" if not legacy_hits else "fail",
            message="No stale spaced legacy filename remains in Knowledge package prose."
            if not legacy_hits
            else "Stale spaced legacy filename remains in Knowledge package prose.",
            expected="no 'Knowledge Package Spec.md' references",
            found=", ".join(legacy_hits) if legacy_hits else "none",
        )
    )

    return results
