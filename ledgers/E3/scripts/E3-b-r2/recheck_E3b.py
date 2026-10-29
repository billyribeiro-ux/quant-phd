"""Independent recomputation for E3 slice b (L04-L06). Written by the verifier; standard library only.

Re-derives the numbers printed or stated in L04, L05 and L06 without importing the lab code.
Run: .venv/bin/python -I ledgers/E3/scripts/E3-b-r1/recheck_E3b.py
"""
from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction as F

SECTION = "L04"
S5 = (1000, 2000, 3000, 4000, 5000)


def cdf(pmf, t):
    return sum((p for x, p in pmf.items() if x <= t), F(0))


def icdf(pmf, t):  # I(t) = E[(t-X)^+] (Lemma 1.2)
    return sum((p * max(t - x, 0) for x, p in pmf.items()), F(0))


def mean(pmf):
    return sum((p * x for x, p in pmf.items()), F(0))


print("== L04 examples (exact)")
X = {2000: F(1, 2), 4000: F(1, 2)}
Y = {1000: F(1, 4), 3000: F(1, 2), 5000: F(1, 4)}
print("Ex2.5 I_X at 1000..5000:", [str(icdf(X, t)) for t in S5])
print("Ex2.5 I_Y at 1000..5000:", [str(icdf(Y, t)) for t in S5])
print("Ex2.5 means:", mean(X), mean(Y), "F_X(2000), F_Y(2000):", cdf(X, 2000), cdf(Y, 2000), "F_X(3000), F_Y(3000):", cdf(X, 3000), cdf(Y, 3000))
X6 = {1000: F(1, 2), 5000: F(1, 2)}
Y6 = {3000: F(1)}
print("Ex2.6 I_X:", [str(icdf(X6, t)) for t in S5], "I_Y:", [str(icdf(Y6, t)) for t in S5])
M1x = {1000: F(1, 2), 4000: F(1, 2)}
M1y = {2000: F(1)}
print("M1 means:", mean(M1x), mean(M1y), "F_X(1000,2000,4000):", [str(cdf(M1x, t)) for t in (1000, 2000, 4000)], "F_Y:", [str(cdf(M1y, t)) for t in (1000, 2000, 4000)])
print("M3 I_X(3000) via F-integral 1/4*(3000-1000) =", F(1, 4) * 2000, " via E(3000-X)^+ =", icdf({1000: F(1, 4), 5000: F(3, 4)}, 3000))
print("E1 I_Y(4000) pair B:", icdf({3000: F(1, 2), 4000: F(1, 2)}, 4000))

print("== L04 Theorems 1.5 and 2.3 sanity: random exact pairs on S5 (witness test vs utility test)")
rng = random.Random(1)


def rnd_pmf():
    w = [rng.randint(0, 4) for _ in S5]
    if sum(w) == 0:
        w[0] = 1
    tot = sum(w)
    return {x: F(wi, tot) for x, wi in zip(S5, w) if wi}


def fosd_witness(px, py):
    fx = all(cdf(px, t) <= cdf(py, t) for t in S5)
    fy = all(cdf(py, t) <= cdf(px, t) for t in S5)
    return fx, fy


bad_fo = 0
bad_so = 0
n_so = 0
for _ in range(3000):
    px, py = rnd_pmf(), rnd_pmf()
    fx, fy = fosd_witness(px, py)
    # utility test over the 4 monotone grid utilities u_k(s)=1{s>S5[k]} is the witness set; check against all nondecreasing
    # integer-valued utilities on S5 with values in {0,1,2} (a finite but rich set)
    ok_x = ok_y = True
    for u in itertools.product((0, 1, 2), repeat=5):
        if any(u[i] > u[i + 1] for i in range(4)):
            continue
        d = sum((px.get(x, F(0)) - py.get(x, F(0))) * uu for x, uu in zip(S5, u))
        if d < 0:
            ok_x = False
        if d > 0:
            ok_y = False
    if (fx == ok_x) is False or (fy == ok_y) is False:
        bad_fo += 1
    if mean(px) == mean(py):
        n_so += 1
        ix = all(icdf(px, t) <= icdf(py, t) for t in S5)
        iy = all(icdf(py, t) <= icdf(px, t) for t in S5)
        ok_x2 = ok_y2 = True
        for u in itertools.product((-4, -3, -2, -1, 0), repeat=5):
            if any(u[i] > u[i + 1] for i in range(4)):
                continue
            # concave test on S5 via chord slopes (nonincreasing)
            sl = [F(u[i + 1] - u[i], S5[i + 1] - S5[i]) for i in range(4)]
            if any(sl[i] < sl[i + 1] for i in range(3)):
                continue
            d = sum((px.get(x, F(0)) - py.get(x, F(0))) * uu for x, uu in zip(S5, u))
            if d < 0:
                ok_x2 = False
            if d > 0:
                ok_y2 = False
        if (ix == ok_x2) is False or (iy == ok_y2) is False:
            bad_so += 1
