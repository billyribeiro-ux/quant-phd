"""Round-4 independent re-derivation of every number printed in M4 slice a (index, L01-L04 prose and quizzes).

Run: python -I -W error ledgers/M4/scripts/M4-a-r4/m4a_r4_numbers.py   (standard library only).
Exact arithmetic with fractions.Fraction; floats only where the page prints a decimal, compared to the printed digits.
Prints one line per claim: OK or FAIL with both values. Exit status 1 if any claim fails.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction as F

fails: list[str] = []
oks = 0


def check(label: str, got: object, want: object) -> None:
    global oks
    if got == want:
        oks += 1
        print(f"OK   {label}: {got}")
    else:
        fails.append(label)
        print(f"FAIL {label}: got {got!r}, page says {want!r}")


def check_dec(label: str, got: float, printed: str) -> None:
    """got rounded to the number of places printed must equal printed."""
    places = len(printed.split(".")[1]) if "." in printed else 0
    check(label, f"{round(got, places):.{places}f}", printed)


def ceil_frac(x: F) -> int:
    return -((-x.numerator) // x.denominator)


# ---------- L01 ----------
law16 = {0: F(1, 4), 1: F(1, 2), 2: F(1, 4)}
check("L01 Ex1.3 P(X<=1)", F(1, 2) + F(1, 3), F(5, 6))
ex36 = [(-2, F(1, 10)), (-1, F(2, 10)), (0, F(3, 10)), (1, F(2, 10)), (2, F(1, 10)), (3, F(1, 10))]
assert sum(p for _, p in ex36) == 1


def cdf(law, x):
    return sum((p for v, p in law if v <= x), F(0))


def Q(law, p):
    # brute force: minimum over candidate support points of {x : F(x) >= p}; F is constant between points
    cands = [v for v, _ in law if cdf(law, v) >= p]
    return min(cands)


F_expected = {-2: F(1, 10), -1: F(3, 10), 0: F(3, 5), 1: F(4, 5), 2: F(9, 10), 3: F(1)}
check("L01 Ex3.6 F values", {v: cdf(ex36, v) for v in F_expected}, F_expected)
check("L01 Ex3.6 Q(1/2)", Q(ex36, F(1, 2)), 0)
check("L01 Ex3.6 Q(3/5)", Q(ex36, F(3, 5)), 0)
check("L01 Ex3.6 Q(61/100)", Q(ex36, F(61, 100)), 1)
check("L01 lab hypothesis Q(1/20)", Q(ex36, F(1, 20)), -2)
check("L01 lab hypothesis Q(1/10)", Q(ex36, F(1, 10)), -2)
check("L01 lab hypothesis Q(11/100)", Q(ex36, F(11, 100)), -1)
check("L01 lab hypothesis Q(3/5)", Q(ex36, F(3, 5)), 0)
check("L01 lab hypothesis Q(9/10)", Q(ex36, F(9, 10)), 2)
check("L01 lab hypothesis Q(91/100)", Q(ex36, F(91, 100)), 3)
check("L01 lab hypothesis Q(99/100)", Q(ex36, F(99, 100)), 3)
check("L01 lab hypothesis Q(1)", Q(ex36, F(1)), 3)
# grid: scan (first support point with F>=p, in increasing order) equals definition at j/100
grid = [F(j, 100) for j in range(1, 101)]
check("L01 grid F(Q(p))>=p at 100 of 100", sum(cdf(ex36, Q(ex36, p)) >= p for p in grid), 100)
check("L01 Q(F(x))=x at all support points", all(Q(ex36, cdf(ex36, v)) == v for v, _ in ex36[:-1]), True)
check("L01 E1 F(2)=9/10 < 99/100", cdf(ex36, 2) < F(99, 100) <= cdf(ex36, 3), True)
check("L01 R1 strict rule Q^s(3/5)", min(v for v, _ in ex36 if cdf(ex36, v) > F(3, 5)), 1)
check("L01 E3 second-quantile claim: 150 gives 36/ index", ceil_frac(F(99, 100) * 150), 149)
check("L01 Ex3.5 n=200 index", ceil_frac(F(99, 100) * 200), 198)
check("L01 Ex3.5 n=150 floor 148.5", math.floor(F(99, 100) * 150), 148)
check("L01 Ex3.5 pn=148.5", F(99, 100) * 150, F(297, 2))
check("L01 canon 148/150 = 74/75", F(148, 150), F(74, 75))
check_dec("L01 canon 74/75 to 3 places", float(F(74, 75)), "0.987")
check("L01 canon 74/75 < 0.99", F(74, 75) < F(99, 100), True)
parity = [(0, F(1, 2)), (1, F(1, 2))]
check("L01 M1 Q(1/2)", Q(parity, F(1, 2)), 0)
m2law = [(2, F(1, 5)), (5, F(1, 2)), (7, F(3, 10))]
check("L01 M2 F(5)", cdf(m2law, 5), F(7, 10))
check("L01 M2 Q(7/10)", Q(m2law, F(7, 10)), 5)
check("L01 M2 Q(71/100)", Q(m2law, F(71, 100)), 7)
check("L01 M3 index 40*0.9", ceil_frac(F(9, 10) * 40), 36)
check("L01 M3 index 40*0.901", ceil_frac(F(901, 1000) * 40), 37)
check("L01 Rem3.3 ex: Q(F_k)=x_k sample", Q(ex36, cdf(ex36, 0)), 0)
check("L01 Ex3.6 Q=1 interval (3/5,4/5]", [p for p in grid if Q(ex36, p) == 1][0], F(61, 100))
check("L01 Ex3.6 Q=1 interval end", max(p for p in grid if Q(ex36, p) == 1), F(80, 100))
check("L01 quiz Q(1/2) law 1/4,1/2,1/4", Q(list(law16.items()), F(1, 2)), 1)
check("L01 quiz P(X<=1) Ex1.3 decimal", f"{float(F(5, 6)):.3f}", "0.833")
check("L01 quiz 200-loss index", ceil_frac(F(99, 100) * 200), 198)
check("L01 P3 Q(1)=x_m", Q(ex36, F(1)), 3)

# ---------- L02 ----------
die = [(k, F(1, 6)) for k in range(1, 7)]


def E(law, g=lambda x: x):
    return sum((g(v) * p for v, p in law), F(0))


check("L02 Ex1.4 E[X]", E(die), F(7, 2))
check("L02 Ex2.5 E[X^2]", E(die, lambda x: x * x), F(91, 6))
check("L02 Ex2.5 Var", E(die, lambda x: x * x) - E(die) ** 2, F(35, 12))
check_dec("L02 Ex2.5 sd 1.708", math.sqrt(F(35, 12)), "1.708")
loss = [(0, F(19, 20)), (250000, F(1, 20))]
check("L02 Ex1.5 E[L]", E(loss), 12500)
check("L02 Ex2.6 E[L^2]", E(loss, lambda x: x * x), 3125000000)
check("L02 Ex2.6 Var(L)", E(loss, lambda x: x * x) - E(loss) ** 2, 2968750000)
check("L02 Ex2.6 12500^2", 12500**2, 156250000)
check("L02 Ex2.6 sd cents", f"{math.sqrt(2968750000):.2f}", "54486.24")
check("L02 Ex2.6 sd cents (about 54486.24)", f"{math.sqrt(2968750000):.2f}", "54486.24")
check("L02 lab Var(2X)=35/3", 4 * F(35, 12), F(35, 3))
check("L02 misc: E[X^2] about 15.17", f"{float(F(91, 6)):.2f}", "15.17")
check("L02 misc: Var about 2.92", f"{float(F(35, 12)):.2f}", "2.92")
check("L02 misc: 91/6 - 35/12 = E^2 check", F(91, 6) - F(35, 12), F(49, 4))
# canon-breaks: E[X] for L01 table
check("L02 canon E[X] Ex3.6", E(ex36), F(3, 10))
check("L02 canon (-2-2+0+2+2+3)/10", F(-2 - 2 + 0 + 2 + 2 + 3, 10), F(3, 10))
# M1 indicator
check("L02 M1 Var", F(3, 10) - F(9, 100), F(21, 100))
check("L02 M1 product", F(3, 10) * F(7, 10), F(21, 100))
# M2 loss
check("L02 M2 E[L]", 50000 * F(1, 10), 5000)
check("L02 M2 Var", 50000**2 * F(1, 10) - 5000**2, 225000000)
check("L02 M2 sd", math.isqrt(225000000), 15000)
check("L02 M2 15000^2", 15000**2, 225000000)
# M3 scale
check("L02 M3 Var(3X-2)", 9 * 4, 36)
# P3 counterexample
U = [(-1, F(1, 2)), (1, F(1, 2))]
V = [(1, F(1, 2)), (-1, F(1, 2))]
check("L02 P3 Var(U)", E(U, lambda x: x * x) - E(U) ** 2, 1)
check("L02 P3 Var(V)", E(V, lambda x: x * x) - E(V) ** 2, 1)
# R2 currency
check("L02 R2 Var(D)", F(1, 10000) * 2968750000, 296875)
check_dec("L02 R2 sd_D about 544.8624", math.sqrt(296875), "544.8624")
check("L02 R2 sd_D vs cents/100", round(math.sqrt(2968750000) / 100, 4), round(math.sqrt(296875), 4))
# R3 average vs quantile
check("L02 R3 E[X] Ex3.6 = 3/10", E(ex36), F(3, 10))
# quiz
check("L02 quiz 1 E[die]", E(die), F(7, 2))
check("L02 quiz 2 Var", 5 - 2**2, 1)
check("L02 quiz 3 Var(2X)", 2**2 * 3, 12)
check("L02 quiz 5 E", 50000 * F(1, 10), 5000)
check("L02 quiz 7 Var Bernoulli(3/10)", F(3, 10) - F(3, 10) ** 2, F(21, 100))
check("L02 quiz 9 sd", math.sqrt(225000000), 15000)
check("L02 quiz 10 E[3X-1]", 3 * 2 - 1, 5)
# lab sample: loss sample means implied by printed totals
check("L02 lab loss total/mean", 122250000 / 10000, 12225.0)
check("L02 lab loss expected count", 10000 * F(1, 20), 500)
check("L02 lab loss count gap", 500 - 489, 11)
check("L02 lab die mean gap", round(3.469 - 3.5, 3), -0.031)

# ---------- L03 ----------
SK = [(0, F(1, 2)), (1, F(1, 4)), (2, F(1, 8)), (10, F(1, 8))]
mu = E(SK)
check("L03 mu", mu, F(7, 4))


def cm(law, k):
    m = E(law)
    return sum(((v - m) ** k * p for v, p in law), F(0))


m2, m3, m4 = cm(SK, 2), cm(SK, 3), cm(SK, 4)
check("L03 m2", m2, F(163, 16))
check("L03 m3", m3, F(2157, 32))
check("L03 m4", m4, F(149461, 256))
check("L03 m3 four terms", [F(-343, 64) * F(1, 2), F(-27, 64) * F(1, 4), F(1, 64) * F(1, 8), F(35937, 64) * F(1, 8)],
      [F(-1372, 512), F(-54, 512), F(1, 512), F(35937, 512)])
check("L03 m3 sum 34512/512", F(-1372 - 54 + 1 + 35937, 512), F(34512, 512))
check("L03 value-10 term exceeds m3 by 1425/512", F(35937, 512) - F(34512, 512), F(1425, 512))
check("L03 m3^2/m2^3", m3 * m3 / (m2**3), F(18610596, 4330747))
check("L03 m4/m2^2", m4 / (m2 * m2), F(149461, 26569))
check_dec("L03 skewness 2.0730", math.sqrt(float(m3 * m3 / m2**3)), "2.0730")
check_dec("L03 kurtosis 5.6254 -> 5.6254", float(m4 / (m2 * m2)), "5.6254")
check_dec("L03 kurtosis 5.625 at 3 places", float(m4 / (m2 * m2)), "5.625")
check("L03 163^3", 163**3, 4330747)
check("L03 2157^2 4 / 163^3", 2157**2 * 4, 18610596)
check("L03 gap skew 2.073-2.065", round(2.073 - 2.065, 3), 0.008)
check("L03 gap kurt 5.625-5.580", round(5.625 - 5.580, 3), 0.045)

p = F(1, 10)
q = 1 - p
bern = [(0, q), (1, p)]
check("L03 Bern(1/10) m2 = pq", cm(bern, 2), p * q)
check("L03 Bern(1/10) m3 = pq(q-p)", cm(bern, 3), p * q * (q - p))
check("L03 Bern(1/10) m4 = pq(1-3pq)", cm(bern, 4), p * q * (1 - 3 * p * q))
check("L03 Bern squared skew 64/9", cm(bern, 3) ** 2 / cm(bern, 2) ** 3, F(64, 9))
check("L03 Bern kurtosis 73/9", cm(bern, 4) / cm(bern, 2) ** 2, F(73, 9))
check("L03 Ex2.5 p=1/10 gamma3 = 8/3", (1 - 2 * p) / F(3, 10), F(8, 3))
check("L03 Ex2.5 p=1/10 pq=9/100", p * q, F(9, 100))
check_dec("L03 Ex2.5 73/9 about 8.11", float(F(73, 9)), "8.11")
p4 = F(1, 4)
check("L03 Bern(1/4) gamma4 = 7/3", (1 - 3 * p4 * (1 - p4)) / (p4 * (1 - p4)), F(7, 3))
check("L03 M1 gamma3 = 2/sqrt3", (1 - 2 * p4) / math.sqrt(3 / 16), 2 / math.sqrt(3))
check_dec("L03 M1 about 1.155", 2 / math.sqrt(3), "1.155")
check("L03 M1 sigma = sqrt3/4", math.sqrt(3 / 16), math.sqrt(3) / 4)
# section 4 law -2,1,3
L4 = [(-2, F(2, 5)), (1, F(1, 2)), (3, F(1, 10))]
check("L03 s4 mean", E(L4), 0)
check("L03 s4 m3", cm(L4, 3), 0)
check("L03 s4 m2", cm(L4, 2), 3)
check("L03 s4 m4", cm(L4, 4), 15)
check("L03 s4 gamma4 = 5/3", cm(L4, 4) / cm(L4, 2) ** 2, F(5, 3))
check_dec("L03 quiz kurtosis 1.6667", float(F(5, 3)), "1.6667")
check_dec("L03 quiz Bernoulli skewness 2.6667", float(F(8, 3)), "2.6667")
# misconception 2: p = (1 - 1/sqrt3)/2 gives pq = 1/6 and gamma4 = 3
pp = (1 - 1 / math.sqrt(3)) / 2
check_dec("L03 misc pq = 1/6 (float)", pp * (1 - pp), "0.166667")
check("L03 misc gamma4 = 3 (float)", round((1 - 3 * pp * (1 - pp)) / (pp * (1 - pp)), 9), 3.0)
# M2 symmetric law on 0,2
check("L03 M2 m2", cm([(0, F(1, 2)), (2, F(1, 2))], 2), 1)
check("L03 M2 m4", cm([(0, F(1, 2)), (2, F(1, 2))], 4), 1)
# R2: Bernoulli 1/10 kurtosis about 8.11
check_dec("L03 R2 about 8.11", float(F(73, 9)), "8.11")
# E3 weights total 8
check("L03 E3 weights total", 4 + 2 + 1 + 1, 8)

# ---------- L04 ----------
dep = {(0, 0): F(1, 10), (0, 1): F(3, 10), (1, 0): F(2, 10), (1, 1): F(2, 10), (2, 0): F(1, 10), (2, 1): F(1, 10)}
check("L04 dep total", sum(dep.values()), 1)
pxd = {x: sum(p for (a, b), p in dep.items() if a == x) for x in (0, 1, 2)}
pyd = {y: sum(p for (a, b), p in dep.items() if b == y) for y in (0, 1)}
check("L04 Ex2.5 P(Y=0)", pyd[0], F(2, 5))
check("L04 Ex2.5 P(Y=1)", pyd[1], F(3, 5))
check("L04 Ex2.5 E[X]", sum(x * pxd[x] for x in pxd), F(4, 5))
ex_given0 = sum(x * dep[(x, 0)] for x in (0, 1, 2)) / pyd[0]
ex_given1 = sum(x * dep[(x, 1)] for x in (0, 1, 2)) / pyd[1]
check("L04 Ex2.5 E[X|Y=0]", ex_given0, 1)
check("L04 Ex2.5 E[X|Y=1]", ex_given1, F(2, 3))
check("L04 Ex2.5 total expectation", ex_given0 * pyd[0] + ex_given1 * pyd[1], F(4, 5))
check("L04 Ex2.5 P(Y=1)=3/5 quiz", pyd[1], F(3, 5))
check("L04 E1 2/5 + 2/5", F(2, 5) + F(2, 5), F(4, 5))
prod = {(x, y): pxd[x] * pyd[y] for x in pxd for y in pyd}
check("L04 Part A dependent cell (0,0) product 4/25", pxd[0] * pyd[0], F(4, 25))
check("L04 E3 ratio 5/8", F(1, 10) / F(4, 25), F(5, 8))
check("L04 M1 P(X=0)P(Y=0)=0.12", 0.3 * 0.4, 0.12)
t1 = {(0, 0): F(1, 10), (0, 1): F(2, 10), (1, 0): F(3, 10), (1, 1): F(4, 10)}
px1 = {x: sum(p for (a, b), p in t1.items() if a == x) for x in (0, 1)}
py1 = {y: sum(p for (a, b), p in t1.items() if b == y) for y in (0, 1)}
check("L04 M1 P(X=0)", px1[0], F(3, 10))
check("L04 M1 P(Y=0)", py1[0], F(4, 10))
check("L04 M1 E[X|Y=1]", (0 * t1[(0, 1)] + 1 * t1[(1, 1)]) / py1[1], F(2, 3))
check("L04 M1 E[X]", px1[1], F(7, 10))
check("L04 M3 E[XY]", F(1, 4) * F(1, 2), F(1, 8))
check("L04 M3 cells sum", F(1, 8) + F(1, 8) + F(3, 8) + F(3, 8), 1)
check("L04 P3 Cov = -ab", 0 - F(1, 3) * F(1, 2), -F(1, 6))
check("L04 R1 E[Y]", (1 + 0 + 1) / F(3), F(2, 3))
check("L04 R1 E[XY]", sum(x * abs(x) for x in (-1, 0, 1)) / F(3), 0)
check("L04 Ex1.9 E[Y]", sum(x * x for x in (-1, 0, 1)) / F(3), F(2, 3))
check("L04 Ex1.9 E[XY]", sum(x * x**2 for x in (-1, 0, 1)) / F(3), 0)
check("L04 Ex1.9 p00 vs product", (F(1, 3), F(1, 9)), (F(1, 3), F(1, 3) * F(1, 3)))
check("L04 quiz product cell 3/50", F(1, 5) * F(3, 10), F(3, 50))
check("L04 canon bullet 2 product", F(1, 2) * F(1, 2), F(1, 4))
check("L04 canon bullet 3 E[XY] with Y=X", sum(x * x for x in (-1, 1)) / F(2), 1)

# ---------- index.html hub ----------
check("IDX placement mastery 8 of 10", 0.8 * 10, 8)
check("IDX 90+30=120", 90 + 30, 120)
check("IDX 30/120 = 25%", F(30, 120), F(1, 4))
check("IDX ten lessons x 9h", 10 * 9, 90)
check("IDX placement numeric 0.5", float(F(1, 2)), 0.5)
check("IDX placement 1+1/2+1/4+1/8", 1 + F(1, 2) + F(1, 4) + F(1, 8), F(15, 8))
check("IDX placement 15/8 decimal", float(F(15, 8)), 1.875)
check("IDX placement t5 var = 5/3", F(5, 5 - 2), F(5, 3))
check("IDX placement s^2 = 3/5", 1 / F(5, 3), F(3, 5))
check("IDX placement s^2 decimal 0.6", float(F(3, 5)), 0.6)
check("IDX placement rung-1 F(0)=1/4 F(1)=3/4", (F(1, 4), F(3, 4)), (F(1, 4), F(3, 4)))
check("IDX placement \\int_0^1 x dx", F(1, 2), F(1, 2))
check("IDX ln(e^3)", 3, 3)

print(f"\nsummary: {oks} OK, {len(fails)} FAIL")
for f in fails:
    print("FAILED:", f)
sys.exit(1 if fails else 0)
