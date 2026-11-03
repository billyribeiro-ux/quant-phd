"""Round 2 verifier re-derivation (E5-b): every number in L04-L06 prose and quiz, recomputed in exact Fractions.

Independent of the lab twins: formulas are written from the page's own definitions, solved by substitution checks.
Run: .venv/bin/python -I ledgers/E5/scripts/E5-b-r2/d2_rederive.py
"""

from __future__ import annotations

import random
from fractions import Fraction as F

FAILS: list[str] = []


def _show(x: object) -> str:
    """Short printable form: exact text when small, a float approximation otherwise."""
    if isinstance(x, bool) or isinstance(x, str):
        return str(x)
    if isinstance(x, F):
        if x.denominator < 10**12 and abs(x.numerator) < 10**15:
            return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)
        return f"~{float(x):.12g}"
    return str(x)


def check(label: str, got: object, want: object) -> None:
    ok = got == want
    print(f"{'OK  ' if ok else 'FAIL'} {label}: got {_show(got)} want {_show(want)}")
    if not ok:
        FAILS.append(label)


def dec(x: F, places: int = 6) -> str:
    """Round half to even at the given places, as the labs print."""
    scaled = round(x * 10**places)
    sign = "-" if scaled < 0 else ""
    whole, frac = divmod(abs(scaled), 10**places)
    return f"{sign}{whole}.{frac:0{places}d}"


# ---------------- L04: IS-LM ----------------
def is_lm(c: F, c0: F, b0: F, b: F, d: F, h: F, tax: F, g: F, m: F) -> tuple[F, F]:
    """Solve (1-c)Y + b i = A and d Y - h i = m by Cramer's rule with A = c0 - c tax + b0 + g."""
    a = c0 - c * tax + b0 + g
    det = (1 - c) * (-h) - b * d  # determinant of [[1-c, b], [d, -h]]
    y = (a * (-h) - b * m) / det
    i = ((1 - c) * m - d * a) / det
    # substitution check of both relations
    assert (1 - c) * y + b * i == a
    assert d * y - h * i == m
    return y, i


c, c0, b0, b, d, h, tax, g, m = F(3, 4), F(1), F(1), F(2), F(1, 2), F(1), F(0), F(1), F(2)
y0, i0 = is_lm(c, c0, b0, b, d, h, tax, g, m)
D = h * (1 - c) + b * d
check("L04 Part A Y*", y0, F(28, 5))
check("L04 Part A i*", i0, F(4, 5))
check("L04 D", D, F(5, 4))
check("L04 Y* decimal", dec(y0), "5.600000")
y1, i1 = is_lm(c, c0, b0, b, d, h, tax, F(11, 10), m)
check("L04 B dY (G 1->11/10)", y1 - y0, F(2, 25))
check("L04 B di (G 1->11/10)", i1 - i0, F(1, 25))
check("L04 B multiplier (11/10)", (y1 - y0) / (F(11, 10) - g), F(4, 5))
y2, i2 = is_lm(c, c0, b0, b, d, h, tax, F(2), m)
check("L04 B dY (G 1->2)", y2 - y0, F(4, 5))
check("L04 B di (G 1->2)", i2 - i0, F(2, 5))
check("L04 benchmark 1/(1-c)", 1 / (1 - c), F(4))
check("L04 h/D", h / D, F(4, 5))
y3, i3 = is_lm(c, c0, b0, b, d, h, tax, g, F(5, 2))
check("L04 C dY (m 2->5/2)", y3 - y0, F(4, 5))
check("L04 C multiplier", (y3 - y0) / (F(5, 2) - m), F(8, 5))
check("L04 C di per unit", (i3 - i0) / (F(5, 2) - m), F(-1, 5))
check("L04 b/D", b / D, F(8, 5))
check("L04 -(1-c)/D", -(1 - c) / D, F(-1, 5))
y4a, _ = is_lm(c, c0, b0, F(0), d, h, tax, g, m)
y4b, _ = is_lm(c, c0, b0, F(0), d, h, tax, F(2), m)
check("L04 D b=0 multiplier", (y4b - y4a) / 1, F(4))
check("L04 share h(1-c)/D (E3)", h * (1 - c) / D, F(1, 5))
check("L04 E3 0.8/4", F(4, 5) / 4, F(1, 5))
# M1: c=1/2, b=2, d=1, h=2, A=4, mbar=3 (solve directly from the closed form and check relations)
c1, b1, d1, h1, A1, m1 = F(1, 2), F(2), F(1), F(2), F(4), F(3)
D1 = h1 * (1 - c1) + b1 * d1
Y1 = (h1 * A1 + b1 * m1) / D1
I1 = (d1 * A1 - (1 - c1) * m1) / D1
check("L04 M1 D", D1, F(3))
check("L04 M1 Y*", Y1, F(14, 3))
check("L04 M1 i*", I1, F(5, 6))
check("L04 M1 IS check", (1 - c1) * Y1 + b1 * I1, A1)
check("L04 M1 LM check", d1 * Y1 - h1 * I1, m1)
check("L04 M2 h/D", h1 / D1, F(2, 3))
check("L04 M2 benchmark", 1 / (1 - c1), F(2))
check("L04 M2 ratio", (h1 / D1) / (1 / (1 - c1)), F(1, 3))
check("L04 M3 b/D", b1 / D1, F(2, 3))
check("L04 M3 -(1-c)/D", -(1 - c1) / D1, F(-1, 6))
check("L04 E1 ratio di/dY", (F(1, 25)) / (F(2, 25)), F(1, 2))
check("L04 E1 closed d/h", d / h, F(1, 2))
check("L04 R1 h/(h(1-c))", h / (h * (1 - c)), 1 / (1 - c))
check("L04 Q3 Y*", (1 * 3 + 2 * 2) / F(5, 4), F(28, 5))

