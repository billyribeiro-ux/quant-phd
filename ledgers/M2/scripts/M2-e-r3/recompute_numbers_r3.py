"""Round-3 independent recomputation of the numbers printed or claimed in project.html and the grader."""

import math
import sys
from fractions import Fraction
from decimal import Decimal, getcontext

ROOT = sys.argv[1]
sys.path.insert(0, ROOT + "/course/modules/M/M2/grader")
from instance import make_instance  # noqa: E402

getcontext().prec = 60

# --- Lab 1: face 1000000, coupon 5 %, 10 years, yield 4 %
def bond_terms(face, cpn_pct, years, y):
    coupon = Fraction(face) * Fraction(cpn_pct) / 100
    flows = [(t, coupon + (face if t == years else 0)) for t in range(1, years + 1)]
    v = 1 / (1 + Fraction(y))
    P = sum(c * v**t for t, c in flows)
    P1 = -sum(t * c * v ** (t + 1) for t, c in flows)
    P2 = sum(t * (t + 1) * c * v ** (t + 2) for t, c in flows)
    return P, P1, P2

P, P1, P2 = bond_terms(1_000_000, 5, 10, Fraction(4, 100))
print("L1 P =", float(P), "round =", round(P), "P1 =", float(P1), "P2 =", float(P2))
print("L1 duration -P1/P =", float(-P1 / P))
print("L1 rel central error (1.56e-2 over 8514667.40) =", 1.56e-2 / 8514667.40)
print("L1 rel second diff error (8.36 over 83766485.12) =", 8.36 / 83766485.12)

# --- Lab 3: face 2500000, coupon 6 %, 12 years, yield 5 %
P3, D3, _ = bond_terms(2_500_000, 6, 12, Fraction(5, 100))
print("L3 P =", float(P3), "round =", round(P3), "dP/dy =", float(D3))
def fwd(h, f, x):
    return (f(x + h) - f(x)) / h
def cen(h, f, x):
    return (f(x + h) - f(x - h)) / (2 * h)
Pf = lambda y: float(sum(c * (1 / (1 + y)) ** t for t, c in [(t, Fraction(2_500_000) * Fraction(6, 100) + (2_500_000 if t == 12 else 0)) for t in range(1, 13)]))
y0 = 0.05
ex = float(D3)
for k in range(1, 13):
    h = 10.0 ** -k
    fe = abs(fwd(h, Pf, y0) - ex)
    ce = abs(cen(h, Pf, y0) - ex)
    print(f"L3 h=1e-{k:02d} fwd={fe:.6e} cen={ce:.6e} cen<fwd={ce < fe}")
print("L3 observed order fwd =", math.log10(abs(fwd(1e-2, Pf, y0) - ex) / abs(fwd(1e-3, Pf, y0) - ex)))
print("L3 observed order cen =", math.log10(abs(cen(1e-2, Pf, y0) - ex) / abs(cen(1e-3, Pf, y0) - ex)))

# --- Grader claim: central ratio for sin over the 100 instances (seeds 0..49, both draws)
ratios = []
for seed in range(50):
    for s in (seed, seed + 7_919):
        inst = make_instance(s)
        x0 = inst["x0"]
        exact = math.cos(x0)
        def err(h):
            return abs((math.sin(x0 + h) - math.sin(x0 - h)) / (2 * h) - exact)
        ratios.append(err(1e-2) / err(5e-3))
print("grader sin central ratio: min %.10f max %.10f n=%d" % (min(ratios), max(ratios), len(ratios)))
print("rounded to 7 dp: min %.7f max %.7f" % (round(min(ratios), 7), round(max(ratios), 7)))
