"""Independent recheck of L09 counts (stdlib only). Run: python -I recheck_L09.py

Brute force over all 5^6 bets with exact Fractions. Posteriors are averages over the states of the cell
(equal priors on every state), and the meet is computed by union-find.
"""

from fractions import Fraction as F
from itertools import product

S = [1, 2, 3, 4, 5, 6]
P1 = [{1, 2}, {3}, {4, 5, 6}]
P2 = [{1, 2, 3}, {4, 5}, {6}]


def cell(parts, w):
    for c in parts:
        if w in c:
            return c
    raise AssertionError


def meet_uf(w0):
    parent = {s: s for s in S}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for parts in (P1, P2):
        for c in parts:
            c = sorted(c)
            for other in c[1:]:
                parent[find(c[0])] = find(other)
    root = find(w0)
    return {s for s in S if find(s) == root}


def post(parts, w, x):
    c = cell(parts, w)
    return sum((x[k] for k in c), F(0)) / len(c)


def run(state):
    m = meet_uf(state)
    strict = strict_and_common = nonneg_meet = nonneg_zero_viol = 0
    first = None
    for vals in product([-2, -1, 0, 1, 2], repeat=6):
        x = dict(zip(S, vals))
        neg = {k: -v for k, v in x.items()}
        g1 = {w: post(P1, w, x) for w in S}
        g2 = {w: post(P2, w, neg) for w in S}
        s_pos = g1[state] > 0 and g2[state] > 0
        nn = all(g1[w] >= 0 and g2[w] >= 0 for w in m)
        if s_pos:
            strict += 1
            if first is None:
                first = (vals, [str(g1[w]) for w in sorted(m)], [str(g2[w]) for w in sorted(m)])
            if nn:
                strict_and_common += 1
        if nn:
            nonneg_meet += 1
            if any(g1[w] != 0 or g2[w] != 0 for w in m):
                nonneg_zero_viol += 1
    return sorted(m), strict, strict_and_common, nonneg_meet, nonneg_zero_viol, first


for st in (1, 4):
    m, strict, sc, nn, viol, first = run(st)
    print(f"state {st}: meet {m}; strictly positive both at state: {strict}; of those nonneg on meet: {sc}; "
          f"nonneg both on meet: {nn}; of those nonzero: {viol}")
    print(f"   first strict bet x={first[0]} agent1 posteriors on meet {first[1]} agent2 {first[2]}")

cnt = 0
for vals in product([-2, -1, 0, 1, 2], repeat=6):
    x = dict(zip(S, vals))
    neg = {k: -v for k, v in x.items()}
    if all(post(P1, w, x) == 0 for w in (1, 2, 3)) and all(post(P2, w, neg) == 0 for w in (1, 2, 3)):
        cnt += 1
print("bets with g1=g2=0 on {1,2,3}:", cnt, "(formula 5*5^3 = 625)")
print("total bets:", 5 ** 6)
