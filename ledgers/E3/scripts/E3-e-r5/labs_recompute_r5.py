"""Independent recomputation of the numbers printed by Lab 1 (rung 1), Lab 2 (rung 2) and Lab 3 (rung 3).

Written from the definitions on project.html (CRRA: u(w)=w^(1-g)/(1-g) of final wealth; prospect: v(x)=x^(1-g) gains,
-lam(-x)^(1-g) losses; logit P(A)=1/(1+exp(-z)), z=kappa(CE_A-CE_B)/10000; cents rounded half up), not from the twins.
Standard library only. Run with: python -I -W error labs_recompute_r5.py
"""

import math
from fractions import Fraction as F

GAMMA, LAM, KAPPA, W = 0.40, 2.00, 1.50, 100_000


def half_up(x: float) -> int:
    return math.floor(x + 0.5)


def crra_ce(prizes, probs, g, w):
    m = sum(float(p) * (w + x) ** (1 - g) for x, p in zip(prizes, probs))
    return m ** (1 / (1 - g)) - w


def prospect_value(x, g, lam):
    return x ** (1 - g) if x >= 0 else -lam * (-x) ** (1 - g)


def prospect_ce(prizes, probs, g, lam):
    v = sum(float(p) * prospect_value(x, g, lam) for x, p in zip(prizes, probs))
    return v ** (1 / (1 - g)) if v >= 0 else -((-v / lam) ** (1 / (1 - g)))


def logit_pa(ca, cb, k):
    z = k * (ca - cb) / 10000.0
    return 1 / (1 + math.exp(-z))


print("== Lab 1 recomputation ==")
pairs = [
    ([2000, -1000], [F(1, 2), F(1, 2)], [500], [F(1)], "A"),
    ([3000], [F(1)], [4000, -2000], [F(1, 4), F(3, 4)], "B"),
    ([1500, 2500], [F(1, 3), F(2, 3)], [-500, 3000], [F(1, 2), F(1, 2)], "A"),
]
total = 0.0
for i, (pa, qa, pb, qb, ch) in enumerate(pairs, 1):
    crra_a, crra_b = half_up(crra_ce(pa, qa, GAMMA, W)), half_up(crra_ce(pb, qb, GAMMA, W))
    ce_a, ce_b = prospect_ce(pa, qa, GAMMA, LAM), prospect_ce(pb, qb, GAMMA, LAM)
    pa_ = logit_pa(ce_a, ce_b, KAPPA)
    lp = math.log(pa_ if ch == "A" else 1 - pa_)
    total += lp
    print(f"pair {i}: CRRA cents A,B {crra_a} {crra_b} | prospect cents A,B {half_up(ce_a)} {half_up(ce_b)} | "
          f"P(A) {pa_:.6f} | log P(chosen) {lp:.6f} | unrounded CE_A {ce_a:.4f} CE_B {ce_b:.4f} CRRA_A {crra_ce(pa,qa,GAMMA,W):.4f} CRRA_B {crra_ce(pb,qb,GAMMA,W):.4f}")
print(f"total {total:.6f}")

print("== Lab 1 pair 2 claims ==")
print("sure 3000 CE under CRRA (unrounded):", f"{crra_ce([3000],[F(1)],GAMMA,W):.6f}",
      "prospect:", f"{prospect_ce([3000],[F(1)],GAMMA,LAM):.6f}")
print("lottery 4000/1/4 -2000/3/4 prospect value:", f"{sum(float(p)*prospect_value(x,GAMMA,LAM) for x,p in zip([4000,-2000],[F(1,4),F(3,4)])):.6f}")

print("== Lab 2 recomputation ==")
z = 2.0 * (1500.0 - 2200.0) / 10000.0
print(f"z = {z}")
print(f"log P(A) = {-math.log1p(math.exp(-z)):.9f}  log P(B) = {-math.log1p(math.exp(z)):.9f}")
print(f"P(A) {1/(1+math.exp(-z)):.9f}  P(B) {1/(1+math.exp(z)):.9f}  sum {1/(1+math.exp(-z)) + 1/(1+math.exp(z)):.15f}")

