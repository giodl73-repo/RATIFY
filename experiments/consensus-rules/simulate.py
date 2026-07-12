#!/usr/bin/env python3
"""Stress-test consensus rules at fixed national support."""

import json
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent


def logistic(value):
    return 1.0 / (1.0 + math.exp(-value))


def calibrated_rates(states, scenario, target, profile_scores, seed):
    rng = random.Random(seed)
    house = [max(electoral - 2, 1) for _, electoral, _ in states]
    log_sizes = [math.log(value) for value in house]
    mean_log_size = sum(log_sizes) / len(log_sizes)
    base_scores = []
    for (_, _, profile), log_size in zip(states, log_sizes):
        score = scenario["size_correlation"] * (log_size - mean_log_size)
        score += scenario["profile_strength"] * profile_scores[profile]
        score += rng.gauss(0.0, scenario["noise"])
        base_scores.append(score)

    low, high = -20.0, 20.0
    for _ in range(100):
        intercept = (low + high) / 2.0
        rates = [logistic(intercept + score) for score in base_scores]
        weighted = sum(rate * weight for rate, weight in zip(rates, house)) / sum(house)
        if weighted < target:
            low = intercept
        else:
            high = intercept
    return [logistic((low + high) / 2.0 + score) for score in base_scores]


def evaluate(states, rates, config):
    house = [max(electoral - 2, 1) for _, electoral, _ in states]
    national = sum(rate * weight for rate, weight in zip(rates, house)) / sum(house)
    state_rows = []
    state_wins = 0
    electoral_yes = 0
    for (state, electoral, profile), rate, population_proxy in zip(states, rates, house):
        yes = rate > config["state_pass_threshold_percent"] / 100.0
        if state != "DC" and yes:
            state_wins += 1
        if yes:
            electoral_yes += electoral
        state_rows.append({"state": state, "profile": profile, "electoral_votes": electoral,
                           "population_proxy_house_seats": population_proxy,
                           "support_percent": round(rate * 100.0, 4), "state_yes": yes})
    popular_pass = national > 0.5
    state_pass = state_wins >= 26
    return {
        "national_support_percent": round(national * 100.0, 6),
        "states_carried_of_50": state_wins,
        "electoral_votes_yes_of_538": electoral_yes,
        "rules": {
            "national_popular_majority": popular_pass,
            "majority_of_states": state_pass,
            "electoral_college_270": electoral_yes >= 270,
            "double_majority_popular_plus_states": popular_pass and state_pass,
            "strong_consensus_55_percent_plus_30_states": national >= config["strong_national_threshold_percent"] / 100.0 and state_wins >= config["strong_state_threshold_count"]
        },
        "territorial_veto_of_popular_majority": popular_pass and not state_pass,
        "state_rows": state_rows
    }


def main():
    config = json.loads((HERE / "config.v1.json").read_text(encoding="utf-8"))
    states = config["states"]
    target = config["national_support_target_percent"] / 100.0
    results = []
    for index, scenario in enumerate(config["scenarios"]):
        rates = calibrated_rates(states, scenario, target, config["profile_scores"], config["seed"] + index)
        results.append({"scenario": scenario["id"], **evaluate(states, rates, config)})

    if sum(state[1] for state in states) != 538:
        raise ValueError("electoral allocations must total 538")
    if any(abs(row["national_support_percent"] - config["national_support_target_percent"]) > 0.0001 for row in results):
        raise ValueError("scenario calibration drifted from the fixed national target")
    if not any(row["territorial_veto_of_popular_majority"] for row in results):
        raise ValueError("stress set must contain at least one territorial veto case")
    if not any(row["rules"]["double_majority_popular_plus_states"] for row in results):
        raise ValueError("stress set must contain at least one double-majority passage case")

    house = [max(electoral - 2, 1) for state, electoral, profile in states if state != "DC"]
    influence = {
        "equal_state_weight_per_population_proxy_max_to_min_ratio": max(house) / min(house),
        "electoral_weight_per_population_proxy_max_to_min_ratio": max(electoral / max(electoral - 2, 1) for state, electoral, _ in states if state != "DC") / min(electoral / max(electoral - 2, 1) for state, electoral, _ in states if state != "DC"),
        "interpretation": "Ratios compare formal territorial weight with a House-seat population proxy; they are not estimates of pivotal voting probability."
    }
    output = {
        "experiment_id": config["experiment_id"],
        "simulation_status": "synthetic_aggregation_stress_test_not_public_opinion",
        "seed": config["seed"],
        "fixed_national_support_target_percent": config["national_support_target_percent"],
        "scenarios": results,
        "formal_weight_diagnostics": influence,
        "limitations": config["limitations"]
    }
    out = HERE / "outputs"
    out.mkdir(exist_ok=True)
    (out / "run.v1.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")

    lines = ["# Consensus Rules Geographic Stress Test — V1", "",
             "> Synthetic aggregation test, not public opinion or a forecast.", "",
             f"Every scenario is calibrated to **{config['national_support_target_percent']:.1f}% national support** using House seats as a population proxy.", "",
             "| Scenario | Popular | States | EC votes | Popular rule | State rule | EC rule | Double majority | Territorial veto? |",
             "|---|---:|---:|---:|:---:|:---:|:---:|:---:|:---:|"]
    for row in results:
        rule = row["rules"]
        mark = lambda value: "pass" if value else "fail"
        lines.append(f"| {row['scenario']} | {row['national_support_percent']:.1f}% | {row['states_carried_of_50']}/50 | {row['electoral_votes_yes_of_538']}/538 | {mark(rule['national_popular_majority'])} | {mark(rule['majority_of_states'])} | {mark(rule['electoral_college_270'])} | {mark(rule['double_majority_popular_plus_states'])} | {'yes' if row['territorial_veto_of_popular_majority'] else 'no'} |")
    lines += ["", "## Formal weighting diagnostics", "",
              f"Equal-state weight per House-seat proxy varies by **{influence['equal_state_weight_per_population_proxy_max_to_min_ratio']:.1f}×** between the smallest and largest states.",
              f"Electoral weight per House-seat proxy varies by **{influence['electoral_weight_per_population_proxy_max_to_min_ratio']:.2f}×**.", "",
              "These ratios describe formal weighting, not the probability that a voter is pivotal.", "", "## Interpretation", "",
              "Holding national support constant does not hold the result constant under territorial rules. A double majority can demonstrate geographic breadth, but it can also allow a territorially distributed minority to veto a national majority. The experiment therefore treats state concurrence as a legitimacy claim that must earn its place, not as consensus by definition.", "", "## Limits", ""]
    lines.extend(f"- {item}" for item in config["limitations"])
    (out / "run.v1.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
