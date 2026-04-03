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
| `src-dpmc-national-transition-period-2020` | `D-family D` | later Comparator B hardening | `verified` | `verified` | `accepted, held` | durable and relevant, but not required for the current five-event main-interval tranche |
| `src-police-level-3-following-rules-2020` | `D-family E` | `2020-04-28` Level 3 compliance continuity | `verified` | `not verified` | `rejected for now` | live page exists but no fixed archive URL was confirmed |
| `src-dpmc-review-alert-level4-paper-minute-2020` | `D-family D` | `2020-04-20` review of Alert Level 4 | `not promoted` | `not verified` | `rejected for now` | save attempt on the migrated PDF path did not yield a fixed archive |
| `src-dpmc-alert-level-framework-details-2020` | `D-family D` | `2020-04-15` Levels 1-3 details and implementation | `verified` | `not verified` | `rejected for now` | live paper known, but no exact fixed capture was confirmed in this pass |
| `src-dpmc-national-transition-period-migrated-path-2020` | `D-family D` | `2020-05-12` national transition period | `verified` | `not verified` | `replaced` | migrated-path save failed; replaced by the original 2020 release-path source above |

## Current admission result

This tranche adds five newly admitted implementation-side sources to the live route and keeps three unstable candidates out of the public ledger.

That is enough to:

- move the ledger past the `30`-event gate if all five accepted sources are coded
- keep the source-promotion rule clean
- avoid reintroducing wildcard archive debt into the route

## Status

`active discovery control log`

## Taiwan starter log

The first Taiwan comparator tranche follows the same admission rule: no source is promoted unless both the live URL and a fixed archive URL are verified.

| Candidate source | Family | Event or use target | Live URL | Fixed archive | Decision | Reason |
|---|---|---|---|---|---|---|
| `src-taiwan-cecc-activation-2020` | `A-family / comparator architecture` | `2020-01-20` CECC activation | `verified` | `verified` | `accepted` | direct official command-centre activation anchor |
| `src-taiwan-home-quarantine-support-2020` | `D/E-family bridge` | `2020-02-15` home-quarantine support and care | `verified` | `verified` | `accepted` | direct quarantine-support and follow-up anchor |
| `src-taiwan-entry-restrictions-home-quarantine-2020` | `E-family` | `2020-03-18` entry restrictions and local quarantine procedure | `verified` | `verified` | `accepted` | direct border restriction plus local-district reporting anchor |
| `src-taiwan-transit-ban-2020` | `E-family` | `2020-03-22` passenger-transit ban | `verified` | `verified` | `accepted` | direct transit-ban timing anchor |
| `src-taiwan-home-quarantine-isolation-regulations-2020` | `D/E-family bridge` | `2020-03-27` quarantine/isolation regulations and local care/support | `verified` | `verified` | `accepted` | direct compliance and care-routing anchor |
| `src-taiwan-transit-extension-2020` | `E-family` | `2020-04-23` extension of flight and transit restrictions | `verified` | `verified` | `accepted` | direct continuity anchor for the starter acute window |
| `vmv22PiH7-k3K-yh6FkmKw` | `candidate check` | pre-comparator architecture scan | `verified` | `verified` | `promoted under source id` | normalized to `src-taiwan-cecc-activation-2020` |
| `pVg_jRVvtHhp94C6GShRkQ` | `candidate check` | additional early Taiwan bulletin | `not promoted` | `not verified` | `rejected for now` | no verified fixed archive in this pass |
| `kM0jm-IqLwNBeT6chKk_wg` | `candidate check` | additional Taiwan border bulletin | `not promoted` | `not verified` | `rejected for now` | no verified fixed archive in this pass |

## Taiwan starter result

This is enough to open a strict first Taiwan comparative tranche without weakening the archive rule.
