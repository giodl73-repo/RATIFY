# Wave: Persistent Candidate Comparison

## Objective

Test whether a persistent three-field difference strip and common-facts refresh
reduce second-card information decay without increasing framing asymmetry or
ballot overload.

## Pulses

| Pulse | Purpose | Status |
|---|---|---|
| 01 | Specify persistent comparison interface | complete |
| 02 | Implement refresh and side-by-side modules | complete |
| 03 | Run V2 order, fatigue, and framing matrix | complete |
| 04 | Select interface for human testing | complete |

## Decision gate

Can the interface keep every primary fact at or above the provisional 70%
synthetic recovery threshold in neutral central-fatigue tests, with no more than
two points of candidate or order asymmetry and no overload regression?

**Decision:** Yes, only for the persistent strip plus common-facts refresh. Its
weakest fact is 73.3%, candidate gap 0.13 points, and maximum order gap 0.55
points in the declared synthetic test. This selects a human-test candidate, not
a public interface.
