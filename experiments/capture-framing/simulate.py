#!/usr/bin/env python3
"""Synthetic sensitivity test for framing and organized influence."""

import json
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent


def weighted_choice(rng, rows):
    point = rng.random() * sum(row["weight"] for row in rows)
    for row in rows:
        point -= row["weight"]
        if point <= 0:
            return row
    return rows[-1]


def closure(package):
    return sum(package["uses"].values()) - sum(package["funding"].values())


def evidence_utility(package, voter):
    return (
        voter["outcome"] * package["outcome_score"] / 20.0
        + voter["continuity"] * package["continuity_score"] / 25.0
        - voter["risk"] * package["implementation_risk"] / 15.0
        - voter["burden"] * package["household_burden_index"] / 20.0
    )


def perceived_utility(rng, package, voter, treatment):
    value = evidence_utility(package, voter)
    if package["id"] == "status_quo":
        value += treatment["status_quo_bonus"]
        value += treatment["incumbent_brand_bonus"] * voter["familiarity"]
    if package["id"] == treatment["sponsor_package"]:
        value += treatment["campaign_exposure"]
        if treatment["funding_disclosed"]:
            value -= treatment["campaign_exposure"] * 0.75 * voter["skepticism"]
    value += rng.gauss(0.0, treatment["noise"])
    return value


def run(config, treatment, seed):
    rng = random.Random(seed)
    packages = config["packages"]
    counts = {package["id"]: 0 for package in packages}
    evidence_optimal = 0
    total_regret = 0.0
    changed_from_evidence = 0
    for _ in range(config["voters_per_run"]):
        voter = weighted_choice(rng, config["archetypes"])
        evidence = [evidence_utility(package, voter) for package in packages]
        perceived = [perceived_utility(rng, package, voter, treatment) for package in packages]
        best_evidence = max(range(len(packages)), key=evidence.__getitem__)
        chosen = max(range(len(packages)), key=perceived.__getitem__)
        counts[packages[chosen]["id"]] += 1
        evidence_optimal += chosen == best_evidence
        changed_from_evidence += chosen != best_evidence
        total_regret += evidence[best_evidence] - evidence[chosen]
    n = config["voters_per_run"]
    return {
        "shares": {key: value / n * 100.0 for key, value in counts.items()},
        "evidence_optimal_choice_percent": evidence_optimal / n * 100.0,
        "choice_changed_from_evidence_percent": changed_from_evidence / n * 100.0,
        "mean_evidence_utility_regret": total_regret / n,
    }


def summarize(values):
    ordered = sorted(values)
    return {"mean": sum(values) / len(values), "min": ordered[0], "max": ordered[-1]}


def main():
    config = json.loads((HERE / "config.v1.json").read_text(encoding="utf-8"))
    if config["model_status"] != "synthetic_parameterized_sensitivity_not_behavioral_evidence":
        raise ValueError("simulation boundary missing")
    for package in config["packages"]:
        if abs(closure(package)) > 1e-9:
            raise ValueError(f"package {package['id']} is not fiscally closed")
    if abs(sum(row["weight"] for row in config["archetypes"]) - 1.0) > 1e-9:
        raise ValueError("archetype weights must sum to one")

    treatments = []
    for treatment_index, treatment in enumerate(config["treatments"]):
        runs = [run(config, treatment, config["seed"] + treatment_index * 1000 + index)
                for index in range(config["runs"])]
        treatments.append({
            "treatment": treatment["id"],
            "package_share_percent": {package["id"]: summarize([row["shares"][package["id"]] for row in runs]) for package in config["packages"]},
            "evidence_optimal_choice_percent": summarize([row["evidence_optimal_choice_percent"] for row in runs]),
            "choice_changed_from_evidence_percent": summarize([row["choice_changed_from_evidence_percent"] for row in runs]),
            "mean_evidence_utility_regret": summarize([row["mean_evidence_utility_regret"] for row in runs])
        })

    neutral = next(row for row in treatments if row["treatment"] == "outcome_first_full_evidence")
    for row in treatments:
        row["status_quo_change_vs_neutral_pp"] = row["package_share_percent"]["status_quo"]["mean"] - neutral["package_share_percent"]["status_quo"]["mean"]
        row["sponsor_change_vs_neutral_pp"] = row["package_share_percent"]["provider_consolidation"]["mean"] - neutral["package_share_percent"]["provider_consolidation"]["mean"]

    output = {
        "experiment_id": config["experiment_id"],
        "simulation_status": config["model_status"],
        "seed": config["seed"],
        "runs": config["runs"],
        "voters_per_run": config["voters_per_run"],
        "packages_fiscally_closed": True,
        "treatments": treatments,
        "interpretation_boundary": "Differences are consequences of declared synthetic parameters, not estimated real-world persuasion effects."
    }
    out = HERE / "outputs"
    out.mkdir(exist_ok=True)
    (out / "run.v1.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")

    lines = ["# Capture and Framing Stress Test — V1", "",
             "> Synthetic parameter sensitivity, not measured voter behavior or public opinion.", "",
             "All four packages are fiscally closed. Only information, branding, advocacy disclosure, and noise assumptions change.", "",
             "| Treatment | Status quo | Outcome reform | Sponsor package | Changed vs evidence | Evidence regret |",
             "|---|---:|---:|---:|---:|---:|"]
    for row in treatments:
        shares = row["package_share_percent"]
        lines.append(f"| {row['treatment']} | {shares['status_quo']['mean']:.1f}% | {shares['outcome_reform']['mean']:.1f}% | {shares['provider_consolidation']['mean']:.1f}% | {row['choice_changed_from_evidence_percent']['mean']:.1f}% | {row['mean_evidence_utility_regret']['mean']:.3f} |")
    hidden = next(row for row in treatments if row["treatment"] == "paid_advocacy_funding_hidden")
    disclosed = next(row for row in treatments if row["treatment"] == "paid_advocacy_funding_disclosed")
    disclosure_effect = hidden["package_share_percent"]["provider_consolidation"]["mean"] - disclosed["package_share_percent"]["provider_consolidation"]["mean"]
    lines += ["", "## Designed sensitivity", "",
              f"Under the declared parameters, disclosing the sponsor reduces its package's share by **{disclosure_effect:.1f} percentage points** relative to identical paid exposure with hidden funding.",
              "This is not an empirical estimate. It verifies that disclosure, familiarity, evidence noise, and ballot overload can be represented as explicit assumptions and audited rather than buried in the result.", "",
              "## Decision use", "",
              "RATIFY should compare outcome-first and brand-first interfaces, disclose material funding beside advocacy, cap ballot complexity, and publish treatment sensitivity. Real effect sizes require randomized or observational evidence.", ""]
    (out / "run.v1.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
