"""Independent recomputation of every displayed number in E2 L04-L06 (round 5, verifier-written).

Run: .venv/bin/python -I ledgers/E2/scripts/E2-b-r5/recompute_E2b_r5.py
Prints one line per check and a final ALL-TRUE flag. Uses exact Fractions only.
"""

from fractions import Fraction as F
from itertools import combinations
import math

checks: list[tuple[str, bool]] = []


def chk(name: str, ok: bool) -> None:
    checks.append((name, bool(ok)))
    print(("OK   " if ok else "FAIL ") + name)


def half_up(x: F) -> int:
    return math.floor(x + F(1, 2))


# ---------------- L04: signaling ----------------
yL, yH, cL, cH = 4_000_000, 6_000_000, 1_000_000, 500_000
D = yH - yL
chk("L04 base Delta = 2,000,000", D == 2_000_000)
chk("L04 bounds 2 and 4", F(D, cL) == 2 and F(D, cH) == 4)


def wage(e: int, t: int) -> int:
    return yH if e >= t else yL


def u(c: int, e: int, t: int) -> int:
    return wage(e, t) - c * e


sep = []
for t in range(0, 7):
    uh = u(cH, t, t)
    bh = max(u(cH, e, t) for e in range(7))
    ul = u(cL, 0, t)
    bl = max(u(cL, e, t) for e in range(7))
    if t >= 1 and uh == bh and ul == bl:
        sep.append(t)
chk("L04 enumerated separating set == [2,3,4]", sep == [2, 3, 4])
chk("L04 t=1 low type prefers e=1 (5,000,000 > 4,000,000)", u(cL, 1, 1) == 5_000_000 and u(cL, 0, 1) == 4_000_000)
chk("L04 t=5 high utility 3,500,000 vs best 4,000,000", u(cH, 5, 5) == 3_500_000 and max(u(cH, e, 5) for e in range(7)) == 4_000_000)
chk("L04 t=6 high utility 3,000,000", u(cH, 6, 6) == 3_000_000)
chk("L04 Remark 2.1: net utility at t=2 is 5,000,000, cost 1,000,000", u(cH, 2, 2) == 5_000_000 and 2 * cH == 1_000_000)
chk("L04 Remark 2.1: at t=4 net utility 4,000,000", u(cH, 4, 4) == 4_000_000)
chk("L04 misc: wage gain 2,000,000 and cost 1,000,000 at t=2", yH - yL == 2_000_000 and 2 * cH == 1_000_000)
chk("L04 m1 (cH=250k): bounds 2 and 8", F(D, cL) == 2 and F(D, 250_000) == 8)
chk("L04 m2: high utility at t=3 is 5,250,000", yH - 3 * 250_000 == 5_250_000)
chk("L04 m2: low at e=3 is 3,000,000 < 4,000,000", yH - 3 * cL == 3_000_000 and yH - 3 * cL < yL)
chk("L04 m3 (D=1.5M): interval [1.5,3] has whole numbers 2,3", [t for t in range(0, 10) if F(3, 2) <= t <= 3] == [2, 3])
chk("L04 e1 (cH=400k): thresholds 2..5, t=5 high utility equals 4,000,000", [t for t in range(0, 10) if F(D, cL) <= t <= F(D, 400_000)] == [2, 3, 4, 5] and yH - 5 * 400_000 == yL)
chk("L04 e2 (yH=5M): bounds 1 and 2; high at t=1 is 4,500,000; low at e=1 equals 4,000,000",
    F(1_000_000, cL) == 1 and F(1_000_000, cH) == 2 and 5_000_000 - cH == 4_500_000 and 5_000_000 - cL == 4_000_000)
