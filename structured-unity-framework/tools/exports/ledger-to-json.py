#!/usr/bin/env python3
"""
Export SUF event ledger from Markdown to JSON.

Usage:
    python ledger-to-json.py --input <ledger.md> --output <ledger.json>
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any


def parse_event_section(section_text: str) -> Dict[str, Any]:
    """Parse a single event section from the ledger."""
    event = {}
    
    # Extract event ID and date from header
    id_match = re.search(r'^### `([^`]+)`', section_text, re.MULTILINE)
    if id_match:
        event['event_id'] = id_match.group(1)
    
    # Extract timestamp/date
    date_match = re.search(r'- `timestamp_or_date`: `([^`]+)`', section_text)
    if date_match:
        event['timestamp_or_date'] = date_match.group(1)
    
    # Extract issuing unit
    issuing_match = re.search(r'- `issuing_unit`: `([^`]+)`', section_text)
    if issuing_match:
        event['issuing_unit'] = issuing_match.group(1)
    
    # Extract receiving units (can be multiple)
    receiving_match = re.search(r'- `receiving_units`: (.+?)(?=\n-)', section_text, re.DOTALL)
    if receiving_match:
        units_text = receiving_match.group(1)
        # Split by semicolon and clean up
        units = [u.strip().strip('`') for u in units_text.split(';')]
        event['receiving_units'] = units
    
    # Extract action type
    action_match = re.search(r'- `action_type`: (.+?)(?=\n-)', section_text, re.DOTALL)
    if action_match:
        event['action_type'] = action_match.group(1).strip()
    
    # Extract dependency types
    dep_match = re.search(r'- `dependency_type`: (.+?)(?=\n-)', section_text, re.DOTALL)
    if dep_match:
        deps_text = dep_match.group(1)
        deps = [d.strip().strip('`') for d in deps_text.split(';')]
        event['dependency_type'] = deps
    
    # Extract implementation marker
    impl_match = re.search(r'- `implementation_marker`: `([^`]+)`', section_text)
    if impl_match:
        event['implementation_marker'] = impl_match.group(1)
    
    # Extract public information marker
    pub_match = re.search(r'- `public_information_marker`: `([^`]+)`', section_text)
    if pub_match:
        event['public_information_marker'] = pub_match.group(1)
    
    # Extract source citation
    src_match = re.search(r'- `source_citation`: `([^`]+)`', section_text)
    if src_match:
        event['source_citation'] = src_match.group(1)
    
    # Extract confidence
    conf_match = re.search(r'- `confidence_note`: `([^`]+)`', section_text)
    if conf_match:
        event['confidence_note'] = conf_match.group(1)
    
    # Extract scale tags
    scale_match = re.search(r'- `scale_tag`: (.+?)(?=\n\n|$)', section_text, re.DOTALL)
    if scale_match:
        scales_text = scale_match.group(1)
        scales = [s.strip().strip('`') for s in scales_text.split(';')]
        event['scale_tag'] = scales
    
    return event


def parse_ledger(ledger_text: str) -> Dict[str, Any]:
    """Parse full ledger into structured format."""
    ledger = {
        'metadata': {},
        'events': []
    }
    
    # Extract metadata (first few lines before ## Summary)
    purpose_match = re.search(r'^## Purpose\n\n(.+?)(?=\n##|$)', ledger_text, re.DOTALL)
    if purpose_match:
        ledger['metadata']['purpose'] = purpose_match.group(1).strip()
    
    # Extract current posture/status
    status_match = re.search(r'Current status: `([^`]+)`', ledger_text)
    if status_match:
        ledger['metadata']['current_status'] = status_match.group(1)
    
    # Extract readout cues
    readout_match = re.search(r'## Current readout cues\n\n(.+?)(?=\n##|$)', ledger_text, re.DOTALL)
    if readout_match:
        readout_text = readout_match.group(1)
        # Parse key metrics
        total_match = re.search(r'- total seeded events: `(\d+)`', readout_text)
        if total_match:
            ledger['metadata']['total_events'] = int(total_match.group(1))
        
        sigma_match = re.search(r'- active `sigma1` units visible: `(\d+ / \d+)`', readout_text)
        if sigma_match:
            ledger['metadata']['sigma1_units_visible'] = sigma_match.group(1)
        
        edges_match = re.search(r'- active directed edges: `(\d+)`', readout_text)
        if edges_match:
            ledger['metadata']['directed_edges'] = int(edges_match.group(1))
    
    # Extract all event sections by finding event IDs and splitting
    event_ids = re.findall(r'### `([^`]+)`', ledger_text)
    for event_id in event_ids:
        # Find the section for this event
        pattern = rf'### `{re.escape(event_id)}`\n\n(.+?)(?=\n### |\n## |\Z)'
        match = re.search(pattern, ledger_text, re.DOTALL)
        if match:
            section_text = match.group(1)
            event = parse_event_section(section_text)
            if event:
                event['event_id'] = event_id
                ledger['events'].append(event)
    
    return ledger


def main():
    parser = argparse.ArgumentParser(description='Export SUF ledger to JSON')
    parser.add_argument('--input', '-i', required=True, help='Input ledger markdown file')
    parser.add_argument('--output', '-o', required=True, help='Output JSON file')
    args = parser.parse_args()
    
    # Read input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    ledger_text = input_path.read_text(encoding='utf-8')
    
    # Parse
    ledger = parse_ledger(ledger_text)
    
    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)
    
    print(f"Exported {len(ledger['events'])} events to {args.output}")
    print(f"Metadata: {ledger['metadata']}")


if __name__ == '__main__':
    main()
