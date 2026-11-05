"""Re-derives every number in prose for L04, L05, L06 with exact fractions, and runs the twins' own functions for seeded counts.

Run from the checkout root with: .venv/bin/python -I ledgers/PC3/scripts/PC3-b-r7/prose_numbers.py
"""

from __future__ import annotations

import math
import re
from fractions import Fraction
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

ROOT = Path.cwd()


def load_twin_functions(name: str) -> dict[str, object]:
    src = (ROOT / "tests/labs/PC3" / name).read_text(encoding="utf-8")
    src = src.rstrip("\n")
    assert src.endswith("\nmain()"), name
    src = src[: -len("\nmain()")]  # drop the top-level call so that functions can be imported
    import sys
    import types

    mod = types.ModuleType("twin_" + name.replace("-", "_").replace(".", "_"))
    sys.modules[mod.__name__] = mod
    exec(compile(src, name, "exec"), mod.__dict__)
    return dict(mod.__dict__)


print("== L04 seeded game (lab's own functions)")
l04 = load_twin_functions("lab-PC3-L04-1.py")
for seed in (0, 1):
    path, turns = l04["play"](seed)  # type: ignore[operator]
    fills = [r for r in turns if r.filled]  # type: ignore[attr-defined]
    cash_flow = sum(r.cash_flow_cents for r in fills)  # type: ignore[attr-defined]
    inv = turns[-1].inventory_after  # type: ignore[attr-defined]
    settle = path[20]
    informed = sum(1 for r in turns if r.arrival == "informed")  # type: ignore[attr-defined]
    print(f"seed {seed}: fills {len(fills)}, cash flow {cash_flow}, inventory {inv}, settlement {settle}, "
          f"mark {inv * settle}, P&L {turns[-1].cash_after_cents + inv * settle}, informed arrivals {informed}")  # type: ignore[attr-defined]
    if seed == 0:
        mid = (turns[-1].bid_cents + turns[-1].ask_cents) // 2  # type: ignore[attr-defined]
        print(f"seed 0 last quote {turns[-1].bid_cents}/{turns[-1].ask_cents}, mid {mid}, "  # type: ignore[attr-defined]
              f"P&L at mid {cash_flow + inv * mid}")

print("== L04 fixed-quote closed forms and prose values")
h = Fraction(10)
p = Fraction(1, 2)
a, b = 10010, 9990
for v in (9985, 10000, 10020):
    cf = (1 - p) * h - p * (max(v - a, 0) + max(b - v, 0))
    print(f"v={v}: closed form {cf}")
print("R1 d at p=3/5, h=10:", (1 - Fraction(3, 5)) * 10 / Fraction(3, 5))
print("E2 z:", Fraction(13, 20) - Fraction(1, 2), "se", math.sqrt(0.25 / 20), "z", (0.65 - 0.5) / math.sqrt(0.25 / 20))
print("R3: 25 I^2 < 100 for I=1 ->", 25 * 1, "; I=2 ->", 25 * 4)
print("Remark 4.2: sd at I=3:", 5 * 3, " at I=10:", 5 * 10)
print("Remark 4.2 trade term at I=10:", Fraction(10) * Fraction(1, 4))
print("E3 P&L settle", -9950 + 1 * 9980, " mid", -9950 + 1 * 9990, " diff", 9990 - 9980)
print("M2 L05/L04 E1 mark", -2 * 10020, "P&L", 20100 - 2 * 10020)

print("== L05 seeded counts (lab's own functions)")
l05 = load_twin_functions("lab-PC3-L05-1.py")
xs5 = l05["make_sequence"](5, 200)  # type: ignore[operator]
xs6 = l05["make_sequence"](6, 200)  # type: ignore[operator]
for label, xs in (("seed 5", xs5), ("seed 6", xs6)):
    for k in (8, 32, 200):
        naive, nc = l05["naive_maxima"](xs, k)  # type: ignore[operator]
        fast, ops = l05["deque_maxima"](xs, k)  # type: ignore[operator]
        print(f"{label} k={k}: outputs equal {naive == fast}, naive {nc}, formula {(200 - k + 1) * (k - 1)}, "
              f"deque comparisons {ops.comparisons}, pushes {ops.pushes}, pops {ops.pops}")  # type: ignore[attr-defined]
