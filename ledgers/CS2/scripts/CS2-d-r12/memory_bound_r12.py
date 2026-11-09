"""Recompute the Corollary 2.6 sums and closed forms quoted by L11 and card CS2-c151 / CS2-c235 (python -I)."""
from fractions import Fraction as F
import math

def exact_sum(n, eps):
    L = math.floor(math.log2(n))
    total = 0
    for h in range(L + 1):
        k = 2 * math.ceil(F(h + 1) * (h + 2) / (2 * eps))
        total += k - 1
    return L, total

def closed(n, eps):
    L = math.floor(math.log2(n))
    return F((L + 1) * (L + 2) * (L + 3), 3) / eps + (L + 1)

eps = F(1, 20)
L, s = exact_sum(5000, eps)
print("n=5000 eps=1/20: L", L, "exact sum", s, "closed form", float(closed(5000, eps)), "exceeds n:", s > 5000)
L, s = exact_sum(10**9, eps)
print("n=1e9 eps=1/20: L", L, "exact sum", s, "closed form", float(closed(10**9, eps)))
print("M3 check eps=1/10: k0 =", 2 * math.ceil(F(1 * 2) / (2 * F(1, 10))), "k1 =", 2 * math.ceil(F(2 * 3) / (2 * F(1, 10))))
