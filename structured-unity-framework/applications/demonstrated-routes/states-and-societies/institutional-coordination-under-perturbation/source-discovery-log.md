# Source Discovery Log

## Purpose

This file records candidate route sources before they are promoted into the public New Zealand route.

For the current hardening pass, a source is promoted only if:

- it is official or oversight material from Families `A-F`
- it adds boundary, timing, implementation, or dependency detail
- the live public URL is verified
- a fixed archive URL is verified

Unstable candidates stay here and do not enter the ledger.

## Current tranche log

| Candidate source | Family | Event or use target | Live URL | Fixed archive | Decision | Reason |
|---|---|---|---|---|---|---|
| `src-dpmc-stranded-people-2020` | `D-family D/E bridge` | `2020-03-31` stranded-people coordination plan | `verified` | `verified` | `accepted` | direct Cabinet-minute anchor for stranded-people coordination |
| `src-dpmc-quarantine-managed-isolation-welfare-2020` | `D-family D/E bridge` | `2020-04-02` welfare of people in quarantine and managed isolation | `verified` | `verified` | `accepted` | direct welfare and managed-isolation coordination anchor |
| `src-dpmc-cdem-powers-guidance-2020` | `D-family D` | `2020-04-09` CDEM key-powers guidance | `verified` | `verified` | `accepted` | direct emergency-powers and authority-routing anchor |
| `src-dpmc-review-level4-status-2020` | `D-family D` | `2020-04-14` Level 4 review preparation | `verified` | `verified` | `accepted` | direct review-preparation anchor for the easing chain |
| `src-dpmc-local-authority-welfare-support-2020` | `D-family D` | `2020-04-21` widened local-authority/CDEM welfare support | `verified` | `verified` | `accepted` | direct local-authority and CDEM implementation-support anchor |
| `src-dpmc-national-transition-period-2020` | `D-family D` | `2020-05-12` Comparator B transition-period planning | `verified` | `verified` | `accepted and coded` | durable direct transition-period planning anchor now promoted into the ledger |
| `src-police-level-3-following-rules-2020` | `D-family E` | `2020-04-28` Level 3 compliance continuity | `verified` | `verified` | `accepted and coded` | fixed archive confirmed; direct Level 3 compliance-continuity page promoted into the ledger |
| `src-police-covid-major-events-2020` | `D-family E` | `2020-05-01` and `2020-05-08` Level 3 continuity chronology | `verified` | `verified` | `accepted and coded` | exact-date official Police chronology page now used for late-Level-3 continuity events |
| `src-dpmc-powers-authorisations-level3-2020` | `D-family D/E bridge` | `2020-04-22` Level 3 powers and authorisations | `verified` | `verified` | `accepted, held` | exact fixed archive now confirmed; held out of the v1 freeze pass because one additional late-transition D event was sufficient for the bounded stop rule |
| `src-dpmc-preparing-review-level3-status-2020` | `D-family D` | `2020-05-04` review-preparation for Level 3 status | `verified` | `verified` | `accepted, held` | exact fixed archive now confirmed; held for later route deepening after the bounded v1 stop rule was met |
| `src-dpmc-preparing-for-alert-level-2-2020` | `D-family D` | `2020-05-06` Alert Level 2 preparation | `verified` | `verified` | `accepted and coded` | exact fixed archive confirmed; promoted as the final late-transition DPMC preparation anchor in the v1 pass |
| `src-dpmc-review-alert-level3-2020` | `D-family D` | `2020-05-11` review of Alert Level 3 | `verified` | `verified` | `accepted, held` | exact fixed archive now confirmed; held for later route deepening after the bounded v1 stop rule was met |
| `src-dpmc-review-alert-level4-paper-minute-2020` | `D-family D` | `2020-04-20` review of Alert Level 4 | `not promoted` | `not verified` | `rejected for now` | save attempt on the migrated PDF path did not yield a fixed archive |
| `src-dpmc-alert-level-framework-details-2020` | `D-family D` | `2020-04-15` Levels 1-3 details and implementation | `verified` | `verified under promoted id` | `superseded` | promoted publicly as `src-dpmc-alert-level-implementation-2020` |
| `src-dpmc-national-transition-period-migrated-path-2020` | `D-family D` | `2020-05-12` national transition period | `verified` | `not verified` | `replaced` | migrated-path save failed; replaced by the original 2020 release-path source above |

## Current admission result

This tranche confirms one additional late-transition DPMC preparation source for the live route and also resolves the archive status of the remaining late-transition DPMC PDFs. The v1 pass promotes only one of those newly archive-clean DPMC papers into the ledger and leaves the others held for later deepening.

