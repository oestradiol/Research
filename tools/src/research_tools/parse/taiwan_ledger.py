from __future__ import annotations

import re
from pathlib import Path

from research_tools.models.ledger import LedgerEvent

SECTION_RE = re.compile(r"^### `([^`]+)`\s*$", re.MULTILINE)
FIELD_RE = re.compile(r"^- `([^`]+)`: (.+)$")
SOURCE_ID_RE = re.compile(r"(src-[A-Za-z0-9-]+)")


def _clean_value(value: str) -> str:
    return value.strip().strip("`")


def _split_semicolon_field(value: str) -> tuple[str, ...]:
    items = []
    for piece in value.split(";"):
        cleaned = _clean_value(piece)
        if cleaned:
            items.append(cleaned)
    return tuple(items)


def _extract_source_ids(value: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys(SOURCE_ID_RE.findall(value)))


def parse_taiwan_ledger(path: Path) -> list[LedgerEvent]:
    text = path.read_text(encoding="utf-8")
    matches = list(SECTION_RE.finditer(text))
    events: list[LedgerEvent] = []
    for index, match in enumerate(matches):
        event_id = match.group(1)
        if not event_id.startswith("tw-"):
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[start:end]
        fields: dict[str, str] = {}
        for line in block.splitlines():
            field_match = FIELD_RE.match(line.strip())
            if field_match:
                fields[field_match.group(1)] = field_match.group(2).strip()
        events.append(
            LedgerEvent(
                event_id=event_id,
                timestamp_or_date=_clean_value(fields["timestamp_or_date"]),
                issuing_unit=_clean_value(fields["issuing_unit"]),
                receiving_units=_split_semicolon_field(fields["receiving_units"]),
                action_type=_clean_value(fields["action_type"]),
                dependency_types=_split_semicolon_field(fields["dependency_type"]),
                implementation_markers=_split_semicolon_field(fields["implementation_marker"]),
                public_information_markers=_split_semicolon_field(fields["public_information_marker"]),
                source_citations=_extract_source_ids(fields["source_citation"]),
                confidence_note=_clean_value(fields["confidence_note"]),
                scale_tags=_split_semicolon_field(fields["scale_tag"]),
            )
        )
    return events
