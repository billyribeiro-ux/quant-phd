"""Verifier round 2, slice d: independent re-derivation of the project page's numbers and propositions.

Uses only fractions and the grader's instance generator (read, not imported from the reference).
Usage: .venv/bin/python -I ledgers/E1/scripts/E1-d-r2/rederive_r2.py
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "course/modules/E/E1/grader"))
from instance import make_instance  # noqa: E402


def rnd(x: Fraction) -> int:
    return math.floor(x + Fraction(1, 2))


def outcome(s: str, a: int, b: int, c: int) -> dict[str, Fraction]:
    d = Fraction(a - b * c)
    if s == "monopoly":
        v, f = d / 2, Fraction(a + b * c, 2 * b)
    elif s == "cournot":
        v, f = 2 * d / 3, Fraction(a + 2 * b * c, 3 * b)
    else:
        v, f = d, Fraction(c)
    pr = (f - c) * v
    cs = v * v / (2 * b)
    w = cs + pr
    dwl = (d - v) ** 2 / (2 * b)
    # independent check of the fee: inverse demand at the volume
    assert f == (a - v) / b, (s, a, b, c)
    # independent check of welfare: integral of inverse demand less cost, by midpoint-free exact formula
    gross = (a * v - v * v / 2) / b
    assert w == gross - c * v, (s, a, b, c)
    return {"v": v, "f": f, "pi": pr, "cs": cs, "w": w, "dwl": dwl}


fails: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        fails.append(msg)


# 1. Reference case and tie case: exact values quoted in the prose and expected blocks.
ref = {s: outcome(s, 120, 1, 20) for s in ("monopoly", "cournot", "bertrand")}
tie = {s: outcome(s, 121, 1, 20) for s in ("monopoly", "cournot", "bertrand")}
check(ref["monopoly"]["v"] == 50 and ref["monopoly"]["f"] == 70, "monopoly 50 trades 70 cents")
check(ref["cournot"]["v"] == Fraction(200, 3) and ref["cournot"]["f"] == Fraction(160, 3), "cournot 200/3, 160/3")
check(
    ref["cournot"]["pi"] == Fraction(20000, 9) and ref["cournot"]["cs"] == Fraction(20000, 9),
    "cournot profit and CS 20000/9",
)
check(
    ref["cournot"]["w"] == Fraction(40000, 9) and ref["cournot"]["dwl"] == Fraction(5000, 9),
    "cournot W 40000/9, DWL 5000/9",
)
check(
    ref["monopoly"]["pi"] == 2500 and ref["monopoly"]["cs"] == 1250 and ref["monopoly"]["w"] == 3750,
    "mono 2500/1250/3750",
)
check(
    ref["monopoly"]["dwl"] == 1250 and ref["bertrand"]["w"] == 5000 and ref["bertrand"]["dwl"] == 0,
    "dwl 1250, B 5000, 0",
)
check(ref["bertrand"]["pi"] == 0 and ref["bertrand"]["f"] == 20 and ref["bertrand"]["v"] == 100, "bertrand 0,20,100")
check(
    tie["monopoly"]["f"] == Fraction(141, 2) and tie["monopoly"]["v"] == Fraction(101, 2),
    "tie a=121 fee 141/2 vol 101/2",
)
check(tie["monopoly"]["pi"] == Fraction(10201, 4), "tie monopoly profit 10201/4 = 2550.25")
check(
    tie["cournot"]["f"] == Fraction(161, 3) and tie["cournot"]["v"] == Fraction(202, 3),
    "tie cournot fee 161/3 vol 202/3",
)
expected_tie = {
    "monopoly": (51, 71, 2550, 1275, 3825, 1275),
    "cournot": (67, 54, 2267, 2267, 4534, 567),
    "bertrand": (101, 20, 0, 5101, 5101, 0),
}
keys = ("v", "f", "pi", "cs", "w", "dwl")
for s, exp in expected_tie.items():
    got = tuple(rnd(tie[s][k]) for k in keys)
    check(got == exp, f"tie block {s}: got {got} want {exp}")
expected_ref = {
    "monopoly": (50, 70, 2500, 1250, 3750, 1250),
    "cournot": (67, 53, 2222, 2222, 4444, 556),
    "bertrand": (100, 20, 0, 5000, 5000, 0),
}
for s, exp in expected_ref.items():
    got = tuple(rnd(ref[s][k]) for k in keys)
    check(got == exp, f"ref block {s}: got {got} want {exp}")

# 2. Prose numbers in Exemplar B and the comparison paragraph.
check(Fraction(100, 3) ** 2 / 2 == Fraction(5000, 9), "(100/3)^2/2 = 5000/9")
check(70 - Fraction(160, 3) == Fraction(50, 3) == Fraction(100, 1) / 6, "fee gap 50/3 = d/(6b)")
check(
    Fraction(200, 3) - 50 == Fraction(50, 3) and 100 - Fraction(200, 3) == Fraction(100, 3),
    "volume gaps 50/3 and 100/3",
)
check(
    Fraction(20000, 9) == Fraction(2222, 1) + Fraction(2, 9)
    and Fraction(2500) - Fraction(20000, 9) == Fraction(2500, 9),
    "profit gap 2500/9",
)
check(Fraction(10000, 36) == Fraction(2500, 9), "d^2/(36b) with d=100,b=1 is 2500/9 = 277.8")
check(4444 - 3750 == 694 and 5000 - 4444 == 556, "printed welfare differences +694 +556")
check(67 - 50 == 17 and 100 - 67 == 33 and 53 - 70 == -17 and 20 - 53 == -33, "printed volume/fee diffs")
check(
    Fraction(40000, 9) - 3750 == Fraction(40000 - 33750, 9)
    and Fraction(40000, 9) - Fraction(33750, 9) == Fraction(6250, 9),
    "exact welfare diff",
)
check(
    Fraction(67, 1) == rnd(Fraction(200, 3)) and rnd(Fraction(202, 3)) == 67,
    "Cournot volume 67 for both a=120 and a=121",
)

# 3. Lab 2 error bound: |q_60 - d/3| = d/(3 * 2^60) < 1e-12, and the iterate is exact.
d = Fraction(100)
q = Fraction(0)
for _ in range(60):
    q = (d - q) / 2
check(abs(q - d / 3) == d / (3 * 2**60), "error after 60 steps is d/(3 2^60)")
check(abs(q - d / 3) < Fraction(1, 10**12), "lab 2 comparison True")

# 4. Propositions on grids (sanity; the proofs are read separately).
# Proposition 1: maximiser of ((a-qv)/b - c) qv on a grid of 1/8.
a, b, c = 120, 1, 20
grid = [Fraction(k, 8) for k in range(0, 8 * 120 + 1)]
best = max(grid, key=lambda qv: ((a - qv) / b - c) * qv)
check(best == 50, f"Prop 1 grid maximiser {best}")

# Proposition 2: Cournot best response equals max(0, (d - qj)/2) on a grid, and unique grid equilibrium.
a2, b2, c2 = 119, 1, 20  # d = 99, d/3 = 33 on a half grid
d2 = a2 - b2 * c2
g2 = [Fraction(k, 2) for k in range(0, 2 * d2 + 1)]


def profit2(qi: Fraction, qj: Fraction) -> Fraction:
    return ((a2 - qi - qj) / b2 - c2) * qi


for qj in g2[::7]:
    br = max(g2, key=lambda qi: profit2(qi, qj))
    check(
        br == max(Fraction(0), (d2 - qj) / 2) or abs(br - max(Fraction(0), (d2 - qj) / 2)) <= Fraction(1, 2),
        f"Prop 2 best response at qj={qj}: {br}",
    )
eqs = [
    (x, y)
    for x in g2
    for y in g2
    if max(g2, key=lambda t: profit2(t, y)) == x and max(g2, key=lambda t: profit2(t, x)) == y
]
check(eqs == [(Fraction(33), Fraction(33))], f"Prop 2 grid equilibria {eqs}")

# Proposition 3: Bertrand grid equilibria for a=40, b=1, c=10 on a quarter grid.
a3, b3, c3 = 40, 1, 10
g3 = [Fraction(k, 4) for k in range(0, 4 * a3 // b3 + 1)]


def bprofit(fi: Fraction, fj: Fraction) -> Fraction:
    dem = a3 - b3 * fi
    if fi < fj:
        share = dem
    elif fi == fj:
        share = dem / 2
    else:
        share = Fraction(0)
    return (fi - c3) * share


eq3 = []
for f1 in g3:
    for f2 in g3:
        ok1 = all(bprofit(f1, f2) >= bprofit(t, f2) for t in g3)
        ok2 = all(bprofit(f2, f1) >= bprofit(t, f1) for t in g3)
        if ok1 and ok2:
            eq3.append((f1, f2))
check(
    eq3 == [(Fraction(c3), Fraction(c3)), (Fraction(41, 4), Fraction(41, 4))], f"Prop 3 quarter-grid equilibria {eq3}"
)
# Refinement: deviations on a 1/64 grid (dyadic, so exact in floats), profiles on the quarter grid.
# The quarter grid has no point strictly between 10 and 10.25, so (41/4, 41/4) is a grid artifact;
# the deviation to (10 + 10.25)/2 = 10.125 (= (f + c)/2 in the proof) must show it is not an equilibrium.
g3f = [k / 64 for k in range(0, 64 * a3 // b3 + 1)]


def bprofit_f(fi: float, fj: float) -> float:
    dem = a3 - b3 * fi
    share = dem if fi < fj else (dem / 2 if fi == fj else 0.0)
    return (fi - c3) * share


eq3f = []
for f1 in [float(x) for x in g3]:
    for f2 in [float(x) for x in g3]:
        base1, base2 = bprofit_f(f1, f2), bprofit_f(f2, f1)
        if all(base1 >= bprofit_f(t, f2) for t in g3f) and all(base2 >= bprofit_f(t, f1) for t in g3f):
            eq3f.append((f1, f2))
check(eq3f == [(float(c3), float(c3))], f"Prop 3 refined equilibria {eq3f}")

# Proposition 4 identities on a grid of qv in [0, d] for several (a,b,c).
for a4, b4, c4 in [(120, 1, 20), (121, 3, 5), (400, 2, 60), (61, 1, 5)]:
    d4 = Fraction(a4 - b4 * c4)
    for k in range(0, 41):
        qv = d4 * k / 40
        f4 = (a4 - qv) / b4
        cs4 = qv * qv / (2 * b4)
        pr4 = (f4 - c4) * qv
        w4 = (a4 * qv - qv * qv / 2) / b4 - c4 * qv
        check(cs4 + pr4 == w4, f"Prop 4 CS+profit=W at {(a4, b4, c4, qv)}")
        check(
            (((a4 * d4 - d4 * d4 / 2) / b4 - c4 * d4) - w4) == (d4 - qv) ** 2 / (2 * b4),
            f"Prop 4 DWL at {(a4, b4, c4, qv)}",
        )

# 5. Prop 5 printed ordering: for all b in 1..3, c in 5..60, gap in 60..400 (instance ranges), and seeds 0..9999.
n_checked = 0
for seed in range(10000):
    inst = make_instance(seed)
    a5, b5, c5 = inst["a"], inst["b"], inst["c"]
    check(a5 > b5 * c5 > 0 and a5 - b5 * c5 > 6 * b5, f"instance seed {seed} gap not above 6b")
    o = {s: {k: rnd(v) for k, v in outcome(s, a5, b5, c5).items()} for s in ("monopoly", "cournot", "bertrand")}
    m, co, be = o["monopoly"], o["cournot"], o["bertrand"]
    ok = (
        m["v"] < co["v"] < be["v"]
        and m["f"] > co["f"] > c5
        and m["w"] < co["w"] < be["w"]
        and m["dwl"] > co["dwl"] > be["dwl"]
        and m["pi"] > co["pi"]
    )
    check(ok, f"Prop 5 printed order fails at seed {seed}")
    n_checked += 1

# Prop 5 exact claim for an arbitrary grid (b=1..10, c=1..60, d=6b+1..400).
n5 = 0
for b5 in range(1, 11):
    for c5 in range(1, 61):
        for gap in range(6 * b5 + 1, 401):
            a5 = b5 * c5 + gap
            d5 = Fraction(gap)
            ex = {s: outcome(s, a5, b5, c5) for s in ("monopoly", "cournot", "bertrand")}
            check(ex["monopoly"]["f"] - ex["cournot"]["f"] == d5 / (6 * b5), "fee diff d/(6b)")
            check(ex["cournot"]["f"] - c5 == d5 / (3 * b5), "cournot fee minus c = d/(3b)")
            check(ex["monopoly"]["pi"] - ex["cournot"]["pi"] == d5 * d5 / (36 * b5), "profit diff d^2/(36b)")
            check(
                ex["cournot"]["w"] - ex["monopoly"]["w"] == Fraction(5, 72) * d5 * d5 / b5, "W(2d/3)-W(d/2)=5d^2/(72b)"
            )
            n5 += 1
print(f"Prop 5 grid cases: {n5}; instance seeds checked: {n_checked}")
print("failures:", len(fails))
for f_ in fails[:20]:
    print("FAIL:", f_)
