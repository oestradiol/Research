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
| `tw-p-006` | `2020-02-08` | 14-day home quarantine requirement expanded to all travelers entering Taiwan |
| `tw-p-001` | `2020-02-15` | home-quarantine support and daily follow-up expectations clarified |
| `tw-p-002` | `2020-03-18` | foreign-entry restrictions and local-district quarantine procedure announced |
| `tw-p-003` | `2020-03-22` | airline passenger transit through Taiwan suspended |
| `tw-p-004` | `2020-03-27` | home quarantine/isolation rules, local care/support centres, and sanctions clarified |
| `tw-p-010` | `2020-03-29` | health-agency notification and medical-care routing observed during home quarantine |
| `tw-p-011` | `2020-04-01` | people under home quarantine barred from domestic flight or ferry travel to offshore islands and transit ban extended |
| `tw-p-007` | `2020-04-01` | cumulative penalties and group-quarantine escalation clarified for quarantine breaches |
| `tw-p-008` | `2020-04-02` | symptomatic inbound travelers routed by epidemic-prevention taxis to designated testing locations |
| `tw-p-009` | `2020-04-14` | Europe and Americas returnees required to notify health officials and use quarantine hotels where needed |
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

### `tw-p-006`

- `timestamp_or_date`: `2020-02-08`
- `issuing_unit`: `strategic executive coordination`
- `receiving_units`: `public-health policy and command`; `border-control coordination`; `public-information coordination`
- `action_type`: all travelers entering Taiwan required to undergo 14-day home quarantine from February 10, with China, Hong Kong, and Macau transit restrictions maintained
- `dependency_type`: `directive or authority dependency`; `legal or compliance dependency`; `public-communication dependency`
- `implementation_marker`: `decision announced`
- `public_information_marker`: `official guidance update`
- `source_citation`: `src-taiwan-all-travelers-home-quarantine-2020`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`; `sigma3`

Why it matters:

This event thickens the early border-to-quarantine routing chain before the later support note. It makes the comparator less dependent on retrospective architecture plus later March escalation.

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

### `tw-p-010`

- `timestamp_or_date`: `2020-03-29`
- `issuing_unit`: `public-health policy and command`
- `receiving_units`: `public-service system coordination`; `public-information coordination`
- `action_type`: health agencies are notified during home quarantine, medical care is arranged, and household contacts are placed into home isolation in confirmed imported-case handling
- `dependency_type`: `information or reporting dependency`; `resource or logistics dependency`; `public-communication dependency`
- `implementation_marker`: `implementation observed`
- `public_information_marker`: `official guidance update`
- `source_citation`: `src-taiwan-home-quarantine-health-agency-routing-2020`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`; `sigma3`

Why it matters:

This is the clearest implementation-observed event yet in the Taiwan branch. It makes one conservative lag pair visible by showing the March 18 quarantine-routing chain not only announced, but later observed in health-agency notification and medical-care handling during home quarantine.

### `tw-p-011`

- `timestamp_or_date`: `2020-04-01`
- `issuing_unit`: `border-control coordination`
- `receiving_units`: `public-service system coordination`; `enforcement and compliance`; `public-information coordination`
- `action_type`: people under home quarantine are prohibited from domestic flight or ferry travel to offshore islands and the passenger-transit ban is extended to April 30
- `dependency_type`: `directive or authority dependency`; `legal or compliance dependency`; `resource or logistics dependency`; `public-communication dependency`
- `implementation_marker`: `implementation initiated`
- `public_information_marker`: `official guidance update`
- `source_citation`: `src-taiwan-home-quarantine-domestic-travel-ban-2020`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`; `sigma3`

Why it matters:

This event improves the Taiwan branch's transport and local-routing visibility. It shows the quarantine regime reaching beyond inbound screening into domestic movement control for offshore-island travel while also carrying the transit-ban continuity forward.

### `tw-p-007`

- `timestamp_or_date`: `2020-04-01`
- `issuing_unit`: `strategic executive coordination`
- `receiving_units`: `public-health policy and command`; `public-service system coordination`; `enforcement and compliance`; `public-information coordination`
- `action_type`: cumulative penalties and group-quarantine escalation clarified for home quarantine and home isolation breaches
- `dependency_type`: `legal or compliance dependency`; `information or reporting dependency`; `public-communication dependency`
- `implementation_marker`: `implementation clarified`
- `public_information_marker`: `enforcement or compliance communication`
- `source_citation`: `src-taiwan-cumulative-penalties-home-quarantine-2020`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`; `sigma3`

Why it matters:

This event improves the comparator's implementation-side thickness beyond border restriction headlines. It makes sanction logic and quarantine enforcement more legible as routed coordination rather than background compliance noise.

### `tw-p-008`

- `timestamp_or_date`: `2020-04-02`
- `issuing_unit`: `strategic executive coordination`
- `receiving_units`: `public-health policy and command`; `public-service system coordination`; `border-control coordination`; `public-information coordination`
- `action_type`: symptomatic inbound travelers at airport or port routed by epidemic-prevention taxis to designated testing and medical-evaluation locations starting April 3
- `dependency_type`: `directive or authority dependency`; `resource or logistics dependency`; `public-communication dependency`
- `implementation_marker`: `decision announced`
- `public_information_marker`: `official guidance update`
- `source_citation`: `src-taiwan-symptomatic-travelers-designated-location-2020`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`; `sigma3`

Why it matters:

This event adds a cleaner operational routing chain between the border surface and downstream medical handling. It improves functional separation inside the Taiwan branch without requiring a broader architecture rewrite.

### `tw-p-009`

- `timestamp_or_date`: `2020-04-14`
- `issuing_unit`: `strategic executive coordination`
- `receiving_units`: `public-health policy and command`; `public-service system coordination`; `border-control coordination`; `enforcement and compliance`; `public-information coordination`
- `action_type`: inbound travelers from Europe and the Americas required to notify health officials before return and use quarantine hotels when home conditions are unsuitable
- `dependency_type`: `directive or authority dependency`; `resource or logistics dependency`; `legal or compliance dependency`; `public-communication dependency`
- `implementation_marker`: `decision announced`
- `public_information_marker`: `official guidance update`
- `source_citation`: `src-taiwan-quarantine-hotels-europe-americas-2020`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`; `sigma3`

Why it matters:

This event gives the Taiwan branch a more visible quarantine-logistics layer. It makes the comparator less command-centre thin by exposing accommodation and vulnerability-management routing inside the border-control chain.

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

- total seeded events: `12`
- active `sigma1` units visible: `6 / 7`
- active directed edges: `10`
- weighted cross-cluster edge share: `35 / 42 = 0.83`
- mean receiving breadth: `3.5`
- issuing concentration: `strategic executive coordination` issues `10 / 12` seeded events
- public-information coordination receives `12 / 12` seeded events

## Current limit

The Taiwan starter tranche is still thinner than the New Zealand route and remains strongly command-centre visible, even after the quarantine-routing additions. It now carries one conservative lag pair and two non-minimal function-specific issuing events, which is enough for a bounded first comparison. It is still not enough for a strong comparative conclusion.

## Status

`starter comparative ledger`
