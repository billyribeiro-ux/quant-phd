"""Independent recomputation of the card numbers in SC1 (no lab code imported).

Usage: python -I recompute_cards_r9.py
"""
import math
from fractions import Fraction
from itertools import product


def walks(n):
    """(max over S_0..S_n, S_n, first k>=1 with S_k>=1 or None) for every step sequence of length n."""
    out = []
    for steps in product((1, -1), repeat=n):
        s = 0
        top = 0
        first = None
        for k, e in enumerate(steps, 1):
            s += e
            top = max(top, s)
            if first is None and s >= 1:
                first = k
        out.append((top, s, first))
    return out


# Card c111: triples (N, a, b) with N<=12, 1<=a<=N, -N<=b<a; reflection identity.
triples = 0
equal = 0
pairs78 = 0
pair_seq_total = 0
tail_equal = 0
for n in range(1, 13):
    w = walks(n)
    ends = {}
    for _, e, _ in w:
        ends[e] = ends.get(e, 0) + 1
    for a in range(1, n + 1):
        pairs78 += 1
        pair_seq_total += 2 ** n
        hits = {}
        for top, e, _ in w:
            if top >= a:
                hits[e] = hits.get(e, 0) + 1
        for b in range(-n, a):
            triples += 1
            equal += hits.get(b, 0) == ends.get(2 * a - b, 0)
        mx = sum(1 for top, _, _ in w if top >= a)
        ge = sum(1 for _, e, _ in w if e >= a)
        gt = sum(1 for _, e, _ in w if e > a)
        tail_equal += mx == ge + gt
print("c111 triples", triples, "equal", equal)
print("c112 pairs", pairs78, "tail equal", tail_equal)
print("c170 (sequence, level) pairs", sum(n * 2 ** n for n in range(1, 13)), "sum 2^n n<=12", sum(2 ** n for n in range(1, 13)))

# Card c113: N=10, a=2 exact fractions.
w10 = walks(10)
P_M = Fraction(sum(1 for top, _, _ in w10 if top >= 2), 1024)
P_gt = Fraction(sum(1 for _, e, _ in w10 if e > 2), 1024)
P_eq = Fraction(sum(1 for _, e, _ in w10 if e == 2), 1024)
print("c113", P_M, 2 * P_gt, P_eq, P_M - 2 * P_gt == P_eq)

# Card c114: N=12, a=3: #{M>=3, S=2} and #{S=4}.
w12 = walks(12)
print("c114", sum(1 for top, e, _ in w12 if top >= 3 and e == 2), sum(1 for _, e, _ in w12 if e == 4), sum(1 for top, _, _ in w12 if top >= 3))

# Card c129: N=3, a=1.
w3 = walks(3)
print("c129 #M3>=1", sum(1 for top, _, _ in w3 if top >= 1), "#S3>=1", sum(1 for _, e, _ in w3 if e >= 1), "#S3>1", sum(1 for _, e, _ in w3 if e > 1))

# Card c148: N=16, a=4 binomial counts and tail.
def cnt_ge(n, m):
    return sum(math.comb(n, u) for u in range(n + 1) if 2 * u - n >= m)
print("c148", cnt_ge(16, 4), cnt_ge(16, 5), cnt_ge(16, 4) + cnt_ge(16, 5), (cnt_ge(16, 4) + cnt_ge(16, 5)) / 65536)

# Card c171/c180/c181: N=12, a=3 first passage counts by step (brute force), walk counts.
w = walks(12)
by_step = {}
for _, _, first in w:
    pass
# recompute first passage to 3 by step directly
counts = {k: 0 for k in range(1, 13)}
for steps in product((1, -1), repeat=12):
    s = 0
    hit = None
    for k, e in enumerate(steps, 1):
        s += e
        if hit is None and s >= 3:
            hit = k
    if hit is not None:
        counts[hit] += 1
print("c171 counts by step (3..12)", [counts[k] for k in range(3, 13)], "sum", sum(counts.values()))
print("c171 P(nu3<=12)", Fraction(sum(counts.values()), 4096), float(Fraction(sum(counts.values()), 4096)))
print("c171 P(S12>=3)", Fraction(sum(1 for _, e, _ in w if e >= 3), 4096), "count", sum(1 for _, e, _ in w if e >= 3))
print("c181 #{S12=3}", sum(1 for _, e, _ in w if e == 3))

# Cards c172/c173: exact truncated means E[min(nu_1,N)] = sum_{k<N} P(max_{j<=k} S_j < 1).
# P(max_{j<=k} S_j <= 0) by an exact DP over the level (no reflection formula).
def prob_stay_nonpositive(k):
    # dist over positions after j steps, restricted to paths that have never reached 1
    dist = {0: 1}
    for _ in range(k):
        nxt = {}
        for pos, c in dist.items():
            for e in (1, -1):
                q = pos + e
                if q >= 1:
                    continue
                nxt[q] = nxt.get(q, 0) + c
        dist = nxt
    return Fraction(sum(dist.values()), 2 ** k)

LEVELS = (16, 64, 256)
run = Fraction(0)
res = {}
for k in range(256):
    run += 1 - (1 - prob_stay_nonpositive(k)) * 0 - prob_stay_nonpositive(k) if False else 0
# simple: E[min(nu,N)] = sum_{k=0}^{N-1} P(nu > k) = sum P(max_{j<=k} S_j < 1)
run = Fraction(0)
stay = [prob_stay_nonpositive(k) for k in range(256)]
for k in range(256):
    run += stay[k]
    if k + 1 in LEVELS:
        res[k + 1] = run
for n in LEVELS:
    print("c172 E[min(nu_1,%d)] = %.6f (exact %s)" % (n, float(res[n]), res[n] if n == 16 else "-"))
print("c172 exact N=16 fraction", res[16], "==179587/32768", res[16] == Fraction(179587, 32768))

# Card c174 and c201/c205: closed forms.
def erfc_tail(a, h):
    return math.erfc(a / math.sqrt(2 * h))
print("c174 P(tau1<=1)", round(erfc_tail(1, 1), 6), "P(tau1<=2)", round(erfc_tail(1, 2), 6))
f = lambda a, h: a * h ** -1.5 * math.exp(-a * a / (2 * h)) / math.sqrt(2 * math.pi)
print("c174 density H=1", round(f(1, 1), 6), "H=2", round(f(1, 2), 6))
print("c201 P(B1>=1)", 0.5 * math.erfc(1 / math.sqrt(2)), "2P", math.erfc(1 / math.sqrt(2)))
print("c115 erfc(1/sqrt2)", math.erfc(1 / math.sqrt(2)))
# c151-style: L07 Part A exact tails
def tail_walk(n, m):
    return Fraction(cnt_ge(n, m) + cnt_ge(n, m + 1), 2 ** n)
print("L07 tails", [round(float(tail_walk(n, math.isqrt(n))), 6) for n in (4, 16, 64, 256, 1024)])
print("c150 gap", (math.sqrt(2 / math.pi) - 0.7586) / 0.0317)
print("c053 eq", 2 * math.sqrt(2) / 20, 2 * 1 / 8 / 20)
