"""E2 slice b verifier script: independent exact recomputation of the L04-L06 numbers and of the page's variant claims.

Usage: <checkout>/.venv/bin/python -I <checkout>/ledgers/E2/scripts/E2-b-r1/recompute_slice_b.py
Pure Fractions; no code from the lessons or twins is imported.
"""

from __future__ import annotations

from fractions import Fraction as F

print("== L04 Proposition 1.3 base case, by brute force over whole years 0..8")
yL, yH, cL, cH = 4_000_000, 6_000_000, 1_000_000, 500_000


def w(e: int, t: int, yL: int = 4_000_000, yH: int = 6_000_000) -> int:
    return yH if e >= t else yL


def sep_thresholds(yL: int, yH: int, cL: int, cH: int, grid: range) -> list[int]:
    out = []
    for t in grid:
        if t < 1:
            continue
        ic_h = (w(t, t, yL, yH) - cH * t) >= max(w(e, t, yL, yH) - cH * e for e in grid)
        ic_l = (w(0, t, yL, yH) - 0) >= max(w(e, t, yL, yH) - cL * e for e in grid)
        if ic_h and ic_l:
            out.append(t)
    return out


print("base, 0..8:", sep_thresholds(yL, yH, cL, cH, range(0, 9)), "closed form", F(yH - yL, cL), F(yH - yL, cH))
print("variant cH=400000:", sep_thresholds(yL, yH, cL, 400_000, range(0, 9)),
      "closed form", F(yH - yL, cL), F(yH - yL, 400_000))
print("variant yH=5000000:", sep_thresholds(yL, 5_000_000, cL, cH, range(0, 9)),
      "closed form", F(5_000_000 - yL, cL), F(5_000_000 - yL, cH))
print("m1 variant cH=250000:", sep_thresholds(yL, yH, cL, 250_000, range(0, 12)))
print("m3 Delta=1.5M cL=1M cH=0.5M:", sep_thresholds(4_000_000, 5_500_000, cL, cH, range(0, 9)))
print("Remark 2.1 net utility t=2:", yH - cH * 2, " t=4:", yH - cH * 4, " cost t=2:", cH * 2)
print("L04 misconception t=1 low type utility e=1 vs e=0:", yH - cL * 1, yL)
print("L04-e3 utilities t=2,3,4:", [yH - cH * t for t in (2, 3, 4)])
print("Q6 utility at t=1, e=1 (page says 5,000,000):", w(1, 1) - cL * 1)

print("== L05 Proposition 1.4 base case")
tL, tH = F(3000), F(6000)
pL, pH = F(3, 4), F(1, 4)


def C(q: F) -> F:
    return q * q / 2


def menu_profit(qL: F, qH: F, pL: F = pL, pH: F = pH) -> F:
    TL = tL * qL
    TH = tH * qH - (tH - tL) * qL
    return pL * (TL - C(qL)) + pH * (TH - C(qH))


print("profit(2000,6000) =", menu_profit(F(2000), F(6000)), "first best =", pL * (tL * tL - C(tL)) + pH * (tH * tH - C(tH)))
# brute force over real-valued grid including negative quantities, with q_H in a grid
best = None
for qL10 in range(-20000, 20001, 10):  # quantities in steps of 0.1 unit between -2000 and 2000
    qL = F(qL10, 10)
    for qH in (F(k, 1) for k in range(0, 12001, 100)):
        val = menu_profit(qL, qH)
        if best is None or val > best[0]:
            best = (val, qL, qH)
print("brute force over qL in [-2000,2000] (step .1), qH in [0,12000] (step 100): best", best)

print("== L05 variant e1: p_H=1/3, p_L=2/3, q_L fixed at 2000 (as the twin's Part D does)")
pl2, ph2 = F(2, 3), F(1, 3)
print("menu profit at q_L=2000:", float(menu_profit(F(2000), F(6000), pl2, ph2)), "exact")
print("best q_L on 0..6000 grid with q_H=6000:",
      max(range(0, 6001), key=lambda q: (menu_profit(F(q), F(6000), pl2, ph2), -q)))
