"""Check Lemmas 0-2 of ledgers/CS2/equivalent/README.md on random streams for one sketch variant, after every add:
Lemma 0(a) sum of g = n; 0(b) first tuple g = 1, Delta = 0; Lemma 1 copy invariant (some copy of v_i has rank in
[R_i, M_i] of the sorted stream); Lemma 2 band g + Delta <= max(1, C_n) with the variant's cap C_n; and the rank
guarantee of Lemma 3 at every probe in a grid of q (exact counts).

Usage: python -I lemma_check.py <variant.py> <cap: ref|d8_01|d9_04|d8_02|rank_clamp_free> <trials> <seed>
"""

import importlib.util
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

spec = importlib.util.spec_from_file_location("v", Path(sys.argv[1]).resolve())
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
kind = sys.argv[2]
trials = int(sys.argv[3])
rng = random.Random(int(sys.argv[4]))
PROBES = [Fraction(k, 40) for k in range(41)]


def cap(n: int, eps: Fraction) -> int:
    if kind == "d8_01":
        return math.floor(2 * eps * (n - 1)) + 1
    if kind == "d9_04":
        return math.floor(2 * eps * n)
    return math.floor(2 * eps * n) + 1


fails = {"sum_g": 0, "first": 0, "copy": 0, "band": 0, "guarantee": 0}
states = 0
for t in range(trials):
    n_total = rng.randint(1, 45)
    eps_f = rng.choice([0.05, 0.1, 0.2, 0.3])
    eps = Fraction(eps_f)
    style = rng.random()
    if style < 0.4:
        stream = [float(rng.randint(0, 5)) for _ in range(n_total)]
    elif style < 0.6:
        stream = sorted(float(rng.randint(0, 5)) for _ in range(n_total))
    else:
        stream = [round(rng.uniform(0, 3), 1) for _ in range(n_total)]
    sk = mod.QuantileSketch(eps_f)
    seen: list[float] = []
    for x in stream:
        sk.add(x)
        seen.append(x)
        n = len(seen)
        states += 1
        vals, g, d = sk._values, sk._g, sk._delta
        if sum(g) != n:
            fails["sum_g"] += 1
        if g[0] != 1 or d[0] != 0:
            fails["first"] += 1
        srt = sorted(seen)
        R = 0
        for i in range(len(vals)):
            R += g[i]
            M = R + d[i]
            if not any(srt[r - 1] == vals[i] for r in range(R, M + 1)):
                fails["copy"] += 1
                break
        for i in range(len(vals)):
            if g[i] + d[i] > max(1, cap(n, eps)):
                fails["band"] += 1
                break
        for q in PROBES:
            qf = float(q)  # the probe the sketch receives; the exact rank uses Fraction(qf), as the grader does
            qe = Fraction(qf)
            v = sk.quantile(qf)
            below = sum(1 for y in seen if y < v)
            at = sum(1 for y in seen if y <= v)
            if not (below <= qe * n + eps * n and at >= qe * n - eps * n):
                fails["guarantee"] += 1
                break
print(f"{Path(sys.argv[1]).name} [{kind}]: states {states}, failures {fails}")
