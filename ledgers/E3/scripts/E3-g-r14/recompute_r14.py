"""Independent round-14 recomputation of the printed numbers of L05-L08 labs and card claims.

Standard library only; run as: python -I ledgers/E3/scripts/E3-g-r14/recompute_r14.py
Uses decimal at 50 digits and fractions; does not import the lab twins.
"""
from decimal import Decimal, getcontext
from fractions import Fraction
import math

getcontext().prec = 60
D = Decimal


def omega(p: Decimal) -> Decimal:
    """omega_{1/2}(p) = p^(1/2) / (p^(1/2) + (1-p)^(1/2))^2, the closed form of Example 1.4 (eta = 1/2)."""
    s = p.sqrt()
    t = (D(1) - p).sqrt()
    return s / ((s + t) ** 2)


def omega_closed(p: Decimal) -> Decimal:
    """sqrt(p)/(1 + 2 sqrt(p(1-p))), the simplified form stated in the lesson."""
    return p.sqrt() / (D(1) + D(2) * (p * (D(1) - p)).sqrt())


print("L07 part A values (closed form, 4 decimals):")
for p in ("0.01", "0.05", "0.3", "0.5", "0.6", "0.95", "0.99"):
    print(f"  p={p} omega={omega(D(p)):.4f}")
print("L07 closed form == general formula at p=0.3 (diff):", abs(omega(D("0.3")) - omega_closed(D("0.3"))))
ratio = omega(D("0.3")) / omega(D("0.6"))
print(f"L07 ratio omega(3/10)/omega(3/5) = {ratio:.10f}")
print(f"L07 thresholds: 1/(1+2^-1) = {1/(1+2**-1):.8f}; 1/(1+2^-0.5) = {1/(1+2**-0.5):.8f}")
print("L07 ratio exceeds both thresholds:", ratio > D(2) / D(3), ratio > D(1) / (D(1) + D(2) ** D("-0.5")))

# Example 2.1 lotteries: A = 0 (2/5), 50 (3/10), 100 (3/10); B = 0 (2/5), 100 (3/5)
w_3_10 = omega(D("0.3"))
w_3_5 = omega(D("0.6"))
for alpha in (D(1), D("0.5")):
    gA = w_3_10 * (D(50) ** alpha + D(100) ** alpha)
    gB = w_3_5 * (D(100) ** alpha)
    print(f"L07 alpha={alpha}: Gamma(A) = {gA:.10f}  Gamma(B) = {gB:.10f}")
gA1 = w_3_10 * D(150)
gB1 = w_3_5 * D(100)
diff = gA1 - gB1
print(f"L07 Gamma(A)-Gamma(B) at alpha=1, 40-digit value: {diff:.12f}")
print(f"L07 difference of 8-decimal roundings: {(gA1.quantize(D('0.00000001')) - gB1.quantize(D('0.00000001'))):.8f}")
print(f"L07 difference rounded to 4 decimals: {diff.quantize(D('0.0001'))}")
print(f"L07 printed 42.8686 - 39.1251 = {D('42.8686')-D('39.1251')}")

# sign changes and last grid point with omega(p) > p on 1001 points
grid = [D(i) / D(1000) for i in range(1, 1000)]
signs = [omega(p) - p > 0 for p in grid]
changes = sum(1 for a, b in zip(signs, signs[1:]) if a != b)
last_above = max(p for p in grid if omega(p) - p > 0)
print(f"L07 interior grid sign changes of omega(p)-p = {changes}; last point with omega(p)>p = {last_above}")

# L07 Lottery L: 100 w.p. 0.01, 50 w.p. 0.99 at alpha=1
print(f"L07 weighted value of L at alpha=1: {omega(D('0.01'))*100 + omega(D('0.99'))*50:.4f}")

# L08 gamble and certainty equivalents (CRRA u(w) = -1/w)
def ce(p_red: Fraction, w_red: Fraction, w_no: Fraction) -> float:
    eu = p_red * (-1 / w_red) + (1 - p_red) * (-1 / w_no)
    return float(1 / (-eu))

W0 = Fraction(100000)
wr, wn = W0 + 10000, W0 - 5000
print(f"L08 EU CE at P(red)=1/2: {ce(Fraction(1,2), wr, wn):.4f}")
print(f"L08 maxmin worst prior P(red)=1/3 CE: {ce(Fraction(1,3), wr, wn):.4f}")
print(f"L08 expected final wealth at 1/2: {Fraction(1,2)*wr + Fraction(1,2)*wn}")
print(f"L08 known urn red CE (P=1/3, bet pays 10000 on red, else 0): {ce(Fraction(1,3), W0+10000, W0):.4f}")
print(f"L08 known urn black CE (P(black)=2/3): {ce(Fraction(1,3), W0, W0+10000):.4f}")  # P(red)=1/3 => black wins w.p. 2/3
black_eu = Fraction(2, 3) * (-1 / (W0 + 10000)) + Fraction(1, 3) * (-1 / W0)
print(f"L08 known urn black CE (P(black)=2/3, wealth 110000 on black, else 100000): {float(1 / (-black_eu)):.4f}")

