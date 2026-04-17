from __future__ import annotations

from collections.abc import Callable

from research_tools.models.clusters import ValidationClusterRun, ValidationClusterSpec
from research_tools.models.reports import ValidationResult
from research_tools.parse.source_registry import parse_source_registry, source_registry_index
from research_tools.parse.subsystems import parse_subsystem_registry
from research_tools.paths import RepoPaths, format_optional_report_path, format_report_path
from research_tools.validate.archives import validate_archive_links
from research_tools.validate.governance import (
    validate_current_claims,
    validate_current_surfaces,
    validate_edit_scope,
    validate_merged_doc_quality,
    validate_repository_file_registry,
    validate_repository_minimality,
    validate_routing_surfaces,
)
from research_tools.validate.knowledge import validate_knowledge_package
from research_tools.validate.links import validate_markdown_links
from research_tools.validate.release_hygiene import validate_release_hygiene
from research_tools.validate.route_consistency import validate_nz_route, validate_taiwan_route
from research_tools.validate.sources import validate_source_registry
from research_tools.validate.status_surfaces import validate_status_surfaces
from research_tools.validate.versions import validate_versions


def _summarize_results(results: list[ValidationResult]) -> tuple[int, int, int, str]:
    passed = sum(1 for result in results if result.status == "pass")
    failed = sum(1 for result in results if result.status == "fail")
    warned = sum(1 for result in results if result.status == "warn")
    status = "fail" if failed else "warn" if warned else "pass"
    return passed, failed, warned, status


def _run_root_governance_cluster(paths: RepoPaths) -> list[ValidationResult]:
    repo_root = paths.research_root
    results: list[ValidationResult] = []
    results.extend(validate_current_surfaces(repo_root))
    results.extend(validate_repository_file_registry(repo_root))
    results.extend(validate_current_claims(repo_root))
    results.extend(validate_repository_minimality(repo_root))
    results.extend(validate_routing_surfaces(repo_root))
    results.extend(validate_merged_doc_quality(repo_root))
    results.extend(validate_edit_scope(repo_root))
    return results


def _run_suf_active_core_cluster(paths: RepoPaths) -> list[ValidationResult]:
    entries = parse_source_registry(paths.source_registry)
    source_index = source_registry_index(entries)
    results: list[ValidationResult] = []
    results.extend(validate_nz_route(paths.nz_route_root, source_index))
    results.extend(validate_taiwan_route(paths.taiwan_route_root, source_index))
    results.extend(validate_status_surfaces(paths))
    return results


def _run_knowledge_cluster(paths: RepoPaths) -> list[ValidationResult]:
    return validate_knowledge_package(paths.knowledge_root)


def _run_tooling_release_cluster(paths: RepoPaths) -> list[ValidationResult]:
    entries = parse_source_registry(paths.source_registry)
    results: list[ValidationResult] = []
    results.extend(validate_markdown_links(paths.research_root))
    results.extend(validate_source_registry(entries))
    results.extend(validate_archive_links(entries))
    results.extend(validate_versions(paths))
    results.extend(validate_release_hygiene(paths.research_root))
    return results


CLUSTER_RUNNERS: dict[str, Callable[[RepoPaths], list[ValidationResult]]] = {
    "root-governance": _run_root_governance_cluster,
    "suf-active-core": _run_suf_active_core_cluster,
    "knowledge-package": _run_knowledge_cluster,
    "tooling-release": _run_tooling_release_cluster,
}


def _build_cluster_run(
    spec: ValidationClusterSpec,
    paths: RepoPaths,
    results: list[ValidationResult],
) -> ValidationClusterRun:
    passed, failed, warned, status = _summarize_results(results)
    return ValidationClusterRun(
        spec=spec,
        source_files=tuple(paths.research_root / rel for rel in spec.source_files),
        results=tuple(results),
        passed=passed,
        failed=failed,
        warned=warned,
        status=status,
    )


def _error_cluster_run(paths: RepoPaths, message: str) -> ValidationClusterRun:
    spec = ValidationClusterSpec(
        cluster_id="subsystem-registry-error",
        owner="Research root governance",
        purpose="Expose subsystem-registry parse failures before cluster orchestration continues.",
        entry_surface="governance/SUBSYSTEM_REGISTRY_v0_1.json",
        source_files=("governance/SUBSYSTEM_REGISTRY_v0_1.json",),
    )
    return _build_cluster_run(
        spec,
        paths,
        [
            ValidationResult(
                check_name="cluster-registry-parse",
                status="fail",
                message=message,
                path=str(paths.subsystem_registry),
                expected="valid subsystem registry JSON",
                found="parse error",
            )
        ],
    )


