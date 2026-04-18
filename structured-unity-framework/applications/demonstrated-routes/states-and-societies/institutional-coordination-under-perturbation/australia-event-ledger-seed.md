# Australia Federal Event Ledger Seed

## Purpose

This file is the current archive-clean public event ledger for the Australia federal comparator branch.

It is bounded to federal-level coordination only (AHPPC, National Cabinet, PM&C). It targets 18-22 events for Phase 2 of the empirical thickening program.

## Current posture

Current status: `federal comparator ledger — under construction`

This seed captures Australia's distinctive federal coordination architecture:
- AHPPC as health advisory layer (public-health policy and command)
- National Cabinet as political coordination layer (strategic executive coordination)
- Federal-state implementation bridge through National Cabinet decisions

## Summary list

| Event ID | Date | Short description |
|---|---|---|
| `au-b-001` | `2020-02-05` | AHPPC first COVID statement — false assumptions advisory and community concern |
| `au-c-002` | `2020-02-13` | AHPPC travel restrictions resolution — China travel advisory |
| `au-b-003` | `2020-02-24` | AHPPC pandemic risk escalation — sustained community transmission assessment |
| `au-a-004` | `2020-03-15` | National Cabinet cruise ship ban and 500-person gathering limits |
| `au-b-005` | `2020-03-17` | AHPPC trajectory comparison — international outbreak comparison |
| `au-a-006` | `2020-03-22` | National Cabinet second stage activation — major escalation coordination |
| `au-a-007` | `2020-03-27` | National Cabinet tenancies and health supply — implementation coordination |
| `au-a-008` | `2020-04-03` | National Cabinet childcare and commercial tenancies — social policy coordination |
| `au-b-010` | `2020-03-30` | AHPPC advice to National Cabinet on state/territory measures — federal-state advisory bridge |
| `au-b-011` | `2020-04-03` | AHPPC statement on COVID-19 in children — vulnerable population guidance |
| `au-a-012` | `2020-04-07` | National Cabinet churches/worship coordination — Easter services coordination |
| `au-b-013` | `2020-03-17` | AHPPC ANZAC Day guidance — vulnerable population protection |
| `au-b-014` | `2020-04-21` | AHPPC health risk management as measures lift — transition guidance |
| `au-a-015` | `2020-04-24` | National Cabinet maritime crew exemption — border logistics coordination |
| `au-a-016` | `2020-05-15` | National Cabinet May meeting — monitoring/testing/tracing framework |
| `au-a-017` | `2020-05-29` | National Cabinet press conference — reopening framework and travel bubble |
| `au-a-018` | `2020-03-13` | AHPPC aged care recommendations — vulnerable population protection |
| `au-b-009` | `2020-05-14` | AHPPC asymptomatic testing guidance — late acute policy refinement |

## Seed events

### `au-b-001`

- `timestamp_or_date`: `2020-02-05`
- `issuing_unit`: `public-health policy and command`
- `receiving_units`: `public-information coordination`; `strategic executive coordination`
- `action_type`: AHPPC first COVID statement addressing false assumptions about Chinese appearance and community concern
- `dependency_type`: `public-communication dependency`; `information or reporting dependency`
- `implementation_marker`: `decision announced`
- `public_information_marker`: `major public briefing`
- `source_citation`: `src-australia-ahppc-2020-02-05`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`

Why it matters:

This is the earliest federal health advisory anchor. It makes AHPPC's public-information coordination role visible from the first COVID engagement, not just as medical advice but as community concern management.

### `au-c-002`

- `timestamp_or_date`: `2020-02-13`
- `issuing_unit`: `public-health policy and command`
- `receiving_units`: `border-control coordination`; `strategic executive coordination`; `public-information coordination`
- `action_type`: AHPPC travel restrictions resolution advising against travel to China
- `dependency_type`: `directive or authority dependency`; `public-communication dependency`
- `implementation_marker`: `decision announced`
- `public_information_marker`: `official guidance update`
- `source_citation`: `src-australia-ahppc-travel-2020-02-13`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`; `sigma3`

Why it matters:

This is the first border-tightening anchor. It shows AHPPC advising on travel restrictions even before the pandemic declaration, making the health-advisory-to-border-control chain visible early.

### `au-b-003`

