from research_tools.parse.source_registry import parse_source_registry, source_registry_index
from research_tools.paths import get_paths
from research_tools.validate.route_consistency import validate_nz_route, validate_taiwan_route
from research_tools.validate.status_surfaces import validate_status_surfaces


def test_nz_route_consistency_matches_current_docs() -> None:
    paths = get_paths()
    entries = parse_source_registry(paths.source_registry)
    results = validate_nz_route(paths.nz_route_root, source_registry_index(entries))

    assert not any(result.status == "fail" for result in results)


def test_taiwan_route_consistency_matches_current_docs() -> None:
    paths = get_paths()
    entries = parse_source_registry(paths.source_registry)
    results = validate_taiwan_route(paths.taiwan_route_root, source_registry_index(entries))

    assert not any(result.status == "fail" for result in results)


def test_status_surfaces_match_current_docs() -> None:
    results = validate_status_surfaces(get_paths())

    assert not any(result.status == "fail" for result in results)
