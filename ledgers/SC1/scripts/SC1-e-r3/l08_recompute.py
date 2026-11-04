"""Independent recomputation of SC1 L08 exact walk numbers by direct enumeration (stdlib, read-only)."""
import math
from fractions import Fraction
from itertools import product

def first_hit(steps, a):
    s = 0
    for k, e in enumerate(steps, 1):
        s += e
        if s >= a:
            return k
    return None

# Part A counts for n=12, a=3
n, a = 12, 3
cnt = {}
for steps in product((1, -1), repeat=n):
    k = first_hit(steps, a)
    if k is not None:
        cnt[k] = cnt.get(k, 0) + 1
print("first-passage counts to 3 by step:", [cnt.get(k, 0) for k in range(3, 13)], "total", sum(cnt.values()))
print("P(nu_3<=12)=", sum(cnt.values()) / 4096, " P(S_12>=3)=", sum(1 for st in product((1,-1), repeat=12) if sum(st) >= 3) / 4096)
# Part A: sequences checked and pair counts
seqs = sum(2 ** m for m in range(1, 13) for _ in range(1, m + 1))
print("sequences checked (sum over n of n*2^n):", seqs)
# Part B: truncated means E[min(nu_1, N)] = sum_{k<N} P(nu_1 > k) with P(nu_1>k)=P(max_{j<=k}S_j = 0)
# Use exact distribution of running max for k up to 256 via binomial reflection
def p_nu_gt(k):
    # P(nu_1 > k) = P(M_k <= 0) = P(S_k <= 0 and never reaches 1) = P(M_k = 0)
    if k == 0:
        return Fraction(1)
    ge1 = sum(math.comb(k, u) for u in range(k + 1) if 2 * u - k >= 1) + sum(math.comb(k, u) for u in range(k + 1) if 2 * u - k >= 2)
    return 1 - Fraction(ge1, 2 ** k)
total = Fraction(0)
vals = {}
for k in range(256):
    total += p_nu_gt(k)
    if k + 1 in (16, 64, 256):
        vals[k + 1] = total
for N in (16, 64, 256):
    print(f"E[min(nu_1,{N})] = {float(vals[N]):.6f}")
