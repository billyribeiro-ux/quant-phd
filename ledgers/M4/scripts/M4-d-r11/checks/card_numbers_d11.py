"""Re-derive the closed-form numbers quoted on M4 cards (round 11, verifier d). Pure standard library + mpmath if present."""

import math
from fractions import Fraction
from itertools import product

print("c157 (2/pi) arctan(0.1) =", f"{(2 / math.pi) * math.atan(0.1):.7f}")
print("c161 10 * (2/pi) arctan(0.1) =", f"{10 * (2 / math.pi) * math.atan(0.1):.7f}")
print("c161 2/pi =", f"{2 / math.pi:.7f}", " gap =", f"{2 / math.pi - 10 * (2 / math.pi) * math.atan(0.1):.7f}")
print("c157 normal P(|Z|>10) = erfc(10/sqrt2) =", f"{math.erfc(10 / math.sqrt(2)):.5e}")
# t(3) tail P(|V|>x) = (2/pi)[arctan(sqrt3/x) - sqrt3 x/(3+x^2)] (card c149); check against numerical integration of density
def t3_density(t: float) -> float:
    return 2 / (math.pi * math.sqrt(3)) * (1 + t * t / 3) ** -2
def tail_formula(x: float) -> float:
    return (2 / math.pi) * (math.atan(math.sqrt(3) / x) - math.sqrt(3) * x / (3 + x * x))
def tail_numeric(x: float, n: int = 400000) -> float:
    # 2 * integral_x^inf density, via substitution t = x + u/(1-u), u in (0,1), midpoint rule
    total = 0.0
    h = 1.0 / n
    for i in range(n):
        u = (i + 0.5) * h
        t = x + u / (1 - u)
        total += t3_density(t) / (1 - u) ** 2 * h
    return 2 * total
print("c168 P(|V|>10) formula =", f"{tail_formula(10):.7f}", " numeric =", f"{tail_numeric(10):.7f}")
print("c168/c149 card value 0.002128 vs formula", f"{tail_formula(10):.6f}")
print("c172 x^3 P(|V|>x) at 1000 =", f"{1000 ** 3 * tail_formula(1000):.6f}", " limit 4 sqrt3/pi =", f"{4 * math.sqrt(3) / math.pi:.6f}")
# c187: limit
# Exact die-sum law: P(Z_n <= 1) = P(S_n <= floor(3.5 n + sqrt(n 35/12)))
def die_sum_pmf(n: int) -> list[Fraction]:
    pmf = [Fraction(1)]
    face = [Fraction(1, 6)] * 6  # faces 1..6 stored as k = 0..5
    for _ in range(n):
        new = [Fraction(0)] * (len(pmf) + 5)
        for s, p in enumerate(pmf):
            if p == 0:
                continue
            for k, q in enumerate(face):
                new[s + k] += p * q  # k = face - 1, so pmf index = S_n - n
        pmf = new
    return pmf
for n in (1, 5, 10, 20, 30, 40, 100, 200):
    pmf = die_sum_pmf(n)
    mean = Fraction(7, 2) * n
    sd_sq = Fraction(35, 12) * n
    thr = math.floor(float(mean) + math.sqrt(float(sd_sq)))
    # S_n offset: S_n = sum of faces, ranges n..6n; Z_n <= 1 <=> S_n - mean <= sqrt(var) <=> S_n <= floor(mean + sqrt(var))
    p = sum(pmf[s] for s in range(0, min(thr - n, 5 * n) + 1))
    print(f"n={n}: P(Z_n<=1) = {float(p):.6f} (exact {p.numerator}/{p.denominator if p.denominator < 10**12 else 'big'}) gap to Phi(1) = {float(p) - 0.8413447460685429:+.4f}")
print("c142 threshold for ten dice:", 35 + math.sqrt(10 * 35 / 12))
print("c141 Chebyshev 7/60 =", 7 / 60, " (35/12)/(100*0.25) =", (35 / 12) / 25)
print("c133 Taylor constant check: |e^{ix}-1-ix+x^2/2| <= |x|^3/6 ; card claims /3 (weaker)")
print("c112 e^5.5 =", f"{math.exp(5.5):.8f}")
print("c183 exact kurtosis 149461/26569 =", f"{149461 / 26569:.6f}", " m3 =", 2157 / 32, " m4 =", 149461 / 256)
m = Fraction(7, 4)
law = [(0, Fraction(1, 2)), (1, Fraction(1, 4)), (2, Fraction(1, 8)), (10, Fraction(1, 8))]
for k in (2, 3, 4):
    print(f"central moment m_{k} =", sum(p * (x - m) ** k for x, p in law), float(sum(p * (x - m) ** k for x, p in law)))
