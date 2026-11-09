"""Round-17 verifier: independent re-derivation of every number on project.html (no lab code imported).

Usage: python -I rederive_r17.py <checkout_root>. Uses decimal, math, statistics and csv only.
Prints the unrounded values and their half-up two-decimal forms, the zero-change months and the extremes.
"""
import csv
import math
import pathlib
import statistics
import sys
from decimal import Decimal, ROUND_HALF_UP

root = pathlib.Path(sys.argv[1])
rows = list(csv.DictReader((root / "course/assets/data/market/fx_monthly.csv").read_text(encoding="utf-8").splitlines()))
gbp = [(r["month"], Decimal(r["GBP"])) for r in rows]


def half_up(x, places=2):
    d = x if isinstance(x, Decimal) else Decimal(repr(x))
    return d.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


# log changes computed as differences of logs (independent of the lab's ratio formula)
changes = [(m, math.log(float(b)) - math.log(float(a))) for (_, a), (m, b) in zip(gbp, gbp[1:])]
w1 = changes
w2 = [c for c in changes if c[0] >= "2000-01"]
w3 = [c for c in changes if c[0] >= "2025-10"]
stats = {}
for name, w in (("w1", w1), ("w2", w2), ("w3", w3)):
    vals = [v for _, v in w]
    sd = statistics.stdev(vals)
    zeros = [m for m, v in w if v == 0.0]
    big_m, big = max(w, key=lambda it: abs(it[1]))
    stats[name] = sd
    print(f"{name}: first {w[0][0]} last {w[-1][0]} n={len(vals)} zeros={len(zeros)} {zeros}")
    print(f"  sd={sd!r} percent={100*sd!r} -> {half_up(100*sd)}")
    print(f"  largest by size: {big!r} at {big_m} -> percent {half_up(100*big)}; signed sign={'+' if big > 0 else '-'}")
    print(f"  mean={statistics.fmean(vals)!r}")
ratio = stats["w2"] / stats["w1"]
print(f"ratio w2/w1 unrounded={ratio!r} -> {half_up(ratio)}; rounded inputs 2.47/2.79={half_up(Decimal('2.47')/Decimal('2.79'),4)}")
diff = 100 * (stats["w1"] - stats["w2"])
print(f"difference w1-w2 percent unrounded={diff!r} -> {half_up(diff)}")
print(f"fall in the ratio from unrounded: 100*(1-ratio)={100*(1-ratio)!r} -> {half_up(100*(1-ratio))}; from rounded 0.89: {half_up(100*(1-Decimal('0.89')))}")
print("window one contains 1985-03:", any(m == "1985-03" for m, _ in w1), "window two contains 1985-03:", any(m == "1985-03" for m, _ in w2))
print("change at 1985-03:", dict(changes)["1985-03"], " change at 2008-10:", dict(changes)["2008-10"], " change at 2026-04:", dict(changes)["2026-04"])
print("first change month of window two uses rate of 1999-12:", dict(gbp)["1999-12"], dict(gbp)["2000-01"])
print("window three rate months 2025-09..2026-09 count:", sum(1 for m, _ in gbp if "2025-09" <= m <= "2026-09"))

# Lab 1 (rung 1) and Lab 2 (rung 2): exact arithmetic, nominal debt in cents
from fractions import Fraction as F
def real(debt, p): return F(debt) / p
falling = [F(p, 100) for p in (100, 97, 94, 91, 88, 85)]
rising = [F(p, 100) for p in (100, 103, 106, 109, 112, 115)]
def cents(x): return int(math.floor(x + F(1, 2)))
print("Lab1 falling real debt (cents):", [cents(real(10_000_000, p)) for p in falling])
print("Lab1 rising real debt (cents):", [cents(real(10_000_000, p)) for p in rising])
burden_f = 100 * (falling[0] / falling[-1] - 1)
burden_r = 100 * (rising[0] / rising[-1] - 1)
print("Lab1 burden falling:", float(burden_f), cents(burden_f * 100) / 100, " rising:", float(burden_r), cents(burden_r * 100) / 100)
diffc = real(10_000_000, falling[-1]) - real(10_000_000, rising[-1])
print("Lab1 difference period 5 (cents, unrounded):", float(diffc), "rounded dollars:", cents(diffc) / 100)
print("Lab1 period-5 falling real debt unrounded cents:", float(real(10_000_000, falling[-1])))
p2 = [F(p, 100) for p in (100, 99, 98, 96, 95, 93)]
print("Lab2 real debt (cents) by period:", [cents(real(4_000_000, p)) for p in p2])
b2 = 100 * (p2[0] / p2[-1] - 1)
print("Lab2 burden:", float(b2), cents(b2 * 100) / 100, " inverted ratio:", float(100 * (p2[-1] / p2[0] - 1)))
