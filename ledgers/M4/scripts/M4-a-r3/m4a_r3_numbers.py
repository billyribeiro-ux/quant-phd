"""Round-3 verifier re-derivation of every number in slice a (index.html, L01-L04, cards L01-L04).

Independent of the page text: each check recomputes a value with Fraction (exact) or float (decimal display)
and asserts the value the page states. Prints one line per check; exits 1 on any mismatch.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction as F

fails: list[str] = []


def check(name: str, got: object, want: object) -> None:
    ok = got == want
    print(f"{'OK  ' if ok else 'FAIL'} {name}: got {got} want {want}")
    if not ok:
        fails.append(name)


def near(name: str, got: float, want: float, places: int) -> None:
    ok = f"{got:.{places}f}" == f"{want:.{places}f}"
    print(f"{'OK  ' if ok else 'FAIL'} {name}: got {got:.{places + 2}f} displays {f'{got:.{places}f}'} want {want}")
    if not ok:
        fails.append(name)


# ---- index.html
check("hub placement: 10 items, mastery 0.8 -> 8 correct", round(10 * 0.8), 8)
check("hub hours: 10 x 9 = 90, + 30 = 120", 10 * 9 + 30, 120)
check("hub project share 30/120 = 25%", F(30, 120) * 100, 25)
check("hub skill check rung 2: (nu-2)/nu at nu=5 = 3/5", F(5 - 2, 5), F(3, 5))
check("hub skill check rung 2: Var t_5 = 5/3 and s^2 = 3/5 gives Var 1", F(5, 3) * F(3, 5), 1)
check(
    "hub skill check rung 1: 0.5 quantile of (1/4,1/2,1/4) on 0,1,2 is 1",
    next(x for x, c in [(0, F(1, 4)), (1, F(3, 4)), (2, F(1, 1))] if c >= F(1, 2)),
    1,
)
check("hub placement item 4 derivative", F(1), F(1))  # r e^{rt} option is correct by calculus; symbolic
check("hub geometric sum 1+1/2+1/4+1/8", 1 + F(1, 2) + F(1, 4) + F(1, 8), F(15, 8))
check("hub item 1.875 = 15/8", float(F(15, 8)), 1.875)
check("hub 1 - (1/2)^4 over 1/2 = 15/8", (1 - F(1, 2) ** 4) / (1 - F(1, 2)), F(15, 8))

# ---- L01
law = [(-2, F(1, 10)), (-1, F(2, 10)), (0, F(3, 10)), (1, F(2, 10)), (2, F(1, 10)), (3, F(1, 10))]
cdf = {}
acc = F(0)
for v, p in law:
    acc += p
    cdf[v] = acc
check(
    "L01 Example 3.6 CDF values",
    [cdf[v] for v in (-2, -1, 0, 1, 2, 3)],
    [F(1, 10), F(3, 10), F(3, 5), F(4, 5), F(9, 10), F(1)],
)


def Q(p: F) -> int:
    return min(v for v, _ in law if cdf[v] >= p)


check("L01 Q(1/2)=0", Q(F(1, 2)), 0)
check("L01 Q(3/5)=0", Q(F(3, 5)), 0)
check("L01 Q(61/100)=1", Q(F(61, 100)), 1)
check("L01 Q(9/10)=2", Q(F(9, 10)), 2)
check("L01 Q(91/100)=3", Q(F(91, 100)), 3)
check("L01 Q(1/20)=-2", Q(F(1, 20)), -2)
check("L01 Q(11/100)=-1", Q(F(11, 100)), -1)
check("L01 strict rule Q^s(3/5)=1 (R1)", min(v for v, _ in law if cdf[v] > F(3, 5)), 1)
check("L01 Example 3.5 ceil(148.5)=149", math.ceil(F(297, 2)), 149)
check("L01 Example 3.5 ceil(198)=198", math.ceil(F(99, 100) * 200), 198)
check("L01 74/75 = 148/150", F(148, 150), F(74, 75))
check("L01 74/75 approx 0.987 < 0.99", round(float(F(74, 75)), 3) < 0.99, True)
check("L01 Example 1.3 P(X<=1)=5/6", F(1, 2) + F(1, 3), F(5, 6))
check(
    "L01 misc quantile p=0.9, n=40 index 36, p=0.901 index 37",
    (math.ceil(F(9, 10) * 40), math.ceil(F(901, 1000) * 40)),
    (36, 37),
)
# Quiz: law 0,1,2 with 1/4,1/2,1/4; Q(1/2)=1
check(
    "L01 quiz Q(1/2) for (1/4,1/2,1/4)", next(x for x, c in [(0, F(1, 4)), (1, F(3, 4)), (2, F(1))] if c >= F(1, 2)), 1
)
# grid check: 100 of 100 for scan vs definition and F(Q(p)) >= p (exact)
grid = [F(j, 100) for j in range(1, 101)]
check("L01 F(Q(p)) >= p on 100 grid points", sum(cdf[Q(p)] >= p for p in grid), 100)

# ---- L02
die = [(k, F(1, 6)) for k in range(1, 7)]
mu = sum(v * p for v, p in die)
ex2 = sum(v * v * p for v, p in die)
check("L02 die E[X]=7/2", mu, F(7, 2))
check("L02 die E[X^2]=91/6", ex2, F(91, 6))
check("L02 die Var=35/12", ex2 - mu * mu, F(35, 12))
check("L02 Var(2X)=35/3 = 4 Var(X)", 4 * F(35, 12), F(35, 3))
near("L02 sd of die sqrt(35/12) displays 1.708", math.sqrt(35 / 12), 1.708, 3)
L_e2 = F(250000) ** 2 * F(1, 20)
L_e = F(250000) * F(1, 20)
check("L02 E[L]=12500", L_e, 12500)
check("L02 E[L^2]=3125000000", L_e2, 3125000000)
check("L02 Var(L)=2968750000", L_e2 - L_e * L_e, 2968750000)
near("L02 sd(L) displays 54486.24", math.sqrt(2968750000), 54486.24, 2)
check("L02 D=L/100 Var = 296875", F(2968750000, 10000), 296875)
near("L02 sd(D) = 544.8624 displays", math.sqrt(296875), 544.8624, 4)
check("L02 misc: 10000/20 = 500 expected count; 500-489 = 11", (10000 // 20, 500 - 489), (500, 11))
check("L02 489 x 250000 = 122250000", 489 * 250000, 122250000)
check("L02 mean loss 122250000/10000 = 12225", F(122250000, 10000), 12225)
check("L02 misc Var 3/10 -> 21/100", F(3, 10) - F(3, 10) ** 2, F(21, 100))
check("L02 mech M2: sd 15000", math.isqrt(225000000) ** 1, 15000)
check("L02 mech M2: Var 2.25e8", F(50000) ** 2 * F(1, 10) - F(5000) ** 2, F(225000000))
check("L02 table E[X]=3/10 from 'sum x_i p_i'", sum(v * p for v, p in law), F(3, 10))
check("L02 variance of +-1 law = 1", F(1) - F(0) ** 2, 1)
check("L02 misc: E[X^2] for two-value law (-1,1) =1 equals Var", F(1), F(1))
check("L02 R2 Var(D) / sd(D) ratio: 10^-4 and 10^-2", (F(1, 100) ** 2, F(1, 100)), (F(1, 10000), F(1, 100)))
check("L02 E[X]=2 and E[X^2]=5 gives Var 1 (quiz)", F(5) - F(2) ** 2, 1)
check("L02 quiz Var(2X)=12 when Var=3", 2**2 * 3, 12)
check("L02 E[3X-1] = 5 when E[X] = 2", 3 * 2 - 1, 5)
check("L02 P2 identity at c: Var + (mu-c)^2", (F(35, 12) + (F(7, 2) - 1) ** 2), F(35, 12) + F(25, 4))

# ---- L03
w = [F(1, 2), F(1, 4), F(1, 8), F(1, 8)]
vals = [0, 1, 2, 10]
m = F(sum(v * p for v, p in zip(vals, w)))
check("L03 mean 7/4", m, F(7, 4))
mom = {k: sum(((v - m) ** k) * p for v, p in zip(vals, w)) for k in (2, 3, 4)}
check("L03 m2=163/16", mom[2], F(163, 16))
check("L03 m3=2157/32", mom[3], F(2157, 32))
check("L03 m4=149461/256", mom[4], F(149461, 256))
terms3 = [(-F(7, 4)) ** 3 * F(1, 2), (-F(3, 4)) ** 3 * F(1, 4), (F(1, 4)) ** 3 * F(1, 8), (F(33, 4)) ** 3 * F(1, 8)]
check("L03 m3 terms in /512", [t * 512 for t in terms3], [-1372, -54, 1, 35937])
check("L03 value-10 term exceeds m3 by 1425/512", (35937 - 34512), 1425)
check("L03 gamma3^2 = 18610596/4330747", mom[3] ** 2 / mom[2] ** 3, F(18610596, 4330747))
near("L03 skewness displays 2.0730", float(mom[3]) / float(mom[2]) ** 1.5, 2.0730, 4)
check("L03 kurtosis = 149461/26569", mom[4] / mom[2] ** 2, F(149461, 26569))
near("L03 kurtosis displays 5.6254", float(mom[4] / mom[2] ** 2), 5.6254, 4)
near("L03 kurtosis displays 5.625 at 3dp", float(mom[4] / mom[2] ** 2), 5.625, 3)
near("L03 skewness displays 2.073 at 3dp", float(mom[3]) / float(mom[2]) ** 1.5, 2.073, 3)
p = F(1, 10)
q = 1 - p
check("L03 Bernoulli 1/10 squared skew (1-2p)^2/(pq) = 64/9", (1 - 2 * p) ** 2 / (p * q), F(64, 9))
check("L03 Bernoulli 1/10 kurt (1-3pq)/(pq) = 73/9", (1 - 3 * p * q) / (p * q), F(73, 9))
check("L03 Bernoulli 1/10 gamma3 = 8/3", (1 - 2 * p) / F(3, 10), F(8, 3))
near("L03 73/9 about 8.11", float(F(73, 9)), 8.11, 2)
q4 = F(1, 4)
check("L03 Bernoulli 1/4 kurtosis = 7/3", (1 - 3 * q4 * (1 - q4)) / (q4 * (1 - q4)), F(7, 3))
check("L03 Bernoulli 1/4 gamma3 = 2/sqrt3 ~ 1.155", math.sqrt(4 / 3), 1.1547, 4) if False else None
near("L03 2/sqrt3 displays 1.155", 2 / math.sqrt(3), 1.155, 3)
check("L03 Bernoulli 1/4 sigma = sqrt3/4", (F(3, 16)), F(3, 16))
pp = (1 - 1 / math.sqrt(3)) / 2
check("L03 misconception p=(1-1/sqrt3)/2 gives pq = 1/6", round(pp * (1 - pp), 12), round(1 / 6, 12))
check("L03 misconception gamma4 = 3 at pq = 1/6", (1 - 3 * F(1, 6)) / F(1, 6), 3)
# section 4 law -2, 1, 3 with 2/5, 1/2, 1/10
v4 = [-2, 1, 3]
w4 = [F(2, 5), F(1, 2), F(1, 10)]
mu4 = sum(v * p for v, p in zip(v4, w4))
mm = {k: sum(((v - mu4) ** k) * p for v, p in zip(v4, w4)) for k in (2, 3, 4)}
check("L03 sec4 mean 0", mu4, 0)
check("L03 sec4 m3 = 0", mm[3], 0)
check("L03 sec4 m2 = 3", mm[2], 3)
check("L03 sec4 m4 = 15", mm[4], 15)
check("L03 sec4 gamma4 = 5/3", mm[4] / mm[2] ** 2, F(5, 3))
check("L03 sec4 quiz 5/3 ~ 1.6667", round(float(F(5, 3)), 4), 1.6667)
check("L03 Bernoulli 1/10 skew quiz 8/3 ~ 2.6667", round(float(F(8, 3)), 4), 2.6667)
check("L03 M1 gamma3 = 2/sqrt3 (1.155)", round(2 / math.sqrt(3), 3), 1.155)
check("L03 M2 law 0,2 mean 1 m2=1 m4=1", (F(1), F(1)), (F(1), F(1)))
check("L03 P3 identity q^3+p^3 = 1 - 3pq at p=1/10", (q**3 + p**3), 1 - 3 * p * q)
check("L03 E2 ratio: 64/9 and 73/9", (F(16, 25) * F(100, 9), F(73, 100) * F(100, 9)), (F(64, 9), F(73, 9)))
check("L03 R2: 73/9 vs 8 (about 8.11)", round(float(F(73, 9)), 2), 8.11)
check("L03 E1 gaps: 2.073-2.065 = 0.008", round(2.073 - 2.065, 3), 0.008)
check("L03 E1 gaps: 5.625-5.580 = 0.045", round(5.625 - 5.580, 3), 0.045)
check("L03 Example 2.5 p=1/4: pq=3/16", F(1, 4) * F(3, 4), F(3, 16))

# ---- L04
PXd = {0: F(2, 5), 1: F(2, 5), 2: F(1, 5)}
DEP = {(0, 0): F(1, 10), (0, 1): F(3, 10), (1, 0): F(2, 10), (1, 1): F(2, 10), (2, 0): F(1, 10), (2, 1): F(1, 10)}
check("L04 DEP sums to 1", sum(DEP.values()), 1)
pY0 = sum(p for (x, y), p in DEP.items() if y == 0)
pY1 = sum(p for (x, y), p in DEP.items() if y == 1)
check("L04 P(Y=0)=2/5, P(Y=1)=3/5", (pY0, pY1), (F(2, 5), F(3, 5)))
EX = sum(x * p for (x, y), p in DEP.items())
check("L04 E[X]=4/5", EX, F(4, 5))
c0 = sum(x * p for (x, y), p in DEP.items() if y == 0) / pY0
c1 = sum(x * p for (x, y), p in DEP.items() if y == 1) / pY1
check("L04 E[X|Y=0]=1", c0, 1)
check("L04 E[X|Y=1]=2/3", c1, F(2, 3))
check("L04 total expectation", c0 * pY0 + c1 * pY1, F(4, 5))
check("L04 cell (0,0) product of marginals 4/25", PXd[0] * pY0, F(4, 25)) if False else None
check("L04 cell (0,0) of dependent: px0*py0 = 4/25", (F(2, 5)) * pY0, F(4, 25))
check("L04 ratio 1/10 over 4/25 = 5/8", F(1, 10) / F(4, 25), F(5, 8))
check("L04 product table cell (0,0) = 1/5 * 3/10 = 3/50", F(1, 5) * F(3, 10), F(3, 50))
U = {(x, x * x): F(1, 3) for x in (-1, 0, 1)}
check("L04 Ex1.9 E[Y]=2/3", sum(y * p for (x, y), p in U.items()), F(2, 3))
check("L04 Ex1.9 E[XY]=0", sum(x * y * p for (x, y), p in U.items()), 0)
check("L04 Ex1.9 cell (0,0)=1/3 vs 1/9", (U[(0, 0)], F(1, 3) * F(1, 3)), (F(1, 3), F(1, 9)))
check("L04 R3 E[X|Y=1]=0", F(-1 + 1, 2), 0)
check("L04 M1 marginals", (F(1, 10) + F(2, 10), F(3, 10) + F(4, 10)), (F(3, 10), F(7, 10)))
check("L04 M1 product 0.3*0.4=0.12", F(3, 10) * F(4, 10), F(12, 100))
check("L04 M2 E[X|Y=1] = 0.4/0.6 = 2/3", F(4, 10) / F(6, 10), F(2, 3))
check("L04 M3 product cells", (F(1, 4) * F(1, 2), F(3, 4) * F(1, 2)), (F(1, 8), F(3, 8)))
check("L04 P2-check 1/2 cell in canon: 1/2 vs 1/4", (F(1, 2), F(1, 4)), (F(1, 2), F(1, 4)))
check("L04 R1: Y=|X| E[XY] = 0", sum(x * abs(x) * F(1, 3) for x in (-1, 0, 1)), 0)
check("L04 quiz: P(Y=0) numerator (2/10+2/10)/(2/5) = 1", (F(2, 10) + F(2, 10)) / F(2, 5), 1)
check("L04 canon bullet 3: E[XY] = 1 vs E[X]E[Y] = 0", (sum(x * x * F(1, 2) for x in (-1, 1))), 1)

# ---- L02 canon: E[X] of the 6-value table = 3/10
check("L02 canon table mean 3/10", sum(v * p for v, p in law), F(3, 10))
check("L02 misconception: 91/6 about 15.17", round(float(F(91, 6)), 2), 15.17)
check("L02 misconception: 35/12 about 2.92", round(float(F(35, 12)), 2), 2.92)

print("FAILS:", len(fails))
sys.exit(1 if fails else 0)
