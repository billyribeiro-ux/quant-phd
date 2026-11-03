"""Round-4: check the reference's docstring invariants of QuantileSketch on the 50 seeds' streams and on random streams.

Invariants stated in reference.py (QuantileSketch docstring): after each add, the sum of g equals n, and g + delta never
exceeds floor(2 epsilon n) + 1; each stored value's exact rank range [running g sum, running g sum + delta] contains a copy.
"""

from __future__ import annotations

import math
import random
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "course/modules/CS/CS2/grader"))
from instance import make_instance  # noqa: E402
from reference import QuantileSketch  # noqa: E402

import json  # noqa: E402

bad = 0
checked = 0
streams: list[list[float]] = []
for seed in range(50):
    streams.append([float(x) for x in json.loads(make_instance(seed)["payload"])["values"]])
rng = random.Random(4)
for _ in range(200):
    streams.append([round(rng.uniform(0, 3), 1) for _ in range(rng.randint(1, 120))])
for stream in streams:
    eps = rng.choice([0.05, 0.1, 0.2])
    sk = QuantileSketch(eps)
    for n, x in enumerate(stream, start=1):
        sk.add(x)
        checked += 1
        if sum(sk._g) != n:
            bad += 1
        cap = math.floor(2 * Fraction(eps) * n) + 1
        if any(g + d > cap for g, d in zip(sk._g, sk._delta)):
            bad += 1
        # the stored values are sorted; each stored value's rank window must contain a copy of it
        running = 0
        for i, (v, g, d) in enumerate(zip(sk._values, sk._g, sk._delta)):
            running += g
            copies = [j + 1 for j, y in enumerate(sorted(stream[:n])) if y == v]
            if not any(running <= r <= running + d for r in copies):
                bad += 1
                break
print(f"adds checked: {checked}; invariant violations: {bad}; streams: {len(streams)}")
