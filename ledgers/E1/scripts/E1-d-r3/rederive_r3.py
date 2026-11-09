"""Independent re-derivation of the project page's numbers, Propositions 1-5 orderings, and the instance ranges.

Uses its own trapezoid-based integrals (not the reference module) with exact Fractions.
"""

from __future__ import annotations

import math
import random
import sys
from fractions import Fraction as F

sys.path.insert(0, sys.argv[1] + "/course/modules/E/E1/grader")
from instance import make_instance  # noqa: E402


def hu(x: F) -> int:
    return math.floor(x + F(1, 2))


def exact(s: str, a: int, b: int, c: int) -> dict[str, F]:
    # independent: volume and fee from inverse demand, integrals via midpoint-free trapezoid on [0, x]
    gap = F(a - b * c)
    vol = {"monopoly": gap / 2, "cournot": 2 * gap / 3, "bertrand": gap}[s]
    fee = (F(a) - vol) / b
    def G(x: F) -> F:  # integral_0^x (a - t)/b dt, trapezoid exact for linear
        return x * ((F(a) / b) + (F(a) - x) / b) / 2
    cs = G(vol) - fee * vol
    profit = (fee - c) * vol
    welfare = cs + profit
    dwl = (G(gap) - c * gap) - (G(vol) - c * vol)
    return {"V": vol, "F": fee, "P": profit, "CS": cs, "W": welfare, "DWL": dwl}


def rounded(s: str, a: int, b: int, c: int) -> dict[str, int]:
    e = exact(s, a, b, c)
    return {k: hu(v) for k, v in e.items()}


# 1. page numbers, a = 120 and a = 121
for a in (120, 121):
    for s in ("monopoly", "cournot", "bertrand"):
        print(a, s, {k: (str(v), hu(v)) for k, v in exact(s, a, 1, 20).items()})

# 2. instance ranges and orderings over seeds 0..9999
bmin = cmin = gmin = 10**9
bmax = cmax = gmax = 0
bad_inst = 0
bad_order = []
for seed in range(10000):
    inst = make_instance(seed)
    b, c, a = inst["b"], inst["c"], inst["a"]
    gap = a - b * c
    bmin, bmax = min(bmin, b), max(bmax, b)
    cmin, cmax = min(cmin, c), max(cmax, c)
    gmin, gmax = min(gmin, gap), max(gmax, gap)
    if not (a > b * c > 0) or not (gap > 6 * b):
        bad_inst += 1
    r = {s: rounded(s, a, b, c) for s in ("monopoly", "cournot", "bertrand")}
    m, cn, bt = r["monopoly"], r["cournot"], r["bertrand"]
    ok = (
        m["V"] < cn["V"] < bt["V"]
        and m["F"] > cn["F"] > bt["F"]
        and m["W"] < cn["W"] < bt["W"]
        and m["DWL"] > cn["DWL"] > bt["DWL"]
        and m["P"] > cn["P"] + bt["P"] and cn["P"] > bt["P"]
    )
    if not ok:
        bad_order.append(seed)
print("instance ranges over 10000 seeds: b", (bmin, bmax), "c", (cmin, cmax), "gap", (gmin, gmax), "invalid", bad_inst)
print("printed strict-order failures over 10000 seeds:", len(bad_order), bad_order[:5])

# 3. grid of whole-number cases with gap > 6b (b 1..10, c 1..60, gap 6b+1..400)
fails = 0
total = 0
for b in range(1, 11):
    for c in range(1, 61):
        for gap in range(6 * b + 1, 401):
            a = b * c + gap
            total += 1
            r = {s: rounded(s, a, b, c) for s in ("monopoly", "cournot", "bertrand")}
            m, cn, bt = r["monopoly"], r["cournot"], r["bertrand"]
            ok = (
                m["V"] < cn["V"] < bt["V"]
                and m["F"] > cn["F"] > bt["F"]
                and m["W"] < cn["W"] < bt["W"]
                and m["DWL"] > cn["DWL"] > bt["DWL"]
                and m["P"] > cn["P"] > bt["P"]
            )
            fails += not ok
print("grid cases", total, "order failures", fails)

# 4. the exact identities on the page: profit gap, DWL, welfare gap at random rationals
rng = random.Random(1)
idc = 0
for _ in range(2000):
    b = rng.randint(1, 9)
    c = rng.randint(1, 50)
    gap = rng.randint(1, 300)
    a = b * c + gap
    d = F(gap)
    m = exact("monopoly", a, b, c)
    cn = exact("cournot", a, b, c)
    ok = (
        m["P"] - cn["P"] == d * d / (36 * b)
        and m["DWL"] == d * d / (8 * b)
        and cn["DWL"] == d * d / (18 * b)
        and cn["W"] - m["W"] == F(5, 72) * d * d / b
    )
    idc += not ok
print("identity failures (profit gap, DWL) over 2000 random cases:", idc)