print("FOSD witness vs grid-utility disagreements in 3000 pairs:", bad_fo)
print("SOSD integrated vs concave-grid-utility disagreements in", n_so, "equal-mean pairs (grid {-4..0}^5, includes min(s-t,0)/1000 witnesses):", bad_so)

print("== L04 Lab 1 printed counts (from the embedded output) re-tallied")
counts = {"X dominates Y": 3, "Y dominates X": 10, "identical": 1, "no ranking": 10}
print("FOSD tallies sum to", sum(counts.values()))
print("SOSD tallies sum to", 3 + 2 + 1 + 2, "over 8 equal-mean pairs")

SECTION = "L05"
print("== L05")


def ez(c0, plan, beta, gamma, psi):
    a = 1 - 1 / psi
    ce = (sum(p * c ** (1 - gamma) for p, c in plan)) ** (1 / (1 - gamma))
    return ((1 - beta) * c0 ** a + beta * ce ** a) ** (1 / a)


def crra_eu(c0, plan, beta, gamma):
    u = lambda c: c ** (1 - gamma) / (1 - gamma)  # noqa: E731
    return (1 - beta) * u(c0) + beta * sum(p * u(c) for p, c in plan)


tree = [(F(1, 2), F(1)), (F(1, 2), F(4))]
beta, gam, psi, c0 = F(9, 10), F(2), F(1, 2), F(2)
a = 1 - 1 / psi
ce1 = sum(p * c ** (1 - gam) for p, c in tree) ** (1 / (1 - gam))
v0 = ((1 - beta) * c0 ** a + beta * sum(p * c ** a for p, c in tree) ** 1) ** (1 / a)  # CE1^a = E c^{-1} at gamma 2 (a = -1)
print("a =", a, "CE1 =", ce1, "mean =", sum(p * c for p, c in tree))
print("V0 by hand (a=-1, E c1^{-1}=5/8):", ((F(1, 10)) * F(1, 2) + F(9, 10) * F(5, 8)) ** -1)
print("U by hand:", (F(1, 10)) * (-F(1, 2)) + F(9, 10) * sum(p * (-1 / c) for p, c in tree))
print("(1-gamma)U vs V0^(1-gamma):", (1 - gam) * (F(-49, 80)), F(80, 49) ** (1 - gam))
print("E2 variant V0 and CE1:", ((F(1, 10)) * F(1, 2) + F(9, 10) * (F(1, 4) * 1 + F(3, 4) * F(1, 4))) ** -1)
print("L05 lab floats: V0(4,4) at psi=2,gamma=2,beta=1/2:", ez(4.0, [(1.0, 4.0)], 0.5, 2.0, 2.0),
      " V0(1,10):", ez(1.0, [(1.0, 10.0)], 0.5, 2.0, 2.0))
print("U(4,4)", crra_eu(4.0, [(1.0, 4.0)], 0.5, 2.0), "U(1,10)", crra_eu(1.0, [(1.0, 10.0)], 0.5, 2.0))

# Theorem 3.2 with gamma < 0 (A2 fails, psi = 1/gamma < 0): does the identity still hold?
for g in (-1.0, -0.5, 0.5):
    psi_g = 1 / g
    plan = [(0.3, 0.5), (0.7, 3.0)]
    b, c0g = 0.95, 1.5
    lhs = (1 - g) * crra_eu(c0g, plan, b, g)
    rhs = ez(c0g, plan, b, g, psi_g) ** (1 - g)
    print(f"Theorem 3.2 identity at gamma={g}, psi={psi_g:.3f}: lhs={lhs:.12f} rhs={rhs:.12f} ok={math.isclose(lhs, rhs, rel_tol=1e-9)}")

# Proposition 2.2 hypotheses omit A3: check whether gamma = 1 matters for deterministic plans (value via formula)
print("deterministic V0 at gamma=1 (formula with c^(1-1) defined via limit not needed):", ez(2.0, [(1.0, 4.0)], 0.9, 1.0 + 1e-12, 0.5))

