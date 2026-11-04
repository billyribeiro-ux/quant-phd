# Independent re-derivation of the exact counts quoted in SC1 lessons 6 to 8 (no lab code reused)
from fractions import Fraction
from itertools import product
from math import comb, erfc, sqrt, pi, exp
import math

def walks(n):
    for steps in product((1, -1), repeat=n):
        s = 0; top = 0; first = None
        for k, e in enumerate(steps, 1):
            s += e; top = max(top, s)
        yield steps
# L06 Part A: triples (N,a,b) with b<a, #{M_N>=a, S_N=b} == #{S_N=2a-b}
triples = eq = 0
pairs = 0; tail_ok = 0
for n in range(1, 13):
    W = []
    for steps in product((1, -1), repeat=n):
        s = 0; top = 0
        for e in steps:
            s += e; top = max(top, s)
        W.append((top, s))
    ends = {}
    for _, e in W: ends[e] = ends.get(e, 0) + 1
    for a in range(1, n + 1):
        for b in range(-n, a):
            triples += 1
            lhs = sum(1 for top, e in W if top >= a and e == b)
            rhs = ends.get(2 * a - b, 0)
            eq += lhs == rhs
        pairs += 1
        m = sum(1 for top, _ in W if top >= a)
        ge = sum(1 for _, e in W if e >= a); gt = sum(1 for _, e in W if e > a)
        tail_ok += m == ge + gt
print("L06 A triples", triples, eq, "| B pairs", pairs, tail_ok)
# L06 part C/D
n = 12
W = []
for steps in product((1, -1), repeat=n):
    s = 0; top = 0
    for e in steps:
        s += e; top = max(top, s)
    W.append((top, s))
print("L06 C: M12>=3", sum(1 for t, e in W if t >= 3), "and S12=2", sum(1 for t, e in W if t >= 3 and e == 2), "S12=4", sum(1 for t, e in W if e == 4))
W10 = []
for steps in product((1, -1), repeat=10):
    s = 0; top = 0
    for e in steps:
        s += e; top = max(top, s)
    W10.append((top, s))
print("L06 D: P(M10>=2)=", Fraction(sum(1 for t, e in W10 if t >= 2), 1024), "2P(S10>2)=", Fraction(2 * sum(1 for t, e in W10 if e > 2), 1024), "P(S10=2)=", Fraction(sum(1 for t, e in W10 if e == 2), 1024))
print("L06 E: erfc(1/sqrt2)=", erfc(1 / sqrt(2)), "half", erfc(1 / sqrt(2)) / 2)
# L08 Part A and B
W12 = []
for steps in product((1, -1), repeat=12):
    s = 0; first = None; k = 0
    for e in steps:
        k += 1; s += e
        if first is None and s >= 3: first = k
    W12.append(first)
print("L08 A first-passage counts k=3..12 at level 3:", [sum(1 for f in W12 if f == k) for k in range(3, 13)], "nu<=12:", sum(1 for f in W12 if f is not None))
def e_min_mean(N, a=1):
    # sum_{k<N} P(nu_a > k) computed by brute force for N<=16 and by binomial recursion otherwise
    # P(max_{j<=k} S_j >= a) = P(S_k>=a)+P(S_k>a) (reflection) ; use exact fraction
    tot = Fraction(0)
    for k in range(N):
        if k == 0:
            p_hit = Fraction(0)
        else:
            def ge(m, nn):
                return sum(comb(nn, (nn + s) // 2) for s in range(-nn, nn + 1, 2) if s >= m)
            p_hit = Fraction(ge(a, k) + ge(a + 1, k), 2 ** k)
        tot += 1 - p_hit
    return tot
for N in (16, 64, 256):
    print("L08 B E[min(nu1,N)] N=", N, float(e_min_mean(N)))
# L07 Part A exact tails
def ge(m, nn):
    return sum(comb(nn, (nn + s) // 2) for s in range(-nn, nn + 1, 2) if s >= m)
for nn in (4, 16, 64, 256, 1024):
    m = math.isqrt(nn)
    print("L07 A N", nn, "m", m, round((ge(m, nn) + ge(m + 1, nn)) / 2 ** nn, 6) if nn <= 256 else round((ge(m, nn) + ge(m + 1, nn)) / 2 ** nn, 6))
print("L07 E2 check: S16>=4 count", ge(4, 16), "S16>4 count", ge(5, 16), "sum", ge(4,16)+ge(5,16), (ge(4,16)+ge(5,16))/65536)
print("L07 E3 SE", sqrt(121*279/(400**2*399)))
print("L08 P(S12>=3)=", ge(3, 12), "/4096")
print("L04 values", exp(1), exp(0.25), exp(4), exp(8))
print("L08 erfc(0.5)", erfc(0.5), "density H=1", exp(-0.5)/sqrt(2*pi), "H=2", (1/sqrt(2*pi))*2**-1.5*exp(-0.25))
print("L05 M1 check", 1/(2*sqrt(pi)), 1/sqrt(4*pi))
