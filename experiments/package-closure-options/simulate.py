#!/usr/bin/env python3
"""Compare explicit synthetic closure packages without predicting support."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    config = json.loads((HERE / "config.v1.json").read_text(encoding="utf-8"))
    base_path = (HERE / config["base_results"]).resolve()
    base = json.loads(base_path.read_text(encoding="utf-8"))
    options = {row["id"]: row for row in config["options"]}
    rows = []
    for index, scenario in enumerate(base["results"]):
        base_total = scenario["total_primary_adjustment_billions"]
        base_vat = scenario["components_billions"]["vat"]

        broad = options["broader_contribution"]
        vat_multiplier = broad["proposed_vat_rate_percent"] / broad["base_vat_rate_percent"]
        broad_total = base_total + base_vat * (vat_multiplier - 1)

        progressive = options["progressive_closure"]
        surtax = progressive["agi_surtax"]
        surtax_added = (surtax["published_two_point_2025_2034_billions"] * surtax["rate_multiplier"] * surtax["window_factor"][index] * surtax["behavior_interaction_retention"][index])
        foreign = progressive["foreign_corporate_income"]
        foreign_added = foreign["published_2025_2034_billions"] * foreign["window_factor"][index] * foreign["behavior_interaction_retention"][index]
        progressive_total = base_total + surtax_added + foreign_added

        partial = options["partial_fiscal_path"]
        package_values = [
            (broad, broad_total, {"incremental_vat_billions": broad_total - base_total}),
            (progressive, progressive_total, {"agi_surtax_billions": surtax_added, "foreign_corporate_income_billions": foreign_added}),
            (partial, base_total, {"policy_change_billions": 0.0})
        ]
        for option, total, additions in package_values:
            target = config["targets_billions"][option["target"]]
            rows.append({
                "scenario": scenario["scenario"],
                "option_id": option["id"],
                "label": option["label"],
                "target_path": option["target"],
                "target_billions": target,
                "base_adjustment_billions": round(base_total, 3),
                "added_adjustment_billions": {key: round(value, 3) for key, value in additions.items()},
                "total_adjustment_billions": round(total, 3),
                "gap_billions": round(target - total, 3),
                "meets_target_under_scenario": total >= target
            })
    output = {
        "experiment_id": config["experiment_id"],
        "simulation_status": config["simulation_status"],
        "results": rows,
        "interpretation": "A package meeting a synthetic case is eligible for further review, not proven sufficient or popular."
    }
    out = HERE / "outputs"
    out.mkdir(exist_ok=True)
    (out / "run.v1.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    lines = ["# Package Closure Options — V1", "", "> Synthetic package construction, not a score or public-opinion forecast.", "", "| Scenario | Package | Target | Adjustment | Gap (+ short / − excess) | Meets case? |", "|---|---|---|---:|---:|:---:|"]
    for row in rows:
        lines.append(f"| {row['scenario'].replace('_', ' ')} | {row['label']} | {row['target_path'].replace('_', ' ')} | ${row['total_adjustment_billions']:,.0f}B | ${row['gap_billions']:,.0f}B | {'yes' if row['meets_target_under_scenario'] else 'no'} |")
    lines += ["", "No option is treated as closed merely because it meets one synthetic case. A joint score and a voter-approved correction corridor remain required.", ""]
    (out / "run.v1.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
