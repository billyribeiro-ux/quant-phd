"""Independent re-derivation of every exact number on the SC1 cards (no lab code reused). Usage: indep_numbers.py"""
import math
from fractions import Fraction
from itertools import product
from collections import Counter

def C(n, k):
    return math.comb(n, k)

# c111: triples (N,a,b) with N<=12, 1<=a<=N, -N<=b<a
triples = sum(1 for N in range(1, 13) for a in range(1, N + 1) for b in range(-N, a))
print("c111 triples", triples)
# c112: pairs
print("c112 pairs", sum(range(1, 13)))
# walks of length n: (max, end) enumeration for small n (exact)
def walks(n):
    out = []
    for steps in product((1, -1), repeat=n):
        p = 0; h = 0; first = {}
        for k, s in enumerate(steps, 1):
            p += s; h = max(h, p)
        out.append((h, p))
    return out
# c111 identity check by my own enumeration
ok = 0
for N in range(1, 13):
    W = walks(N)
    for a in range(1, N + 1):
        for b in range(-N, a):
            ok += sum(1 for h, e in W if h >= a and e == b) == sum(1 for h, e in W if e == 2 * a - b)
print("c111 identity holds on", ok, "of", triples)
# c113: N=10, a=2
W10 = walks(10)
tail = Fraction(sum(1 for h, e in W10 if h >= 2), 1024)
above = Fraction(sum(1 for h, e in W10 if e > 2), 1024)
eq = Fraction(sum(1 for h, e in W10 if e == 2), 1024)
print("c113", tail, above * 2, eq, "P(S10=2)=C(10,6)/1024 =", Fraction(C(10, 6), 1024))
# c114: N=12, a=3
W12 = walks(12)
print("c114 M>=3,S=2:", sum(1 for h, e in W12 if h >= 3 and e == 2), " S=4:", sum(1 for h, e in W12 if e == 4), " M>=3:", sum(1 for h, e in W12 if h >= 3))
# c129: N=3 a=1
W3 = walks(3)
print("c129 M3>=1:", sum(1 for h, e in W3 if h >= 1), "of 8")
# c148: N=16
print("c148 #S>=4", sum(C(16, u) for u in range(16 + 1) if 2 * u - 16 >= 4), "#S>4", sum(C(16, u) for u in range(17) if 2 * u - 16 > 4),
      "total", sum(C(16, u) for u in range(17) if 2 * u - 16 >= 4) + sum(C(16, u) for u in range(17) if 2 * u - 16 > 4),
      "tail", (sum(C(16, u) for u in range(17) if 2 * u - 16 >= 4) + sum(C(16, u) for u in range(17) if 2 * u - 16 > 4)) / 2**16)
# c170: sum n 2^n
print("c170 pairs", sum(n * 2**n for n in range(1, 13)), "sequences", sum(2**n for n in range(1, 13)))
# c171: first passage to 3 for n=12
def first_hits(n, a):
    counts = Counter()
    for steps in product((1, -1), repeat=n):
        p = 0; hit = None
        for k, s in enumerate(steps, 1):
            p += s
            if hit is None and p >= a:
                hit = k
        if hit is not None:
            counts[hit] += 1
    return counts
fh = first_hits(12, 3)
print("c171 counts by step (3..12) over all 4096 sequences:", [fh[k] for k in range(3, 13)], "sum", sum(fh[k] for k in range(3, 13)))
print("c171 sum of counts", sum(fh[k] for k in range(3, 13)), "of 4096")
print("c171 P(nu<=12)=", Fraction(sum(fh[k] for k in range(3, 13)), 4096), float(Fraction(1588, 4096)))
print("c171 P(S12>=3)=", Fraction(sum(C(12, u) for u in range(13) if 2 * u - 12 >= 3), 4096), "=", float(Fraction(794, 4096)))
print("c171 #S12>=3", sum(C(12, u) for u in range(13) if 2 * u - 12 >= 3), "#S12=3", sum(C(12, u) for u in range(13) if 2 * u - 12 == 3))
# c172: truncated means E[min(nu_1,N)] = sum_{k<N} P(nu_1>k), P(nu_1>k)=1-P(M_k>=1)
def pM_ge1(k):
    # P(max_{j<=k} S_j >= 1) = (#S_k>=1 + #S_k>1)/2^k  for k>=1 ; k=0 -> 0
    if k == 0:
        return Fraction(0)
    ge = sum(C(k, u) for u in range(k + 1) if 2 * u - k >= 1)
    gt = sum(C(k, u) for u in range(k + 1) if 2 * u - k > 1)
    return Fraction(ge + gt, 2 ** k)
def trunc_mean(N):
    return sum(1 - pM_ge1(k) for k in range(N))
for N in (16, 64, 256):
    tm = trunc_mean(N)
    print("c172 N=%d E[min(nu1,N)] = %.6f" % (N, float(tm)))
# c174: Brownian first passage
def Phi(x):
    return 0.5 * math.erfc(-x / math.sqrt(2))
for H in (1.0, 2.0):
    cdf = math.erfc(1 / math.sqrt(2 * H))
    dens = (1 / math.sqrt(2 * math.pi)) * H ** (-1.5) * math.exp(-1 / (2 * H))
    print("c174 H=%g P=%.6f density=%.9f" % (H, cdf, dens))
print("c201/c176 tail B1>=1 =", 1 - Phi(1.0), " 2x =", 2 * (1 - Phi(1.0)))
print("c115 erfc(1/sqrt2)=", math.erfc(1 / math.sqrt(2)))
# c150/c149: Brownian grid values use the lab; here closed form values
print("c150 sqrt(2/pi)=", math.sqrt(2 / math.pi), " gap", math.sqrt(2 / math.pi) - 0.7586, " in SE", (math.sqrt(2 / math.pi) - 0.7586) / 0.0317)
# c159 / c149 SE
print("c159 SE k=121,n=400:", math.sqrt(121 * 279 / (400 ** 2 * 399)))
# c052 SE formula
print("c052 H sqrt(2/N)/20 at N=128,H=2 =", 2 * math.sqrt(2 / 128) / 20)
# c141 integral check via simpson
def simpson(f, a, b, n):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3
print("c141 int_0^13 (1-Phi)", simpson(lambda u: 1 - Phi(u), 0, 13, 4000), " 1/sqrt(2pi)=", 1 / math.sqrt(2 * math.pi))
# c183 mode
print("c183 derivative sign check: (a^2-3H)/(2H^2) at a=1: H=0.3 ->", (1 - 0.9) / (2 * 0.09), " H=0.5 ->", (1 - 1.5) / (2 * 0.25))
# c140: E[M_H] = sqrt(2H/pi): numerically integrate 2(1-Phi(a/sqrtH)) da for H=1
H = 1.0
EM = simpson(lambda a: 2 * (1 - Phi(a / math.sqrt(H))), 0, 40, 40000)
print("c140 E[M_1] numeric", EM, " sqrt(2/pi)=", math.sqrt(2 / math.pi))
# c165 density check: derivative of F(H)=2(1-Phi(a H^-1/2)) at H=1, a=1 vs closed density
F = lambda h: 2 * (1 - Phi(1 / math.sqrt(h)))
d = (F(1 + 1e-6) - F(1 - 1e-6)) / 2e-6
print("c165 central diff", d, " closed", (1 / math.sqrt(2 * math.pi)) * math.exp(-0.5))
