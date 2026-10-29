"""Verifier r8: high-precision check of L10 part D tail products and the float formula used in the lab twin.
Uses only the standard library (decimal). Run: python -I ledgers/M4/scripts/M4-d-r8/l10_precision_r8.py
"""
import math
from decimal import Decimal as D, getcontext

getcontext().prec = 80
PI = D("3.14159265358979323846264338327950288419716939937510582097494459230781640628620899")

def atan_series(z):
    # arctan for 0 < z <= 1 by argument halving to speed convergence, then Taylor series
    k = 0
    while z > D("0.01"):
        z = z / (1 + (1 + z * z).sqrt())  # arctan(z) = 2 arctan(z / (1 + sqrt(1+z^2)))
        k += 1
    s, term, n = D(0), z, 0
    while True:
        t = term / (2 * n + 1)
        if abs(t) < D(10) ** -75:
            break
        s += t if n % 2 == 0 else -t
        term = term * z * z
        n += 1
    return s * (2 ** k)

def atan_big(u):  # arctan of positive Decimal u
    if u <= 1:
        return atan_series(u)
    return PI / 2 - atan_series(1 / u)

def tail_exact(x):  # P(V > x), x > 0 exact to ~70 digits; V = t(3)
    x = D(x)
    y = x / D(3).sqrt()
    return (atan_big(1 / y) - y / (1 + y * y)) / PI

def tail_float(x):  # the lab twin formula, float
    y = x / math.sqrt(3.0)
    return (math.atan(1.0 / y) - y / (1.0 + y * y)) / math.pi

for x in (10.0, 100.0, 1000.0):
    ex = tail_exact(x)
    fl = tail_float(x)
    prod_exact = D(x) ** 3 * 2 * ex
    prod_float = x**3 * 2.0 * fl
    rel = abs((D(fl) - ex) / ex)
    print(f"x={x:.0f} exact P(V>x)={ex:.25E} float={fl!r} relerr={float(rel):.3e}")
    print(f"  x^3 P(|V|>x) exact={prod_exact:.12f} float={prod_float:.12f} printed6={prod_float:.6f} exact6={float(prod_exact):.6f}")
