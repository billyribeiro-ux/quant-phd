"""Verifier round 2: variance of the rounded and truncated losses in the grader's rounding test (comment claims ~2.5).

Usage: .venv/bin/python -I ledgers/M4/scripts/M4-d-r2/trunc_variance_r2.py
"""

import random

rng = random.Random(1)
xs = [-rng.gauss(0, 2) for _ in range(400000)]


def sv(v):
    m = sum(v) / len(v)
    return sum((a - m) ** 2 for a in v) / (len(v) - 1)


print("exact variance of the continuous loss:", round(sv(xs), 4))
print("variance after round():", round(sv([round(x) for x in xs]), 4))
print("variance after int() (truncation toward zero):", round(sv([int(x) for x in xs]), 4))
