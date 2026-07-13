# Balanced Ballot Aggregation — V1

> Synthetic method test, not public opinion.

Generated **6,000** complete ballots. Every ballot allocates 100 use points and 100 funding points.

| Method | Uses | Funding | Closure gap | Mean voter distance | Actual ballot? |
|---|---:|---:|---:|---:|:---:|
| arithmetic_mean | 100.000 | 100.000 | +0.000 | 49.906 | no |
| fieldwise_median | 81.650 | 85.649 | -3.999 | 51.441 | no |
| fieldwise_trimmed_mean_10_percent | 91.189 | 92.411 | -1.222 | 50.283 | no |
| feasible_geometric_median | 100.000 | 100.000 | +0.000 | 49.902 | no |
| approximate_actual_ballot_medoid | 100.000 | 100.000 | +0.000 | 51.280 | yes |

## Result

**2 of 5 methods break fiscal closure without an additional repair rule.**
The arithmetic mean and feasible geometric median preserve closure because they remain weighted combinations of complete ballots. The actual-ballot medoid is both closed and interpretable as a package somebody really chose. Fieldwise robust statistics can splice dimensions together and require a disclosed feasibility repair.

## Ratification use

Aggregation constructs a candidate challenger; it does not enact law. The resulting complete package still receives legal, fiscal, rights, distribution, and implementation review before facing current law in a Yes/No ratification.
