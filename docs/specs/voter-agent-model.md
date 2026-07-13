# Voter Agent Model Contract

## Traffic-simulation analogy

Traffic microsimulators do not model every driver as identical or assign one
permanent “driver type.” They combine continuous traits, vehicle and road
constraints, local information, interactions, and changing conditions. RATIFY
should model voters the same way.

An archetype is a sampling distribution and an interpretive label—not a claim
that a person belongs to a fixed political species.

## Agent layers

### Stable or slowly changing traits

- outcome orientation;
- pocketbook sensitivity;
- fiscal and debt concern;
- risk and uncertainty tolerance;
- status-quo preference;
- institutional trust;
- anti-establishment orientation;
- rights and minority-protection concern;
- issue intensity and breadth;
- numeracy and policy familiarity;
- social conformity or independence;
- strategic sophistication; and
- propensity to participate.

### Situational state

- current household exposure;
- beneficiary, taxpayer, worker, provider, owner, or regional interests;
- information received and retained;
- source credibility as perceived by the agent;
- campaign exposure and disclosed funding;
- peer-network signals;
- ballot fatigue and time pressure;
- recent institutional performance;
- perceived closeness and pivotality; and
- uncertainty about personal and public effects.

### Institutional environment

- ballot wording and number of questions;
- Yes/No, numeric, approval, ranked, or other choice rule;
- current-law default;
- qualification and campaign-finance rules;
- official evidence and dissent;
- turnout, registration, and voting access;
- popular, state, electoral, or double-majority aggregation; and
- implementation credibility and correction rules.

## Decision sequence

```text
sample traits and exposure
-> receive information through bounded attention
-> update beliefs with heterogeneous trust
-> observe selected peer and campaign signals
-> decide whether to participate
-> form sincere preference
-> optionally choose a strategic ballot
-> cast a valid or invalid ballot
-> aggregate under the institutional rule
```

The model retains sincere preference, expressed ballot, abstention reason, and
information state separately.

## Population design

- Use continuous distributions inside and across archetypes.
- Preserve correlations; independent random traits create implausible agents.
- Represent multimodal and polarized populations, not only normal noise.
- Vary geographic sorting independently from national support.
- Include low-information, cross-pressured, uncertain, and nonparticipating agents.
- Never infer protected-group behavior from stereotypes.
- Use empirical demographic or political calibration only with sourced data and
  an explicit ethical and privacy review.

## Behavioral modules

Each module is optional and separately switchable:

- bounded attention and information decay;
- motivated reasoning;
- source-trust updating;
- loss aversion and status-quo bias;
- pocketbook and beneficiary exposure;
- social-network diffusion;
- paid-campaign reach and frequency;
- funding and conflict disclosure;
- misinformation and correction;
- strategic voting and strategic abstention;
- turnout mobilization and fatigue;
- repeated-vote learning; and
- implementation feedback between election cycles.

## Calibration ladder

1. **Invariants:** ballots reconcile, probabilities are valid, seeds reproduce,
   and aggregation implements the published rule.
2. **Internal sensitivity:** changing one parameter moves only mechanisms it is
   supposed to affect.
3. **Stylized facts:** the model can reproduce broad documented patterns such
   as turnout decline with ballot length without claiming a universal effect.
4. **Retrodiction:** fit only declared parameters to historical ballot and
   turnout cases.
5. **Held-out validation:** test jurisdictions and elections not used in fitting.
6. **Prospective humility:** publish intervals and scenario dependence rather
   than point forecasts.

Failing calibration is retained. Parameters are not tuned to make a preferred
institution win.

## Required experiment matrix

Every consequential design runs at least:

- multiple seeds;
- low, central, and high polarization;
- weak and strong geographic sorting;
- low and high information;
- neutral, incumbent, and paid-advocacy framing;
- disclosed and hidden material interests;
- low and high ballot fatigue;
- sincere and strategic behavior;
- representative and skewed turnout; and
- popular, territorial, and proposed aggregation rules.

## Versioning

Every output records:

- voter-model version;
- archetype-distribution version;
- behavioral modules and parameters;
- calibration dataset versions;
- institutional configuration;
- random seed and run count;
- code commit;
- uncertainty summary; and
- known mismatches and disabled mechanisms.

No result may be compared across voter-model versions without a bridge run that
executes both models on the same scenario suite.
