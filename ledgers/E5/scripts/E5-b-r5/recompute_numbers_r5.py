"""Independent re-derivation (E5 slice b, round 5) of every printed number in the L04-L06 prose.

Uses its own elimination (no closed forms as the source of truth), exact Fraction arithmetic,
and rounding to six places half-to-even only for display. Run with: .venv/bin/python -I <this file>
"""

from __future__ import annotations

import random
from fractions import Fraction as F


def solve2(a11: F, a12: F, a21: F, a22: F, r1: F, r2: F) -> tuple[F, F]:
    """Gaussian elimination for a 2x2 linear system, exact."""
    det = a11 * a22 - a12 * a21
    assert det != 0
    return (r1 * a22 - a12 * r2) / det, (a11 * r2 - r1 * a21) / det


def is_eq(c: F, b: F, d: F, h: F, g: F, mbar: F, tax: F = F(0), c0: F = F(1), b0: F = F(1)) -> tuple[F, F]:
    # IS: (1-c) Y + b i = c0 - c*tax + b0 + g ; LM: d Y - h i = mbar
    rhs_is = c0 - c * tax + b0 + g
    return solve2(1 - c, b, d, -h, rhs_is, mbar)


def r(x: F) -> str:
    scaled = round(x * 10**6)
    sign = "-" if scaled < 0 else ""
    whole, frac = divmod(abs(scaled), 10**6)
    return f"{sign}{whole}.{frac:06d}"


# ---- L04 ----
c, b, d, h = F(3, 4), F(2), F(1, 2), F(1)
y0, i0 = is_eq(c, b, d, h, F(1), F(2))
print("L04 Y*", y0, "i*", i0)  # expect 28/5, 4/5
y1, i1 = is_eq(c, b, d, h, F(11, 10), F(2))
y2, i2 = is_eq(c, b, d, h, F(2), F(2))
print("L04 dY(11/10)", y1 - y0, "mult", (y1 - y0) / F(1, 10), "di", i1 - i0)  # 2/25, 4/5, 1/25
print("L04 dY(2)", y2 - y0, "mult", (y2 - y0) / 1, "di", i2 - i0)  # 4/5, 4/5, 2/5
ym, im = is_eq(c, b, d, h, F(1), F(5, 2))
print("L04 monetary dY", ym - y0, "mult", (ym - y0) / F(1, 2), "di per unit", (im - i0) / F(1, 2))  # 4/5, 8/5, -1/5
y_b0, _ = is_eq(c, F(0), d, h, F(2), F(2))
y_b0_1, _ = is_eq(c, F(0), d, h, F(1), F(2))
print("L04 b=0 multiplier", (y_b0 - y_b0_1) / 1)  # 4
print("L04 share E3 h(1-c)/D", h * (1 - c) / (h * (1 - c) + b * d))  # 1/5
# M1 uses A = 4: c0 - c*tax + b0 + g = 4 with c0=1,b0=1 -> g=2
print("L04 M1 via g=2", is_eq(F(1, 2), F(2), F(1), F(2), F(2), F(3)))

# ---- L05 ----
def sr(a: F, eta: F, nu: F, ybar: F, pe: F) -> tuple[F, F]:
    y, p = solve2(F(1), eta, F(1), -nu, a, ybar - nu * pe)  # unknowns (Y, P): Y + eta P = a ; Y - nu P = ybar - nu pe
    return p, y

p0, y0_ = sr(F(1160), F(100), F(200), F(1000), F(1))
p1, y1_ = sr(F(1190), F(100), F(200), F(1000), F(1))
print("L05 P*", p0, "Y*", y0_, "dP", p1 - p0, "dY", y1_ - y0_)  # 6/5, 1040, 1/10, 20
for nu in (F(50), F(100), F(200), F(400), F(800)):
    pa, ya = sr(F(1160), F(100), nu, F(1000), F(1))
    pb, yb = sr(F(1190), F(100), nu, F(1000), F(1))
    print("L05 nu", nu, "share", r(nu / (F(100) + nu)), "dP", r(pb - pa), "dY", r(yb - ya))
lr0 = (F(1160) - F(1000)) / F(100)
lr1 = (F(1190) - F(1000)) / F(100)
print("L05 LR", r(lr0), r(lr1), "LR Y", F(1160) - F(100) * lr0, F(1190) - F(100) * lr1)
print("L05 R2 P*", sr(F(1190), F(100), F(200), F(1000), F(13, 10)))  # 3/2, 1040
print("L05 R3 gap", sr(F(1190), F(100), F(200), F(1000), F(1))[1] - F(1000))  # 60
print("L05 M1", sr(F(1100), F(100), F(100), F(1000), F(11, 10)))  # 21/20, 995
print("L05 M2 share", F(150) / (F(50) + F(150)), "dY", F(40) * F(150) / F(200), "dP", F(40) / F(200))
print("L05 M3", (F(1100) - F(1000)) / F(100), (F(1140) - F(1000)) / F(100))
print("L05 E2 increase 400->800", F(30) * (F(800) / F(900) - F(400) / F(500)))  # 8/3

# ---- L06 ----
YBAR, NU, KAPPA, UN = F(1000), F(200), F(200), F(5, 100)
P0, PI0 = F(6, 5), F(3, 100)
pe_a = P0 * (1 + PI0)
pa = pe_a - KAPPA * (F(6, 100) - UN) / NU
print("L06 A pe", pe_a, "P", pa, "pi", (pa - P0) / P0, "form", PI0 - (KAPPA / (NU * P0)) * (F(6, 100) - UN))
rng = random.Random(20261028)
price, pi = P0, PI0
for t in range(1, 13):
    draw = rng.randint(-100, 100)
    u = UN + F(draw, 10000)
    pe = price * (1 + pi)
    newp = pe - KAPPA * (u - UN) / NU
    newpi = (newp - price) / price
    ch = newpi - pi
    print(f"L06 t {t} draw {draw} infl {r(newpi)} change {r(ch)} sign_ok {(ch < 0) == (draw > 0)}")
    price, pi = newp, newpi
for step in (-4, -1, 0, 1, 4):
    u = UN + F(step, 200)
    print("L06 C step", step, "u%", r(u * 100), "change", r(-(F(200) / (NU * P0)) * (u - UN)))
print("L06 misc: 1/120", r(F(5, 6) * F(1, 100)), "1/60", r(F(5, 6) * F(2, 100)))
print("L06 R2 u", UN + F(1, 100) / (F(5, 6)))  # 0.062
print("L06 E3 change", r(-(F(5, 6)) * F(58, 10000)), "row 5.5", r(-(F(5, 6)) * F(5, 1000)))
