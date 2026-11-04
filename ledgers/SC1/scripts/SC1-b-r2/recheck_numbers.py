"""Independent recomputation of the numbers printed or stated on SC1 L04-L06 (verifier, round 2).

Uses only the standard library (decimal, fractions, itertools, math). Run as:
    python -I -W error ledgers/SC1/scripts/SC1-b-r2/recheck_numbers.py
"""

from __future__ import annotations

import math
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import product

getcontext().prec = 60
PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494459")


def dexp(x: Decimal) -> Decimal:
    return x.exp()


def dpdf(u: Decimal, x: Decimal, y: Decimal) -> Decimal:
    """p_u(x, y) = (2 pi u)^(-1/2) exp(-(y-x)^2 / (2u)), in Decimal."""
    return dexp(-((y - x) ** 2) / (2 * u)) / (2 * PI * u).sqrt()


def dsimpson(f, a: Decimal, b: Decimal, n: int) -> Decimal:
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        total += (Decimal(4) if i % 2 else Decimal(2)) * f(a + i * h)
    return total * h / 3


print("== L04 closed forms ==")
print("e^1 =", f"{math.exp(1):.9f}", " e^0.25 =", f"{math.exp(0.25):.9f}", " e^4 =", f"{math.exp(4):.9f}")
print("e^8 =", f"{math.exp(8):.6f}", " e^(0.25) rounded to 9 places:", f"{math.exp(0.25):.9f}")
print("E[e^{2B_2}] check, theta=1,t=2: e^{1*2/2}=", f"{math.exp(1):.9f}")

print("== L04 Lemma 2.1 quadrature (exact closed forms only; quadrature is in the twin) ==")
for theta in (-1.0, 0.5, 2.0):
    print(theta, math.exp(theta * theta * 2 / 2))

print("== L05 Lemma 2.2 identity, exact rational check on a grid ==")
bad = 0
cases = 0
vals = [Fraction(k, 4) for k in range(-8, 9)]
for u, v in product([Fraction(1, 2), Fraction(1), Fraction(2), Fraction(3)], repeat=2):
    for x, y, z in product(vals[::4], vals[::4], vals[::3]):
        m = (v * x + u * y) / (u + v)
        lhs = (z - x) ** 2 / u + (y - z) ** 2 / v
        rhs = (u + v) / (u * v) * (z - m) ** 2 + (y - x) ** 2 / (u + v)
        cases += 1
        if lhs != rhs:
            bad += 1
print(f"Lemma 2.2 exact rational identity: cases={cases} failures={bad}")

print("== L05 P1 worked example: u=1, v=3, x=0, y=1 ==")
for zq in (Fraction(0), Fraction(1, 3), Fraction(-2)):
    u, v, x, y, z = Fraction(1), Fraction(3), Fraction(0), Fraction(1), zq
    m = (v * x + u * y) / (u + v)
    lhs = (z - x) ** 2 / u + (y - z) ** 2 / v
    rhs = (u + v) / (u * v) * (z - m) ** 2 + (y - x) ** 2 / (u + v)
    print(f"z={z}: lhs={lhs} rhs={rhs} equal={lhs == rhs} (page form (4z^2-2z+1)/3 -> {(4*z*z-2*z+1)/3})")

print("== L05 M1: integral of p_1(0,z) p_1(z,0) and p_2(0,0) ==")
print("1/(2 sqrt pi) =", f"{1 / (2 * math.sqrt(math.pi)):.12f}", " (4 pi)^(-1/2)=", f"{(4 * math.pi) ** -0.5:.12f}")

print("== L05 Q4: p_1(0,0) ==")
print("(2 pi)^(-1/2) =", f"{(2 * math.pi) ** -0.5:.10f}")

print("== L05 Q9 / P2: Phi(-1/sqrt2) ==")
phi = 0.5 * math.erfc((1 / math.sqrt(2)) / math.sqrt(2))
print("Phi(-1/sqrt2) =", f"{phi:.10f}")

print("== L05 Chapman-Kolmogorov quadrature in Decimal (prec 60), 225 cases, Simpson 2000 intervals ==")
TIMES = (Decimal("0.5"), Decimal(1), Decimal(2))
POINTS = (Decimal(-1), Decimal("-0.25"), Decimal(0), Decimal("0.5"), Decimal(1))
LOWER, UPPER = Decimal(-12), Decimal(12)
worst_dec = Decimal(0)
worst_float = 0.0
worst_float_case = None
n_cases = 0
float_gap_max_dec = Decimal(0)
for s in TIMES:
    for t in TIMES:
        for x in POINTS:
            for y in POINTS:
                quad = dsimpson(lambda z: dpdf(s, x, z) * dpdf(t, z, y), LOWER, UPPER, 2000)
                exact = dpdf(s + t, x, y)
                gap = quad - exact
                n_cases += 1
                if abs(gap) > worst_dec:
                    worst_dec = abs(gap)
