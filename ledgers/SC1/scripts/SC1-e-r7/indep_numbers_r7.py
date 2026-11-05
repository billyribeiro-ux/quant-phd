"""Independent exact recomputation of the SC1 walk and Gaussian numbers quoted on cards and lesson pages (round 7).

No lab code is imported. Exact integer and Fraction arithmetic for the walk counts; math.erfc for Gaussian values.
Usage: python -I indep_numbers_r7.py
"""
import itertools
import math
from fractions import Fraction
from math import comb, erfc, exp, pi, sqrt

print("L06 Part A: triples (N,a,b), 1<=N<=12, 1<=a<=N, -N<=b<a, identity #{M>=a,S=b}=#{S=2a-b}")
trip = 0
ok = 0
for N in range(1, 13):
    seqs = list(itertools.product((-1, 1), repeat=N))
    for a in range(1, N + 1):
        for b in range(-N, a):
            lhs = sum(1 for s in seqs if max(_partial := list(itertools.accumulate(s))) >= a and sum(s) == b)
            rhs = sum(1 for s in seqs if sum(s) == 2 * a - b)
            trip += 1
            ok += lhs == rhs
print("  triples", trip, "equal", ok)

print("L06 Part B: pairs (N,a), N=1..12, a=1..N, #{M>=a} = #{S>=a} + #{S>a}")
pairs = 0
ok = 0
for N in range(1, 13):
    cnt = {}
    for s in itertools.product((-1, 1), repeat=N):
        path = list(itertools.accumulate(s))
        cnt.setdefault("paths", []).append((max(path), sum(s)))
    for a in range(1, N + 1):
        pairs += 1
        lhs = sum(1 for m, e in cnt["paths"] if m >= a)
        rhs = sum(1 for m, e in cnt["paths"] if e >= a) + sum(1 for m, e in cnt["paths"] if e > a)
        ok += lhs == rhs
print("  pairs", pairs, "equal", ok)

print("L06 Part C: N=12, a=3, walks with M>=3 and S=2 / S=4; walks with M>=3 total")
c_m_s2 = c_m_s4 = c_m = 0
for s in itertools.product((-1, 1), repeat=12):
    path = list(itertools.accumulate(s))
    m = max(path)
    if m >= 3:
        c_m += 1
        if path[-1] == 2:
            c_m_s2 += 1
        if path[-1] == 4:
            c_m_s4 += 1
print("  M>=3:", c_m, " M>=3 and S=2:", c_m_s2, " S=4:", c_m_s4)

print("L06 Part D: N=10, a=2 exact fractions")
N, a = 10, 2
pm = Fraction(sum(1 for s in itertools.product((-1, 1), repeat=N) if max(itertools.accumulate(s)) >= a), 2**N)
ps_gt = Fraction(sum(comb(N, k) for k in range(N + 1) if 2 * k - N > a), 2**N)
ps_eq = Fraction(sum(comb(N, k) for k in range(N + 1) if 2 * k - N == a), 2**N)
print("  P(M>=2)", pm, float(pm), " 2P(S>2)", 2 * ps_gt, float(2 * ps_gt), " P(S=2)", ps_eq, float(ps_eq))

print("L07 Part A: tails P(M_N>=m) with m = sqrt(N), N=4,16,64,256,1024 (SRW, exact):")
for N in (4, 16, 64, 256, 1024):
    m = int(round(sqrt(N)))
    # P(M_N>=m) = P(S_N>=m)+P(S_N>m) (reflection; checked for small N in L06 Part B above)
    p_ge = Fraction(sum(comb(N, k) for k in range(N + 1) if 2 * k - N >= m), 2**N)
    p_gt = Fraction(sum(comb(N, k) for k in range(N + 1) if 2 * k - N > m), 2**N)
    tail = p_ge + p_gt
    print(f"  N={N} m={m}: {float(tail):.6f}")
print("  N=16 counts: S>=4 =", sum(comb(16, k) for k in range(17) if 2 * k - 16 >= 4), " S>4 =", sum(comb(16, k) for k in range(17) if 2 * k - 16 > 4), " sum =", sum(comb(16, k) for k in range(17) if 2 * k - 16 >= 4) + sum(comb(16, k) for k in range(17) if 2 * k - 16 > 4), " /65536 =", (sum(comb(16, k) for k in range(17) if 2 * k - 16 >= 4) + sum(comb(16, k) for k in range(17) if 2 * k - 16 > 4)) / 65536)
print("  closed form 2(1-Phi(1)) =", 2 * 0.5 * erfc(1 / sqrt(2)), " unrounded erfc(1/sqrt2) =", erfc(1 / sqrt(2)))

