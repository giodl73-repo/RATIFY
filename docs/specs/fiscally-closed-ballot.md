# Fiscally Closed Ballot Contract

## Invariant

Every public package and every cast ballot must identify how its uses are
financed. The computer rejects an incomplete or nonreconciling ballot.

```text
program cost
+ administration and transition
+ contingency or uncertainty reserve
+ resulting debt-service change
= dedicated taxes and contributions
+ general-revenue changes
+ fees and other receipts
+ reductions or offsets elsewhere
+ explicit net borrowing
```

There is no unfunded benefit choice and no unnamed “savings” plug.

## Complete package record

Every option presented to voters includes:

- policy and outcome promise;
- gross annual and multiyear cost;
- implementation and transition cost;
- uncertainty range and reserve treatment;
- tax, contribution, fee, or other receipt changes;
- named spending offsets with service and distribution effects;
- annual borrowing or repayment;
- debt and interest path;
- household and regional incidence;
- expiration, review, and automatic-correction rules; and
- consequences if revenue, cost, or outcome forecasts miss.

## Voter interaction

The interface may allow voters to adjust benefits, rates, offsets, and timing,
but linked values update immediately. A voter may not submit until the package
reconciles under the published accounting rule.

For example:

```text
Increase benefit level             +$120B
Reduce provider price target        -$35B
Raise contribution rate             +$55B
Use general revenue                 +$20B
Explicit annual borrowing           +$10B
Remaining gap                         $0B
```

The display must distinguish a real program reduction, an efficiency estimate,
a tax expenditure change, a user fee, and borrowing. They are not
interchangeable merely because each changes the deficit arithmetic.

## Borrowing is a visible choice

RATIFY does not prohibit borrowing categorically. Emergency response,
recession stabilization, and long-lived investment may justify it. But the
ballot must show:

- amount and duration;
- expected interest cost;
- resulting debt path;
- who receives the asset or protection;
- who bears repayment; and
- the rule for returning to the normal fiscal path.

“Borrow” is never the hidden default balancing item.

## Aggregation cannot break closure

Aggregating each field independently can create a package nobody chose: median
benefits combined with median taxes and median offsets may not reconcile or may
violate linked legal constraints.

RATIFY must aggregate **complete feasible ballots**. Candidate methods include:

- selecting the medoid—the cast, balanced ballot minimizing total distance to
  all other ballots;
- computing a geometric median constrained to the fiscally feasible set;
- clustering balanced ballots into coherent packages followed by ranked choice;
  or
- choosing among pre-scored, fully financed packages.

Any synthesized result must be projected back onto the feasible set under a
published rule, and voters must see whether the final package differs from any
actual ballot.

## Forecast error

Fiscal closure at enactment is a forecast, not a guarantee. Every package must
state what happens when actuals differ:

1. use a bounded reserve;
2. publish forecast-versus-actual reconciliation;
3. trigger predefined rate, benefit, timing, or offset adjustments inside a
   voter-approved corridor;
4. require legislative action for larger deviations; and
5. trigger early public review when the deviation crosses a material threshold.

Automatic corrections may not silently violate rights, contracts, or essential
continuity floors.

## Anti-gaming rules

- The same independent scoring basis applies to every package.
- Optimistic efficiency and fraud-recovery assumptions require evidence and a
  haircut or reserve; unverified amounts cannot balance the package.
- Temporary revenue may not finance permanent benefits without an explicit
  post-expiration plan.
- Delayed costs and accelerated receipts remain visible beyond the headline
  window.
- State, local, employer, household, and provider cost shifts are disclosed.
- A package cannot claim both a spending reduction and the same downstream
  receipt increase without modeling interaction.
