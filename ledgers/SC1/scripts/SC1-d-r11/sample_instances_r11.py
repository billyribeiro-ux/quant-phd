#!/usr/bin/env python3
"""Sample 20 seeds: validity of grader/instance.py instances, and whether the reference answers change with the seed."""

from __future__ import annotations

import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "course/modules/SC/SC1/grader"))
from instance import make_instance  # noqa: E402

SEEDS = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]


def tail(a: float, h: float) -> float:
    return math.erfc(a / math.sqrt(2.0 * h))


def one_step(inst: dict) -> float:
    rng = random.Random(int(inst["seed"]))
    sd = math.sqrt(inst["H"])
    hits = sum(1 for _ in range(inst["n_paths"]) if rng.gauss(0.0, sd) >= inst["a"])
    return hits / inst["n_paths"]


def main() -> None:
    answers = set()
    for seed in SEEDS:
        inst = make_instance(seed)
        valid = (
            inst["H"] > 0
            and inst["a"] > 0
            and 4 <= inst["n_steps"] <= 256
            and 400 <= inst["n_paths"] <= 800
            and inst["n_steps"] * inst["n_paths"] <= 200_000
            and inst["label"] == "SIMULATED"
        )
        answers.add(round(tail(inst["a"], inst["H"]), 9))
        print(f"seed {seed:5d} H={inst['H']:.3f} a={inst['a']:.3f} n={inst['n_steps']:3d} N={inst['n_paths']:3d} "
              f"tail={tail(inst['a'], inst['H']):.6f} one_step={one_step(inst):.6f} valid={valid}")
    print(f"distinct tails over 20 seeds: {len(answers)}")


if __name__ == "__main__":
    main()