print("L08 Part A: first-passage counts of nu_3 at step k, N=12")
# DP over walk positions with first-passage at level a: count sequences whose first visit to a is at step k
def first_passage_counts(a, Nmax):
    # dist[pos] = number of sequences of length k with no visit to a so far, ending at pos
    dist = {0: 1}
    out = {}
    for k in range(1, Nmax + 1):
        new = {}
        hit = 0
        for pos, c in dist.items():
            for step in (-1, 1):
                q = pos + step
                if q == a:
                    hit += c
                else:
                    new[q] = new.get(q, 0) + c
        out[k] = hit * 2 ** (Nmax - k)
        dist = new
    return out
fp = first_passage_counts(3, 12)
print("  counts (weighted to 2^12 sequences) k=1..12:", [fp[k] for k in range(1, 13)], " sum", sum(fp.values()))
print("  P(nu_3<=12) =", Fraction(sum(fp.values()), 4096), float(Fraction(sum(fp.values()), 4096)))
print("  #{S_12>=3} =", sum(comb(12, k) for k in range(13) if 2 * k - 12 >= 3), " 2*794-0 check:", 2 * sum(comb(12, k) for k in range(13) if 2 * k - 12 >= 3))

print("L08 Part A: pairs (sequence, level): n=1..12, a=1..n, all 2^n sequences; total =", sum(n * 2 ** n for n in range(1, 13)))

print("L08 Part B: exact E[min(nu_1,N)] = sum_{k<N} P(nu_1>k), P(nu_1>k)=P(max_{j<=k} S_j <= 0)")
# P(nu_1 > k) = (#sequences of length k never reaching 1)/2^k = count of sequences of length k with max <= 0
def no_hit_counts(Nmax):
    res = []
    for k in range(0, Nmax):
        # number of length-k walks with max_{j<=k} S_j <= 0 equals C(k, floor(k/2)) (reflection)
        res.append(comb(k, k // 2))
    return res
# direct DP to avoid relying on the reflection identity:
def survive(Nmax):
    dist = {0: 1}
    res = [1]
    for k in range(1, Nmax):
        new = {}
        for pos, c in dist.items():
            for step in (-1, 1):
                q = pos + step
                if q < 1:
                    new[q] = new.get(q, 0) + c
        dist = new
        res.append(sum(dist.values()))
    return res
surv = survive(256)
for N in (16, 64, 256):
    E = sum(Fraction(surv[k], 2 ** k) for k in range(N))
    print(f"  N={N}: exact {E} = {float(E):.6f}")
print("  E[min(nu_1,16)] vs 179587/32768 =", Fraction(179587, 32768), float(Fraction(179587, 32768)))
print("  reflection check (C(k,floor k/2)) equals DP for k<=20:", all(surv[k] == comb(k, k // 2) for k in range(0, 21)))

print("L08 Part D and L08 quiz values:")
print("  2(1-Phi(1)) =", 2 * (1 - 0.5 * (1 + math.erf(1 / sqrt(2)))), " erfc(1/sqrt2)=", erfc(1 / sqrt(2)))
print("  P(tau_1<=2)=erfc(1/2)=", erfc(0.5))
f1 = 1 * 1 ** -1.5 * exp(-0.5) / sqrt(2 * pi)
f2 = 1 * 2 ** -1.5 * exp(-1 / 4) / sqrt(2 * pi)
print("  f_1(1)=", f1, " f_1(2)=", f2)
print("  E[M_1]=sqrt(2/pi)=", sqrt(2 / pi), "  1/sqrt(2pi)=", 1 / sqrt(2 * pi))
print("  1-Phi(1)=", 0.5 * erfc(1 / sqrt(2)))
print("  Corollary 1.5 at a=1,H=2 density:", f2)
print("  L03 SE at H=1,N=1:", sqrt(2) / 20, " H=2,N=1:", 2 * sqrt(2) / 20)
print("  L03 c187 check: printed 0.1601 vs formula", 2 * sqrt(2) / 20, "gap%", (0.1601 - 2 * sqrt(2) / 20) / (2 * sqrt(2) / 20) * 100)
print("  c057 check: N*sqrt(2/pi)*sqrt(t/N)=sqrt(2Nt/pi) at N=4,t=1:", 4 * sqrt(2 / pi) * sqrt(1 / 4), sqrt(2 * 4 / pi))
print("  c159 SE k=121,n=400:", sqrt(121 * 279 / (400 ** 2 * 399)))
print("  c140 E[M_H] H=1: sqrt(2/pi)=", sqrt(2 / pi))
print("  c183: a^2/3 examples: a=1 ->", 1 / 3)
print("  c091 machine epsilon ratio:", 5.55e-16 / 2.22e-16)
print("  c150 gap in SE units:", (0.797885 - 0.7586) / 0.0317)
print("  c149 SE check N=4: sqrt(0.2275*0.7725/400)=", sqrt(0.2275 * 0.7725 / 400), " N=256 p=0.3025:", sqrt(0.3025 * 0.6975 / 400))
