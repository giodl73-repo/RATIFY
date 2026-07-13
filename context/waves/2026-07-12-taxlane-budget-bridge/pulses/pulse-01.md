# Pulse 01: TAXLANE Input and Provenance Contract

## Result

Captured a compact RATIFY snapshot of TAXLANE commit
`c6b22bd642724ce11f3e19c17c759edfc8f74179`, including artifact paths and
SHA-256 hashes, the 15-lane current and V2 synthetic allocations, and four
first-order fiscal paths.

## Boundary

- TAXLANE retains ownership of fiscal evidence and its original experiment.
- RATIFY owns civic aggregation, funding choices, challenger construction, and
  ratification design.
- The snapshot preserves TAXLANE's synthetic-not-public-opinion status.
- The bridge does not modify TAXLANE or imply its endorsement.

## Role findings

- Comparative Evidence Steward: cross-repo source and interpretation ownership
  are explicit.
- Simulation Auditor: hashes and commit pin the input; rounded snapshot values
  require tolerance checks.
- Future Citizen: upstream artifacts remain discoverable by public repository,
  commit, and path.

## Decision

Proceed to complete use-and-funding ballots. Do not treat allocation shares as
program savings or as financing; the fiscal-adjustment choice remains a
separate, linked component.
