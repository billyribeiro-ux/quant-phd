"""Seeds 0-19 of grader/instance.py: validity under the page's rules and distinctness of answers (read-only)."""
import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1] + "/course/modules/FC/FC1/grader")
from instance import make_instance  # noqa: E402

def half_away(x):
    m = abs(x)
    w = (2 * m.numerator + m.denominator) // (2 * m.denominator)
    return w if x >= 0 else -w

prices, flows = [], []
for s in range(20):
    c = make_instance(s)
    assert c["periods"] >= 1 and c["face_cents"] > 0 and c["coupon_bps"] >= 0, s
    assert c["yield_bps"] > -10000 and c["quantity"] >= 1 and c["price_cents"] >= 0, s
    assert c["side"] in (1, -1) and c["settlement_day"] >= 1, s
    y = Fraction(c["yield_bps"], 10000)
    coupon = half_away(Fraction(c["face_cents"] * c["coupon_bps"], 10000))
    ev = [(t, coupon) for t in range(1, c["periods"] + 1)]
    ev[-1] = (c["periods"], ev[-1][1] + c["face_cents"])
    prices.append(half_away(sum((Fraction(a) / (1 + y) ** t for t, a in ev), Fraction(0))))
    flows.append(-c["side"] * c["quantity"] * c["price_cents"])
    print(s, "periods", c["periods"], "face", c["face_cents"], "coupon_bps", c["coupon_bps"], "yield_bps", c["yield_bps"],
          "qty", c["quantity"], "px", c["price_cents"], "side", c["side"], "day", c["settlement_day"], "price", prices[-1], "flow", flows[-1])
print("all 20 valid: yes; distinct prices:", len(set(prices)), "/20; distinct trade flows:", len(set(flows)), "/20")
