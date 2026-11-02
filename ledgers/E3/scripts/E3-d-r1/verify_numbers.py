"""Independent re-derivation of the numbers printed on project.html (E3-d round 1)."""
import math, re, sys
from decimal import Decimal, getcontext
from fractions import Fraction
getcontext().prec = 50
# Lab 1: parameters and pairs as on the page
G, L, K, W = Decimal("0.40"), Decimal("2.00"), Decimal("1.50"), 100000
def dpow(x, e):
    return (x.ln() * e).exp()
def v(x):
    x = Decimal(x)
    if x >= 0:
        return dpow(x, 1 - G)
    return -L * dpow(-x, 1 - G)
def pce(prizes, probs):
    tot = sum(Decimal(p.numerator) / Decimal(p.denominator) * v(x) for x, p in zip(prizes, probs))
    if tot >= 0:
        return dpow(tot, 1 / (1 - G))
    return -dpow(-tot / L, 1 / (1 - G))
def crra(prizes, probs):
    e = sum(Decimal(p.numerator) / Decimal(p.denominator) * dpow(Decimal(W + x), 1 - G) for x, p in zip(prizes, probs))
    return dpow(e, 1 / (1 - G)) - W
def half_up(d):
    return int((d + Decimal("0.5")).to_integral_value(rounding="ROUND_FLOOR"))
pairs = [
    ([2000, -1000], [Fraction(1, 2), Fraction(1, 2)], [500], [Fraction(1)], "A"),
    ([3000], [Fraction(1)], [4000, -2000], [Fraction(1, 4), Fraction(3, 4)], "B"),
    ([1500, 2500], [Fraction(1, 3), Fraction(2, 3)], [-500, 3000], [Fraction(1, 2), Fraction(1, 2)], "A"),
]
ll = Decimal(0)
for i, (pa, qa, pb, qb, ch) in enumerate(pairs, 1):
    ca, cb = pce(pa, qa), pce(pb, qb)
    print(f"pair {i} exact prospect CE A={ca:.6f} B={cb:.6f} | CRRA A={crra(pa,qa):.6f} B={crra(pb,qb):.6f}")
    print(f"  distance to half-cent: prospect A {abs((ca - ca.to_integral_value(rounding='ROUND_FLOOR')) - Decimal('0.5')):.3e}")
    z = K * (ca - cb) / Decimal(10000)
    pA = 1 / (1 + (-z).exp())
    pch = pA if ch == "A" else 1 - pA
    ll += pch.ln()
    print(f"  P(A)={pA:.9f} log P(chosen)={pch.ln():.9f}")
print("Lab1 total log-likelihood", f"{ll:.9f}")
# Lab 2 exact
z = Decimal(2) * (Decimal(1500) - Decimal(2200)) / Decimal(10000)
print("Lab2 z", z, "logA", -(1 + (-z).exp()).ln(), "logB", -(1 + z.exp()).ln())
# Lab 3 prize range and mixed count over ANSWERS in the page
src = open("course/modules/E/E3/project.html", encoding="utf-8").read()
blk = src[src.index("ANSWERS: list"):src.index("\n]\n", src.index("ANSWERS: list"))]
rows = re.findall(r"\((\d+), \"([AB])\", \[([^\]]*)\], \[([^\]]*)\], \[([^\]]*)\], \[([^\]]*)\]\)", blk)
prizes = []
mixed = 0
for pid, ch, a, qa, b, qb in rows:
    pa = [int(x) for x in a.split(",")]; pb = [int(x) for x in b.split(",")]
    prizes += pa + pb
    def mx(p, q):
        ps = [Fraction(s.strip().strip('"')) for s in q.split(",")]
        return any(x > 0 and pr > 0 for x, pr in zip(p, ps)) and any(x < 0 and pr > 0 for x, pr in zip(p, ps))
    qa_l = [s for s in qa.split(",")]
    qb_l = [s for s in qb.split(",")]
    mixed += int(mx(pa, qa) or mx(pb, qb))
print("answers", len(rows), "mixed", mixed, "prize min", min(prizes), "prize max", max(prizes))
# Probabilities sum to 1 in every answer
bad = 0
for pid, ch, a, qa, b, qb in rows:
    for q in (qa, qb):
        s = sum(Fraction(t.strip().strip('"')) for t in q.split(","))
        bad += (s != 1)
print("answers with a lottery not summing to 1:", bad)