print("seed 5 first five maxima at k=8:", l05["deque_maxima"](xs5, 8)[0][:5])  # type: ignore[operator]
print("E1 ratio 5239/382 =", float(Fraction(5239, 382)))
print("L05 remark 3.6: 3*200*floor(log2 200) =", 3 * 200 * int(math.log2(200)), " 2n =", 400)

print("== L05 P1/R2 arithmetic")
print("(200-101+1)(101-1) =", (200 - 101 + 1) * (101 - 1), " n^2/4 =", 200 * 200 // 4)

print("== L06 unrounded break-evens and rounding")
def annuity(rate: Fraction) -> Fraction:
    return sum((1 / (1 + rate) ** t for t in range(1, 4)), Fraction(0))

I, m = 15_000_000, 5_000
for rate in (Fraction(8, 100), Fraction(10, 100), Fraction(12, 100)):
    be = Fraction(I, m) / annuity(rate)
    dec = (Decimal(be.numerator) / Decimal(be.denominator)).quantize(Decimal("0.0000001"), rounding=ROUND_HALF_UP)
    print(f"rate {rate}: annuity {annuity(rate)} = {float(annuity(rate)):.8f}, break-even {float(be):.7f} ({dec})")
ann10 = annuity(Fraction(10, 100))
print("annuity at 10% exact:", ann10, "== 3310/1331:", ann10 == Fraction(3310, 1331))
be10 = Fraction(I, m) / ann10
print("break-even 10% exact:", be10, "== 399300/331:", be10 == Fraction(399300, 331), float(be10))
be8 = Fraction(I, m) / annuity(Fraction(8, 100))
be12 = Fraction(I, m) / annuity(Fraction(12, 100))
d1 = Fraction(10**7) * 0 + (be10 - be8)
d2 = be12 - be10
print("differences (unrounded):", float(d1), float(d2), "width 8..12:", float(be12 - be8), "per point:", float((be12 - be8) / 4))
print("E3 values rounded to 4 dp of the unrounded:", f"{float(be8):.4f} {float(be10):.4f} {float(be12):.4f}")
print("printed-value differences:", Fraction("1206.34") - Fraction("1164.10"), Fraction("1249.05") - Fraction("1206.34"))


def npv(cfs: list[Fraction], r: Fraction) -> Fraction:
    return sum((c / (1 + r) ** t for t, c in enumerate(cfs)), Fraction(0))


def cfs(u: Fraction) -> list[Fraction]:
    return [Fraction(-I)] + [u * m] * 3

print("E2 NPV at 1200:", npv(cfs(Fraction(1200)), Fraction(1, 10)), float(npv(cfs(Fraction(1200)), Fraction(1, 10))))
print("E2 NPV at 1300:", npv(cfs(Fraction(1300)), Fraction(1, 10)), float(npv(cfs(Fraction(1300)), Fraction(1, 10))))
grid = [Fraction(u) for u in range(200, 1601, 100)]
print("grid positive count at 10%:", sum(1 for u in grid if npv(cfs(u), Fraction(1, 10)) > 0))
print("NPV at 200 and 1600 by rate sign:", [(float(npv(cfs(Fraction(200)), r)) < 0, float(npv(cfs(Fraction(1600)), r)) > 0) for r in (Fraction(8, 100), Fraction(10, 100), Fraction(12, 100))])
print("R3 margin m* =", float(Fraction(I) * 1331 / (1600 * 3310)), " ratio", float(Fraction(I) * 1331 / (1600 * 3310) / 5000), " fall %", float((1 - Fraction(I) * 1331 / (1600 * 3310) / 5000) * 100))
print("M3 break-even:", Fraction(100000, 400) * Fraction(1331, 3310), float(Fraction(100000, 400) * Fraction(1331, 3310)))
print("E1 annuity at 12%:", float(annuity(Fraction(12, 100))), " break-even 3000/A:", float(3000 / annuity(Fraction(12, 100))))
print("M2 NPV:", -100 + Fraction(60) / Fraction(11, 10) + Fraction(60) / Fraction(121, 100), "vs 500/121 =", Fraction(500, 121))
print("lower bound NPV (exact):", npv(cfs(Fraction(200)), Fraction(1, 10)))
print("upper bound NPV (exact):", npv(cfs(Fraction(1600)), Fraction(1, 10)), float(npv(cfs(Fraction(1600)), Fraction(1, 10))))