print("cases:", n_cases)
print("max |Simpson(60-digit) - exact| =", f"{float(worst_dec):.3e}")
print("max |Simpson(60-digit) - exact| / 2.22e-16 =", f"{float(worst_dec) / 2.220446049250313e-16:.3f}")

print("== L05 E1: tail mass ratio ==")
tail_printed = 3.81e-29
gap_printed = 5.55e-16
print("gap / tail =", f"{gap_printed / tail_printed:.4e}")

print("== L06 combinatorics: Parts A-E, independent implementation ==")
def walks(n: int):
    for steps in product((1, -1), repeat=n):
        s = 0
        top = 0
        for e in steps:
            s += e
            top = max(top, s)
        yield top, s


triples = 0
eq_a = 0
pairs = 0
eq_b = 0
for n in range(1, 13):
    data = list(walks(n))
    end_counts: dict[int, int] = {}
    for _, s in data:
        end_counts[s] = end_counts.get(s, 0) + 1
    for a in range(1, n + 1):
        cnt_max_ge = {}
        for top, s in data:
            if top >= a:
                cnt_max_ge[s] = cnt_max_ge.get(s, 0) + 1
        for b in range(-n, a):
            triples += 1
            eq_a += cnt_max_ge.get(b, 0) == end_counts.get(2 * a - b, 0)
        pairs += 1
        m_ge = sum(1 for top, _ in data if top >= a)
        ge = sum(1 for _, s in data if s >= a)
        gt = sum(1 for _, s in data if s > a)
        eq_b += m_ge == ge + gt
print(f"Part A: triples={triples} equal={eq_a} (page: 1014)")
print(f"Part B: pairs={pairs} equal={eq_b} (page: 78)")

data12 = list(walks(12))
print("Part C: #M12>=3 =", sum(1 for top, _ in data12 if top >= 3), "of", 2**12, "(page: 1588 of 4096)")
print("Part C: #M12>=3 and S12=2 =", sum(1 for top, s in data12 if top >= 3 and s == 2), "(page: 495)")
print("Part C: #S12=4 =", sum(1 for _, s in data12 if s == 4), "(page: 495)")
print("Part C: #S12=2 =", sum(1 for _, s in data12 if s == 2))

data10 = list(walks(10))
tot = 2**10
tail = Fraction(sum(1 for top, _ in data10 if top >= 2), tot)
above = Fraction(sum(1 for _, s in data10 if s > 2), tot)
at = Fraction(sum(1 for _, s in data10 if s == 2), tot)
print("Part D: P(M10>=2) =", tail, "(page 281/512)")
print("Part D: 2P(S10>2) =", 2 * above, "(page 11/32)")
print("Part D: P(S10=2) =", at, "(page 105/512)")
print("Part D: difference equals P(S10=2):", tail - 2 * above == at)
print("Part D: binomial C(10,6)/1024 =", Fraction(math.comb(10, 6), 1024))

print("== L06 Part E / Cor 2.6 ==")
erfc_val = math.erfc(1 / math.sqrt(2))
print("erfc(1/sqrt2) =", f"{erfc_val:.12f}", " rounded 10:", f"{erfc_val:.10f}", " half:", f"{erfc_val / 2:.12f}")
print("P(B_1 >= 1) rounded 4:", f"{erfc_val / 2:.4f}", " erfc rounded 4:", f"{erfc_val:.4f}")
print("Q8 0.1587 within 1e-4:", abs(erfc_val / 2 - 0.1587) <= 1e-4)
print("Q4 0.3173 within 1e-4:", abs(erfc_val - 0.3173) <= 1e-4)

print("== L06 M1 (N=3, a=1): count of M3>=1 ==")
d3 = list(walks(3))
print("M3>=1 count:", sum(1 for top, _ in d3 if top >= 1), "of 8 (page: 5)")
print("S3>=1:", sum(1 for _, s in d3 if s >= 1), "S3>1:", sum(1 for _, s in d3 if s > 1))

print("== L06 M3 worked path ==")
steps = (1, 1, -1, -1, 1)
s = [0]
for e in steps:
    s.append(s[-1] + e)
kappa = next(k for k, v in enumerate(s) if v == 2)
refl = list(steps[:kappa]) + [-e for e in steps[kappa:]]
sp = [0]
for e in refl:
    sp.append(sp[-1] + e)
print("S =", s, "kappa =", kappa, "reflected steps =", tuple(refl), "S' =", sp)
print("Lemma 1.2 check 2a-S_k for k>=kappa:", [4 - v for v in s[kappa:]], "vs S'", sp[kappa:])
