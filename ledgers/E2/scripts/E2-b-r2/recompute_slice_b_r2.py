"""Independent recomputation for E2 slice b (L04-L06), round 2. Exact Fractions only; run with python -I."""
import difflib
import json
from fractions import Fraction as F

ok = []

def check(name, value, expected):
    assert value == expected, (name, value, expected)
    ok.append(f"{name} = {value}")

# ---- L04: base case
YL, YH, CL, CH = 4_000_000, 6_000_000, 1_000_000, 500_000
D = YH - YL
check("L04 Delta", D, 2_000_000)
check("L04 lower bound", F(D, CL), 2)
check("L04 upper bound", F(D, CH), 4)
def wage(e, t): return YH if e >= t else YL
def util(c, e, t): return wage(e, t) - c * e
sep = []
for t in range(0, 7):
    uh = util(CH, t, t); bh = max(util(CH, e, t) for e in range(7))
    ul = util(CL, 0, t); bl = max(util(CL, e, t) for e in range(7))
    if t >= 1 and uh == bh and ul == bl:
        sep.append(t)
check("L04 enumerated separating thresholds", sep, [2, 3, 4])
check("L04 high net utility at t=2", util(CH, 2, 2), 5_000_000)
check("L04 high net utility at t=4", util(CH, 4, 4), 4_000_000)
check("L04 low utility at e=1 under t=1", util(CL, 1, 1), 5_000_000)
# problem variants
check("L04 m1 upper bound (c_H=250000)", F(D, 250_000), 8)
check("L04 p1 bounds (Delta=1.5M)", (F(1_500_000, CL), F(1_500_000, CH)), (F(3, 2), 3))
check("L04 e1 upper bound (c_H=400000)", F(D, 400_000), 5)
check("L04 e2 bounds (y_H=5M)", (F(1_000_000, CL), F(1_000_000, CH)), (1, 2))

# ---- L05: base case (theta in cents per unit, q in units, C(q)=q^2/2)
TL, TH, PL, PH = 3000, 6000, F(3, 4), F(1, 4)
C = lambda q: F(q) * F(q) / 2
qL = TL - PH / PL * (TH - TL)
check("L05 q_L*", qL, 2000)
mL = TL * qL; mH = TH * TH - (TH - TL) * qL
check("L05 m_L", mL, 6_000_000); check("L05 m_H", mH, 30_000_000)
check("L05 U_H", mH and (TH * TH - mH), 6_000_000)
def profit(ql, qh, pl=PL, ph=PH):
    m_l = TL * ql; m_h = TH * qh - (TH - TL) * ql
    return pl * (m_l - C(ql)) + ph * (m_h - C(qh))
check("L05 menu profit", profit(F(2000), F(6000)), 6_000_000)
fb = PL * (TL * 3000 - C(3000)) + PH * (TH * 6000 - C(6000))
check("L05 first best", fb, 7_875_000)
check("L05 gap", fb - profit(F(2000), F(6000)), 1_875_000)
check("L05 gap, low-type surplus part PL*(4.5M-4.0M)", PL * ((TL*3000 - C(3000)) - (TL*2000 - C(2000))), F(375_000))
check("L05 gap, high rent part PH*6M", PH * 6_000_000, 1_500_000)
# grid search over the low quantity with q_H = 6000 (exact fractions), and the reduced problem
best_q = max(range(0, 6001), key=lambda q: (profit(F(q), F(6000)), -q))
check("L05 grid argmax of low quantity (q_H=6000)", best_q, 2000)
# brute search over a wider two-dimensional grid (0..4000 step 100 for q_L, 0..8000 step 500 for q_H): optimum must be (2000, 6000)
cands = [(profit(F(a), F(b)), a, b) for a in range(0, 4001, 100) for b in range(0, 8001, 500)]
bp = max(cands)
check("L05 2D grid optimum (q_L, q_H)", (bp[1], bp[2]), (2000, 6000))
# percents
check("L05 loss as % of first best (display 23.81)", round(float(F(1_875_000, 7_875_000) * 100), 2), 23.81)
check("L05 first best over menu, % (display 31.25)", float(F(7_875_000, 6_000_000) - 1) * 100, 31.25)
# p_H = 1/3 variant: q_L* = 1500, profit at 1500 with q_H=6000 is 6,750,000; menu at 2000 is 6,666,666.67 -> 6666667
pl3, ph3 = F(2, 3), F(1, 3)
check("L05 variant q_L*", TL - ph3 / pl3 * (TH - TL), 1500)
check("L05 variant profit at 1500", profit(F(1500), F(6000), pl3, ph3), 6_750_000)
check("L05 variant profit at 2000 (exact)", profit(F(2000), F(6000), pl3, ph3), F(20_000_000, 3))
fb3 = pl3 * (TL * 3000 - C(3000)) + ph3 * (TH * 6000 - C(6000))
check("L05 variant first best", fb3, 9_000_000)
check("L05 variant gap at 2000 (exact)", fb3 - profit(F(2000), F(6000), pl3, ph3), F(7_000_000, 3))
check("L05 variant gap at 1500", fb3 - profit(F(1500), F(6000), pl3, ph3), 2_250_000)
# Remark 2.1 / problem m2, m3
check("L05 m2 U_H", TH * 6000 - (TH * 6000 - (TH - TL) * 1000), 3_000_000)
check("L05 m2 IC-L slack side", TL * 6000 - (TH * 6000 - (TH - TL) * 1000), -15_000_000)
check("L05 m3 profit", F(3, 4) * (3_000_000 - C(1000)) + F(1, 4) * (33_000_000 - C(6000)), 5_625_000)
check("L05 m1 q_L* at p_H=1/2", TL - F(1, 2) / F(1, 2) * (TH - TL), 0)
check("L05 m1 profit", F(1, 2) * (36_000_000 - 18_000_000), 9_000_000)
# Research r1 counterexample: participation holds, q_L > 0, IC-H violated, high-type rent zero
menu = dict(qL=F(1000), mL=F(0), qH=F(0), mH=F(0))
UL = TL * menu["qL"] - menu["mL"]; UH = TH * menu["qH"] - menu["mH"]
ic_h = UH >= TH * menu["qL"] - menu["mL"]
check("L05 r1 counterexample: U_L>=0", UL >= 0, True)
check("L05 r1 counterexample: U_H = 0 with q_L>0", (UH, menu["qL"] > 0), (0, True))
check("L05 r1 counterexample: IC-H fails", ic_h, False)

