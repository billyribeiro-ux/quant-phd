"""Independent re-derivation of every number on the FC2 project page (round 14), with exact Fractions.

Usage: python3 rederive.py <checkout>. Reads the two lab chains from project.html text is NOT used; the chains are
typed from the page's Lab 1 and Lab 3 hypotheses and code, and the reference scan is run on each for comparison.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from fractions import Fraction as F
from pathlib import Path

root = Path(sys.argv[1])


def half_up(x: F) -> int:
    return math.floor(x + F(1, 2))


def gap(c: int, p: int, s: int, k: int, df_ppm: int) -> F:
    return F(c) - F(p) - (F(s) - F(k) * F(df_ppm, 1_000_000))


def chord_minus_call(ks: list[int], cs: list[int], j: int) -> F:
    # chord through (ks[j-1], cs[j-1]) and (ks[j+1], cs[j+1]) at ks[j], less cs[j]
    lo, mid, hi = ks[j - 1], ks[j], ks[j + 1]
    return (F(hi - mid) * cs[j - 1] + F(mid - lo) * cs[j + 1]) / F(hi - lo) - cs[j]


def scan(name: str, ks, cs, ps, s, df, fee, spread):
    cost = 3 * (fee + spread)
    print(f"== {name}: cost per finding {cost}")
    kept = []
    for i, k in enumerate(ks):
        g = gap(cs[i], ps[i], s, k, df)
        gross = half_up(abs(g))
        net = gross - cost
        print(f"  parity K={k}: gap={g} gross={gross} net={net} kept={net > 0}")
        if net > 0:
            kept.append(("parity", k, gross, net))
    for j in range(1, len(ks) - 1):
        d = chord_minus_call(ks, cs, j)
        if d < 0:
            gross = half_up(-d)
            net = gross - cost
            print(f"  convexity K={ks[j]}: chord-call={d} gross={gross} net={net} kept={net > 0}")
            if net > 0:
                kept.append(("convexity", ks[j], gross, net))
        else:
            print(f"  convexity K={ks[j]}: chord-call={d} no violation")
    print("  kept:", kept)
    return kept


lab1 = dict(ks=[9000, 9500, 10000, 10500, 11000, 11500], cs=[1500, 1100, 800, 700, 450, 350],
            ps=[410, 385, 700, 1095, 1360, 1735], s=10000, df=990000, fee=5, spread=10)
lab3 = dict(ks=[4000, 4500, 5000, 6000, 6500, 7000], cs=[1210, 820, 500, 330, 151, 90],
            ps=[10, 155, 250, 1030, 1100, 1200], s=5000, df=950000, fee=8, spread=12)
k1 = scan("Lab 1 chain", **lab1)
k3 = scan("Lab 3 chain", **lab3)
assert k1 == [("parity", 9500, 120, 75), ("convexity", 10500, 75, 30)], k1
assert k3 == [("parity", 6500, 226, 166), ("parity", 7000, 540, 480), ("convexity", 6000, 63, 3)], k3
assert chord_minus_call(lab3["ks"], lab3["cs"], 3) == F(-188, 3)
assert chord_minus_call(lab3["ks"], lab3["cs"], 2) == F(470, 3)
assert F(500 + 2 * 151, 3) == F(802, 3)
assert gap(151, 1100, 5000, 6500, 950000) == 226 and half_up(F(226)) == 226
print("chord at 6000 exact:", F(802, 3) - 330, " gross", half_up(F(188, 3)), "float check:", round(188 / 3, 2))
print("Lab 3 discounted strikes: 6500 ->", F(6500) * F(950000, 10**6), " 7000 ->", F(7000) * F(950000, 10**6))
assert F(6500) * F(950000, 10**6) == 6175 and F(7000) * F(950000, 10**6) == 6650

# reference scan on both chains must equal the hand derivation above
spec = importlib.util.spec_from_file_location("ref", root / "course/modules/FC/FC2/grader/reference.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
for name, lab in (("lab1", lab1), ("lab3", lab3)):
    chain = {"spot_cents": lab["s"], "df_ppm": lab["df"], "strikes_cents": lab["ks"], "call_cents": lab["cs"],
             "put_cents": lab["ps"], "cost": {"fee_cents_per_contract": lab["fee"], "half_spread_cents": lab["spread"]}}
    rows = [(r["kind"], r["strike_cents"], r["gross_cents"], r["net_cents"]) for r in ref.scan(chain)]
    print(name, "reference.scan:", rows)
    assert rows == (k1 if name == "lab1" else k3), (name, rows)
print("ALL ASSERTIONS PASS")
