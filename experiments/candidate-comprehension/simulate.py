#!/usr/bin/env python3
"""Synthetic fact-recovery stress test; never estimates candidate support."""

import json
import random
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent


def clipped_normal(rng, mean, sd):
    return min(1.0, max(0.0, rng.gauss(mean, sd)))


def weighted_archetype(rng, rows):
    point = rng.random()
    for row in rows:
        point -= row["weight"]
        if point <= 0:
            return row
    return rows[-1]


def main():
    config = json.loads((HERE / "config.v1.json").read_text(encoding="utf-8"))
    voter = json.loads((HERE / config["voter_model"]).resolve().read_text(encoding="utf-8"))
    trait_index = {name: index for index, name in enumerate(voter["traits"])}
    model = config["probability_model"]
    counts = defaultdict(lambda: [0, 0])
    archetype_counts = defaultdict(lambda: [0, 0])
    for seed in config["seeds"]:
        rng = random.Random(seed)
        for scenario in config["scenarios"]:
            for _ in range(config["agents_per_run"]):
                archetype = weighted_archetype(rng, voter["archetypes"])
                traits = [clipped_normal(rng, mean, archetype["sd"]) for mean in archetype["means"]]
                cards = list(config["cards"])
                rng.shuffle(cards)
                for card in cards:
                    for question in config["questions"]:
                        targeted = scenario["targeted_penalties"].get(card, {}).get(question, 0.0)
                        probability = (
                            model["intercept"]
                            + model["numeracy"] * traits[trait_index["numeracy"]]
                            + model["outcome_orientation"] * traits[trait_index["outcome_orientation"]]
                            + model["institutional_trust"] * traits[trait_index["institutional_trust"]]
                            + model["fatigue_sensitivity"] * scenario["fatigue"] * traits[trait_index["fatigue_sensitivity"]]
                            - model["question_difficulty"][question]
                            - scenario["general_penalty"]
                            - targeted
                        )
                        probability = min(0.98, max(0.05, probability))
                        correct = rng.random() < probability
                        counts[(scenario["id"], card, question)][0] += int(correct)
                        counts[(scenario["id"], card, question)][1] += 1
                        archetype_counts[(scenario["id"], archetype["id"])][0] += int(correct)
                        archetype_counts[(scenario["id"], archetype["id"])][1] += 1
    results = []
    for scenario in config["scenarios"]:
        for card in config["cards"]:
            question_accuracy = {}
            total_correct = total = 0
            for question in config["questions"]:
                correct, attempts = counts[(scenario["id"], card, question)]
                question_accuracy[question] = round(correct / attempts * 100, 2)
                total_correct += correct
                total += attempts
            results.append({"scenario":scenario["id"], "card":card, "accuracy_percent":round(total_correct / total * 100, 2), "question_accuracy_percent":question_accuracy})
    neutral_gaps = []
    for scenario_id in ["neutral_low_fatigue", "neutral_high_fatigue"]:
        rows = [row for row in results if row["scenario"] == scenario_id]
        neutral_gaps.append({"scenario":scenario_id, "absolute_card_gap_percentage_points":round(abs(rows[0]["accuracy_percent"] - rows[1]["accuracy_percent"]), 2)})
    lowest_archetypes = []
    for scenario in config["scenarios"]:
        rows = []
        for archetype in voter["archetypes"]:
            correct, attempts = archetype_counts[(scenario["id"], archetype["id"])]
            rows.append((correct / attempts * 100, archetype["id"]))
        accuracy, archetype_id = min(rows)
        lowest_archetypes.append({"scenario":scenario["id"], "archetype":archetype_id, "accuracy_percent":round(accuracy, 2)})
    output = {"experiment_id":config["experiment_id"], "status":config["status"], "runs":len(config["seeds"]), "agents_per_run":config["agents_per_run"], "results":results, "neutral_symmetry":neutral_gaps, "lowest_accuracy_archetypes":lowest_archetypes, "guardrails":config["guardrails"]}
    out = HERE / "outputs"
    out.mkdir(exist_ok=True)
    (out / "run.v1.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    lines = ["# Candidate Comprehension Stress — V1", "", "> Synthetic fact recovery only; no support, turnout, or election result is modeled.", "", "| Presentation | Progressive card | Partial-path card |", "|---|---:|---:|"]
    for scenario in config["scenarios"]:
        rows = {row["card"]:row for row in results if row["scenario"] == scenario["id"]}
        lines.append(f"| {scenario['id'].replace('_', ' ')} | {rows['progressive_primary_balance']['accuracy_percent']:.1f}% | {rows['protected_partial_path']['accuracy_percent']:.1f}% |")
    lines += ["", "Neutral card gaps: " + ", ".join(f"{row['scenario'].replace('_', ' ')} {row['absolute_card_gap_percentage_points']:.2f} points" for row in neutral_gaps) + ".", "", "Framing scenarios deliberately obscure the favored card's cost field; overload reduces both. These are model mechanics, not measured human effects.", ""]
    (out / "run.v1.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