# EIS = psi for several gamma, analytic MRS check
for g in (0.5, 2.0, 3.0):
    b, p_ = 0.9, 0.5
    c0v, c1v = 2.0, 4.0
    h = 1e-6
    val = lambda x, y: ez(x, [(1.0, y)], b, g, p_)  # noqa: E731
    dv0 = (val(c0v * (1 + h), c1v) - val(c0v * (1 - h), c1v)) / (2 * c0v * h)
    dv1 = (val(c0v, c1v * (1 + h)) - val(c0v, c1v * (1 - h))) / (2 * c1v * h)
    mrs = dv0 / dv1
    print(f"gamma={g}: numeric MRS {mrs:.9f}; formula {((1-b)/b)*(c1v/c0v)**(1/p_):.9f}")

print("== L05 Remark 3.4 witness and CE1 falls: CE1 at gammas 0.5,2,3:",
      [round(sum(p * c ** (1 - g) for p, c in [(0.5, 1.0), (0.5, 4.0)]) ** (1 / (1 - g)), 4) for g in (0.5, 2.0, 3.0)])

print("== L06")
SECTION = "L06"
# Remark 3.2 check: reference point EV, alpha = delta; sign change location
def V_ref(p, g, l, alpha, lam):
    ev = p * g - (1 - p) * l
    gain = g - ev
    loss = l + ev
    return p * gain ** alpha - (1 - p) * lam * loss ** alpha


def thr_ref(p, g, l, alpha):
    ev = p * g - (1 - p) * l
    return p * (g - ev) ** alpha / ((1 - p) * (l + ev) ** alpha)


print("Example 2.3 gamble, EV reference, alpha=delta=0.5: V at lam=1:", round(V_ref(0.5, 1000, 600, 0.5, 1.0), 6),
      "threshold:", round(thr_ref(0.5, 1000, 600, 0.5), 6))
print("Counter-case p=1/3, g=1000, l=300, alpha=delta=1/2: threshold =", round(thr_ref(1 / 3, 1000, 300, 0.5), 6),
      " V at lam=1 =", round(V_ref(1 / 3, 1000, 300, 0.5, 1.0), 6), " V at lam=0.5 =", round(V_ref(1 / 3, 1000, 300, 0.5, 0.5), 6))
print("Counter-case p=1/3, g=1000, l=300, alpha=delta=1: threshold =", round(thr_ref(1 / 3, 1000, 300, 1.0), 6))

print("Prop 2.2 check alpha=delta=1/2 threshold sqrt(5/3) =", math.sqrt(5 / 3), " V at lam=2:",
      0.5 * 1000 ** 0.5 - 0.5 * 2 * 600 ** 0.5)
print("Remark 2.5 values:", F(1, 4) * 2000 + F(1, 2) * 400 - F(1, 4) * 2 * 1200, 2 * (500 - 300 * 2), 700 - 300 * F(3, 2), 1000 - 600 * F(3, 2))
print("E3 threshold window: separate negative above 5/3:", 1000 - 600 * F(5, 3), "; combined positive below 7/3:", 700 - 300 * F(7, 3))
print("M1 threshold:", F(1, 3) * 900 / (F(2, 3) * 300), "V at 2:", F(1, 3) * 900 - F(2, 3) * 2 * 300)
print("M2 V:", F(1, 2) * 100 - F(1, 2) * 2 * 100)
print("M3 v(16), v(-16):", 16 ** 0.5, -2 * 16 ** 0.5)
print("Ex2.3 V at 1, 3/2, 2:", [500 - 300 * l for l in (F(1), F(3, 2), F(2))])
print("Grid check for Prop 1.4 at alpha=delta=0.5 (gains concave, losses convex, lam=2):")
g_grid = (1.0, 2.0, 4.0, 9.0)
l_grid = (-9.0, -4.0, -2.0, -1.0)


def vp(x, lam=2.0, a=0.5):
    return x ** a if x >= 0 else -lam * (-x) ** a


print(" concave gains:", all(vp((x + y) / 2) >= (vp(x) + vp(y)) / 2 - 1e-15 for x in g_grid for y in g_grid),
      " convex losses:", all(vp((x + y) / 2) <= (vp(x) + vp(y)) / 2 + 1e-15 for x in l_grid for y in l_grid))
print("Lab check values V at lam=2 power:", 0.5 * 1000 ** 0.5 - 0.5 * 2 * 600 ** 0.5)
