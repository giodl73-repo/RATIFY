#!/usr/bin/env python3
"""Validate packet symmetry and write a reproducible SHA-256 input lock."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REQUIRED_CANDIDATE_FIELDS = {"id", "target", "marginal_policy", "automatic_corridor", "outside_corridor"}
REQUIRED_PACKET_FILES = ["README.md", "nonfiscal-legal-review.md", "human-comprehension-protocol.md"]


def main():
    manifest = json.loads((HERE / "manifest.v1.json").read_text(encoding="utf-8"))
    if len(manifest["candidates"]) != 2:
        raise ValueError("packet must contain exactly two construction candidates")
    for candidate in manifest["candidates"]:
        if set(candidate) != REQUIRED_CANDIDATE_FIELDS:
            raise ValueError(f"asymmetric candidate fields for {candidate.get('id')}")
    if len({candidate["id"] for candidate in manifest["candidates"]}) != 2:
        raise ValueError("candidate IDs must be unique")
    for filename in REQUIRED_PACKET_FILES:
        if not (HERE / filename).is_file():
            raise FileNotFoundError(filename)
    lock = []
    for relative in manifest["common_inputs"]:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        lock.append({"path": relative, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    output = {"packet_id": manifest["packet_id"], "manifest": "review-packets/v1/manifest.v1.json", "inputs": lock}
    (HERE / "input-lock.v1.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    completeness = {
        "packet_id": manifest["packet_id"],
        "internal_packet_complete": True,
        "candidate_symmetry_validated": True,
        "locked_common_inputs": len(lock),
        "external_reviews_completed": False,
        "unresolved_external_dependencies": manifest["known_dependencies"],
        "ballot_ready": False
    }
    (HERE / "completeness.v1.json").write_text(json.dumps(completeness, indent=2) + "\n", encoding="utf-8")
    print(f"validated {len(manifest['candidates'])} symmetric candidates and locked {len(lock)} common inputs")


if __name__ == "__main__":
    main()