# ---- L06
X = 1_000_000; PHS, PLS = F(3, 4), F(1, 4); cH = 100_000
EH, EL = PHS * X, PLS * X
check("L06 E_H", EH, 750_000); check("L06 E_L", EL, 250_000)
check("L06 first best", EH - cH, 650_000)
def prof(beta):
    uh = beta * EH - cH; ul = beta * EL
    if uh >= ul and uh >= 0: return EH - beta * EH
    if ul >= 0: return EL - beta * EL
    return F(0)
grid = [F(k, 100) for k in range(101)]
bb = max(grid, key=lambda b: (prof(b), -b))
check("L06 best grid share", bb, F(1, 5)); check("L06 best profit", prof(bb), 600_000)
check("L06 profit at 0.30", prof(F(3, 10)), 525_000)
check("L06 agency cost", (EH - cH) - prof(bb), 50_000)
check("L06 identity: profit + agent utility = E_H - c_H at 1/5", prof(F(1, 5)) + (F(1, 5) * EH - cH), 650_000)
check("L06 m1 utilities", (F(1, 4) * EH - cH, F(1, 4) * EL), (87_500, 62_500))
check("L06 m1 profit", EH * (1 - F(1, 4)), 562_500)
check("L06 m2 high utility at 2/15", F(2, 15) * EH - cH, 0)
check("L06 m3 profit", EH - (10_000 + F(1, 5) * EH), 590_000)
check("L06 p1 witness utilities", (-1_000_000 + F(1, 2) * EH - cH, -1_000_000 + F(1, 2) * EL), (-725_000, -875_000))
check("L06 p1 IC holds at 1/2", F(1, 2) * (EH - EL) >= cH, True)
check("L06 e1 threshold and profit (c_H=150000)", (F(150_000, 500_000), EH * (1 - F(3, 10))), (F(3, 10), 525_000))
check("L06 e1 first best", EH - 150_000, 600_000)
E2H, E2L = F(800_000), F(200_000)
check("L06 e2 threshold", F(100_000, E2H - E2L), F(1, 6))
check("L06 e2 profit", E2H * (1 - F(1, 6)), F(2_000_000, 3))
check("L06 e2 first best", E2H - cH, 700_000)
# Remark 1.4: alpha = c_H - beta E_H, participation binds, profit = first best for beta >= 1/5
for b in (F(1, 5), F(1, 2), F(1)):
    a = cH - b * EH
    check(f"L06 remark 1.4 profit at beta={b}", EH - (a + b * EH), 650_000)

# ---- card duplicate scan (fronts and backs), difflib ratio
cards = json.load(open("course/modules/E/E2/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
assert len(ids) == len(set(ids))
pairs_front = []; pairs_back = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        rf = difflib.SequenceMatcher(None, cards[i]["front"], cards[j]["front"]).ratio()
        rb = difflib.SequenceMatcher(None, cards[i]["back"], cards[j]["back"]).ratio()
        if rf > 0.8: pairs_front.append((cards[i]["id"], cards[j]["id"], round(rf, 3)))
        if rb > 0.9: pairs_back.append((cards[i]["id"], cards[j]["id"], round(rb, 3)))
print("\n".join(ok))
print("card ids unique:", len(ids), "unique:", len(set(ids)))
print("front pairs >0.8 (all cards of unit):", pairs_front)
print("back pairs >0.9 (all cards of unit):", pairs_back)
