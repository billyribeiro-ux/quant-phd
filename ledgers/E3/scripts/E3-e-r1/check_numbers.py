"""Independent recomputation of the project page's numbers (E3 slice e, round 1)."""
import math
import re
import sys
from fractions import Fraction
from html.parser import HTMLParser

PAGE = sys.argv[1]

sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD1-E3-e/ledgers/E3/scripts/E3-e-r1")

# ---- Rung 1/2 numbers (own implementation)
GAMMA, LAM, KAPPA, WEALTH = 0.40, 2.00, 1.50, 100_000


def nearest_cent(a):
    return math.floor(a + 0.5)


def crra_ce(prizes, probs, g, w):
    finals = [w + x for x in prizes]
    e = sum(float(p) * w_ ** (1.0 - g) for p, w_ in zip(probs, finals))
    return e ** (1.0 / (1.0 - g)) - w


def v(x, g, lam):
    return x ** (1 - g) if x >= 0 else -lam * (-x) ** (1 - g)


def pce(prizes, probs, g, lam):
    t = sum(float(p) * v(x, g, lam) for x, p in zip(prizes, probs))
    return t ** (1 / (1 - g)) if t >= 0 else -((-t / lam) ** (1 / (1 - g)))


pairs = [
    ([2000, -1000], [Fraction(1, 2), Fraction(1, 2)], [500], [Fraction(1)], "A"),
    ([3000], [Fraction(1)], [4000, -2000], [Fraction(1, 4), Fraction(3, 4)], "B"),
    ([1500, 2500], [Fraction(1, 3), Fraction(2, 3)], [-500, 3000], [Fraction(1, 2), Fraction(1, 2)], "A"),
]
tot = 0.0
for i, (pa, qa, pb, qb, ch) in enumerate(pairs, 1):
    print("pair", i, "CRRA", nearest_cent(crra_ce(pa, qa, GAMMA, WEALTH)), nearest_cent(crra_ce(pb, qb, GAMMA, WEALTH)),
          "PROSP", nearest_cent(pce(pa, qa, GAMMA, LAM)), nearest_cent(pce(pb, qb, GAMMA, LAM)),
          "unrounded", round(pce(pa, qa, GAMMA, LAM), 4), round(pce(pb, qb, GAMMA, LAM), 4))
    ca, cb = pce(pa, qa, GAMMA, LAM), pce(pb, qb, GAMMA, LAM)
    p = 1 / (1 + math.exp(-KAPPA * (ca - cb) / 10000))
    pc = p if ch == "A" else 1 - p
    tot += math.log(pc)
    print("  P(A)=%.6f logP(chosen)=%.6f" % (p, math.log(pc)))
print("total %.6f" % tot)

# Lab 2 numbers
z = 2.0 * (1500 - 2200) / 10000
print("lab2 A %.9f B %.9f" % (-math.log1p(math.exp(-z)), -math.log1p(math.exp(z))))

# ---- ANSWERS prize range and mixed count
src = open(PAGE, encoding="utf-8").read()
block = src.split("ANSWERS: list")[1].split("]\n\n\ndef value")[0]
rows = re.findall(r"\((\d+), \"([AB])\", (\[[^\]]*\]), (\[[^\]]*\]), (\[[^\]]*\]), (\[[^\]]*\])\)", block)
print("rows", len(rows))
prizes_all = []
mixed = 0
for r in rows:
    pa, qa, pb, qb = (eval(r[2]), eval(r[3]), eval(r[4]), eval(r[5]))
    prizes_all += pa + pb
    def is_mixed(pr, pq):
        qs = [Fraction(q) for q in pq]
        return any(x > 0 and q > 0 for x, q in zip(pr, qs)) and any(x < 0 and q > 0 for x, q in zip(pr, qs))
    mixed += int(is_mixed(pa, qa) or is_mixed(pb, qb))
    for pr, pq in ((pa, qa), (pb, qb)):
        assert sum(Fraction(q) for q in pq) == 1, r[0]
print("prize min", min(prizes_all), "max", max(prizes_all), "mixed pairs", mixed)
