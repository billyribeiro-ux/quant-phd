"""Independent recomputation (own formulas, stdlib only) of the project page's prose numbers.

Run: .venv/bin/python -I ledgers/E3/scripts/E3-d-r4/recompute_numbers.py
"""
import math
from fractions import Fraction as F

G, L, K = 0.40, 2.00, 1.50

def crra_ce(prizes, probs, g, w=100_000):
    e = sum(float(p) * ((w + x) ** (1 - g)) / (1 - g) for x, p in zip(prizes, probs))
    # invert u(W) = W^(1-g)/(1-g)
    v = e * (1 - g)
    return v ** (1 / (1 - g)) - w

def v(x, g, l):
    return x ** (1 - g) if x >= 0 else -l * (-x) ** (1 - g)

def pros_ce(prizes, probs, g, l):
    tot = sum(float(p) * v(x, g, l) for x, p in zip(prizes, probs))
    return tot ** (1 / (1 - g)) if tot >= 0 else -((-tot / l) ** (1 / (1 - g)))

def floor_half(c):
    return math.floor(c + 0.5)

def pa(ca, cb, k):
    return 1 / (1 + math.exp(-k * (ca - cb) / 10000))

# Lab 1 pairs
pairs = [
    ([2000, -1000], [F(1, 2), F(1, 2)], [500], [F(1)], "A"),
    ([3000], [F(1)], [4000, -2000], [F(1, 4), F(3, 4)], "B"),
    ([1500, 2500], [F(1, 3), F(2, 3)], [-500, 3000], [F(1, 2), F(1, 2)], "A"),
]
tot = 0
for i, (pa_, qa, pb, qb, ch) in enumerate(pairs, 1):
    ca_c, cb_c = floor_half(crra_ce(pa_, qa, G)), floor_half(crra_ce(pb, qb, G))
    ca_p, cb_p = pros_ce(pa_, qa, G, L), pros_ce(pb, qb, G, L)
    p = pa(ca_p, cb_p, K)
    lp = math.log(p if ch == "A" else 1 - p)
    tot += lp
    print(f"pair {i} CRRA {ca_c} {cb_c} | prospect {floor_half(ca_p)} {floor_half(cb_p)} | P(A) {p:.6f} | log {lp:.6f}")
print(f"total {tot:.6f}")
print("pair2 prospect CE of -20 w.p.3/4, +40 w.p.1/4 :", round(pros_ce([4000, -2000], [F(1, 4), F(3, 4)], G, L), 3))

# Lab 2: CE_A=1500, CE_B=2200, kappa=2
z = 2 * (1500 - 2200) / 10000
print("Lab2 z =", z, "logPA =", -math.log1p(math.exp(-z)), "logPB =", -math.log1p(math.exp(z)), "P(A)=", 1 / (1 + math.exp(-z)))

# Lab 3 pair data & mixed count & prize range from the page's ANSWERS block
import re
page = open("course/modules/E/E3/project.html", encoding="utf-8").read()
m = re.search(r'ANSWERS: list\[.*?\] = \[(.*?)\n\]', page, re.S)
ans = eval("[" + m.group(1) + "]")
mixed = 0
prizes = []
for pid, ch, pa_, qa, pb, qb in ans:
    def has_mix(ps, qs):
        g_ = any(x > 0 and F(q) > 0 for x, q in zip(ps, qs))
        l_ = any(x < 0 and F(q) > 0 for x, q in zip(ps, qs))
        return g_ and l_
    mixed += has_mix(pa_, qa) or has_mix(pb, qb)
    prizes += pa_ + pb
    sums = [sum(F(q) for q in qa), sum(F(q) for q in qb)]
    assert sums == [1, 1], (pid, sums)
print("answers", len(ans), "mixed", mixed, "prize range", min(prizes), max(prizes))
print("pair ids", [a[0] for a in ans], "non-mixed ids", [a[0] for a in ans if not (lambda a: ((lambda ps,qs: any(x>0 and F(q)>0 for x,q in zip(ps,qs)) and any(x<0 and F(q)>0 for x,q in zip(ps,qs)))(a[2],a[3]) or (lambda ps,qs: any(x>0 and F(q)>0 for x,q in zip(ps,qs)) and any(x<0 and F(q)>0 for x,q in zip(ps,qs)))(a[4],a[5])))(a)])