# ---------------- L05: AD-AS ----------------
ybar, eta, nu, pe = F(1000), F(100), F(200), F(1)


def short_run(a: F, eta_: F, nu_: F, pe_: F) -> tuple[F, F]:
    p = (a - ybar + nu_ * pe_) / (eta_ + nu_)
    y = a - eta_ * p
    assert y == ybar + nu_ * (p - pe_)  # A2 at the solution
    return p, y


p0, y0a = short_run(F(1160), eta, nu, pe)
check("L05 A P*", p0, F(6, 5))
check("L05 A Y*", y0a, F(1040))
p1, y1a = short_run(F(1190), eta, nu, pe)
check("L05 B dP", p1 - p0, F(1, 10))
check("L05 B dY", y1a - y0a, F(20))
check("L05 B share", nu / (eta + nu), F(2, 3))
check("L05 B price per unit a", 1 / (eta + nu), F(1, 300))
check("L05 misc post-shift Y at P^e=1", F(1190) - eta * short_run(F(1190), eta, nu, F(1))[0], F(1060))
check("L05 misc demand at P=1", F(1160) - eta * 1, F(1060))
check("L05 misc demand at P=1.6", F(1160) - eta * F(16, 10), F(1000))
check("L05 R2 P* with Pe=1.3", (F(190) + nu * F(13, 10)) / (eta + nu), F(3, 2))
check("L05 R2 Y*", F(1190) - eta * F(3, 2), F(1040))
check("L05 R3 output gap", F(1060) - ybar, F(60))
check("L05 C LR price before", (F(1160) - ybar) / eta, F(8, 5))
check("L05 C LR price after", (F(1190) - ybar) / eta, F(19, 10))
check("L05 C LR change", (F(1190) - ybar) / eta - (F(1160) - ybar) / eta, F(3, 10))
for slope, share, pc, oc in [
    (F(50), F(1, 3), F(1, 5), F(10)),
    (F(100), F(1, 2), F(3, 20), F(15)),
    (F(200), F(2, 3), F(1, 10), F(20)),
    (F(400), F(4, 5), F(3, 50), F(24)),
    (F(800), F(8, 9), F(1, 30), F(80, 3)),
]:
    check(f"L05 D nu={slope} share", slope / (eta + slope), share)
    check(f"L05 D nu={slope} price change", F(30) / (eta + slope), pc)
    check(f"L05 D nu={slope} output change", F(30) * slope / (eta + slope), oc)
