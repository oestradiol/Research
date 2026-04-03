# Taiwan Event Ledger Seed

## Purpose

This file is the first archive-clean public event ledger for the Taiwan comparator starter tranche.

It is not a full Taiwan route. It is a minimal official seed built to test whether the same route-local logic can support a bounded external comparison.

## Current posture

Current status: `starter comparative ledger`

This seed is intentionally conservative:

- only official Taiwan CDC / CECC materials with fixed archives are admitted
- the current focus is activation, border control, quarantine support, and quarantine compliance
- the seed is functionally matched to the New Zealand route, not date-matched

## Summary list

| Event ID | Date | Short description |
|---|---|---|
| `tw-a-001` | `2020-01-20` | CECC activated as cross-agency command centre |
| `tw-p-001` | `2020-02-15` | home-quarantine support and daily follow-up expectations clarified |
| `tw-p-002` | `2020-03-18` | foreign-entry restrictions and local-district quarantine procedure announced |
| `tw-p-003` | `2020-03-22` | airline passenger transit through Taiwan suspended |
| `tw-p-004` | `2020-03-27` | home quarantine/isolation rules, local care/support centres, and sanctions clarified |
| `tw-p-005` | `2020-04-23` | direct-flight restrictions and transit ban extended |

## Starter events

### `tw-a-001`

- `timestamp_or_date`: `2020-01-20`
- `issuing_unit`: `strategic executive coordination`
- `receiving_units`: `public-health policy and command`; `public-service system coordination`; `border-control coordination`; `public-information coordination`
- `action_type`: activation of the CECC and cross-agency command-centre support
- `dependency_type`: `directive or authority dependency`; `information or reporting dependency`; `public-communication dependency`
- `implementation_marker`: `implementation initiated`
- `public_information_marker`: `major public briefing`
- `source_citation`: `src-taiwan-cecc-activation-2020`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`; `sigma3`

Why it matters:

This is the architecture anchor. It makes early command-centre activation explicit and already links cross-agency support, quarantine, and public-information activity.

### `tw-p-001`

- `timestamp_or_date`: `2020-02-15`
- `issuing_unit`: `strategic executive coordination`
- `receiving_units`: `public-health policy and command`; `border-control coordination`; `public-information coordination`
- `action_type`: clarification of home-quarantine support, daily follow-up, and airport/port notification expectations
- `dependency_type`: `information or reporting dependency`; `public-communication dependency`; `directive or authority dependency`
- `implementation_marker`: `implementation clarified`
- `public_information_marker`: `official guidance update`
- `source_citation`: `src-taiwan-home-quarantine-support-2020`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`

Why it matters:

This is an early support-and-follow-up event rather than only a border headline. It shows quarantine as a routed care and reporting arrangement.

### `tw-p-002`

- `timestamp_or_date`: `2020-03-18`
- `issuing_unit`: `strategic executive coordination`
- `receiving_units`: `public-health policy and command`; `public-service system coordination`; `border-control coordination`; `enforcement and compliance`; `public-information coordination`
- `action_type`: restriction of foreign entry and routing of travelers into home-quarantine procedure through local district offices
- `dependency_type`: `directive or authority dependency`; `legal or compliance dependency`; `information or reporting dependency`; `public-communication dependency`
- `implementation_marker`: `implementation initiated`
- `public_information_marker`: `major public briefing`
- `source_citation`: `src-taiwan-entry-restrictions-home-quarantine-2020`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`; `sigma3`

Why it matters:

This is the clearest starter event for the Taiwan border-plus-local-administration routing chain.

### `tw-p-003`

- `timestamp_or_date`: `2020-03-22`
- `issuing_unit`: `strategic executive coordination`
- `receiving_units`: `border-control coordination`; `public-information coordination`
- `action_type`: suspension of airline passenger transit through Taiwan
- `dependency_type`: `directive or authority dependency`; `public-communication dependency`
- `implementation_marker`: `implementation initiated`
- `public_information_marker`: `official guidance update`
- `source_citation`: `src-taiwan-transit-ban-2020`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`; `sigma3`

Why it matters:

This is a clean border-intensification event and a useful matched contrast with New Zealand's later transit and border tightening.

### `tw-p-004`

- `timestamp_or_date`: `2020-03-27`
- `issuing_unit`: `strategic executive coordination`
- `receiving_units`: `public-health policy and command`; `public-service system coordination`; `enforcement and compliance`; `public-information coordination`
- `action_type`: clarification of home-quarantine and home-isolation rules, local care/support routing, and sanction language
- `dependency_type`: `legal or compliance dependency`; `information or reporting dependency`; `public-communication dependency`
- `implementation_marker`: `implementation clarified`
- `public_information_marker`: `enforcement or compliance communication`
- `source_citation`: `src-taiwan-home-quarantine-isolation-regulations-2020`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`; `sigma3`

Why it matters:

This makes the Taiwan starter tranche less purely border-focused. It exposes local support centres, daily follow-up, and sanction logic in one official surface.

### `tw-p-005`

- `timestamp_or_date`: `2020-04-23`
- `issuing_unit`: `strategic executive coordination`
- `receiving_units`: `border-control coordination`; `enforcement and compliance`; `public-information coordination`
- `action_type`: extension of direct-flight restrictions and passenger-transit ban
- `dependency_type`: `directive or authority dependency`; `legal or compliance dependency`; `public-communication dependency`
- `implementation_marker`: `implementation continued`
- `public_information_marker`: `official guidance update`
- `source_citation`: `src-taiwan-transit-extension-2020`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`; `sigma3`

Why it matters:

This supplies continuity for the acute border-control window instead of leaving the starter tranche as a one-shot closure sequence.

## Starter readout cues

- total seeded events: `6`
- active `sigma1` units visible: `6 / 7`
- active directed edges: `5`
- weighted cross-cluster edge share: `18 / 21 = 0.86`
- mean receiving breadth: `3.5`
- issuing concentration: `strategic executive coordination` issues `6 / 6` seeded events
- public-information coordination receives `6 / 6` seeded events

## Current limit

The Taiwan starter tranche is thinner than the New Zealand route and remains strongly command-centre visible. It is enough for a bounded first comparison, not enough for a strong comparative conclusion.

## Status

`starter comparative ledger`