print("menu profit at q_L=1500 (best under variant):", menu_profit(F(1500), F(6000), pl2, ph2))
print("first best under variant:", pl2 * (tL * tL - C(tL)) + ph2 * (tH * tH - C(tH)))
print("gap if first best minus menu at 2000:", float(pl2 * (tL * tL - C(tL)) + ph2 * (tH * tH - C(tH)) - menu_profit(F(2000), F(6000), pl2, ph2)))
print("gap if first best minus best menu at 1500:", float(pl2 * (tL * tL - C(tL)) + ph2 * (tH * tH - C(tH)) - menu_profit(F(1500), F(6000), pl2, ph2)))

print("== L05 Remark 2.1 decomposition of the 1,875,000 gap (base case)")
fb_low = pL * (tL * tL - C(tL))
fb_high = pH * (tH * tH - C(tH))
m_low = pL * (tL * F(2000) - C(F(2000)))
m_high = pH * (tH * tH - (tH - tL) * F(2000) - C(tH))
print("low-type contribution: first best", fb_low, "menu", m_low, "diff", fb_low - m_low)
print("high-type contribution: first best", fb_high, "menu", m_high, "diff", fb_high - m_high)
print("p_H * rent =", pH * (tH - tL) * F(2000))

print("== L05 m1 (p_H=1/2): q_L*, profit at (0, 6000)")
print(tL - (F(1, 2) / F(1, 2)) * (tH - tL), F(1, 2) * (F(36_000_000) - C(F(6000))))
print("== L05 m3 profit at (1000, 6000)", menu_profit(F(1000), F(6000)))
print("== L05 e3 percent bases", float(F(1_875_000, 7_875_000)) * 100, float(F(7_875_000, 6_000_000) - 1) * 100)
print("== L05 e2 rents", 3000 * 2000, 3000 * (tL - tL * 0 - (tL - tL) * 0) * 0 + 3000 * 1500)

print("== L06 contracts, alpha=0")
XB, EH, EL = 1_000_000 * F(1), F(3, 4) * 1_000_000, F(1, 4) * 1_000_000
cH_, cL_ = 100_000, 0


def agent(beta: F, alpha: F) -> tuple[str, F, F]:
    uH = alpha + beta * EH - cH_
    uL = alpha + beta * EL - cL_
    if uH >= uL and uH >= 0:
        return "high", uH, uL
    if uL >= 0:
        return "low", uH, uL
    return "refuses", uH, uL


def prof(beta: F, alpha: F) -> F:
    a, _, _ = agent(beta, alpha)
    if a == "high":
        return EH - alpha - beta * EH
    if a == "low":
        return EL - alpha - beta * EL
    return F(0)


grid = [F(k, 100) for k in range(101)]
bestb = max(grid, key=lambda b: (prof(b, F(0)), -b))
print("best grid share alpha=0:", bestb, prof(bestb, F(0)), agent(bestb, F(0)))
print("P1 counterexample alpha=-1,000,000 beta=1/2:", agent(F(1, 2), F(-1_000_000)))
print("P1 counterexample alpha=-1,000,000 beta=1/2 high-effort IC holds:",
      (F(1, 2) * (EH - EL) >= cH_), "participation holds:", (F(-1_000_000) + F(1, 2) * EH - cH_ >= 0))
print("Part C profits:", [(str(b), prof(b, cH_ - b * EH)) for b in (F(1, 5), F(1, 2), F(1))])
print("e1 variant cH=150000: threshold", F(150_000, 500_000), "profit at 0.3", prof(F(3, 10), F(0)), "first best", EH - 150_000)
print("e2 variant: EH", F(8, 10) * 1_000_000, "EL", F(2, 10) * 1_000_000, "threshold", F(100_000, 600_000),
      "profit", F(800_000) * F(5, 6), "first best", F(800_000) - 100_000)
print("m1 beta=1/4:", F(1, 4) * EH - cH_, F(1, 4) * EL, EH * (1 - F(1, 4)))
print("m2 beta=2/15:", F(2, 15) * EH - cH_, float(F(2, 15) * EL))
print("m3 alpha=10000 beta=1/5 profit:", EH - (10_000 + F(1, 5) * EH))
print("Remark 2.1 identity:", (EH - (EH - 0)) + 0, "surplus", EH - cH_, "profit+rent", F(600_000) + F(50_000))
