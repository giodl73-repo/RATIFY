#!/usr/bin/env python3
"""Stress persistent comparison interfaces with Voter Lab v2."""

import json
import random
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
VOTER_LAB = (HERE / "../voter-lab").resolve()
sys.path.insert(0, str(VOTER_LAB))
from sample_v2 import sample_traits  # noqa: E402


def choose(rng, rows):
    point = rng.random()
    for row in rows:
        point -= row["weight"]
        if point <= 0:
            return row
    return rows[-1]


def main():
    config = json.loads((HERE / "persistent-config.v1.json").read_text(encoding="utf-8"))
    base_config = json.loads((HERE / "config.v1.json").read_text(encoding="utf-8"))
    voters = json.loads((VOTER_LAB / "archetypes.v1.json").read_text(encoding="utf-8"))
    correlations = json.loads((VOTER_LAB / "correlation-model.v2.json").read_text(encoding="utf-8"))
    trait = {name:i for i, name in enumerate(voters["traits"])}
    model = base_config["probability_model"]
    counts = defaultdict(lambda:[0, 0])
    for seed in config["seeds"]:
        rng = random.Random(seed)
        for interface in config["interfaces"]:
            for condition in config["conditions"]:
                for _ in range(config["agents_per_run"]):
                    archetype = choose(rng, voters["archetypes"])
                    values = sample_traits(rng, archetype, voters["traits"], correlations)
                    cards = list(base_config["cards"])
                    rng.shuffle(cards)
                    for position, card in enumerate(cards, start=1):
                        decay = interface["second_card_decay"] * values[trait["fatigue_sensitivity"]] if position == 2 else 0.0
                        for question in config["questions"]:
                            framed = condition["frame_penalty"].get(card, {}).get(question, 0.0)
                            probability = (model["intercept"] + model["numeracy"] * values[trait["numeracy"]] + model["outcome_orientation"] * values[trait["outcome_orientation"]] + model["institutional_trust"] * values[trait["institutional_trust"]] + model["fatigue_sensitivity"] * condition["fatigue"] * values[trait["fatigue_sensitivity"]] - model["question_difficulty"][question] + config["base_layered_bonus"] + interface["question_bonus"][question] - interface["overload_penalty"] - decay - framed)
                            correct = rng.random() < min(0.98, max(0.05, probability))
                            for dimension in [(card, f"position_{position}"), (card, "all")]:
                                counts[(interface["id"], condition["id"], question, *dimension)][0] += int(correct)
                                counts[(interface["id"], condition["id"], question, *dimension)][1] += 1
    summaries = []
    for interface in config["interfaces"]:
        for condition in config["conditions"]:
            card_rows = []
            for card in base_config["cards"]:
                facts = {}
                positions = {}
                for question in config["questions"]:
                    for position in ["position_1", "position_2", "all"]:
                        correct, total = counts[(interface["id"], condition["id"], question, card, position)]
                        value = round(correct / total * 100, 2)
                        if position == "all": facts[question] = value
                        positions.setdefault(position, []).append(value)
                card_rows.append({"card":card,"fact_accuracy_percent":facts,"overall_percent":round(sum(facts.values())/len(facts),2),"position_1_percent":round(sum(positions["position_1"])/len(config["questions"]),2),"position_2_percent":round(sum(positions["position_2"])/len(config["questions"]),2)})
            summaries.append({"interface":interface["id"],"condition":condition["id"],"cards":card_rows})
    decisions = []
    central = [row for row in summaries if row["condition"] == "neutral_central_fatigue"]
    for row in central:
        every_fact = min(value for card in row["cards"] for value in card["fact_accuracy_percent"].values())
        candidate_gap = abs(row["cards"][0]["overall_percent"] - row["cards"][1]["overall_percent"])
        order_gap = max(abs(card["position_1_percent"] - card["position_2_percent"]) for card in row["cards"])
        passed = every_fact >= config["acceptance"]["minimum_each_fact_percent"] and candidate_gap <= config["acceptance"]["maximum_candidate_gap_points"] and order_gap <= config["acceptance"]["maximum_order_gap_points"]
        decisions.append({"interface":row["interface"],"minimum_fact_percent":round(every_fact,2),"candidate_gap_points":round(candidate_gap,2),"maximum_order_gap_points":round(order_gap,2),"passes_neutral_central":passed})
    output = {"experiment_id":config["experiment_id"],"status":config["status"],"decisions":decisions,"summaries":summaries,"guardrails":config["guardrails"]}
    out = HERE / "outputs"
    (out / "persistent.v1.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    lines = ["# Persistent Comparison Stress — V1", "", "> Synthetic interface sensitivity, not human validation or public opinion.", "", "| Interface | Minimum fact | Candidate gap | Maximum order gap | Pass? |", "|---|---:|---:|---:|:---:|"]
    for row in decisions:
        lines.append(f"| {row['interface'].replace('_',' ')} | {row['minimum_fact_percent']:.1f}% | {row['candidate_gap_points']:.2f} | {row['maximum_order_gap_points']:.2f} | {'yes' if row['passes_neutral_central'] else 'no'} |")
    lines += ["", "Passing selects a design for preregistered human testing only.", ""]
    (out / "persistent.v1.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
