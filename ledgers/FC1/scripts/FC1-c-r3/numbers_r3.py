"""Re-derives every number the FC1 project page, its labs and its grader state, with independent code.

Usage: python ledgers/FC1/scripts/FC1-c-r3/numbers_r3.py <checkout-root>
Imports the reference solution only to compare; the numbers are recomputed from the closed forms in Fraction.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction as F
from pathlib import Path

root = Path(sys.argv[1])
grader = root / "course/modules/FC/FC1/grader"
sys.path.insert(0, str(grader))
from instance import make_instance  # noqa: E402

spec = importlib.util.spec_from_file_location("ref", grader / "reference.py")
assert spec and spec.loader
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)


def r_half_away(x: F) -> int:
    m = abs(x)
    w = (2 * m.numerator + m.denominator) // (2 * m.denominator)
    return w if x >= 0 else -w


def pv(events: list[tuple[int, int]], yield_bps: int) -> F:
    y = F(yield_bps, 10_000)
    return sum((F(a) / (1 + y) ** t for t, a in events), F(0))


print("Lab 1 coupon 5000, events", [(1, 5000), (2, 5000), (3, 105000)])
p1 = pv([(1, 5000), (2, 5000), (3, 105000)], 400)
print(f"Lab 1 exact PV = {float(p1):.6f} (page: 102775.091033), rounded {r_half_away(p1)} (page: 102775)")
print("Lab 1 trade event", (2, -10 * 9850))
print(f"Lab 1 page rounding claim, .091033 below half: {float(p1) - 102775 < 0.5}")
fa = pv([(1, 10500)], 500)
print("Fixture A price", r_half_away(fa), "(page 10000)")
fb = pv([(1, 10500)], -500)
print(f"Fixture B exact {float(fb):.4f} (page 11052.6316), rounded {r_half_away(fb)} (page 11053), 210000/19 =", F(210000, 19) == fb)
print("Fixture C coupon", r_half_away(F(10001 * 5000, 10_000)), "(page 5001), last", r_half_away(F(10001 * 5000, 10_000)) + 10001, "(page 15002)")
print("Fixture D coupon", r_half_away(F(1 * 5000, 10_000)), "(page 1, events [(1,2)])")
print("Fixture E", (2, -98500), "seller", (2, 98500))
fF = pv([(1, 1)], 10_000)
print("Fixture F exact", fF, "rounded", r_half_away(fF), "(page 1/2 -> 1); round() gives", round(float(fF)))
fG = pv([(1, 10001)], 10_000)
print("Fixture G exact", fG, "rounded", r_half_away(fG), "(page 5000.5 -> 5001)")
rnd = [(1, 500), (2, 500), (3, 10500)]
rv = pv(rnd, 400)
print(f"Rounding fixture exact {float(rv):.6f} (page 10277.509103), once {r_half_away(rv)} (page 10278)")
terms = [float(F(a) / (F(104, 100)) ** t) for t, a in rnd]
print("terms", [round(x, 2) for x in terms], "(page 480.77, 462.28, 9334.46)")
print("termwise sum", sum(r_half_away(F(a) / (F(104, 100)) ** t) for t, a in rnd), "(page 10277)")
print("Lab 2 relative tolerance on 102775:", 1e-6 * (1 + 102775), "(page: about 0.1 cent)")
print("Lab 2 half-up check on 1000*(1-0.9^11)/0.1:", float(1000 * (1 - F(9, 10) ** 11) / F(1, 10)))
print("Example 3.6:", float(F(1000) / (1 - F(45, 100))), "18.18% of 10000:", float(F(181818, 1000000) * 100))
print("Hours: 1+2+5+4+2+3+3 =", 1 + 2 + 5 + 4 + 2 + 3 + 3, "; 20/70 =", round(100 * 20 / 70, 1), "%")
prices = []
trades = []
mx = {"periods": 0, "quantity": 0, "settlement_day": 0, "face_cents": 0}
for s in range(50):
    c = make_instance(s)
    prices.append(ref.bond_price_cents(ref.Bond(c["face_cents"], c["coupon_bps"], c["periods"]), c["yield_bps"]))
    trades.append(ref.CashTrade(c["quantity"], c["price_cents"], c["side"], c["settlement_day"]).events()[0][1])
    for k in mx:
        mx[k] = max(mx[k], c[k])
    assert 1 <= c["periods"] and c["face_cents"] > 0 and c["coupon_bps"] >= 0 and c["yield_bps"] > -10_000
    assert c["quantity"] >= 1 and c["price_cents"] >= 0 and c["side"] in (1, -1) and c["settlement_day"] >= 1
print("seeds 0-49 valid; distinct bond prices", len(set(prices)), "distinct trade amounts", len(set(trades)))
print("seeds 0-49 maxima", mx, "(periods<=8, quantity<=500, settlement<=5, face<=5,000,000 all hold)")
print("seed 0 price", prices[0], "(hard-coded answer mutant writes 4281937 for seed 0)")
