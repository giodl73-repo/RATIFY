#!/usr/bin/env python3
"""Validate RATIFY Voter Lab model records."""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    model = json.loads((HERE / "archetypes.v1.json").read_text(encoding="utf-8"))
    traits = model["traits"]
    rows = model["archetypes"]
    if model["status"] != "synthetic_prior_not_empirically_calibrated":
        raise ValueError("voter model calibration boundary missing")
    if abs(sum(row["weight"] for row in rows) - 1.0) > 1e-9:
        raise ValueError("archetype weights must sum to one")
    if len({row["id"] for row in rows}) != len(rows):
        raise ValueError("duplicate archetype id")
    for row in rows:
        if len(row["means"]) != len(traits):
            raise ValueError(f"{row['id']} trait width mismatch")
        if any(value < 0 or value > 1 for value in row["means"]):
            raise ValueError(f"{row['id']} trait mean outside zero-to-one range")
        if row["sd"] <= 0 or row["sd"] > 0.5:
            raise ValueError(f"{row['id']} invalid standard deviation")
    print(f"validated {len(rows)} voter mixture components across {len(traits)} traits")


if __name__ == "__main__":
    main()
