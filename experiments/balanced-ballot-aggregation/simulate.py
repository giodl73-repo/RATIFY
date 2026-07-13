#!/usr/bin/env python3
"""Compare aggregation methods for complete fiscally balanced ballots."""

import json
import math
import random
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent


def weighted_choice(rng, rows):
    point = rng.random()
    for row in rows:
        point -= row["weight"]
        if point <= 0:
            return row
    return rows[-1]


def dirichlet(rng, alpha):
    values = [rng.gammavariate(value, 1.0) for value in alpha]
    total = sum(values)
    return [value / total * 100.0 for value in values]


def distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def closure(row, width):
    return sum(row[:width]) - sum(row[width:])


def coordinate_mean(ballots):
    return [sum(row[index] for row in ballots) / len(ballots) for index in range(len(ballots[0]))]


def coordinate_median(ballots):
    return [statistics.median(row[index] for row in ballots) for index in range(len(ballots[0]))]


def trimmed_mean(ballots, trim=0.1):
    result = []
    cut = int(len(ballots) * trim)
    for index in range(len(ballots[0])):
        values = sorted(row[index] for row in ballots)[cut:len(ballots)-cut]
        result.append(sum(values) / len(values))
    return result


def geometric_median(ballots, iterations=100):
    point = coordinate_mean(ballots)
    for _ in range(iterations):
        weights = [1.0 / max(distance(point, row), 1e-9) for row in ballots]
        updated = [sum(weight * row[index] for weight, row in zip(weights, ballots)) / sum(weights) for index in range(len(point))]
        if distance(point, updated) < 1e-8:
            return updated
        point = updated
    return point


def approximate_medoid(ballots, rng, candidates=400, evaluation=1600):
    candidate_rows = rng.sample(ballots, min(candidates, len(ballots)))
    evaluation_rows = rng.sample(ballots, min(evaluation, len(ballots)))
    return min(candidate_rows, key=lambda candidate: sum(distance(candidate, row) for row in evaluation_rows))


def method_record(name, row, ballots, width, actual_ballot):
    return {
        "method": name,
        "uses_sum": sum(row[:width]),
        "funding_sum": sum(row[width:]),
        "fiscal_closure_gap": closure(row, width),
        "mean_distance_to_ballots": sum(distance(row, ballot) for ballot in ballots) / len(ballots),
        "actual_cast_ballot": actual_ballot,
        "vector": row
    }


def main():
    config = json.loads((HERE / "config.v1.json").read_text(encoding="utf-8"))
    rng = random.Random(config["seed"])
    if abs(sum(row["weight"] for row in config["archetypes"]) - 1.0) > 1e-9:
        raise ValueError("archetype weights must sum to one")
    ballots = []
    for _ in range(config["ballots"]):
        archetype = weighted_choice(rng, config["archetypes"])
        uses_alpha = list(archetype["uses"])
        funding_alpha = list(archetype["funding"])
        if rng.random() < config["outlier_probability"]:
            uses_alpha[rng.randrange(len(uses_alpha))] *= 12.0
            funding_alpha[rng.randrange(len(funding_alpha))] *= 12.0
        ballots.append(dirichlet(rng, uses_alpha) + dirichlet(rng, funding_alpha))

    width = len(config["uses"])
    if any(abs(closure(row, width)) > 1e-8 for row in ballots):
        raise ValueError("cast ballot is not closed")
    medoid = approximate_medoid(ballots, rng)
    methods = [
        method_record("arithmetic_mean", coordinate_mean(ballots), ballots, width, False),
        method_record("fieldwise_median", coordinate_median(ballots), ballots, width, False),
        method_record("fieldwise_trimmed_mean_10_percent", trimmed_mean(ballots), ballots, width, False),
        method_record("feasible_geometric_median", geometric_median(ballots), ballots, width, False),
        method_record("approximate_actual_ballot_medoid", medoid, ballots, width, True)
    ]
    output = {
        "experiment_id": config["experiment_id"],
        "simulation_status": config["simulation_status"],
        "seed": config["seed"],
        "ballots": len(ballots),
        "ballot_invariant": "uses_sum_100_and_funding_sum_100",
        "columns": config["uses"] + config["funding"],
        "methods": methods,
        "interpretation_boundary": "Method comparison on synthetic balanced ballots; not a public preference estimate."
    }
    out = HERE / "outputs"
    out.mkdir(exist_ok=True)
    (out / "run.v1.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    lines = ["# Balanced Ballot Aggregation — V1", "",
             "> Synthetic method test, not public opinion.", "",
             f"Generated **{len(ballots):,}** complete ballots. Every ballot allocates 100 use points and 100 funding points.", "",
             "| Method | Uses | Funding | Closure gap | Mean voter distance | Actual ballot? |",
             "|---|---:|---:|---:|---:|:---:|"]
    for row in methods:
        lines.append(f"| {row['method']} | {row['uses_sum']:.3f} | {row['funding_sum']:.3f} | {row['fiscal_closure_gap']:+.3f} | {row['mean_distance_to_ballots']:.3f} | {'yes' if row['actual_cast_ballot'] else 'no'} |")
    broken = [row for row in methods if abs(row["fiscal_closure_gap"]) > 0.01]
    lines += ["", "## Result", "",
              f"**{len(broken)} of {len(methods)} methods break fiscal closure without an additional repair rule.**",
              "The arithmetic mean and feasible geometric median preserve closure because they remain weighted combinations of complete ballots. The actual-ballot medoid is both closed and interpretable as a package somebody really chose. Fieldwise robust statistics can splice dimensions together and require a disclosed feasibility repair.", "",
              "## Ratification use", "",
              "Aggregation constructs a candidate challenger; it does not enact law. The resulting complete package still receives legal, fiscal, rights, distribution, and implementation review before facing current law in a Yes/No ratification.", ""]
    (out / "run.v1.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
