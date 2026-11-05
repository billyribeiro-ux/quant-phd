"""Check instance validity for seeds 0-49 and that answers differ across seeds (grader/instance.py contract)."""
import sys
sys.path.insert(0, sys.argv[1])
from fractions import Fraction
from instance import make_instance, _exact_price_cents, _cubic_is_well_conditioned
rows = []
ok = True
for seed in range(50):
    for s in (seed, seed + 7_919):
        i = make_instance(s)
        fv = 1_000_000 <= i["face_cents"] <= 50_000_000
        cv = 0 <= i["coupon_bps"] <= 1000
        mv = 1 <= i["maturity_years"] <= 30
        yv = 100 <= i["yield_bps"] <= 1500
        price = _exact_price_cents(i["face_cents"], i["coupon_bps"], i["maturity_years"], i["yield_bps"])
        frac = price - (price.numerator // price.denominator)
        clear = abs(frac - Fraction(1, 2)) > Fraction(1, 1_000_000)
        wc = _cubic_is_well_conditioned(i["cubic"], i["x0"])
        valid = fv and cv and mv and yv and clear and wc
        ok = ok and valid
        rows.append((s, float(price), i["yield_bps"], i["maturity_years"], i["x0"]))
print("instances checked", len(rows), "all valid:", ok)
prices = {round(r[1], 4) for r in rows}
yields = {r[2] for r in rows}
x0s = {r[4] for r in rows}
print("distinct prices", len(prices), "distinct yields", len(yields), "distinct x0", len(x0s))
