"""Brute-force checks: Lemma 3.1 (IC and IR iff the interval conditions) and Proposition 2.2 (revelation)."""
import itertools
import random
from fractions import Fraction as F

vL, vH = 6000, 10000
D = vH - vL
rng = random.Random(4)
qs = [F(k, 8) for k in range(9)]
ts = list(range(-3000, 12001, 500))
bad = 0
count = 0
for qL, qH in itertools.product(qs, qs):
    for tL, tH in itertools.product(ts, ts):
        UL = vL * qL - tL
        UH = vH * qH - tH
        ic = (UH >= vH * qL - tL) and (UL >= vL * qH - tH)
        ir = UL >= 0 and UH >= 0
        lem = (UL >= 0) and (qL <= qH) and (UL + D * qL <= UH <= UL + D * qH)
        count += 1
        if (ic and ir) != lem:
            bad += 1
print("Lemma 3.1 grid cases", count, "mismatches", bad)

# Proposition 2.2: random finite one-agent mechanisms, equilibria found by enumeration of strategies
trials = 0
fails = 0
for _ in range(300):
    Th = list(range(rng.randint(1, 3)))
    M = list(range(rng.randint(1, 3)))
    X = list(range(rng.randint(1, 3)))
    x = {m: rng.choice(X) for m in M}
    u = {(t, y): rng.randint(-3, 3) for t in Th for y in X}
    strategies = [dict(zip(Th, combo)) for combo in itertools.product(M, repeat=len(Th))]
    for s in strategies:
        is_eq = all(u[(t, x[s[t]])] >= u[(t, x[m])] for t in Th for m in M)
        if not is_eq:
            continue
        trials += 1
        xhat = {t: x[s[t]] for t in Th}
        truthful = all(u[(t, xhat[t])] >= u[(t, xhat[r])] for t in Th for r in Th)
        same = all(xhat[t] == x[s[t]] for t in Th)
        if not (truthful and same):
            fails += 1
print("Proposition 2.2 random equilibria checked", trials, "failures", fails)
