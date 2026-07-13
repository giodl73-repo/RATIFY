# Broad Shared-Contribution VAT Credit

Machine specification: `designs/us/broad-shared-vat-credit.v1.json`.

The narrow 5% VAT follows CBO option 60961. It excludes new and existing
housing, food for home consumption, health care, primary through postsecondary
education, and specified government, nonprofit, and implicit-fee financial
services.

## Credit formula

In 2027 dollars:

- $600 per eligible adult;
- $300 per qualifying dependent;
- full credit through 200% of the household-size poverty guideline;
- linear phaseout from 200% through 400%; and
- CPI-U indexing with no nominal reduction.

The dollar amounts equal 5% of a protected taxable-consumption allowance of
$12,000 per adult and $6,000 per dependent. That formula makes the protection
inspectable rather than selecting a round rebate after observing the score.

The credit is paid monthly, is not taxable, does not count against federal
means-tested benefits, and has a nonfiler enrollment route. Annual
reconciliation pays underpayments but does not claw back ordinary
income-estimation or household-change errors absent fraud or material
misrepresentation.

## Tradeoffs fixed before scoring

The 200%–400% phaseout targets resources but adds an effective marginal rate.
Monthly administration improves cash flow but costs more than an annual credit.
Including lawful resident tax filers with SSNs or ITINs broadens protection and
administrative requirements. Excluding the credit from benefit calculations
prevents circular benefit losses but changes federal and state interactions.

These are package choices. The scorer should measure them, not replace them.

## Score gate

CBO's published narrow-VAT estimate does not include this RATIFY credit or its
administration. Required outputs include gross VAT, income/payroll offsets,
credit cost, take-up and underpayment, systems cost, household incidence,
monthly cash-flow adequacy, and state-sales-tax interactions. The net revenue
may be materially below the earlier envelope.
