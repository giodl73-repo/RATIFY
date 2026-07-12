# Consensus Rules Geographic Stress Test — V1

> Synthetic aggregation test, not public opinion or a forecast.

Every scenario is calibrated to **52.0% national support** using House seats as a population proxy.

| Scenario | Popular | States | EC votes | Popular rule | State rule | EC rule | Double majority | Territorial veto? |
|---|---:|---:|---:|:---:|:---:|:---:|:---:|:---:|
| uniform | 52.0% | 50/50 | 538/538 | pass | pass | pass | pass | no |
| large_state_concentration | 52.0% | 10/50 | 254/538 | pass | fail | fail | fail | yes |
| small_state_concentration | 52.0% | 42/50 | 316/538 | pass | pass | pass | pass | no |
| profile_polarization | 52.0% | 21/50 | 235/538 | pass | fail | fail | fail | yes |
| large_state_plus_profile | 52.0% | 12/50 | 267/538 | pass | fail | fail | fail | yes |
| small_state_plus_profile | 52.0% | 39/50 | 320/538 | pass | pass | pass | pass | no |

## Formal weighting diagnostics

Equal-state weight per House-seat proxy varies by **52.0×** between the smallest and largest states.
Electoral weight per House-seat proxy varies by **2.89×**.

These ratios describe formal weighting, not the probability that a voter is pivotal.

## Interpretation

Holding national support constant does not hold the result constant under territorial rules. A double majority can demonstrate geographic breadth, but it can also allow a territorially distributed minority to veto a national majority. The experiment therefore treats state concurrence as a legitimacy claim that must earn its place, not as consensus by definition.

## Limits

- House seats are a population proxy, not current state population or turnout.
- State support rates are synthetic and calibrated to the same national support target.
- Electoral votes use winner-take-all aggregation for every jurisdiction, including Maine and Nebraska, solely as a rule comparator.
- The experiment measures aggregation behavior, not voter preferences or constitutional validity.
