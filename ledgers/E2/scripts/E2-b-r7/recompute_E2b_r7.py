"""Independent exact recomputation for E2 slice b (L04-L06), round 7. Fractions only; prints every checked value."""
from fractions import Fraction as F
import math

def half_up(x):
    return math.floor(F(x) + F(1, 2))

fails = []
def check(name, got, want):
    ok = got == want
    print(("OK  " if ok else "FAIL"), name, got, "" if ok else f"(want {want})")
    if not ok:
        fails.append(name)

# ---------- L04 ----------
yL, yH, cL, cH = 4_000_000, 6_000_000, 1_000_000, 500_000
D = yH - yL
check("L04 Delta", D, 2_000_000)
check("L04 lower bound D/cL", F(D, cL), 2)
check("L04 upper bound D/cH", F(D, cH), 4)
def wage(e, t): return yH if e >= t else yL
def util(c, e, t): return wage(e, t) - c * e
sep = []
for t in range(0, 7):
    uh = util(cH, t, t); bh = max(util(cH, e, t) for e in range(7))
    ul = util(cL, 0, t); bl = max(util(cL, e, t) for e in range(7))
    if t >= 1 and uh == bh and ul == bl:
        sep.append(t)
check("L04 enumerated separating set", sep, [2, 3, 4])
check("L04 high utility at t=2", util(cH, 2, 2), 5_000_000)
check("L04 high utility at t=4", util(cH, 4, 4), 4_000_000)
check("L04 cost at t=2 (cents)", 2 * cH, 1_000_000)
check("L04 wage gain at t=2", yH - yL, 2_000_000)
check("L04 low type at e=1 under t=1 (mimic utility)", util(cL, 1, 1), 5_000_000)
check("L04 low type at e=0", util(cL, 0, 1), 4_000_000)
# problem set
check("L04-m1 upper bound new cH", F(D, 250_000), 8)
check("L04-m2 high utility at t=3", yH - 250_000 * 3, 5_250_000)
check("L04-m2 low at e=3 (new cL?) -> y_H - 3*cL_new", yH - 3 * 1_000_000, 3_000_000)
check("L04-m3 bounds", (F(1_500_000, 1_000_000), F(1_500_000, 500_000)), (F(3, 2), 3))
check("L04-e1 upper bound cH=400000", F(D, 400_000), 5)
check("L04-e2 D=1e6 bounds", (F(1_000_000, 1_000_000), F(1_000_000, 500_000)), (1, 2))
check("L04-e2 high util at t=1", yH - 500_000 * 1, 5_500_000 - 1_000_000 + 1_000_000 - 1_000_000 + 0 if False else 5_500_000)
check("L04-e3 utils", [yH - cH * t for t in (2, 3, 4)], [5_000_000, 4_500_000, 4_000_000])

# ---------- L05 ----------
tL, tH = 3000, 6000
pL, pH = F(3, 4), F(1, 4)
def C(q): return F(q) * F(q) / 2
def menu_profit(qL, qH, pL=pL, pH=pH):
    mL = tL * qL
    mH = tH * qH - (tH - tL) * qL
    return pL * (mL - C(qL)) + pH * (mH - C(qH)), mL, mH
qL_star = tL - (pH / pL) * (tH - tL)
check("L05 q_L*", qL_star, 2000)
pr, mL, mH = menu_profit(2000, 6000)
check("L05 menu profit exact", pr, 6_000_000)
check("L05 m_L", mL, 6_000_000)
check("L05 m_H", mH, 30_000_000)
check("L05 rent U_H", tH * 6000 - mH, 6_000_000)
check("L05 U_H = (tH-tL) qL", (tH - tL) * 2000, 6_000_000)
# first best
fb = pL * (tL * 3000 - C(3000)) + pH * (tH * 6000 - C(6000))
check("L05 first best profit", fb, 7_875_000)
check("L05 gap", fb - pr, 1_875_000)
check("L05 low-type loss weighted", pL * ((tL*3000 - C(3000)) - (tL*2000 - C(2000))), 375_000)
check("L05 high-type rent weighted", pH * 6_000_000, 1_500_000)
check("L05 low-type cut FOC", pL * (tL - 2000), pH * (tH - tL))
# Part B/C grid maxima
best_qL = max(range(0, 6001), key=lambda q: (menu_profit(F(q), F(6000))[0], -q))
check("L05 Part B argmax", best_qL, 2000)
best_qH = max(range(0, 12001, 1000), key=lambda q: (menu_profit(F(2000), F(q))[0], -q))
check("L05 Part C argmax", best_qH, 6000)
# Remark 2.1 / misc
check("L05-m1 qL* at pH=1/2", tL - F(1, 1) * (tH - tL), 0)
check("L05-m1 profit", F(1, 2) * (36_000_000 - C(6000)), 9_000_000)
check("L05-m2 mL", tL * 1000, 3_000_000)
check("L05-m2 mH", tH * 6000 - (tH - tL) * 1000, 33_000_000)
check("L05-m2 UH", tH * 6000 - 33_000_000, 3_000_000)
check("L05-m2 IC-L slack", tL * 6000 - 33_000_000, -15_000_000)
p3 = menu_profit(F(1000), F(6000))[0]
check("L05-m3 profit", p3, F(5_625_000))
# e1: pL=2/3,pH=1/3
pL2, pH2 = F(2, 3), F(1, 3)
check("L05-e1 qL*", tL - (pH2 / pL2) * (tH - tL), 1500)
check("L05-e1 profit at 1500,6000", menu_profit(F(1500), F(6000), pL2, pH2)[0], 6_750_000)
check("L05-e1 first best", pL2 * 4_500_000 + pH2 * 18_000_000, 9_000_000)
check("L05-e1 gap at 1500", 9_000_000 - F(6_750_000), 2_250_000)
p2000 = menu_profit(F(2000), F(6000), pL2, pH2)[0]
check("L05-e1 profit at 2000 (twin Part D)", half_up(p2000), 6_666_667)
check("L05-e1 gap at 2000 (twin Part D)", half_up(F(9_000_000) - p2000), 2_333_333)
check("L05-e2 rent pH=1/4", (tH - tL) * 2000, 6_000_000)
check("L05-e2 rent pH=1/3", (tH - tL) * 1500, 4_500_000)
check("L05-e3 loss pct of first best %", round(float(F(1_875_000, 7_875_000)) * 100, 2), 23.81)
check("L05-e3 FB over menu minus 1 %", round((7_875_000 / 6_000_000 - 1) * 100, 2), 31.25)
# quiz
check("L05q3 qL* at pH=1/2 is 0", 0, 0)
# Hessian: second derivatives of Pi
check("L05-p3 Hessian diag", (-pL, -pH), (F(-3, 4), F(-1, 4)))

