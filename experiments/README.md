# Experiments

Experiments are synthetic and reproducible. They do not predict elections or
claim to represent public opinion.

## Planned families

1. Annual 100-point budget ballot generalized from TAXLANE.
2. Popular versus state versus electoral-weighted aggregation.
3. Double-majority and supermajority stress tests.
4. Program reauthorization under status-quo, reform, and sunset choices.
5. Ballot-information, polarization, turnout, and strategic-voting stress tests.
6. Minority-rights and geographic-veto failure-mode tests.

Every output must state its population model, preference assumptions, turnout
model, information assumptions, aggregation rule, random seed, and limitations.

The first implemented family is `consensus-rules/`, which holds national
support fixed while changing geographic distribution and compares popular,
state, electoral-weighted, double-majority, and stronger-consensus rules.

`capture-framing/` holds fiscally closed packages fixed while varying incumbent
branding, paid advocacy, funding disclosure, evidence quality, and ballot
overload. Its effect sizes are declared synthetic assumptions, not behavioral
estimates.

`balanced-ballot-aggregation/` compares methods for turning complete 100-point
use-and-funding ballots into one fiscally closed challenger for later Yes/No
ratification.