def _cluster_spec_from_registry(subsystem) -> ValidationClusterSpec:
    validation_cluster = subsystem.validation_cluster
    if validation_cluster is None:
        raise ValueError(f"subsystem `{subsystem.subsystem_id}` has no validation cluster")
    return ValidationClusterSpec(
        cluster_id=validation_cluster.cluster_id,
        owner=subsystem.owner,
        purpose=subsystem.purpose,
        entry_surface=subsystem.entry_surface,
        source_files=validation_cluster.source_files,
    )


def _cluster_protocol_results(paths: RepoPaths, subsystem) -> list[ValidationResult]:
    results: list[ValidationResult] = []
    entry_path = paths.research_root / subsystem.entry_surface
    authoritative_path = paths.research_root / subsystem.authoritative_surface
    results.append(
        ValidationResult(
            check_name="cluster-entry-surface-exists",
            status="pass" if entry_path.exists() else "fail",
            message=(
                "Cluster entry surface exists."
                if entry_path.exists()
                else "Cluster entry surface is missing."
            ),
            path=str(paths.subsystem_registry),
            expected=subsystem.entry_surface,
            found=subsystem.entry_surface if entry_path.exists() else "missing",
        )
    )
    results.append(
        ValidationResult(
            check_name="cluster-authoritative-surface-exists",
            status="pass" if authoritative_path.exists() else "fail",
            message=(
                "Cluster authoritative surface exists."
                if authoritative_path.exists()
                else "Cluster authoritative surface is missing."
            ),
            path=str(paths.subsystem_registry),
            expected=subsystem.authoritative_surface,
            found=(
                subsystem.authoritative_surface
                if authoritative_path.exists()
                else "missing"
            ),
        )
    )
    missing_sources = [
        rel
        for rel in subsystem.validation_cluster.source_files
        if not (paths.research_root / rel).exists()
    ]
    results.append(
        ValidationResult(
            check_name="cluster-source-files-exist",
            status="pass" if not missing_sources else "fail",
            message=(
                "Cluster source files exist."
                if not missing_sources
                else "Cluster source files are missing."
            ),
            path=str(paths.subsystem_registry),
            expected="all cluster source files exist",
            found="ok" if not missing_sources else ", ".join(missing_sources),
        )
    )
    return results


def collect_validation_clusters(paths: RepoPaths) -> list[ValidationClusterRun]:
    try:
        subsystems = parse_subsystem_registry(paths.subsystem_registry)
    except Exception as exc:
        return [_error_cluster_run(paths, f"Subsystem registry could not be parsed: {exc}")]

    clusters: list[ValidationClusterRun] = []
    for subsystem in subsystems:
        if subsystem.validation_cluster is None:
            continue
        spec = _cluster_spec_from_registry(subsystem)
        results = _cluster_protocol_results(paths, subsystem)
        runner = CLUSTER_RUNNERS.get(spec.cluster_id)
        if runner is None:
            results.append(
                ValidationResult(
                    check_name="cluster-runner-registered",
                    status="fail",
                    message="Validation cluster has no registered runner.",
                    path=str(paths.subsystem_registry),
                    expected=spec.cluster_id,
                    found="missing",
                )
            )
        else:
            results.extend(runner(paths))
        clusters.append(_build_cluster_run(spec, paths, results))
    return clusters


def render_cluster_report(generated_at: str, clusters: list[ValidationClusterRun]) -> str:
    cluster_summaries = "\n".join(
        f"- `{cluster.spec.cluster_id}` [{cluster.status}] owner `{cluster.spec.owner}` entry `{cluster.spec.entry_surface}` passed `{cluster.passed}` failed `{cluster.failed}` warned `{cluster.warned}`"
        for cluster in clusters
    )
    cluster_sections = []
    for cluster in clusters:
        files = "\n".join(f"- `{format_report_path(path)}`" for path in cluster.source_files)
        results = "\n".join(
            f"- `{result.check_name}` [{result.status}] {result.message}"
            + (f" Expected `{result.expected}`." if result.expected else "")
            + (f" Found `{result.found}`." if result.found else "")
            + (f" Path `{format_optional_report_path(result.path)}`." if result.path else "")
            for result in cluster.results
        )
        cluster_sections.append(
            f"""## {cluster.spec.cluster_id}

- owner: `{cluster.spec.owner}`
- purpose: {cluster.spec.purpose}
- entry surface: `{cluster.spec.entry_surface}`
- status: `{cluster.status}`
- passed: `{cluster.passed}`
- failed: `{cluster.failed}`
- warned: `{cluster.warned}`

### Source files

{files}

### Results

{results}
"""
        )
    body = "\n".join(cluster_sections)
    return f"""# Federated Validation Clusters

Generated: `{generated_at}`

## Summary

{cluster_summaries}

{body}

## Human validation required

This output is read-only and provisional until a human reviews it.
"""