check("L05 E2 increase 400->800", F(80, 3) - F(24), F(8, 3))
check("L05 E2 increase 50->100", F(15) - F(10), F(5))
check("L05 E2 increase 100->200", F(20) - F(15), F(5))
check("L05 E2 increase 200->400", F(24) - F(20), F(4))
check("L05 M1 P*", (F(1100) - ybar + F(100) * F(11, 10)) / (F(100) + F(100)), F(21, 20))
check("L05 M1 Y*", F(1100) - F(100) * F(21, 20), F(995))
check("L05 M1 supply", ybar + F(100) * (F(21, 20) - F(11, 10)), F(995))
check("L05 M2 share", F(150) / F(200), F(3, 4))
check("L05 M2 dY", F(3, 4) * 40, F(30))
check("L05 M2 dP", F(40) / F(200), F(1, 5))
check("L05 M3 before", (F(1100) - ybar) / F(100), F(1))
check("L05 M3 after", (F(1140) - ybar) / F(100), F(7, 5))
check("L05 P2 1-share", 1 - F(150) / F(200), F(1, 4))
check("L05 E1 share nu=400", F(400) / F(500), F(4, 5))
check("L05 E1 dY nu=400", F(4, 5) * 30, F(24))
check("L05 E1 dP nu=400", F(30) / F(500), F(3, 50))
check("L05 P3 P* with Pe=(a-Ybar)/eta", (F(160) + nu * F(8, 5)) / (eta + nu), F(8, 5))
check("L05 Remark2.3 identity nu/(eta+nu) = 1/(1+eta/nu) at nu=200", nu / (eta + nu), 1 / (1 + eta / nu))

# ---------------- L06: Phillips ----------------
kappa, nu6, un, P0, pi0 = F(200), F(200), F(5, 100), F(6, 5), F(3, 100)
beta0 = kappa / (nu6 * P0)
check("L06 beta at P=6/5", beta0, F(5, 6))
check("L06 beta at P=1", kappa / (nu6 * 1), F(1))
check("L06 R1 ratio", (kappa / nu6) / beta0, F(6, 5))
pe_a = P0 * (1 + pi0)
pa = pe_a - kappa * (F(6, 100) - un) / nu6
pi_levels = (pa - P0) / P0
pi_form = pi0 - beta0 * (F(6, 100) - un)
check("L06 A levels", pi_levels, F(13, 600))
check("L06 A Phillips", pi_form, F(13, 600))
check("L06 A decimal", dec(pi_levels), "0.021667")
check("L06 Q6 pi_t", F(3, 100) - F(5, 6) * F(1, 100), F(13, 600))
check("L06 Q6 decimal", dec(F(3, 100) - F(5, 6) * F(1, 100)), "0.021667")
check("L06 misc1 change at gap -0.01", -beta0 * F(-1, 100), F(1, 120))
check("L06 misc2 change at 3%", -beta0 * (F(3, 100) - un), F(1, 60))
check("L06 E1 change at 4%", -beta0 * (F(4, 100) - un), F(1, 120))
check("L06 M1 beta", F(100) / (F(200) * 1), F(1, 2))
check("L06 M1 pi", F(4, 100) - F(1, 2) * F(2, 100), F(3, 100))
check("L06 M2 beta", F(200) / (F(200) * F(5, 4)), F(4, 5))
check("L06 M2 pi", F(4, 100) - F(4, 5) * F(-1, 100), F(48, 1000))
check("L06 M3 at un", F(2, 100) - F(1, 2) * 0, F(2, 100))
check("L06 M3 at un+0.03", F(2, 100) - F(1, 2) * F(3, 100), F(5, 1000))
check("L06 R2 u", un + F(1, 100) / beta0, F(62, 1000))

# seeded path (Part B): the same draws the page reports, recomputed from the Phillips form
rng = random.Random(20261028)
price, pi = P0, pi0
changes: list[tuple[int, F, F]] = []
for t in range(1, 13):
    draw = rng.randint(-100, 100)
    gap = F(draw, 10000)
    u = un + gap
    pe_t = price * (1 + pi)
    new_price = pe_t - kappa * (u - un) / nu6
    new_pi = (new_price - price) / price
    form = pi - (kappa / (nu6 * price)) * (u - un)
    check(f"L06 B t={t} identity", new_pi, form)
    changes.append((draw, gap, new_pi - pi))
    price, pi = new_price, new_pi
signs = [(dr > 0 and ch < 0) or (dr < 0 and ch > 0) for dr, _, ch in changes]
check("L06 B opposite sign every period", all(signs), True)
check("L06 B positive gap count", sum(1 for dr, _, _ in changes if dr > 0), 9)
check("L06 B negative gap count", sum(1 for dr, _, _ in changes if dr < 0), 3)
check("L06 E3 period-1 change", changes[0][2], F(-5, 6) * F(58, 10000))
check("L06 E3 5.5% row", -F(5, 6) * F(5, 1000), F(-5, 1200))
print("FAIL COUNT", len(FAILS), FAILS)
