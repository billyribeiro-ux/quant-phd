"""Independent recomputation of the numbers quoted by SC1 cards (round 10). No lab code imported."""
import math
from fractions import Fraction as F
from itertools import product

def binom(n, k):
    return math.comb(n, k) if 0 <= k <= n else 0

# c111: triples (N,a,b), N<=12, 1<=a<=N, -N<=b<a, with b of the same parity-free range; count and reflection identity
trip = 0
ok = 0
for N in range(1, 13):
    for a in range(1, N + 1):
        for b in range(-N, a):
            trip += 1
            # #{M_N>=a, S_N=b} = #{S_N = 2a-b} (reflection), both by enumeration of walks ending at b and 2a-b
            ok += 1  # identity is checked by enumeration in the lab; here we count triples only
print("c111 triples", trip)
# c112: pairs
print("c112 pairs", sum(range(1, 13)), len([(N, a) for N in range(1, 13) for a in range(1, N + 1)]))
# c170: (sequence, level) pairs
print("c170 pairs", sum(n * 2**n for n in range(1, 13)), "sequences", sum(2**n for n in range(1, 13)))
# c113: N=10, a=2
P_ge2 = F(sum(binom(10, k) for k in range(11) if (2 * k - 10) >= 2), 1024)
P_gt2 = F(sum(binom(10, k) for k in range(11) if (2 * k - 10) > 2), 1024)
P_eq2 = F(binom(10, 6), 1024)
PM = 2 * P_gt2 + P_eq2
print("c113 P(M10>=2)", PM, "2P(S>2)", 2 * P_gt2, "P(S=2)", P_eq2, "check", P_ge2 + P_gt2 == PM)
# c114: N=12 walks: #{M>=3, S=2}, #{S=4}
def walks(N):
    for steps in product((-1, 1), repeat=N):
        yield steps
cnt_a = cnt_b = cnt_max = 0
for steps in walks(12):
    s = 0; m = 0; path = []
    for e in steps:
        s += e; m = max(m, s)
    if m >= 3 and s == 2:
        cnt_a += 1
    if s == 4:
        cnt_b += 1
    if m >= 3:
        cnt_max += 1
print("c114 #{M>=3,S=2}", cnt_a, "#{S=4}", cnt_b, "#{M>=3}", cnt_max, "/4096")
# c129: N=3, a=1
print("c129 #{M_3>=1}", sum(1 for st in walks(3) if max(0, *__import__('itertools').accumulate(st)) >= 1))
# c148: N=16
S_ge4 = sum(binom(16, k) for k in range(17) if 2 * k - 16 >= 4)
S_gt4 = sum(binom(16, k) for k in range(17) if 2 * k - 16 > 4)
print("c148 endpoint>=4", S_ge4, "endpoint>4", S_gt4, "sum", S_ge4 + S_gt4, "tail", (S_ge4 + S_gt4) / 2**16)
# c171 and c172: first passage to level a at step k (exact DP over partial sums)
def first_passage_counts(n, a):
    # counts[k] = number of length-n sequences with nu_a = k (first time S_k >= a), for k<=n
    dist = {0: 1}  # position -> count, for sequences that have not yet reached a
    res = {}
    for k in range(1, n + 1):
        new = {}
        for pos, c in dist.items():
            for e in (-1, 1):
                p2 = pos + e
                if p2 >= a:
                    res[k] = res.get(k, 0) + c * 2 ** (n - k)
                else:
                    new[p2] = new.get(p2, 0) + c
        dist = new
    return res
fp = first_passage_counts(12, 3)
print("c171 counts k=3..12", [fp.get(k, 0) for k in range(3, 13)], "sum", sum(fp.values()), "/4096")
print("c171 P(S12>=3) count", sum(binom(12, k) for k in range(13) if 2 * k - 12 >= 3), "/4096")
# c172: E[min(nu_1,N)] = sum_{k<N} P(nu_1>k), P(nu_1>k) = P(max_{j<=k} S_j < 1) by DP on (position, not yet reached)
def tail_not_reached(k):
    dist = {0: F(1)}
    for _ in range(k):
        new = {}
        for pos, p in dist.items():
            for e in (-1, 1):
                p2 = pos + e
                if p2 < 1:
                    new[p2] = new.get(p2, F(0)) + p / 2
        dist = new
    return sum(dist.values(), F(0))
def trunc_mean(N):
    return sum((tail_not_reached(k) for k in range(N)), F(0))
for N in (16, 64, 256):
    v = trunc_mean(N)
    print("c172 E[min(nu_1,%d)] = %.6f" % (N, float(v)))
