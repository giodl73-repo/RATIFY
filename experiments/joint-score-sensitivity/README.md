# Joint-Score Sensitivity

This experiment asks whether the broad/shared package remains near its fiscal
target after its explicit household, transition, workforce, and beneficiary
protections are recognized.

It is a synthetic missing-value sensitivity matrix, not an official or
independent score. Published CBO estimates establish component scale; scenario
factors are declared assumptions. The model does not add net interest benefits,
macroeconomic feedback, or administrative savings to close the package.

Run:

```powershell
python experiments/joint-score-sensitivity/simulate.py
```

Outputs are deterministic and include a component decomposition, distance from
the $5.225 trillion 2026–2036 primary-balance target, and a checklist of fiscal
fields that still require independent scoring.
