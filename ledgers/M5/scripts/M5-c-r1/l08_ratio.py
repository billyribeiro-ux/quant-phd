"""Unrounded largest sampled contraction ratio of L08 Lab 1 Part B, and the L08 worked values.

Usage: python3 -I l08_ratio.py <repo-root>
"""

import math
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
src = (root / "tests/labs/M5/lab-M5-L08-1.py").read_text(encoding="utf-8")
head = src.split("def part_a()")[0].replace("\nmain()", "")
g: dict[str, object] = {"__name__": "lab_head"}
exec(compile(head, "head", "exec"), g)
GRID = g["GRID"]
BETA = g["BETA"]
bellman = g["bellman"]
import random

rng = random.Random(g["SEED"])
worst = 0.0
for _ in range(g["PAIRS"]):
    v = [rng.uniform(-10.0, 10.0) for _ in GRID]
    w = [rng.uniform(-10.0, 10.0) for _ in GRID]
    bv, _ = bellman(v, GRID, BETA)
    bw, _ = bellman(w, GRID, BETA)
    num = max(abs(a - b) for a, b in zip(bv, bw, strict=True))
    den = max(abs(a - b) for a, b in zip(v, w, strict=True))
    worst = max(worst, num / den)
print("unrounded worst ratio:", repr(worst))
print("worst - beta:", repr(worst - BETA), " in units of 2^-52 (ulp at 1):", (worst - BETA) / 2**-52)
print("worst > beta + 1e-12:", worst > BETA + 1e-12)

# Example 1.2 and M1/E2 numbers
print("Ex1.2 (BV)(1.0) =", math.sqrt(0.75), " F(1.0) check:", [kp for kp in (0.25, 1.0) if kp <= 1.0**0.5])
print("E2: sqrt(0.5^0.5 - 0.25) =", math.sqrt(0.5**0.5 - 0.25), " 0.9*5 + that =", math.sqrt(0.5**0.5 - 0.25) + 4.5)
print("Ex2.3: 1/(1-0.9)*0.5 =", 0.5 / (1 - 0.9))
print("M2 L8: 0.5/0.05 =", 0.5 / 0.05)
print("M3 F(0.5) output:", 0.5**0.5, " F(0.75) output:", 0.75**0.5)
print("canon break 2: sqrt(2) =", math.sqrt(2))
