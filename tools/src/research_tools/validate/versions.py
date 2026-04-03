from __future__ import annotations

import re
from pathlib import Path

from research_tools.models.reports import ValidationResult
from research_tools.paths import RepoPaths

VERSION_RE = re.compile(r'^version:\s*"([^"]+)"\s*$', re.MULTILINE)
DATE_RE = re.compile(r'^date-released:\s*"([^"]+)"\s*$', re.MULTILINE)
PYPROJECT_VERSION_RE = re.compile(r'^version\s*=\s*"([^"]+)"\s*$', re.MULTILINE)
INIT_VERSION_RE = re.compile(r'__version__\s*=\s*"([^"]+)"')
CHANGELOG_VERSION_RE = re.compile(r"^## `([^`]+)` - ([0-9]{4}-[0-9]{2}-[0-9]{2})$", re.MULTILINE)
ROOT_README_SNAPSHOT_RE = re.compile(
    r"(?:\*\*Current snapshot:\*\*|Current snapshot:)\s+\*\*`([^`]+)`\*\*\s+dated\s+"
    r"\*\*`?([0-9-]+)`?\*\*\."
)
SUF_README_SNAPSHOT_RE = ROOT_README_SNAPSHOT_RE
SUF_STATUS_RE = re.compile(
    r"\*\*`([^`]+)`\*\* names the dated local snapshot in this tree \(\*\*([0-9-]+)\*\*\)\."
)
KNOWLEDGE_README_SNAPSHOT_RE = re.compile(r"- `([^`]+)` dated `([^`]+)`")
TOOLS_README_SNAPSHOT_RE = re.compile(r"Current snapshot: `([^`]+)` dated `([^`]+)`\.")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_required(pattern: re.Pattern[str], text: str, path: Path, field_name: str) -> str:
    match = pattern.search(text)
    if not match:
        raise ValueError(f"{field_name} not found in {path}")
    return match.group(1)


def _extract_changelog(path: Path) -> tuple[str, str]:
    text = _read_text(path)
    matches = CHANGELOG_VERSION_RE.findall(text)
    if not matches:
        raise ValueError(f"No released changelog section found in {path}")
    return matches[0]


def _comparison(
    check_name: str,
    message: str,
    expected: str,
    found: str,
    path: Path | None = None,
) -> ValidationResult:
    status = "pass" if expected == found else "fail"
    return ValidationResult(
        check_name=check_name,
        status=status,
        message=message if status == "pass" else f"{message} Value mismatch.",
        path=str(path) if path else None,
        expected=expected,
        found=found,
    )


def _normalize_version(value: str) -> str:
    return value[1:] if value.startswith("v") else value


