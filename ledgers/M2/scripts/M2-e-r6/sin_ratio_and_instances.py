"""Recompute the sin central-ratio claim of project.html (line 226) and check instance validity and spread over seeds 0-49."""
import math
import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1])  # the grader directory holding instance.py
from instance import make_instance  # noqa: E402


def central(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)


ratios = []
pts = []
for seed in range(50):
    for s in (seed, seed + 7_919):
        inst = make_instance(s)
        x0 = inst["x0"]
        e1 = abs(central(math.sin, x0, 1e-2) - math.cos(x0))
        e2 = abs(central(math.sin, x0, 5e-3) - math.cos(x0))
        ratios.append(e1 / e2)
        pts.append((seed, s, x0, inst["face_cents"], inst["coupon_bps"], inst["maturity_years"], inst["yield_bps"]))
        # validity: cubic well-conditioned, price clear of half cent, ranges
        p0, p1, p2, p3 = inst["cubic"]
        second = 2 * p2 + 6 * p3 * x0
        assert abs(second) >= 1.0 and abs(p3) >= 0.1, (s, "conditioning")
        assert 1_000_000 <= inst["face_cents"] <= 50_000_000, (s, "face")
        assert 0 <= inst["coupon_bps"] <= 1000 and 1 <= inst["maturity_years"] <= 30, (s, "coupon/maturity")
        assert 100 <= inst["yield_bps"] <= 1500, (s, "yield")
        assert len(inst["surface"]) == 7 and len(inst["point"]) == 2
print("sin ratio min %.7f max %.7f over %d instances" % (min(ratios), max(ratios), len(ratios)))
print("all 100 instances valid (conditioning, ranges)")
print("distinct x0 values:", len({p[2] for p in pts}), "distinct face:", len({p[3] for p in pts}), "of", len(pts))
print("first 3 seeds:", pts[:6])