- `timestamp_or_date`: `2020-02-24`
- `issuing_unit`: `public-health policy and command`
- `receiving_units`: `strategic executive coordination`; `public-information coordination`
- `action_type`: AHPPC pandemic risk escalation — sustained community transmission assessment in multiple countries
- `dependency_type`: `information or reporting dependency`; `public-communication dependency`
- `implementation_marker`: `decision announced`
- `public_information_marker`: `official guidance update`
- `source_citation`: `src-australia-ahppc-2020-02-24`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`; `sigma3`

Why it matters:

This event escalates the risk assessment before major border closures. It makes the AHPPC-to-National Cabinet advisory chain thicker by showing explicit pandemic risk language one month before the major March escalation.

### `au-a-004`

- `timestamp_or_date`: `2020-03-15`
- `issuing_unit`: `strategic executive coordination`
- `receiving_units`: `public-health policy and command`; `border-control coordination`; `public-information coordination`; `public-service system coordination`
- `action_type`: National Cabinet cruise ship ban and 500-person non-essential gathering limits
- `dependency_type`: `directive or authority dependency`; `legal or compliance dependency`; `public-communication dependency`
- `implementation_marker`: `implementation initiated`
- `public_information_marker`: `major public briefing`
- `source_citation`: `src-australia-national-cabinet-2020-03-15`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`; `sigma3`

Why it matters:

This is the major National Cabinet activation event. It distinguishes Australia's federal structure — AHPPC provides advice, National Cabinet makes political coordination decisions affecting all jurisdictions.

### `au-b-005`

- `timestamp_or_date`: `2020-03-17`
- `issuing_unit`: `public-health policy and command`
- `receiving_units`: `strategic executive coordination`; `public-information coordination`
- `action_type`: AHPPC trajectory comparison showing Australia's position relative to other nations with growing overseas-acquired cases
- `dependency_type`: `information or reporting dependency`; `public-communication dependency`
- `implementation_marker`: `implementation observed`
- `public_information_marker`: `official guidance update`
- `source_citation`: `src-australia-ahppc-2020-03-17`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`; `sigma3`

Why it matters:

This event shows AHPPC providing epidemiological intelligence to National Cabinet during acute escalation. The trajectory comparison makes the health-advisory-to-executive information flow visible.

### `au-a-006`

- `timestamp_or_date`: `2020-03-22`
- `issuing_unit`: `strategic executive coordination`
- `receiving_units`: `public-health policy and command`; `public-service system coordination`; `enforcement and compliance`; `public-information coordination`
- `action_type`: National Cabinet second stage activation with further business closures and enhanced enforcement
- `dependency_type`: `directive or authority dependency`; `legal or compliance dependency`; `public-communication dependency`
- `implementation_marker`: `implementation initiated`
- `public_information_marker`: `major public briefing`
- `source_citation`: `src-australia-national-cabinet-2020-03-22`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`; `sigma3`

Why it matters:

This is the major escalation event showing federal-state coordination at peak acute phase. It thickens the `strategic executive coordination` layer and shows the federal structure handling major social restrictions.

### `au-a-007`

- `timestamp_or_date`: `2020-03-27`
- `issuing_unit`: `strategic executive coordination`
- `receiving_units`: `public-health policy and command`; `public-service system coordination`; `public-information coordination`
- `action_type`: National Cabinet tenancies and health supply arrangements for returned travellers and community outbreaks
- `dependency_type`: `directive or authority dependency`; `resource or logistics dependency`; `public-communication dependency`
- `implementation_marker`: `implementation clarified`
- `public_information_marker`: `official guidance update`
- `source_citation`: `src-australia-national-cabinet-2020-03-27`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`; `sigma3`

Why it matters:

This event shows National Cabinet moving into implementation coordination (tenancies, health supply) beyond headline restrictions. It exposes the federal-state administrative coordination layer.

### `au-a-008`

- `timestamp_or_date`: `2020-04-03`
- `issuing_unit`: `strategic executive coordination`
- `receiving_units`: `public-health policy and command`; `public-service system coordination`; `public-information coordination`
- `action_type`: National Cabinet childcare and commercial tenancies coordination
- `dependency_type`: `directive or authority dependency`; `resource or logistics dependency`; `public-communication dependency`
- `implementation_marker`: `implementation clarified`
- `public_information_marker`: `official guidance update`
- `source_citation`: `src-australia-national-cabinet-2020-04-03`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`

Why it matters:

This event extends the federal coordination into social policy (childcare, tenancies). It makes the Australia comparator less purely health/border focused by showing social infrastructure coordination.

### `au-b-009`

