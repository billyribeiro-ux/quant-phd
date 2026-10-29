"""Numerical check of L09 Proposition 2.2 on three finitely valued standardized laws (verifier, round 1).

|phi_Y(s) - (1 - s^2/2)| <= |s|^3 E|Y|^3 / 3 for |s| <= 1/M, M = max|Y|.
"""
import cmath
import math

def check(values, probs, label):
    mean = sum(v * p for v, p in zip(values, probs))
    var = sum((v - mean) ** 2 * p for v, p in zip(values, probs))
    ys = [(v - mean) / math.sqrt(var) for v in values]
    M = max(abs(y) for y in ys)
    m3 = sum(abs(y) ** 3 * p for y, p in zip(ys, probs))
    worst = 0.0
    worst_ratio = 0.0
    for k in range(-2000, 2001):
        s = k / 2000 / M  # covers |s| <= 1/M
        phi = sum(cmath.exp(1j * s * y) * p for y, p in zip(ys, probs))
        lhs = abs(phi - (1 - s * s / 2))
        rhs = abs(s) ** 3 * m3 / 3
        if rhs > 0:
            worst_ratio = max(worst_ratio, lhs / rhs)
        worst = max(worst, lhs - rhs)
    print(f"{label}: M={M:.4f} E|Y|^3={m3:.4f} max(lhs-rhs)={worst:.3e} (must be <= 0) max(lhs/rhs)={worst_ratio:.4f}")
    return worst <= 1e-12

ok = True
ok &= check(list(range(1, 7)), [1 / 6] * 6, "fair die")
ok &= check([0.0, 2.0], [0.5, 0.5], "two-point {0,2}")
ok &= check([-1.0, 1.0, 4.0], [0.5, 0.25, 0.25], "three-point")
print("Prop 2.2 bound holds on all three grids:", ok)
