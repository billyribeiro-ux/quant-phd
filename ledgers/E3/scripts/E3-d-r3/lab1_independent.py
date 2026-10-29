"""Independent re-derivation (round 3) of the Rung-1 worked-example numbers quoted on project.html (Lab 1 hypothesis and
interpretation) and of the Lab 2 completion numbers, using mpmath-free float arithmetic written from the page's formulas.
Usage: .venv/bin/python -I ledgers/E3/scripts/E3-d-r3/lab1_independent.py
"""
import math

G, LAM, K, W = 0.40, 2.00, 1.50, 100_000


def crra_ce(prizes, probs):
    e = sum(p * (W + x) ** (1 - G) for x, p in zip(prizes, probs))
    return e ** (1 / (1 - G)) - W


def v(x):
    return x ** (1 - G) if x >= 0 else -LAM * (-x) ** (1 - G)


def pros_ce(prizes, probs):
    total = sum(p * v(x) for x, p in zip(prizes, probs))
    return total ** (1 / (1 - G)) if total >= 0 else -((-total / LAM) ** (1 / (1 - G)))


def half_up(y):
    return math.floor(y + 0.5)


pairs = [
    ([2000, -1000], [0.5, 0.5], [500], [1.0], "A"),
    ([3000], [1.0], [4000, -2000], [0.25, 0.75], "B"),
    ([1500, 2500], [1 / 3, 2 / 3], [-500, 3000], [0.5, 0.5], "A"),
]
ll = 0.0
for pa, qa, pb, qb, ch in pairs:
    ca, cb = pros_ce(pa, qa), pros_ce(pb, qb)
    pA = 1 / (1 + math.exp(-K * (ca - cb) / 10_000))
    lp = math.log(pA if ch == "A" else 1 - pA)
    ll += lp
    print("CRRA", half_up(crra_ce(pa, qa)), half_up(crra_ce(pb, qb)), "| prospect", half_up(ca), half_up(cb),
          "| P(A) %.6f" % pA, "| logP %.6f" % lp)
print("total %.6f" % ll)
# Lab 2: CE_A = 1500, CE_B = 2200, kappa = 2
z = 2 * (1500 - 2200) / 10_000
print("Lab2 logP(A) %.9f logP(B) %.9f" % (-math.log1p(math.exp(-z)), -math.log1p(math.exp(z))))
