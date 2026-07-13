#!/usr/bin/env python3
"""Summarize declared ordinal closure exposures without inferring preferences."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OPTIONS = ["broader_contribution", "progressive_closure", "partial_fiscal_path"]


def weighted_quantile(rows, option, quantile):
    ordered = sorted(rows, key=lambda row: row[option])
    cumulative = 0.0
    for row in ordered:
        cumulative += row["synthetic_weight"]
        if cumulative >= quantile:
            return row[option]
    return ordered[-1][option]


def main():
    config = json.loads((HERE / "exposure-config.v1.json").read_text(encoding="utf-8"))
    profiles = config["profiles"]
    if abs(sum(row["synthetic_weight"] for row in profiles) - 1.0) > 1e-9:
        raise ValueError("synthetic profile weights must total one")
    summaries = []
    for option in OPTIONS:
        mean = sum(row["synthetic_weight"] * row[option] for row in profiles)
        highest = max(profiles, key=lambda row: row[option])
        summaries.append({
            "option_id": option,
            "weighted_mean_exposure": round(mean, 2),
            "weighted_p90_exposure": weighted_quantile(profiles, option, 0.90),
            "highest_exposure_profile": highest["id"],
            "highest_exposure": highest[option],
            "nonhousehold_risks": config["nonhousehold_risks"][option]
        })
    output = {
        "model_id": config["model_id"],
        "status": config["status"],
        "summaries": summaries,
        "profiles": profiles,
        "guardrails": config["guardrails"]
    }
    out = HERE / "outputs"
    out.mkdir(exist_ok=True)
    (out / "exposure.v1.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    lines = ["# Closure Exposure Stress — V1", "", "> Declared ordinal stress inputs, not incidence estimates or voter preferences.", "", "| Option | Weighted mean | Weighted p90 | Highest-exposure profile |", "|---|---:|---:|---|"]
    for row in summaries:
        lines.append(f"| {row['option_id'].replace('_', ' ')} | {row['weighted_mean_exposure']:.1f} | {row['weighted_p90_exposure']} | {row['highest_exposure_profile'].replace('_', ' ')} ({row['highest_exposure']}) |")
    lines += ["", "The weighted mean is a model check, not a ranking rule. Concentration, administration, rights, service, regional, and intergenerational effects remain separate decisions.", ""]
    (out / "exposure.v1.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
