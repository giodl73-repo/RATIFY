#!/usr/bin/env python3
"""Construct one complete synthetic challenger from TAXLANE-derived inputs."""

import json
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent


def choose(rng, weighted):
    point = rng.random() * sum(weighted.values())
    for key, weight in weighted.items():
        point -= weight
        if point <= 0:
            return key
    return next(reversed(weighted))


def weighted_row(rng, rows):
    point = rng.random()
    for row in rows:
        point -= row["weight"]
        if point <= 0:
            return row
    return rows[-1]


def dirichlet(rng, alpha):
    values = [rng.gammavariate(max(value, 0.001), 1.0) for value in alpha]
    return [value / sum(values) * 100.0 for value in values]


def distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def approximate_medoid(ballots, rng, candidates=500, evaluation=1800):
    candidate_rows = rng.sample(ballots, min(candidates, len(ballots)))
    evaluation_rows = rng.sample(ballots, min(evaluation, len(ballots)))
    return min(candidate_rows, key=lambda row: sum(distance(row["vector"], other["vector"]) for other in evaluation_rows))


def main():
    config = json.loads((HERE / "config.v1.json").read_text(encoding="utf-8"))
    source = json.loads((HERE / "source-snapshot.v1.json").read_text(encoding="utf-8"))
    rng = random.Random(config["seed"])
    if abs(sum(row["weight"] for row in config["archetypes"]) - 1.0) > 1e-9:
        raise ValueError("archetype weights must total one")
    target_uses = [row[3] for row in source["lanes"]]
    if abs(sum(target_uses) - 100.0) > 0.01:
        raise ValueError("rounded TAXLANE target does not total 100")
    paths = {row["id"]: row for row in source["fiscal_paths"]}
    path_scale = {"partial":0.0,"primary_balance":50.0,"primary_surplus_one_percent":100.0}
    ballots = []
    for _ in range(config["ballots"]):
        archetype = weighted_row(rng, config["archetypes"])
        uses = dirichlet(rng, [max(value, 0.05) / 100.0 * config["use_concentration"] for value in target_uses])
        funding = dirichlet(rng, archetype["funding_alpha"])
        admin_index = len(funding) - 1
        if funding[admin_index] > config["administration_savings_cap_percent_of_adjustment"]:
            excess = funding[admin_index] - config["administration_savings_cap_percent_of_adjustment"]
            funding[admin_index] -= excess
            other_total = sum(funding[:-1])
            for index in range(len(funding) - 1):
                funding[index] += excess * funding[index] / other_total
        path_id = choose(rng, archetype["path_weights"])
        vector = uses + funding + [path_scale[path_id]]
        ballots.append({"archetype":archetype["id"],"path_id":path_id,"uses":uses,"funding":funding,"vector":vector})
    if any(abs(sum(row["uses"]) - 100.0) > 1e-8 or abs(sum(row["funding"]) - 100.0) > 1e-8 for row in ballots):
        raise ValueError("incomplete ballot")
    challenger = approximate_medoid(ballots, rng)
    path = paths[challenger["path_id"]]
    funding_amounts_2036 = {key: share / 100.0 * path["fy2036_primary_adjustment_billions"] for key, share in zip(config["funding_categories"], challenger["funding"])}
    result = {
        "experiment_id":config["experiment_id"],
        "simulation_status":config["simulation_status"],
        "seed":config["seed"],
        "ballots":len(ballots),
        "upstream_snapshot_id":source["snapshot_id"],
        "selection_method":"approximate_actual_ballot_medoid",
        "challenger_is_actual_complete_ballot":True,
        "challenger_archetype":challenger["archetype"],
        "fiscal_path":path,
        "use_allocation_percent":{row[0]:value for row,value in zip(source["lanes"],challenger["uses"])},
        "adjustment_funding_mix_percent":dict(zip(config["funding_categories"],challenger["funding"])),
        "fy2036_adjustment_funding_billions":funding_amounts_2036,
        "invariants":{"uses_sum_100":True,"funding_mix_sum_100":True,"administration_savings_cap_respected":challenger["funding"][-1] <= config["administration_savings_cap_percent_of_adjustment"] + 1e-9},
        "authority_status":"candidate_for_review_then_binary_ratification_not_law"
    }
    out = HERE / "outputs"
    out.mkdir(exist_ok=True)
    (out / "challenger.v1.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = ["# TAXLANE Bridge Challenger — V1", "", "> Synthetic package construction, not public opinion, a score, ratification, or law.", "",
             f"Selected an actual complete ballot medoid from **{len(ballots):,}** synthetic ballots.", "",
             f"Fiscal path: **{path['id']}**; FY2036 primary adjustment: **${path['fy2036_primary_adjustment_billions']:.1f}B**; first-order FY2036 debt: **{path['fy2036_debt_percent_gdp']:.1f}% of GDP**.", "",
             "## Funding of the FY2036 adjustment", "", "| Source | Share | Amount |", "|---|---:|---:|"]
    for key in config["funding_categories"]:
        lines.append(f"| {key.replace('_',' ')} | {result['adjustment_funding_mix_percent'][key]:.1f}% | ${funding_amounts_2036[key]:.1f}B |")
    lines += ["", f"Every use allocation and funding mix sums to 100. Administration savings are capped at {config['administration_savings_cap_percent_of_adjustment']:.0f}% of the adjustment under the current evidence gate; they cannot serve as an unsupported balancing plug.", "", "## Next gate", "", "This challenger must receive updated fiscal, legal, distribution, rights, outcome, and implementation review. Only then can it be rendered as YES challenger / NO current law.", ""]
    (out / "challenger.v1.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