print("== Lab 3 recomputation (independent of twin: own grid + own Newton; checks the printed estimates) ==")
ANS = [
    (0, "B", [6200, -15100], ["9/10", "1/10"], [3300, -3000, -700], ["1/20", "7/20", "3/5"]),
    (1, "B", [-9400, -10100, 19000], ["2/5", "3/10", "3/10"], [-12200, 17000, -1100], ["1/2", "1/4", "1/4"]),
    (2, "A", [10700, -3400, -13400], ["7/10", "1/10", "1/5"], [-14900, -13600, 15200], ["9/20", "2/5", "3/20"]),
    (3, "A", [18800, -12500], ["3/4", "1/4"], [16500, -17700], ["2/5", "3/5"]),
    (4, "B", [-10700, -5600, -7300], ["1/2", "2/5", "1/10"], [-13800, -9700], ["1/4", "3/4"]),
    (5, "B", [-11600, 7900, -12200], ["3/4", "1/10", "3/20"], [-12000, 11300], ["17/20", "3/20"]),
    (6, "A", [-9900, 5400, -4200], ["1/2", "1/4", "1/4"], [-15300, 16100, 6800], ["1/4", "1/2", "1/4"]),
    (7, "A", [600, -17500], ["3/5", "2/5"], [15800, -2600, -17600], ["2/5", "2/5", "1/5"]),
    (8, "B", [-10400, 13800], ["9/10", "1/10"], [10400, 1800], ["1/20", "19/20"]),
    (9, "B", [-17900, -12000, -3600], ["1/4", "1/4", "1/2"], [15600, 11600, -12200], ["3/10", "13/20", "1/20"]),
    (10, "B", [17000, 1600], ["1/10", "9/10"], [-18700, 3800], ["7/20", "13/20"]),
    (11, "B", [10400, -11300], ["2/5", "3/5"], [9300, 7200, -13200], ["1/2", "1/4", "1/4"]),
]


def pv(x, g, lam):
    return x ** (1 - g) if x >= 0 else -lam * (-x) ** (1 - g)


def pce(prizes, probs, g, lam):
    v = sum(float(F(p)) * pv(x, g, lam) for x, p in zip(prizes, probs))
    return v ** (1 / (1 - g)) if v >= 0 else -((-v / lam) ** (1 / (1 - g)))


def ll(g, lam, k):
    s = 0.0
    for _, c, pa, qa, pb, qb in ANS:
        z = k * (pce(pa, qa, g, lam) - pce(pb, qb, g, lam)) / 10000.0
        s += -math.log1p(math.exp(-z)) if c == "A" else -math.log1p(math.exp(z))
    return s


# grid over gamma in (0,1), lambda>0, kappa>0 in the same log scale, then Newton-free refinement by shrinking grid
best = None
for gi in range(1, 200):
    g = gi / 200
    for li in range(-40, 81):
        lam = math.exp(li / 20)
        for ki in range(-40, 61):
            k = math.exp(ki / 20)
            v = ll(g, lam, k)
            if best is None or v > best[0]:
                best = (v, g, lam, k)
v, g, lam, k = best
step = [1 / 200, 0.05, 0.05]
for _ in range(60):
    improved = False
    for dg in (-1, 0, 1):
        for dl in (-1, 0, 1):
            for dk in (-1, 0, 1):
                if dg == dl == dk == 0:
                    continue
                g2 = min(max(g + dg * step[0], 1e-6), 1 - 1e-6)
                l2 = lam * math.exp(dl * step[1])
                k2 = k * math.exp(dk * step[2])
                v2 = ll(g2, l2, k2)
                if v2 > v:
                    v, g, lam, k = v2, g2, l2, k2
                    improved = True
    if not improved:
        step = [s / 2 for s in step]
        if step[1] < 1e-9:
            break
print(f"coordinate-search estimate: gamma {g:.4f} lambda {lam:.4f} kappa {k:.4f} loglik {v:.4f}")
print("answers:", len(ANS), "mixed:", sum(1 for a in ANS if any(x > 0 for x in a[2]) and any(x < 0 for x in a[2]) or
      any(x > 0 for x in a[4]) and any(x < 0 for x in a[4])))
