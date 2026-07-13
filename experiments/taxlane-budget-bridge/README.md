# TAXLANE Budget Bridge

This experiment generalizes TAXLANE's synthetic annual 100-point allocation
work into a RATIFY package-construction workflow.

## Ownership boundary

TAXLANE owns the fiscal evidence, lane taxonomy, original experiment, and claim
boundaries. RATIFY snapshots exact upstream paths, hashes, and commit ids, then
owns the added funding ballot, aggregation methods, challenger construction,
and Yes/No ratification example.

The snapshot does not imply TAXLANE endorsement of citizen lawmaking or of any
RATIFY package.

Administrative savings are currently capped at zero because no evidence-backed
joint package score exists. A percentage guardrail cannot substitute for a
verified dollar amount.

## Planned flow

```text
TAXLANE evidence + synthetic allocation
-> each RATIFY ballot chooses uses and funding
-> complete-ballot aggregation
-> independent package review
-> YES challenger / NO current law
```

`source-snapshot.v1.json` is a small, reviewable input snapshot, not a replacement
for the upstream artifacts.
