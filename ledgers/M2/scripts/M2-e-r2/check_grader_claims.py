"""Re-derive grader claims: sin central ratio range over seeds 0-49 (both instances), instance validity, and
the forward-estimate ratio range for the cubic (page: must lie in 1.9..2.1)."""
import math
import sys

sys.path.insert(0, sys.argv[1])  # directory holding instance.py
from instance import make_instance  # noqa: E402

def central(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)

lo, hi = math.inf, -math.inf
flo, fhi = math.inf, -math.inf
bad = []
for seed in range(50):
    for inst in (make_instance(seed), make_instance(seed + 7_919)):
        x0 = inst["x0"]
        e1 = abs(central(math.sin, x0, 1e-2) - math.cos(x0))
        e2 = abs(central(math.sin, x0, 5e-3) - math.cos(x0))
        r = e1 / e2
        lo, hi = min(lo, r), max(hi, r)
        p0, p1, p2, p3 = inst["cubic"]
        cub = lambda x: p0 + x * (p1 + x * (p2 + x * p3))
        d = lambda x: p1 + x * (2 * p2 + 3 * p3 * x)
        def fe(h):
            return abs((cub(x0 + h) - cub(x0)) / h - d(x0))
        q = fe(1e-2) / fe(5e-3)
        flo, fhi = min(flo, q), max(fhi, q)
        if not (1.9 <= q <= 2.1):
            bad.append((seed, q))
        # validity: face range, coupon, maturity, yield, cubic conditioning, price clear of half cent
        assert 10_000 * 100 <= inst["face_cents"] <= 50_000_000, seed
        assert 1 <= inst["maturity_years"] <= 30 and 100 <= inst["yield_bps"] <= 1500, seed
        assert 0 <= inst["coupon_bps"] <= 1000, seed
        assert 0.25 <= x0 <= 1.75
        second = 2 * p2 + 6 * p3 * x0
        assert abs(second) >= 1.0 and abs(p3) >= 0.1, seed
print(f"sin central ratio (1e-2 / 5e-3) range over 100 instances: min {lo:.7f} max {hi:.7f}")
print(f"cubic forward ratio range: min {flo:.7f} max {fhi:.7f}; outside 1.9..2.1: {bad}")
