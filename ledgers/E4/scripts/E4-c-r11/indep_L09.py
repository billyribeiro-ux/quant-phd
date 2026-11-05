"""Independent enumeration for E4 L09 (verifier round 11). Does not import the course code or the lab twin.

Model: six states, uniform prior, P1 = {12}{3}{456}, P2 = {123}{45}{6}. Bets take values in {-2,...,2}.
Counts: bets strictly positive for both at state 1 and at state 4; of those, nonnegative for both on the meet;
bets nonnegative for both on the meet; of those with a nonzero posterior on the meet. Also the closed-form count
of the zero-posterior bets on {1,2,3} (Emp 3 of the page): 5 * 5**3 = 625.
Run: python3 -I -W error indep_L09.py
"""

from __future__ import annotations

import itertools
from fractions import Fraction as F

S = [1, 2, 3, 4, 5, 6]
P1 = [{1, 2}, {3}, {4, 5, 6}]
P2 = [{1, 2, 3}, {4, 5}, {6}]
PI = F(1, 6)


def cell(part, w):
    return next(c for c in part if w in c)


def post(part, w, x):
    c = cell(part, w)
    return sum(PI * x[k] for k in c) / (PI * len(c))


def meet(w):
    reach = {w}
    changed = True
    while changed:
        changed = False
        for part in (P1, P2):
            for r in list(reach):
                for k in cell(part, r):
                    if k not in reach:
                        reach.add(k)
                        changed = True
    return reach


bets = []
for vals in itertools.product((-2, -1, 0, 1, 2), repeat=6):
    bets.append(dict(zip(S, vals)))
print("bets enumerated:", len(bets))

M1, M4 = meet(1), meet(4)
print("meet(1) =", sorted(M1), " meet(4) =", sorted(M4))
for label, st, M in (("state 1", 1, M1), ("state 4", 4, M4)):
    strict = 0
    strict_nonneg_on_meet = 0
    nonneg_meet = 0
    nonneg_meet_nonzero = 0
    for x in bets:
        negx = {k: -v for k, v in x.items()}
        g1 = {w: post(P1, w, x) for w in S}
        g2 = {w: post(P2, w, negx) for w in S}
        if g1[st] > 0 and g2[st] > 0:
            strict += 1
            if all(g1[w] >= 0 and g2[w] >= 0 for w in M):
                strict_nonneg_on_meet += 1
        if all(g1[w] >= 0 and g2[w] >= 0 for w in M):
            nonneg_meet += 1
            if any(g1[w] != 0 or g2[w] != 0 for w in M):
                nonneg_meet_nonzero += 1
    print(f"{label}: strict-both={strict}, strict-both & nonneg-on-meet={strict_nonneg_on_meet}, "
          f"nonneg-on-meet={nonneg_meet}, nonneg-on-meet with nonzero posterior={nonneg_meet_nonzero}")

# Emp 3 closed-form count: bets with g1=g2=0 on {1,2,3} <=> x3=0 and x2=-x1 (x4,x5,x6 free)
zero_on_123 = sum(1 for x in bets
                  if all(post(P1, w, x) == 0 for w in (1, 2, 3)) and all(post(P2, w, {k: -v for k, v in x.items()}) == 0 for w in (1, 2, 3)))
closed = 5 * 5 ** 3
print("zero posteriors on {1,2,3} (enumerated):", zero_on_123, " closed form 5*5^3 =", closed)

# Example 2.4 numbers
x = {1: -1, 2: 2, 3: -2, 4: -2, 5: -2, 6: -2}
print("g1(1), g2(1), g1(3) =", post(P1, 1, x), post(P2, 1, {k: -v for k, v in x.items()}), post(P1, 3, x))

# Remark 2.5 / canon-breaks two-prior example: q1(H)=0.7, q2(H)=0.4, x(H)=1, x(L)=-1
q1, q2 = F(7, 10), F(4, 10)
r1 = q1 * 1 + (1 - q1) * (-1)
r2 = -(q2 * 1 + (1 - q2) * (-1))
print("two-prior example receipts:", r1, r2)

# Res 2 algebra check: t = theta/(1-theta), theta = (nu1+nu2)/2, nu1=0.7, nu2=0.4 (nu2 < nu1 case)
nu1, nu2 = F(7, 10), F(4, 10)
th = (nu1 + nu2) / 2
t = th / (1 - th)
print("Res 2 witness: theta", th, "t", t,
      "trader1", nu1 - (1 - nu1) * t, "trader2", (1 - nu2) * t - nu2)
