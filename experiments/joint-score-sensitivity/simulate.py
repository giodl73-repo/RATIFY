#!/usr/bin/env python3
"""Run disclosed synthetic fiscal sensitivities; never represent them as a score."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def pick(component, field, scenario_index):
    values = component[field]
    if len(values) != 3:
        raise ValueError(f"{component['id']}.{field} must contain three scenario values")
    return values[scenario_index]


def calculate(component, index):
    component_id = component["id"]
    if component_id == "vat":
        gross = component["published_2025_2034_billions"] * pick(component, "window_factor", index)
        interacted = gross * pick(component, "gross_retention_after_tax_interactions", index)
        protected = interacted * (1 - pick(component, "vat_credit_cost_share_of_post_interaction_gross", index))
        return protected * (1 - pick(component, "implementation_cost_share_of_post_credit_amount", index))
    if component_id == "emissions":
        receipts = component["published_2025_2034_billions"] * pick(component, "window_factor", index) * pick(component, "receipt_rescore_factor", index)
        retained = receipts * pick(component, "primary_balance_allocation_share", index)
        return retained * (1 - pick(component, "implementation_cost_share_of_retained_amount", index))
    if component_id == "employer_health_exclusion":
        amount = component["published_2025_2034_billions"] * pick(component, "window_factor", index) * pick(component, "protection_and_interaction_retention", index)
        return amount * (1 - pick(component, "implementation_cost_share", index))
    if component_id == "capital_gains_dividends":
        amount = component["published_2025_2034_billions"] * pick(component, "window_factor", index) * pick(component, "behavior_and_interaction_retention", index)
        return amount * (1 - pick(component, "implementation_cost_share", index))
    if component_id == "defense":
        base = component["published_2027_2034_billions"] * pick(component, "force_plan_realization", index)
        protected = base * pick(component, "transition_and_protection_retention", index)
        return protected + pick(component, "extension_2035_2036_billions", index)
    if component_id == "medicare_advantage":
        amount = component["published_2027_2034_billions"] * pick(component, "plan_response_and_protection_retention", index)
        return amount * (1 - pick(component, "implementation_cost_share", index))
    raise ValueError(f"unsupported component {component_id}")


def main():
    config = json.loads((HERE / "config.v1.json").read_text(encoding="utf-8"))
    results = []
    for index, scenario in enumerate(config["scenarios"]):
        components = {row["id"]: round(calculate(row, index), 3) for row in config["components"]}
        revenue = sum(value for row_id, value in components.items() if next(row for row in config["components"] if row["id"] == row_id)["side"] == "revenue")
        outlay = sum(value for row_id, value in components.items() if next(row for row in config["components"] if row["id"] == row_id)["side"] == "primary_outlay")
        total = revenue + outlay
        target = config["target_2026_2036_billions"]
        results.append({
            "scenario": scenario,
            "components_billions": components,
            "revenue_billions": round(revenue, 3),
            "primary_outlay_billions": round(outlay, 3),
            "total_primary_adjustment_billions": round(total, 3),
            "realized_revenue_share_percent": round(revenue / total * 100, 2),
            "gap_to_target_billions": round(target - total, 3),
            "target_coverage_percent": round(total / target * 100, 2)
        })
    output = {
        "experiment_id": config["experiment_id"],
        "simulation_status": config["simulation_status"],
        "target_2026_2036_billions": config["target_2026_2036_billions"],
        "results": results,
        "closure_exclusions": config["excluded_from_closure"],
        "interpretation": "Diagnostic assumption matrix only; not a forecast, public opinion estimate, or independent fiscal score."
    }
    out = HERE / "outputs"
    out.mkdir(exist_ok=True)
    (out / "run.v1.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    lines = ["# Broad/Shared Joint-Score Sensitivity — V1", "", "> Synthetic missing-value diagnostic, not an official or independent score.", "", "| Scenario | Revenue | Primary outlay | Total adjustment | Target covered | Gap | Realized mix |", "|---|---:|---:|---:|---:|---:|---:|"]
    for row in results:
        lines.append(f"| {row['scenario'].replace('_', ' ')} | ${row['revenue_billions']:,.0f}B | ${row['primary_outlay_billions']:,.0f}B | ${row['total_primary_adjustment_billions']:,.0f}B | {row['target_coverage_percent']:.1f}% | ${row['gap_to_target_billions']:,.0f}B | {row['realized_revenue_share_percent']:.1f}% revenue |")
    lines += ["", "## Component decomposition", ""]
    for row in results:
        parts = ", ".join(f"{key.replace('_', ' ')} ${value:,.0f}B" for key, value in row["components_billions"].items())
        lines.append(f"- **{row['scenario'].replace('_', ' ')}:** {parts}.")
    lines += ["", "No administrative savings, 2035–2036 defense extension, net-interest dividend, or macroeconomic feedback is used as a balancing plug.", ""]
    (out / "run.v1.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
