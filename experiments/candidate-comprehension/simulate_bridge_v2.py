#!/usr/bin/env python3
"""Bridge V1 independent traits to V2 correlated traits and order decay."""

import json
import random
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
VOTER_LAB = (HERE / "../voter-lab").resolve()
sys.path.insert(0, str(VOTER_LAB))
from sample_v2 import sample_traits  # noqa: E402


def clipped_normal(rng, mean, sd):
    return min(1.0, max(0.0, rng.gauss(mean, sd)))


def choose_archetype(rng, rows):
    point = rng.random()
    for row in rows:
        point -= row["weight"]
        if point <= 0:
            return row
    return rows[-1]


def main():
    bridge = json.loads((HERE / "bridge-config.v2.json").read_text(encoding="utf-8"))
    comprehension = json.loads((HERE / "config.v1.json").read_text(encoding="utf-8"))
    voter = json.loads((VOTER_LAB / "archetypes.v1.json").read_text(encoding="utf-8"))
    correlation = json.loads((VOTER_LAB / "correlation-model.v2.json").read_text(encoding="utf-8"))
    index = {trait:i for i, trait in enumerate(voter["traits"])}
    probability_model = comprehension["probability_model"]
    counts = defaultdict(lambda: [0, 0])
    for model_id in ["v1_independent", "v2_correlated_order_decay"]:
        for seed in bridge["seeds"]:
            rng = random.Random(seed)
            for presentation in bridge["presentations"]:
                for _ in range(bridge["agents_per_run"]):
                    archetype = choose_archetype(rng, voter["archetypes"])
                    if model_id == "v1_independent":
                        traits = [clipped_normal(rng, mean, archetype["sd"]) for mean in archetype["means"]]
                    else:
                        traits = sample_traits(rng, archetype, voter["traits"], correlation)
                    cards = list(comprehension["cards"])
                    rng.shuffle(cards)
                    for position, card in enumerate(cards, start=1):
                        order_penalty = 0.0
                        if model_id == "v2_correlated_order_decay" and position == 2:
                            order_penalty = bridge["v2_modules"]["second_card_decay_base"] * traits[index["fatigue_sensitivity"]]
                        for question in comprehension["questions"]:
                            probability = (
                                probability_model["intercept"]
                                + probability_model["numeracy"] * traits[index["numeracy"]]
                                + probability_model["outcome_orientation"] * traits[index["outcome_orientation"]]
                                + probability_model["institutional_trust"] * traits[index["institutional_trust"]]
                                + probability_model["fatigue_sensitivity"] * presentation["fatigue"] * traits[index["fatigue_sensitivity"]]
                                - probability_model["question_difficulty"][question]
                                + presentation["design_bonus"]
                                - order_penalty
                            )
                            correct = rng.random() < min(0.98, max(0.05, probability))
                            for key in [(model_id, presentation["id"], card, f"position_{position}"), (model_id, presentation["id"], card, "all")]:
                                counts[key][0] += int(correct)
                                counts[key][1] += 1
    results = []
    for model_id in ["v1_independent", "v2_correlated_order_decay"]:
        for presentation in bridge["presentations"]:
            for card in comprehension["cards"]:
                row = {"model":model_id, "presentation":presentation["id"], "card":card}
                for position in ["position_1", "position_2", "all"]:
                    correct, attempts = counts[(model_id, presentation["id"], card, position)]
                    row[f"{position}_accuracy_percent"] = round(correct / attempts * 100, 2)
                results.append(row)
    v2 = [row for row in results if row["model"] == "v2_correlated_order_decay"]
    neutral = [row for row in v2 if row["presentation"] == "neutral"]
    neutral_gap = abs(neutral[0]["all_accuracy_percent"] - neutral[1]["all_accuracy_percent"])
    position_pairs = [(row["position_1_accuracy_percent"], row["position_2_accuracy_percent"]) for row in v2]
    promotion = {
        "declared_correlations_validated_separately": True,
        "second_card_decay_observed_in_every_v2_cell": all(first > second for first, second in position_pairs),
        "neutral_candidate_gap_percentage_points": round(neutral_gap, 2),
        "neutral_gap_within_limit": neutral_gap <= bridge["promotion_criteria"]["neutral_candidate_gap_max_percentage_points"],
        "support_or_turnout_generated": False
    }
    promotion["criteria_pass"] = all([promotion["declared_correlations_validated_separately"], promotion["second_card_decay_observed_in_every_v2_cell"], promotion["neutral_gap_within_limit"], not promotion["support_or_turnout_generated"]])
    output = {"experiment_id":bridge["experiment_id"], "status":bridge["status"], "results":results, "promotion":promotion}
    out = HERE / "outputs"
    (out / "bridge.v2.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    lines = ["# Voter Lab V1–V2 Comprehension Bridge", "", "> Synthetic model comparison, not human validation or public opinion.", "", "| Model | Presentation | Card | First | Second | Overall |", "|---|---|---|---:|---:|---:|"]
    for row in results:
        lines.append(f"| {row['model'].replace('_', ' ')} | {row['presentation'].replace('_', ' ')} | {row['card'].replace('_', ' ')} | {row['position_1_accuracy_percent']:.1f}% | {row['position_2_accuracy_percent']:.1f}% | {row['all_accuracy_percent']:.1f}% |")
    lines += ["", f"V2 promotion criteria: **{'pass' if promotion['criteria_pass'] else 'fail'}**. Neutral candidate gap: {promotion['neutral_candidate_gap_percentage_points']:.2f} points.", ""]
    (out / "bridge.v2.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
