# First-Pass Sensitivity and Null Note

## Purpose

This file is the current bounded sensitivity and null check for the New Zealand demonstrated route.

It does **not** claim full robustness. It asks a narrower question:

does the route's current bounded gain survive reasonable perturbations and null framings, or does it collapse as soon as the ledger is stressed?

Primary companions:

- [Event Ledger Seed](event-ledger-seed.md)
- [Estimator Implementation](estimator-implementation.md)
- [First-Pass Seed Readout](first-pass-seed-readout.md)
- [First-Pass Window Comparison](first-pass-window-comparison.md)

## Rule for this pass

This note now works from the current `30`-event public ledger and expands the bounded check set to `10` tests total:

- `6` perturbation checks
- `2` additional perturbation-family checks required by the current hardening plan
- `2` null framings

The point is still modest: test whether the route immediately falls apart under plausible stress, not whether it is already estimator-complete.

## Baseline reference

Current baseline:

- `30` total coded events
- `23` main-interval events
- `strategic executive coordination` issues `21 / 30`
- `public-information coordination` receives `25 / 30`
- weighted cross-cluster routing = `86 / 113 = 0.76`

## Sensitivity check 1: remove the most architecture-heavy observation events

Perturbation:

- remove `nz-a-001`
- remove `nz-p-007`

What survives:

- `28` coded events remain
- the main interval still contains `22` events
- `strategic executive coordination` still issues `19 / 28`
- `public-information coordination` still receives `23 / 28`
- all `7 / 7` `sigma1` units still remain active

Reading:

The route does not depend only on a couple of architecture-observation events. The hub-centred shape and the public-information pattern remain visible without them.

## Sensitivity check 2: reassign one implementation paper away from the strategic centre

Perturbation:

- reassign `nz-p-015` from `strategic executive coordination` to `public-service system coordination`

What survives:

- `strategic executive coordination` still issues `20 / 30`
- inside the main interval, the strategic centre still issues `15 / 23`
- `public-information coordination` still receives `25 / 30`
- all `7 / 7` units remain active

Reading:

The route becomes slightly less monopolized by the strategic centre, which is exactly why this perturbation matters. But the route still reads as hub-centred rather than flat.

## Sensitivity check 3: split one bundled escalation event into two same-day events

Perturbation:

- split `nz-p-010` into:
  - a Level 3 transition announcement event
  - a Level 4-in-48-hours escalation-preparation event

What survives:

- the ledger rises from `30` to `31` events
- `strategic executive coordination` rises to `22 / 31`
- the main interval rises from `23` to `24` events
- public-information participation remains visible in the split chain
- the route still preserves non-zero lag between the `2020-03-23` announcement side and the `2020-03-25` implementation side

Reading:

The route does not flatten under same-day splitting. If anything, the acute escalation chain looks more visibly sequenced.

## Sensitivity check 4: remove the Comparator B legal-handoff event

Perturbation:

- remove `nz-b-005`

What survives:

- Comparator B still contains `4` coded events
- Comparator B still keeps `6 / 7` active units
- Comparator B still has explicit public-information markers in `4 / 4` remaining events
- the lower-acuity transition window still looks more coherent and denser than Comparator A

Reading:

Comparator B becomes thinner, but it does not collapse into a mere labeling artifact.

## Sensitivity check 5: boundary-cut perturbation

Perturbation:

- remove `nz-p-019`
- remove `nz-p-023`

Why these two:

- they sit on the welfare and boundary-handling edge of the implementation layer
- a skeptical reader could argue they are helpful thickening rather than core coordination

What survives:

- `28` coded events remain
- the main interval still contains `21` events
- `strategic executive coordination` still issues `20 / 28`
- `public-information coordination` still receives `24 / 28`

Reading:

The route loses some welfare/boundary detail, but the main structural payoff still holds.

## Sensitivity check 6: `sigma2` cluster-reassignment perturbation

Perturbation:

- reclassify `public-service system coordination` from the strategic cluster into the response-operations cluster

What changes:

- weighted cross-cluster routing rises from `86 / 113 = 0.76` to `96 / 113 = 0.85`

Reading:

The integration reading does **not** depend on one favorable `sigma2` placement. Under this reassignment, the cross-cluster signal becomes stronger, not weaker. That means the current clustering choice is conservative for the route's integration claim.

## Sensitivity check 7: chronology-gap / missingness perturbation

Perturbation:

- remove `nz-p-023` as if the local-authority/CDEM welfare-support paper were missing from the public record

What survives:

- the ledger falls only to `29` events
- the main interval still contains `22` events
- `strategic executive coordination` still issues `21 / 29`
- `public-information coordination` still receives `25 / 29`

Reading:

The route does not depend on perfect completeness in one late-April implementation paper. Missingness weakens detail, but not the current bounded gain.

## Sensitivity check 8: interval-boundary perturbation

Perturbation:

- remove `nz-p-019`
- remove `nz-p-020`

Why these two:

- they are the strongest newly admitted left-side thickening events inside the post-lockdown build-out

What survives:

- `28` coded events remain
- the main interval still contains `21` events
- `strategic executive coordination` still issues `20 / 28`
- `public-information coordination` still receives `23 / 28`

Reading:

Even if the early-April implementation thickening were thinner than currently coded, the route would still retain a dense main interval with a visible strategic centre and strong public-information involvement.

## Null check 1: treat public-information coordination as downstream messaging only

Null framing:

public-information coordination is only an output wrapper around "real" executive action and should not count as part of the route's working coordination architecture.

Why the null is weak:

- `public-information coordination` receives `25 / 30` coded events
- it remains active across all Comparator B boundary events
- it is visible not only at acute alert-level transitions but also in compliance guidance, checkpoint governance, and the later transition chain

Reading:

To preserve this null, a reader has to discard a large amount of visible routing activity.

## Null check 2: collapse decision and implementation into the same moment

Null framing:

decision and implementation are effectively the same moment, so lag should not count as a meaningful category.

Why the null is weak:

- the current public ledger still contains paired gaps of `1`, `2`, `3`, and `8` days
- those pairs span both acute escalation and later easing transitions
- the newly admitted DPMC papers thicken the implementation context around those pairs without erasing the staged gaps

Reading:

This null erases visible structure that is already present even at date grain.

## First bounded conclusion

The most defensible current sensitivity/null reading is:

**The route's current bounded gains survive architecture-event removal, one issuer reassignment, one same-day split, a Comparator B legal-handoff removal, a welfare/boundary cut, a chronology-gap perturbation, and an interval-boundary perturbation. They also remain stronger than the two flattest null framings currently available.**

That is still modest. It does **not** mean the route is already fully robust. It means the current payoff is sturdier than a one-pass impression.

## Next best step

The next practical move is to:

1. keep adding direct D-family `D` and `E` events only under the live-plus-fixed-archive rule
2. test the current route again after the first Taiwan tranche exists
3. then move from bounded robustness checks toward a more explicit estimator-stage perturbation program

## Status

`expanded first-pass sensitivity and null note`
