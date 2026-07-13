#!/usr/bin/env python3
"""Validate Voter Lab v2 factor structure and sampled sign hypotheses."""

import json
import random
from pathlib import Path

from sample_v2 import sample_traits

HERE = Path(__file__).resolve().parent


def correlation(xs, ys):
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    denominator = (sum((x - mean_x) ** 2 for x in xs) * sum((y - mean_y) ** 2 for y in ys)) ** 0.5
    return numerator / denominator


def main():
    base = json.loads((HERE / "archetypes.v1.json").read_text(encoding="utf-8"))
    model = json.loads((HERE / "correlation-model.v2.json").read_text(encoding="utf-8"))
    if set(model["loadings"]) != set(base["traits"]):
        raise ValueError("v2 loading traits must exactly match v1 traits")
    for trait, loadings in model["loadings"].items():
        if len(loadings) != len(model["factors"]):
            raise ValueError(f"{trait} loading width mismatch")
        if sum(value * value for value in loadings) > 1.0:
            raise ValueError(f"{trait} loadings exceed unit variance")
    rng = random.Random(82002)
    archetype = next(row for row in base["archetypes"] if row["id"] == "cross_pressured_uncertain")
    samples = [sample_traits(rng, archetype, base["traits"], model) for _ in range(30000)]
    columns = {trait:[row[index] for row in samples] for index, trait in enumerate(base["traits"])}
    checks = []
    for left, right, sign in model["declared_sign_checks"]:
        value = correlation(columns[left], columns[right])
        passed = value > 0.05 if sign == "positive" else value < -0.05
        if not passed:
            raise ValueError(f"sign check failed: {left}/{right} {value:.3f}")
        checks.append((left, right, value))
    print("validated v2 factor sampler: " + ", ".join(f"{left}/{right}={value:.2f}" for left, right, value in checks))


if __name__ == "__main__":
    main()