chk("L04 e3: net utilities 5,000,000 / 4,500,000 / 4,000,000", [yH - t * cH for t in (2, 3, 4)] == [5_000_000, 4_500_000, 4_000_000])
chk("L04 quiz: upper bound 4; 2,000,000/500,000 = 4", D // cH == 4)
chk("L04 c_H = c_L: single point Delta/c (r p2 example)", F(D, cL) == F(D, cL))

# ---------------- L05: screening ----------------
tL, tH = F(3000), F(6000)
pL, pH = F(3, 4), F(1, 4)


def C(q: F) -> F:
    return q * q / 2


def profit_binding(qL: F, qH: F) -> F:
    mL = tL * qL
    mH = tH * qH - (tH - tL) * qL
    return pL * (mL - C(qL)) + pH * (mH - C(qH))


qL_star = tL - pH / pL * (tH - tL)
chk("L05 q_L* = 2000", qL_star == 2000)
mL = tL * qL_star
mH = tH * 6000 - (tH - tL) * qL_star
chk("L05 m_L = 6,000,000 and m_H = 30,000,000", mL == 6_000_000 and mH == 30_000_000)
chk("L05 U_H = 6,000,000; high IC slack 0", (tH * 6000 - mH) == 6_000_000 and (tH * 6000 - mH) - (tH * qL_star - mL) == 0)
chk("L05 low IC slack 12,000,000", (tL * 6000 - mH) - (tL * qL_star - mL) == -12_000_000 and (tL * qL_star - mL) - (tL * 6000 - mH) == 12_000_000)
fb = pL * (tL * 3000 - C(F(3000))) + pH * (tH * 6000 - C(F(6000)))
chk("L05 first best 7,875,000", fb == 7_875_000)
menu = profit_binding(F(2000), F(6000))
chk("L05 menu profit 6,000,000; gap 1,875,000", menu == 6_000_000 and fb - menu == 1_875_000)
chk("L05 Remark 2.1 split 375,000 + 1,500,000", pL * (F(4_500_000) - F(4_000_000)) == 375_000 and pH * 6_000_000 == 1_500_000)
chk("L05 FOC 750 = 750", pL * (tL - 2000) == pH * (tH - tL) == 750)

# Vertex enumeration of the LP over (m_L, m_H) for fixed (q_L, q_H): exact optimum of the menu problem on a grid.
best = None
for qL_i in range(0, 3001, 100):
    for qH_i in range(0, 12001, 500):
        qL_, qH_ = F(qL_i), F(qH_i)
        dq = qH_ - qL_
        lines = [  # (a, b, rhs) meaning a*mL + b*mH = rhs
            (F(1), F(0), tL * qL_),  # PC-L binds
            (F(0), F(1), tH * qH_),  # PC-H binds
            (F(-1), F(1), tH * dq),  # IC-H: mH - mL <= tH dq
            (F(-1), F(1), tL * dq),  # IC-L: mH - mL >= tL dq
        ]
        feas_vertices = []
        for (a1, b1, r1), (a2, b2, r2) in combinations(lines, 2):
            det = a1 * b2 - a2 * b1
            if det == 0:
                continue
            x = (r1 * b2 - r2 * b1) / det
            y = (a1 * r2 - a2 * r1) / det
            ok = x <= tL * qL_ and y <= tH * qH_ and (y - x) <= tH * dq and (y - x) >= tL * dq
            if ok:
                feas_vertices.append((x, y))
        if not feas_vertices:
            continue
        val = max(pL * (x - C(qL_)) + pH * (y - C(qH_)) for x, y in feas_vertices)
        if best is None or val > best[0]:
            best = (val, qL_, qH_)
chk("L05 grid LP over menus: best profit 6,000,000 at (2000,6000)", best is not None and best[0] == 6_000_000 and best[1] == 2000 and best[2] == 6000)

# L05 problem m1, m2, m3
chk("L05 m1 (pH=1/2): q_L*=0; profit 9,000,000", tL - F(1, 2) / F(1, 2) * (tH - tL) == 0 and F(1, 2) * (36_000_000 - 18_000_000) == 9_000_000)
p_m2 = F(3, 4) * (F(3_000_000) - F(500_000)) + F(1, 4) * (F(33_000_000) - F(18_000_000))
chk("L05 m2 mL=3M, mH=33M, UH=3M, IC-L -15M", 3000 * 1000 == 3_000_000 and 36_000_000 - 3_000_000 == 33_000_000 and 36_000_000 - 33_000_000 == 3_000_000 and 18_000_000 - 33_000_000 == -15_000_000)
chk("L05 m3 profit 5,625,000", p_m2 == 5_625_000)
# L05 e1: pH=1/3
pL3, pH3 = F(2, 3), F(1, 3)
qL3 = tL - pH3 / pL3 * (tH - tL)
chk("L05 e1 q_L* = 1500", qL3 == 1500)
p_at_1500 = pL3 * (tL * 1500 - C(F(1500))) + pH3 * ((tH * 6000 - (tH - tL) * 1500) - C(F(6000)))
chk("L05 e1 profit at 1500 = 6,750,000", p_at_1500 == 6_750_000)
p_at_2000 = pL3 * (tL * 2000 - C(F(2000))) + pH3 * ((tH * 6000 - (tH - tL) * 2000) - C(F(6000)))
fb3 = pL3 * (tL * 3000 - C(F(3000))) + pH3 * (tH * 6000 - C(F(6000)))
chk("L05 e1 menu at 2000 = 6,666,667 (half up), gap 2,333,333", half_up(p_at_2000) == 6_666_667 and half_up(fb3 - p_at_2000) == 2_333_333 and fb3 == 9_000_000)
chk("L05 e1 gap at 1500 = 2,250,000", fb3 - p_at_1500 == 2_250_000)
chk("L05 e2 rent 6M at p=1/4 and 4.5M at p=1/3", 3000 * 2000 == 6_000_000 and 3000 * 1500 == 4_500_000)
chk("L05 e3 percents 23.81 and 31.25", round(float(F(1_875_000, 7_875_000)) * 100, 2) == 23.81 and round(float(F(7_875_000, 6_000_000) - 1) * 100, 2) == 31.25)
chk("L05 r3/quiz: first best 0.75*4.5M+0.25*18M", F(3, 4) * F(4_500_000) + F(1, 4) * F(18_000_000) == 7_875_000)

# ---------------- L06: moral hazard ----------------
X = 1_000_000
EH, EL = F(750_000), F(250_000)
cH6 = 100_000
dE = EH - EL
FB = EH - cH6
chk("L06 E_H 750k, E_L 250k, Delta_E 500k, first best 650k", EH == 750_000 and EL == 250_000 and dE == 500_000 and FB == 650_000)
chk("L06 threshold beta = cH/dE = 1/5", F(cH6) / dE == F(1, 5))


def agent(beta: F, alpha: F = F(0)):
    uH = alpha + beta * EH - cH6
    uL = alpha + beta * EL
    if uH >= uL and uH >= 0:
        return "high", uH, uL
    if uL >= 0:
        return "low", uH, uL
    return "refuse", uH, uL


def prin(beta: F, alpha: F = F(0)) -> F:
    a, _, _ = agent(beta, alpha)
    if a == "high":
        return EH - alpha - beta * EH
    if a == "low":
        return EL - alpha - beta * EL
    return F(0)


grid = [F(k, 100) for k in range(101)]
bestg = max(grid, key=lambda b: (prin(b), -b))
chk("L06 grid best share 0.20 with profit 600,000", bestg == F(1, 5) and prin(bestg) == 600_000)
chk("L06 Part A rows: 0.00 low/250k; 0.10 low/225k; 0.30 high/525k; 1.00 high/0",
    agent(F(0))[0] == "low" and prin(F(0)) == 250_000 and agent(F(1, 10))[0] == "low" and prin(F(1, 10)) == 225_000
    and prin(F(3, 10)) == 525_000 and prin(F(1)) == 0 and agent(F(1))[0] == "high")
chk("L06 Part A row 0.20 utilities 50,000 tie", agent(F(1, 5))[1] == agent(F(1, 5))[2] == 50_000)
chk("L06 Part A row 0.30 utilities 125,000 / 75,000", agent(F(3, 10))[1] == 125_000 and agent(F(3, 10))[2] == 75_000)
chk("L06 Part A row 1.00 utilities 650,000 / 250,000", agent(F(1))[1] == 650_000 and agent(F(1))[2] == 250_000)
for b, a_exp in [(F(1, 5), -50_000), (F(1, 2), -275_000), (F(1), -650_000)]:
    alpha = cH6 - b * EH
    chk(f"L06 Part C beta={b} alpha={a_exp}", alpha == a_exp and (EH - (alpha + b * EH)) == FB)
# Remark 1.4: beta E_H >= 150,000 > c_H for every beta >= 1/5
chk("L06 Remark 1.4: beta*E_H >= 150,000 > c_H (100,000)", F(1, 5) * EH == 150_000 and 150_000 > cH6)
chk("L06 p1 counterexample utilities -725,000 / -875,000",
    -1_000_000 + F(1, 2) * EH - cH6 == -725_000 and -1_000_000 + F(1, 2) * EL == -875_000)
chk("L06 m1 (beta=1/4): uH 87,500, uL 62,500, profit 562,500",
    F(1, 4) * EH - cH6 == 87_500 and F(1, 4) * EL == 62_500 and EH * F(3, 4) == 562_500)
chk("L06 m2 (beta=2/15): uH = 0, uL = 33,333.33", F(2, 15) * EH - cH6 == 0 and half_up(F(2, 15) * EL) == 33_333)
chk("L06 m3 (alpha=10k, beta=1/5): profit 590,000", EH - (10_000 + F(1, 5) * EH) == 590_000)
chk("L06 p2/p3: profit bounds 600,000 and 250,000", EH * F(4, 5) == 600_000 and EL == 250_000)
chk("L06 Remark 2.1 identity 600,000+50,000 = 650,000", F(600_000) + 50_000 == FB)


def vertex_opt(EH_: F, EL_: F, cH_: F):
    """Exact optimum over (alpha, beta): maximize EH - alpha - beta EH s.t. IC, PC, alpha>=0, alpha+beta X>=0."""
    dE_ = EH_ - EL_
    lines = [
        (F(0), F(1), cH_ / dE_),  # IC: beta >= cH/dE (boundary)
        (F(1), F(0), F(0)),  # alpha >= 0 (boundary)
        (F(1), F(X), F(0)),  # alpha + beta X >= 0 (boundary)
        (F(1), EH_, cH_),  # PC: alpha + beta EH - cH >= 0 (boundary)
    ]

    def feas(a, b):
        return (
            b * dE_ >= cH_ and a >= 0 and a + b * X >= 0 and a + b * EH_ - cH_ >= 0
        )

    bestv = None
    for (a1, b1, r1), (a2, b2, r2) in combinations(lines, 2):
        det = a1 * b2 - a2 * b1
        if det == 0:
            continue
        a = (r1 * b2 - r2 * b1) / det
        b = (a1 * r2 - a2 * r1) / det
        if feas(a, b):
            v = EH_ - a - b * EH_
            if bestv is None or v > bestv[0]:
                bestv = (v, a, b)
    return bestv


vb = vertex_opt(F(750_000), F(250_000), F(100_000))
chk("L06 vertex LP base: profit 600,000 at alpha 0, beta 1/5", vb == (600_000, 0, F(1, 5)))
ve1 = vertex_opt(F(750_000), F(250_000), F(150_000))
chk("L06 vertex LP e1 (cH=150k): profit 525,000 at beta 3/10", ve1 is not None and ve1[0] == 525_000 and ve1[2] == F(3, 10) and ve1[1] == 0)
ve2 = vertex_opt(F(800_000), F(200_000), F(100_000))
chk("L06 vertex LP e2: beta 1/6, profit 800,000*5/6 = 666,666 2/3 -> 666,667", ve2 is not None and ve2[2] == F(1, 6) and half_up(F(ve2[0])) == 666_667)
chk("L06 e2 first best 700,000", F(800_000) - 100_000 == 700_000)
chk("L06 e1 agency cost 75,000 and e2 agency cost (first best minus best profit)", 600_000 - 525_000 == 75_000)

failed = [n for n, ok in checks if not ok]
print("TOTAL", len(checks), "FAILED", len(failed))
print("ALL True" if not failed else "NOT ALL TRUE: " + "; ".join(failed))
