"""Structured streams (decreasing chains between fixed extremes, then random) against a QuantileSketch variant.

Usage: python -I structured_probe.py <variant.py>. Prints violations of the two rank inequalities (exact counts)."""

from __future__ import annotations

import importlib.util
import random
import sys
from bisect import bisect_left, bisect_right
from fractions import Fraction
from pathlib import Path

spec = importlib.util.spec_from_file_location("variant", Path(sys.argv[1]).resolve())
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
Sketch = mod.QuantileSketch
found = 0
checked = 0


def run(stream: list[float], eps: float) -> None:
    global found, checked
    sk = Sketch(eps)
    for x in stream:
        sk.add(x)
    srt = sorted(stream)
    n = len(stream)
    for k in range(0, 101):
        q = k / 100
        v = sk.quantile(q)
        below = bisect_left(srt, v)
        at = bisect_right(srt, v)
        checked += 1
        if not (below <= Fraction(q) * n + Fraction(eps) * n and at >= Fraction(q) * n - Fraction(eps) * n):
            found += 1
            if found <= 3:
                print(f"VIOLATION eps={eps} n={n} q={q} v={v} below={below} at={at}")
            return


for eps in (0.05, 0.1, 0.2):
    for n_total in (60, 120, 240, 400):
        # decreasing chain placed between a fixed minimum and maximum, the rest interleaved
        stream = [0.0, 1000.0]
        stream += [999.0 - i * 0.5 for i in range(n_total - 2)]
        run(stream, eps)
        # chain of increasing values that each land before the same successor
        stream2 = [0.0, 1000.0] + [1.0 + i * 0.5 for i in range(n_total - 2)]
        run(stream2, eps)
        rng = random.Random(n_total)
        for _ in range(30):
            head = [0.0, 1000.0]
            tail = [rng.choice([rng.uniform(0, 1000), 999.0 - rng.randint(0, 500) * 0.5]) for _ in range(n_total - 2)]
            run(head + tail, eps)
print(f"{Path(sys.argv[1]).name}: checked={checked} violations={found}")
