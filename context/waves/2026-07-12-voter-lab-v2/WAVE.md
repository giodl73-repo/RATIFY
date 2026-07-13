# Wave: Voter Lab V2 Correlation and Order Effects

## Objective

Replace independent clipped trait sampling with declared correlations and add
card-order and information-decay modules, then bridge-run the comprehension
experiment against Voter Lab v1.

## Pulses

| Pulse | Purpose | Status |
|---|---|---|
| 01 | Specify correlation and sampling contract | complete |
| 02 | Implement bounded correlated agents | complete |
| 03 | Add order and information-decay modules | complete |
| 04 | Run bridge matrix and decide model promotion | complete |

## Decision gate

Does V2 improve behavioral coherence and declared validation criteria without
being tuned to favor a package, voting rule, or comprehension result?

**Decision:** Yes for internal synthetic work. V2 passes structural and bridge
criteria without generating preferences. The current sequential card interface
fails its provisional recovery threshold after order decay and must be revised.