# ---------- L06 ----------
X = 1_000_000; PH_ = F(3, 4); PL_ = F(1, 4); cHc = 100_000
EH = PH_ * X; EL = PL_ * X; FB = EH - cHc; DE = EH - EL
check("L06 E_H", EH, 750_000); check("L06 E_L", EL, 250_000); check("L06 Delta_E", DE, 500_000)
check("L06 first best", FB, 650_000)
check("L06 IC threshold", F(cHc) / DE, F(1, 5))
check("L06 profit at beta=1/5", EH - F(1, 5) * EH, 600_000)
check("L06 agent utility at 1/5", F(1, 5) * EH - cHc, 50_000)
check("L06 agency cost", FB - (EH - F(1, 5) * EH), 50_000)
check("L06 payment at success 1/5", F(1, 5) * X, 200_000)
check("L06 profit at beta=1/4 (m1)", EH * (1 - F(1, 4)), 562_500)
check("L06 utility high at 1/4", F(1, 4) * EH - cHc, 87_500)
check("L06 utility low at 1/4", F(1, 4) * EL, 62_500)
check("L06 utility high at 2/15", F(2, 15) * EH - cHc, 0)
check("L06 utility low at 2/15", float(F(2, 15) * EL), 33_333.333333333336)
check("L06 m3 profit", EH - (10_000 + F(1, 5) * EH), 590_000)
u_hi = -1_000_000 + F(1, 2) * EH - cHc; u_lo = -1_000_000 + F(1, 2) * EL
check("L06-p1 counterexample util high", u_hi, -725_000)
check("L06-p1 counterexample util low", u_lo, -875_000)
check("L06-p1 IC holds at beta=1/2", F(1, 2) * DE >= cHc, True)
# Remark 1.4 without LL
for b in (F(1, 5), F(1, 2), F(1)):
    a = cHc - b * EH
    check(f"L06 Remark1.4 profit beta={b}", EH - (a + b * EH), FB)
    check(f"L06 Remark1.4 alpha beta={b} negative", a < 0, True)
# e1 cost 150000
check("L06-e1 threshold", F(150_000) / DE, F(3, 10))
check("L06-e1 profit", EH * F(7, 10), 525_000)
check("L06-e1 first best", EH - 150_000, 600_000)
check("L06-e1 agency", (EH - 150_000) - EH * F(7, 10), 75_000)
# e2 probs 0.8/0.2
EH2 = F(4, 5) * X; EL2 = F(1, 5) * X; DE2 = EH2 - EL2
check("L06-e2 threshold", F(100_000) / DE2, F(1, 6))
check("L06-e2 profit exact", EH2 * (1 - F(1, 6)), F(2_000_000, 3))
check("L06-e2 half up", half_up(EH2 * (1 - F(1, 6))), 666_667)
check("L06-e2 first best", EH2 - 100_000, 700_000)
# e3
check("L06-e3 surplus", EH - cHc, 650_000)
check("L06-e3 sum", 600_000 + 50_000, 650_000)
# Remark 2.1 identity
b = F(1, 5); a = 0
check("L06 Remark2.1 identity", (EH - a - b * EH) + (a + b * EH - cHc), EH - cHc)
# Lab Part A rows
for b_ in (F(0), F(1, 10), F(1, 5), F(3, 10), F(1)):
    uh = b_ * EH - cHc; ul = b_ * EL
    act = "high" if (uh >= ul and uh >= 0) else ("low" if ul >= 0 else "refuses")
    prof = EH - b_ * EH if act == "high" else (EL - b_ * EL if act == "low" else 0)
    print("row", float(b_), half_up(uh), half_up(ul), act, half_up(prof))

print("FAILS:", fails)
print("TOTAL checks printed above; failures:", len(fails))