# ---- L05 printed values (Lab 1), exact Fractions unless stated ----
F = Fraction
beta, gam, psi, c0 = F(9, 10), F(2), F(1, 2), F(2)
tree = [(F(1, 2), F(1)), (F(1, 2), F(4))]
a = 1 - 1 / psi  # -1
ce1 = (sum(p * c ** (1 - gam) for p, c in tree)) ** (1 / (1 - gam))  # exponent 1/(1-gam) = -1
v0 = ((1 - beta) * c0 ** a + beta * ce1 ** a) ** (1 / a)
u_crra = (1 - beta) * (c0 ** (1 - gam) / (1 - gam)) + beta * sum(p * c ** (1 - gam) / (1 - gam) for p, c in tree)
print("L05 V0 =", v0, "(printed 80/49)", "U =", u_crra, "(printed -49/80)", "CE1 =", ce1, "(printed 8/5)")
print("L05 (1-gamma)U == V0^(1-gamma):", (1 - gam) * u_crra == v0 ** (1 - gam))
print("L05 theta =", (1 - gam) / (1 - 1 / psi))
def ce_g(g: float) -> float:
    return (0.5 * 1.0 ** (1 - g) + 0.5 * 4.0 ** (1 - g)) ** (1 / (1 - g))
print("L05 CE1 at gamma 0.5, 2, 3:", [round(ce_g(g), 4) for g in (0.5, 2.0, 3.0)], "(printed 2.2500, 1.6000, 1.3720)")
def v0_f(c0f: float, plan, b: float, g: float, ps: float) -> float:
    aa = 1 - 1 / ps
    cef = sum(p * c ** (1 - g) for p, c in plan) ** (1 / (1 - g))
    return ((1 - b) * c0f ** aa + b * cef ** aa) ** (1 / aa)
def u_f(c0f: float, plan, b: float, g: float) -> float:
    return (1 - b) * c0f ** (1 - g) / (1 - g) + b * sum(p * c ** (1 - g) / (1 - g) for p, c in plan)
plans = [
    [(0.5, 1.0), (0.5, 4.0)],
    [(0.25, 1.0), (0.75, 3.0)],
    [(1.0, 2.0)],
    [(1 / 3, 1.0), (2 / 3, 5.0)],
]
vs = [v0_f(2.0, p, 0.9, 2.0, 0.5) for p in plans]
us = [u_f(2.0, p, 0.9, 2.0) for p in plans]
print("L05 four plans V0:", [round(x, 6) for x in vs], "U:", [round(x, 6) for x in us])
print("L05 same ranking under V0 and U:", sorted(range(4), key=lambda i: vs[i]) == sorted(range(4), key=lambda i: us[i]))
print("L05 V0(4,4)=", round(v0_f(4.0, [(1.0, 4.0)], 0.5, 2.0, 2.0), 4), " V0(1,10)=", round(v0_f(1.0, [(1.0, 10.0)], 0.5, 2.0, 2.0), 4))
print("L05 U(4,4)=", round(u_f(4.0, [(1.0, 4.0)], 0.5, 2.0), 4), " U(1,10)=", round(u_f(1.0, [(1.0, 10.0)], 0.5, 2.0), 4))
print("L05 EIS analytic = psi: 0.5, 2, 0.25 (Proposition 2.2); MRS at (2,4), beta 0.9, psi 0.5 =",
      ((1 - 0.9) / 0.9) * (4.0 / 2.0) ** (1 / 0.5))

# ---- L06 printed values: prospect value W = sum over gains v(x) pi(p) - lam * ... for the gamble (+1000 p=1/2, -600 p=1/2)
def W(lam: float, al: float, de: float) -> float:
    gain = 0.5 * 1000 ** al
    loss = 0.5 * 600 ** de
    return gain - lam * loss
print("L06 W(lam=1,al=de=1)=", W(1, 1, 1), " W(3/2)=", W(1.5, 1, 1), " W(2)=", W(2, 1, 1), " lam*=", 500 / 300)
print("L06 two copies, combined W at lam=2 (outcomes 2000 p1/4, 400 p1/2, -1200 p1/4):",
      0.25 * 2000 - 2 * 0.25 * 1200 + 0.5 * 400, " separate:", 2 * W(2, 1, 1))
print("L06 alpha=delta=0.5: lam* =", round(0.5 * 1000 ** 0.5 / (0.5 * 600 ** 0.5), 4), " W(2) =", round(W(2, 0.5, 0.5), 4))

# ---- L08 Part B: Epstein-Zin CE at date 1 for the gamble (date 0 consumes w0 = 100000, date 1 = 110000 or 95000, P = 1/2)
# Closed form for the sure amount x that gives the same V0 as the gamble: x^a = (V^a - (1-beta) w0^a) / beta, a = 1 - 1/psi.
def ez_ce_gamble(psi: float, beta: float, gamma: float = 2.0) -> float:
    w0, w1, w2 = 100000.0, 110000.0, 95000.0
    a = 1 - 1 / psi
    expc = 0.5 * w1 ** (1 - gamma) + 0.5 * w2 ** (1 - gamma)
    ce1 = expc ** (1 / (1 - gamma))
    v = ((1 - beta) * w0 ** a + beta * expc ** (a / (1 - gamma))) ** (1 / a)
    x = ((v ** a - (1 - beta) * w0 ** a) / beta) ** (1 / a)
    return x, ce1
for psi_v, beta_v in ((0.5, 0.9), (0.5, 0.95), (1.5, 0.9), (1.5, 0.95), (3.0, 0.9), (3.0, 0.95)):
    x, ce1 = ez_ce_gamble(psi_v, beta_v)
    print(f"L08 part B psi={psi_v} beta={beta_v}: EZ CE (closed form) = {x:.6f}, CRRA CE1 = {ce1:.6f}, gap = {x - ce1:.2e}")