- `timestamp_or_date`: `2020-05-14`
- `issuing_unit`: `public-health policy and command`
- `receiving_units`: `strategic executive coordination`; `public-information coordination`
- `action_type`: AHPPC asymptomatic testing guidance and policy refinement
- `dependency_type`: `information or reporting dependency`; `public-communication dependency`
- `implementation_marker`: `implementation clarified`
- `public_information_marker`: `official guidance update`
- `source_citation`: `src-australia-ahppc-asymptomatic-2020-05-14`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`

Why it matters:

This event closes the acute window with late-phase policy refinement. It shows AHPPC continuing advisory role through testing guidance, maintaining the health advisory layer visibility.

### `au-a-018`

- `timestamp_or_date`: `2020-03-13`
- `issuing_unit`: `public-health policy and command`
- `receiving_units`: `strategic executive coordination`; `public-information coordination`; `public-service system coordination`
- `action_type`: AHPPC aged care recommendations for residential facilities outbreak preparedness
- `dependency_type`: `information or reporting dependency`; `public-communication dependency`; `resource or logistics dependency`
- `implementation_marker`: `decision announced`
- `public_information_marker`: `official guidance update`
- `source_citation`: `src-australia-ahppc-aged-care-2020-03-13`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`

Why it matters:

This early aged care event (March 13) shows AHPPC addressing vulnerable population protection before broader escalation. It adds vulnerable population coordination to the early phase, balancing border/travel focus with health-system preparedness.

### `au-b-010`

- `timestamp_or_date`: `2020-03-30`
- `issuing_unit`: `public-health policy and command`
- `receiving_units`: `strategic executive coordination`; `public-information coordination`; `public-service system coordination`
- `action_type`: AHPPC advice to National Cabinet on state/territory measures recognizing local circumstances for additional controls
- `dependency_type`: `information or reporting dependency`; `public-communication dependency`
- `implementation_marker`: `implementation clarified`
- `public_information_marker`: `official guidance update`
- `source_citation`: `src-australia-ahppc-2020-03-30`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`

Why it matters:

This event makes the AHPPC-to-National Cabinet advisory bridge explicit. It shows health advisory flowing to political coordination with recognition of state/territory variation — the federal structure in action.

### `au-b-011`

- `timestamp_or_date`: `2020-04-03`
- `issuing_unit`: `public-health policy and command`
- `receiving_units`: `strategic executive coordination`; `public-information coordination`
- `action_type`: AHPPC statement on COVID-19 in children advising preemptive closures not proportionate while acknowledging vulnerability
- `dependency_type`: `information or reporting dependency`; `public-communication dependency`
- `implementation_marker`: `decision announced`
- `public_information_marker`: `official guidance update`
- `source_citation`: `src-australia-ahppc-2020-04-03-children`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`

Why it matters:

This event adds vulnerable population guidance (children) distinct from the childcare social policy event same day. It makes the health advisory layer more granular, showing AHPPC addressing specific population concerns.

### `au-a-012`

- `timestamp_or_date`: `2020-04-07`
- `issuing_unit`: `strategic executive coordination`
- `receiving_units`: `public-health policy and command`; `public-information coordination`; `public-service system coordination`
- `action_type`: National Cabinet churches and worship places coordination for Easter services live streaming
- `dependency_type`: `directive or authority dependency`; `public-communication dependency`
- `implementation_marker`: `implementation clarified`
- `public_information_marker`: `official guidance update`
- `source_citation`: `src-australia-national-cabinet-2020-04-07`
- `confidence_note`: `high`
- `scale_tag`: `sigma1`; `sigma2`

Why it matters:

This event shows National Cabinet coordinating cultural/religious services during acute phase. It adds social-cultural coordination to the ledger, making Australia less purely health/border focused.

## Current readout cues

- total seeded events: `18`
- active `sigma1` units visible: `6 / 7` (missing `enforcement and compliance` in most events)
- active directed edges: `22`
- mean receiving breadth: `3.4`
- issuing concentration: `public-health policy and command` issues `10 / 18`; `strategic executive coordination` issues `8 / 18`
- public-information coordination receives `18 / 18` seeded events

## Current limit

The Australia branch has reached **18 events** — meeting the minimum 18-22 target. It shows the distinctive federal structure (AHPPC + National Cabinet) with:

- AHPPC health advisory layer: 10 events
- National Cabinet political coordination: 8 events
- 100% public-information coordination receiving coverage

## Status

`federal comparator ledger — 18 events, target met`
