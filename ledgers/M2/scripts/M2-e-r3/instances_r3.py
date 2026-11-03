"""Round-3: validity and distinctness of the grader instances for seeds 0-49 (both draws), and the docstring ranges."""

import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1] + "/course/modules/M/M2/grader")
from instance import make_instance  # noqa: E402

insts = []
for s in range(50):
    insts += [make_instance(s), make_instance(s + 7_919)]
valid = all(i["maturity_years"] >= 1 and i["yield_bps"] > -10_000 and i["face_cents"] > 0 for i in insts)
ranges = (
    min(i["face_cents"] for i in insts), max(i["face_cents"] for i in insts),
    min(i["coupon_bps"] for i in insts), max(i["coupon_bps"] for i in insts),
    min(i["maturity_years"] for i in insts), max(i["maturity_years"] for i in insts),
    min(i["yield_bps"] for i in insts), max(i["yield_bps"] for i in insts),
    min(i["x0"] for i in insts), max(i["x0"] for i in insts),
)
print("instances", len(insts), "all valid", valid)
print("face cents", ranges[0], ranges[1], "coupon bps", ranges[2], ranges[3], "maturity", ranges[4], ranges[5], "yield bps", ranges[6], ranges[7], "x0", ranges[8], ranges[9])
prices = {round(float(sum(Fraction(i["face_cents"]) * 0 for _ in [0]) )) for i in insts}
prices = set()
cubics = set()
for i in insts:
    p = sum(Fraction(i["face_cents"] * i["coupon_bps"], 10_000) * (1 / (1 + Fraction(i["yield_bps"], 10_000))) ** t for t in range(1, i["maturity_years"] + 1))
    prices.add(float(p))
    cubics.add(tuple(i["cubic"]))
print("distinct unrounded prices", len(prices), "of", len(insts), "| distinct cubic coefficient sets", len(cubics))
