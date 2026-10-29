"""Recompute L08 E1 thresholds, L09 bounds and ratios, and L10 Example 3.3 closed forms (exact where possible).

Usage: .venv/bin/python -I ledgers/M5/scripts/M5-c-r6/l09_l10_numeric.py
"""
import math
from fractions import Fraction

# L08 E1: a priori thresholds n >= ln(tau(1-b)/d)/ln b, d = sqrt(3)/2, tau = 1e-12
d = math.sqrt(3) / 2
tau = 1e-12
for b in (0.5, 0.9, 0.95):
    thr = math.log(tau * (1 - b) / d) / math.log(b)
    print(f"L08-E1 beta={b} threshold={thr:.2f} least_n={math.ceil(thr)}")

# L09 R2: a priori bound (beta^n/(1-beta)) * d with d = sqrt(3)/2, beta = 0.9
for n in (147, 151, 152):
    print(f"L09-R2 n={n} bound={0.9**n / 0.1 * d:.6e}")
print(f"L09-R2 least n with bound <= 1e-6: {min(n for n in range(1, 1000) if 0.9**n / 0.1 * d <= 1e-6)}")

# L09 E2: printed ratio and factor
print(f"L09-E2 ratio={0.0000085808 / 0.0000009534:.4f} factor={0.9 / (1 - 0.9):.4f}")
# L09 M1 / E1 / quiz
print(f"L09-quiz a priori 0.9^10/0.1={0.9**10 / 0.1:.7f}")

# L10 Example 3.3 closed forms, exact
for n in (4, 10, 100, 1000):
    pts = [Fraction(i, n) for i in range(n + 1)]
    g = lambda x: x * x
    right = sum(pts[i] * (g(pts[i]) - g(pts[i - 1])) for i in range(1, n + 1))
    left = sum(pts[i - 1] * (g(pts[i]) - g(pts[i - 1])) for i in range(1, n + 1))
    assert right == Fraction((n + 1) * (4 * n - 1), 6 * n * n), n
    assert left == Fraction(4 * n * n - 3 * n - 1, 6 * n * n), n
    assert right - Fraction(2, 3) == Fraction(3 * n - 1, 6 * n * n)
    assert left - Fraction(2, 3) == -Fraction(3 * n + 1, 6 * n * n)
    print(f"L10-3.3 n={n} right={float(right):.12f} left={float(left):.12f} closed_forms_exact=True")
print(f"L10-E1 gap of errors (abs) = {float(Fraction(31, 600) - Fraction(29, 600))!r}")
print(f"L10-E3 n=1000 average={(float(Fraction(1001, 2000)) + float(Fraction(999, 2000))) / 2}")
print(f"L10-quiz (1001)(3999)/(6e6)={1001 * 3999 / 6e6:.7f}")
