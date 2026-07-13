# Voter Lab

Voter Lab is RATIFY's shared agent-based simulation layer. It replaces isolated
experiment-specific “personality” lists with versioned continuous traits,
situational state, behavioral modules, institutional environments, and a
calibration ladder.

Version 1 contains synthetic priors only. It is not calibrated public opinion.

Validate:

```powershell
python experiments/voter-lab/validate.py
```

## Development loop

1. Add or revise a mechanism only with a falsifiable behavioral hypothesis.
2. Run the common scenario matrix and retain bridge comparisons to the prior model.
3. Calibrate against sourced data without tuning for a preferred voting rule.
4. Test held-out cases.
5. Publish mismatches, uncertainty, and disabled mechanisms.
6. Promote a model version only when it improves declared validation criteria.

Future work will add bounded correlated sampling, network topologies, turnout,
information updating, strategic behavior, repeated cycles, and calibration
adapters.