def validate_versions(paths: RepoPaths) -> list[ValidationResult]:
    results: list[ValidationResult] = []

    umbrella_cff = paths.research_root / "CITATION.cff"
    suf_cff = paths.suf_root / "CITATION.cff"
    knowledge_cff = paths.knowledge_root / "CITATION.cff"
    tools_pyproject = paths.tools_root / "pyproject.toml"
    tools_init = paths.tools_root / "src" / "research_tools" / "__init__.py"
    root_readme = paths.research_root / "README.md"
    suf_readme = paths.suf_root / "README.md"
    suf_status = paths.suf_root / "docs" / "project-status.md"
    knowledge_readme = paths.knowledge_root / "README.md"
    tools_readme = paths.tools_root / "README.md"
    root_changelog = paths.research_root / "CHANGELOG.md"
    suf_changelog = paths.suf_root / "CHANGELOG.md"
    knowledge_changelog = paths.knowledge_root / "CHANGELOG.md"

    umbrella_text = _read_text(umbrella_cff)
    suf_text = _read_text(suf_cff)
    knowledge_text = _read_text(knowledge_cff)
    pyproject_text = _read_text(tools_pyproject)
    init_text = _read_text(tools_init)

    umbrella_version = _extract_required(VERSION_RE, umbrella_text, umbrella_cff, "version")
    umbrella_date = _extract_required(DATE_RE, umbrella_text, umbrella_cff, "date-released")
    suf_version = _extract_required(VERSION_RE, suf_text, suf_cff, "version")
    suf_date = _extract_required(DATE_RE, suf_text, suf_cff, "date-released")
    knowledge_version = _extract_required(VERSION_RE, knowledge_text, knowledge_cff, "version")
    knowledge_date = _extract_required(DATE_RE, knowledge_text, knowledge_cff, "date-released")
    tools_version = _extract_required(
        PYPROJECT_VERSION_RE,
        pyproject_text,
        tools_pyproject,
        "version",
    )
    tools_init_version = _extract_required(INIT_VERSION_RE, init_text, tools_init, "__version__")

    root_readme_match = ROOT_README_SNAPSHOT_RE.search(_read_text(root_readme))
    suf_readme_match = SUF_README_SNAPSHOT_RE.search(_read_text(suf_readme))
    suf_status_match = SUF_STATUS_RE.search(_read_text(suf_status))
    knowledge_readme_match = KNOWLEDGE_README_SNAPSHOT_RE.search(_read_text(knowledge_readme))
    tools_readme_match = TOOLS_README_SNAPSHOT_RE.search(_read_text(tools_readme))

    if not root_readme_match:
        results.append(
            ValidationResult(
                check_name="versions-umbrella-readme",
                status="fail",
                message="Umbrella README snapshot line not found.",
                path=str(root_readme),
            )
        )
    else:
        results.append(
            _comparison(
                "versions-umbrella-readme-version",
                "Umbrella README version matches umbrella citation.",
                umbrella_version,
                _normalize_version(root_readme_match.group(1)),
                root_readme,
            )
        )
        results.append(
            _comparison(
                "versions-umbrella-readme-date",
                "Umbrella README date matches umbrella citation.",
                umbrella_date,
                root_readme_match.group(2),
                root_readme,
            )
        )

    if not suf_readme_match:
        results.append(
            ValidationResult(
                check_name="versions-suf-readme",
                status="fail",
                message="SUF README snapshot line not found.",
                path=str(suf_readme),
            )
        )
    else:
        results.append(
            _comparison(
                "versions-suf-readme-version",
                "SUF README version matches SUF citation.",
                suf_version,
                _normalize_version(suf_readme_match.group(1)),
                suf_readme,
            )
        )
        results.append(
            _comparison(
                "versions-suf-readme-date",
                "SUF README date matches SUF citation.",
                suf_date,
                suf_readme_match.group(2),
                suf_readme,
            )
        )

    if not suf_status_match:
        results.append(
            ValidationResult(
                check_name="versions-suf-status",
                status="fail",
                message="SUF project-status version line not found.",
                path=str(suf_status),
            )
        )
    else:
        results.append(
            _comparison(
                "versions-suf-status-version",
                "SUF project-status version matches SUF citation.",
                suf_version,
                _normalize_version(suf_status_match.group(1)),
                suf_status,
            )
        )
        results.append(
            _comparison(
                "versions-suf-status-date",
                "SUF project-status date matches SUF citation.",
                suf_date,
                suf_status_match.group(2),
                suf_status,
            )
        )

    if not knowledge_readme_match:
        results.append(
            ValidationResult(
                check_name="versions-knowledge-readme",
                status="fail",
                message="Knowledge README snapshot line not found.",
                path=str(knowledge_readme),
            )
        )
    else:
        results.append(
            _comparison(
                "versions-knowledge-readme-version",
                "Knowledge README version matches Knowledge citation.",
                knowledge_version,
                _normalize_version(knowledge_readme_match.group(1)),
                knowledge_readme,
            )
        )
        results.append(
            _comparison(
                "versions-knowledge-readme-date",
                "Knowledge README date matches Knowledge citation.",
                knowledge_date,
                knowledge_readme_match.group(2),
                knowledge_readme,
            )
        )

    if not tools_readme_match:
        results.append(
            ValidationResult(
                check_name="versions-tools-readme",
                status="fail",
                message="Tools README snapshot line not found.",
                path=str(tools_readme),
            )
        )
    else:
        results.append(
            _comparison(
                "versions-tools-readme-version",
                "Tools README version matches tools metadata.",
                tools_version,
                tools_readme_match.group(1),
                tools_readme,
            )
        )
        results.append(
            _comparison(
                "versions-tools-readme-date",
                "Tools README date matches umbrella release date.",
                umbrella_date,
                tools_readme_match.group(2),
                tools_readme,
            )
        )

    results.append(
        _comparison(
            "versions-tools-metadata-sync",
            "Tools pyproject and package __init__ versions match.",
            tools_version,
            tools_init_version,
            tools_pyproject,
        )
    )

    for check_prefix, version, date, changelog_path in (
        ("versions-umbrella-changelog", umbrella_version, umbrella_date, root_changelog),
        ("versions-suf-changelog", suf_version, suf_date, suf_changelog),
        ("versions-knowledge-changelog", knowledge_version, knowledge_date, knowledge_changelog),
    ):
        changelog_version, changelog_date = _extract_changelog(changelog_path)
        results.append(
            _comparison(
                f"{check_prefix}-version",
                "Top changelog release version matches package version.",
                version,
                _normalize_version(changelog_version),
                changelog_path,
            )
        )
        results.append(
            _comparison(
                f"{check_prefix}-date",
                "Top changelog release date matches package date.",
                date,
                changelog_date,
                changelog_path,
            )
        )

    return results
