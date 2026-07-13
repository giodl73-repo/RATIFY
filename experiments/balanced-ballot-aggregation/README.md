# Balanced Ballot Aggregation

This experiment generates complete synthetic ballots with 100 use points and
100 funding points, then compares methods for constructing one challenger.

Run:

```powershell
python experiments/balanced-ballot-aggregation/simulate.py
```

The output tests fiscal closure, distance from cast ballots, and whether the
result is an actual package selected by a voter. Aggregation forms a candidate;
binding authority still comes from final Yes/No ratification.
