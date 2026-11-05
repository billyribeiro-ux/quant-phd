"""Round 11 independent recomputation of card numbers (no lab code imported).

Usage: python -I recompute_r11.py <lab_L03.stdout> <lab_L00.stdout-unused>
"""
import math
import re
import sys
from fractions import Fraction
from math import comb, erfc, exp, pi, sqrt

def Phi(x: float) -> float:
    return 0.5 * erfc(-x / sqrt(2))

# c187: relative gap of printed SE vs H*sqrt(2/N)/20, from the lab L03 stdout
rows = []
H = None
for line in open(sys.argv[1], encoding="utf-8"):
    m = re.match(r"H = (\d+): mean", line)
    if m:
        H = int(m.group(1))
    m = re.match(r"\s+N =\s*(\d+) steps: mean ([\d.]+), se ([\d.]+), z = (-?[\d.]+)", line)
    if m and H is not None:
        N, se, z = int(m.group(1)), float(m.group(3)), float(m.group(4))
        f = H * sqrt(2 / N) / 20
        rows.append((H, N, se, f, se / f - 1, z))
print("c187 relative gaps: max", max(rows, key=lambda r: r[4])[:2], round(max(r[4] for r in rows) * 100, 2), "min", round(min(r[4] for r in rows) * 100, 2))
print("c051 max |z| at H=1,N=2?", max(rows, key=lambda r: abs(r[5]))[:2], "max|z| other:", max(abs(r[5]) for r in rows if (r[0], r[1]) != (1, 2)))

# c172 exact truncated means E[min(nu_1,N)] = sum_{k<N} P(nu_1>k), via first-passage counting on Fractions
def truncated_mean(N: int, a: int = 1) -> Fraction:
    # P(nu_a > k) = P(max_{j<=k} S_j < a) = 1 - P(M_k >= a); P(M_k>=a)= P(S_k>=a)+P(S_k>a)
    total = Fraction(0)
    for k in range(N):
        cnt_ge = sum(comb(k, u) for u in range(k + 1) if 2 * u - k >= a)
        cnt_gt = sum(comb(k, u) for u in range(k + 1) if 2 * u - k > a)
        p_max = Fraction(cnt_ge + cnt_gt, 2 ** k)
        total += 1 - p_max
    return total
for N in (16, 64, 256):
    print(f"c172 E[min(nu_1,{N})] = {float(truncated_mean(N)):.6f}")

# c174 densities and c115/c201/c174 probabilities
f = lambda h: 1 * h ** -1.5 * exp(-1 / (2 * h)) / sqrt(2 * pi)
print("c174 density H=1", round(f(1), 6), "H=2", round(f(2), 6), " P(tau<=1)", round(2 * (1 - Phi(1)), 6), "P(tau<=2)", round(2 * (1 - Phi(1 / sqrt(2))), 6))
print("c115 erfc(1/sqrt2)", round(erfc(1 / sqrt(2)), 10), "1-Phi(1)", round(1 - Phi(1), 10))
print("c201 P(B_1>=1)", round(1 - Phi(1), 10))
print("c148 2^16 count", sum(comb(16, u) for u in range(17) if 2 * u - 16 >= 4) + sum(comb(16, u) for u in range(17) if 2 * u - 16 > 4), "tail", round((sum(comb(16, u) for u in range(17) if 2 * u - 16 >= 4) + sum(comb(16, u) for u in range(17) if 2 * u - 16 > 4)) / 65536, 6))
print("c113 P(M10>=2)", Fraction(281, 512), "check", Fraction(sum(comb(10, u) for u in range(11) if 2 * u - 10 >= 2) * 2 - 0, 1024) * 0 + Fraction(sum(comb(10, u) for u in range(11) if 2 * u - 10 >= 2) + sum(comb(10, u) for u in range(11) if 2 * u - 10 > 2), 1024))
print("c111 triples", sum(1 for N in range(1, 13) for a in range(1, N + 1) for b in range(-N, a)), "pairs", sum(1 for N in range(1, 13) for a in range(1, N + 1)))
print("c170 sum n2^n", sum(n * 2 ** n for n in range(1, 13)))
print("c114 M12>=3 & S12=2 via reflection", sum(comb(12, u) for u in range(13) if 2 * u - 12 == 4))
print("c159 SE k=121 n=400", round(sqrt(121 * 279 / (400 ** 2 * 399)), 6))
print("c150 gap in SE", round((sqrt(2 / pi) - 0.7586) / 0.0317, 3), "sqrt(2/pi)", round(sqrt(2 / pi), 6))
print("c141 int(1-Phi)=phi(0)", round(1 / sqrt(2 * pi), 10))
print("c220/c221 sums: sum_m m r^m r=2^-1/2", round(sum(m * (2 ** -0.5) ** m for m in range(1, 200)), 6), "r/(1-r)^2", round((2 ** -0.5) / (1 - 2 ** -0.5) ** 2, 6))
print("c054 Var(Q) equal-increment N=10 t=1", round(sum(1 for _ in []) + 2 * 1 ** 2, 6))
print("Phi(-1/sqrt2)", round(Phi(-1 / sqrt(2)), 8))
print("c030 M_m check m=3: lambda*2^-(m+1)/2 vs sqrt(2log2)sqrt(m)2^-m/2:", round(sqrt(4 * 3 * math.log(2)) * 2 ** (-(3 + 1) / 2), 9), round(sqrt(2 * math.log(2)) * sqrt(3) * 2 ** (-3 / 2), 9))