That is enough to:

- deepen Comparator B and late-Level-3 continuity without weakening the archive rule
- keep the source-promotion rule clean
- replace the earlier archive-uncertainty note with a cleaner bounded-stop note for the v1 freeze pass

## Status

`active discovery control log`

## Taiwan starter log

The first Taiwan comparator tranche follows the same admission rule: no source is promoted unless both the live URL and a fixed archive URL are verified.

| Candidate source | Family | Event or use target | Live URL | Fixed archive | Decision | Reason |
|---|---|---|---|---|---|---|
| `src-taiwan-cecc-activation-2020` | `A-family / comparator architecture` | `2020-01-20` CECC activation | `verified` | `verified` | `accepted and coded` | direct official command-centre activation anchor |
| `src-taiwan-home-quarantine-support-2020` | `D/E-family bridge` | `2020-02-15` home-quarantine support and care | `verified` | `verified` | `accepted and coded` | direct quarantine-support and follow-up anchor |
| `src-taiwan-entry-restrictions-home-quarantine-2020` | `E-family` | `2020-03-18` entry restrictions and local quarantine procedure | `verified` | `verified` | `accepted and coded` | direct border restriction plus local-district reporting anchor |
| `src-taiwan-transit-ban-2020` | `E-family` | `2020-03-22` passenger-transit ban | `verified` | `verified` | `accepted and coded` | direct transit-ban timing anchor |
| `src-taiwan-home-quarantine-isolation-regulations-2020` | `D/E-family bridge` | `2020-03-27` quarantine/isolation regulations and local care/support | `verified` | `verified` | `accepted and coded` | direct compliance and care-routing anchor |
| `src-taiwan-all-travelers-home-quarantine-2020` | `E-family` | `2020-02-08` universal home-quarantine shift | `verified` | `verified` | `accepted and coded` | direct early quarantine-control and transit-restriction anchor |
| `src-taiwan-cumulative-penalties-home-quarantine-2020` | `D/E-family bridge` | `2020-04-01` cumulative penalties and group-quarantine escalation | `verified` | `verified` | `accepted and coded` | direct compliance-and-sanction anchor with local care/support consequences |
| `src-taiwan-home-quarantine-health-agency-routing-2020` | `D/E-family bridge` | `2020-03-29` health-agency notification and medical-care routing observed during home quarantine | `verified` | `verified` | `accepted and coded` | direct implementation-observed quarantine-routing anchor now used as the first conservative Taiwan lag-pair partner |
| `src-taiwan-home-quarantine-domestic-travel-ban-2020` | `D/E-family bridge` | `2020-04-01` offshore-island travel prohibition for people under home quarantine and transit-ban extension | `verified` | `verified` | `accepted and coded` | direct quarantine-travel and border-continuity anchor that improves local-administrative and transport routing visibility |
| `src-taiwan-symptomatic-travelers-designated-location-2020` | `D/E-family bridge` | `2020-04-02` designated transport and testing routing for symptomatic inbound travelers | `verified` | `verified` | `accepted and coded` | direct point-of-entry screening and transport-logistics anchor |
| `src-taiwan-quarantine-hotels-europe-americas-2020` | `D/E-family bridge` | `2020-04-14` quarantine-hotel and pre-boarding notification routing | `verified` | `verified` | `accepted and coded` | direct quarantine-hotel and pre-return notification anchor |
| `src-taiwan-transit-extension-2020` | `E-family` | `2020-04-23` extension of flight and transit restrictions | `verified` | `verified` | `accepted and coded` | direct continuity anchor for the starter acute window |
| `vmv22PiH7-k3K-yh6FkmKw` | `candidate check` | pre-comparator architecture scan | `verified` | `verified` | `promoted under source id` | normalized to `src-taiwan-cecc-activation-2020` |
| `pVg_jRVvtHhp94C6GShRkQ` | `candidate check` | additional early Taiwan bulletin | `not promoted` | `not verified` | `rejected for now` | no verified fixed archive in this pass |
| `kM0jm-IqLwNBeT6chKk_wg` | `candidate check` | additional Taiwan border bulletin | `not promoted` | `not verified` | `rejected for now` | no verified fixed archive in this pass |

## Taiwan starter result

This is enough to deepen the Taiwan comparator from a `10`-event starter into a `12`-event archive-clean tranche without weakening the archive rule.

It also makes one conservative lag pair visible:

- `2020-03-18` foreign-entry restriction and local-district quarantine routing announcement
- `2020-03-29` health-agency notification and medical-care routing observed during home quarantine
