"""Round-10 re-derivation of every number in project.html prose, the Lab 1-3 expected values, the grader docstrings
and the instance ranges (verifier, FC1 slice c). Exact Fractions only, plus the float forms the docstrings quote.

Usage: python -I ledgers/FC1/scripts/FC1-c-r10/numbers_r10.py
"""

from __future__ import annotations

import math
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "course" / "modules" / "FC" / "FC1" / "grader"))
import instance  # noqa: E402


def half_away(x: F) -> int:
    m = abs(x)
    r = math.floor(m + F(1, 2))
    return r if x >= 0 else -r


def events(face: int, bps: int, n: int) -> list[tuple[int, int]]:
    c = half_away(F(face * bps, 10_000))
    rows = [(t, c) for t in range(1, n + 1)]
    rows[-1] = (n, rows[-1][1] + face)
    return rows


def price(ev: list[tuple[int, int]], yb: int) -> F:
    y = F(yb, 10_000)
    return sum((F(a) / (1 + y) ** t for t, a in ev), F(0))


out: list[str] = []
say = out.append

pv1 = price(events(100_000, 500, 3), 400)
say(f"Lab1 events {events(100_000, 500, 3)}; exact PV float {float(pv1)!r}; '%.6f' {float(pv1):.6f}; price {half_away(pv1)}")
say(f"A events {events(10000, 500, 1)} price@500 {half_away(price(events(10000, 500, 1), 500))}")
bexact = F(10500) / F(95, 100)
say(f"B exact 10500/0.95 = {bexact} = {float(bexact):.4f}; price@-500 {half_away(price(events(10000, 500, 1), -500))}")
say(f"C events {events(10001, 5000, 2)}")
say(f"D events {events(1, 5000, 1)}")
pf = price(events(1, 0, 1), 10000)
say(f"F events {events(1, 0, 1)} exact {pf} price {half_away(pf)}; Python round(float) {round(float(pf))}")
pg = price(events(10001, 0, 1), 10000)
say(f"G events {events(10001, 0, 1)} exact {pg} price {half_away(pg)}")
rnd = events(10000, 500, 3)
exact_rnd = price(rnd, 400)
term = sum(half_away(F(a) / (1 + F(400, 10_000)) ** t) for t, a in rnd)
say(f"rounding events {rnd}; exact {float(exact_rnd):.6f}; once {half_away(exact_rnd)}; term-by-term {term}")
say(f"E trade {-1 * 10 * 9850}")
c496 = F(1704285 * 179, 10000)
ev496 = half_away(c496) + 1704285
say(f"496bps coupon {c496} = {float(c496)}; event {ev496}")
pv496 = F(1734792) / F(10496, 10000)
say(f"496bps exact PV {pv496} == 3305625/2: {pv496 == F(3305625, 2)}; rounds {half_away(pv496)}; float 1734792/1.0496 = {1734792 / 1.0496!r}; round() {round(1734792 / 1.0496)}")
pv13 = F(13) / (1 + F(4, 100))
say(f"Bond(13,0,1) at 400: exact {pv13} rounds {half_away(pv13)}; float (1+0.04)**-1*13 = {(1 + 0.04) ** -1 * 13!r}; round() {round((1 + 0.04) ** -1 * 13)}")
hair = F(300_075_005) / F(10001, 10000) ** 3
claim = F(299_985_000) + F(1, 2) - F(1, 2 * 1000300030001)
say(f"hair exact {float(hair)!r}; identity holds {hair == claim}; rounds {half_away(hair)}")
say(f"10**10+1 -> {half_away(price(events(10**10 + 1, 0, 1), 10000))}; 10**12+1 -> {half_away(price(events(10**12 + 1, 0, 1), 10000))}")
getcontext().prec = 10
say(f"Decimal prec 10 of 5000000000.5 -> {+Decimal('5000000000.5')}")
f40 = half_away(price(events(10**40 + 1, 0, 1), 10000))
say(f"10**40+1 -> {f40}; equals 5*10**39+1: {f40 == 5 * 10**39 + 1}; digits of 10**40+1: {len(str(10**40 + 1))}")
c17 = F((10**17 + 4999) * 1, 10000)
say(f"10**17+4999 at 1 bps: coupon {c17} rounds {half_away(c17)} == 10**13 + ... : {half_away(c17) == 10**13}; face of 10**17 + 4999 + 10**13 event")
say(f"yield checks: 150% {half_away(price(events(10000, 500, 1), 15000))} (10500/2.5); 300% {half_away(price(events(10000, 500, 1), 30000))} (10500/4); "
    f"2000% {half_away(price(events(10000, 500, 1), 200000))} (10500/21); 10000% exact {F(10500, 101)} = {float(F(10500, 101)):.4f} rounds {half_away(price(events(10000, 500, 1), 1_000_000))}")
say(f"2**40+1 times 9851 = {(2**40 + 1) * 9851}; 2**53 = {2**53}; above: {(2**40 + 1) * 9851 > 2**53}")
say(f"events of Bond(1000000,0,3): {events(1_000_000, 0, 3)}")
say(f"Bond(10000,500,1) price at 10**7 bps exact {F(10500, 1001)} = {float(F(10500, 1001)):.4f} rounds {half_away(price(events(10000, 500, 1), 10_000_000))}")
inst = [instance.make_instance(s) for s in range(50)]
distinct = len({tuple(sorted((k, v) for k, v in i.items() if k not in ("seed", "label"))) for i in inst})
say(f"instances distinct {distinct} of 50")
for k in ("periods", "yield_bps", "settlement_day", "quantity", "coupon_bps", "price_cents"):
    vals = [i[k] for i in inst]
    say(f"{k}: min {min(vals)} max {max(vals)}")
say(f"face_cents: min {min(i['face_cents'] for i in inst)} max {max(i['face_cents'] for i in inst)}")
say(f"side values {sorted({i['side'] for i in inst})}")
print("\n".join(out))
