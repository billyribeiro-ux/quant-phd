"""Round-2 slice-a independent re-derivation of the numbers on L01-L04 and the hub (exact Fractions, plus one numeric integral).

Run from the repository root: .venv/bin/python -I ledgers/M4/scripts/M4-a-r2/m4a_r2_numbers.py
"""

import math
from fractions import Fraction as F
import itertools

OK = []
BAD = []


def check(name, got, want):
    (OK if got == want else BAD).append(f"{name}: got {got} want {want}")


def mean(law):
    return sum(v * p for v, p in law)


def cm(law, k):
    mu = mean(law)
    return sum((v - mu) ** k * p for v, p in law)


# ---- L03 Example 2.5 (Bernoulli) ----
for p in (F(1, 10), F(1, 4)):
    q = 1 - p
    bern = ((0, q), (1, p))
    m2, m3, m4 = cm(bern, 2), cm(bern, 3), cm(bern, 4)
    check(f"Bern m2=pq p={p}", m2, p * q)
    check(f"Bern m3 formula p={p}", m3, p * q * (q - p))
    check(f"Bern m4 formula p={p}", m4, p * q * (1 - 3 * p * q))
    check(f"Bern kurt p={p}", m4 / m2**2, (1 - 3 * p * q) / (p * q))
check("kurt Bern 1/10", (1 - 3 * F(9, 100)) / F(9, 100), F(73, 9))
check("kurt Bern 1/4", (1 - 3 * F(3, 16)) / F(3, 16), F(7, 3))
check("skew Bern 1/10 squared", ((1 - 2 * F(1, 10)) ** 2) / F(9, 100), F(64, 9))
check("skew Bern 1/10 value", (F(4, 5)) / F(3, 10), F(8, 3))
check("M1 gamma3 p=1/4 is 2/sqrt3", round((F(1, 2)) / math.sqrt(3 / 16), 9), round(2 / math.sqrt(3), 9))

# ---- L03 section 3 skewed law ----
SK = ((0, F(1, 2)), (1, F(1, 4)), (2, F(1, 8)), (10, F(1, 8)))
check("skew law sums to 1", sum(p for _, p in SK), 1)
check("skew law mean", mean(SK), F(7, 4))
check("skew law m2", cm(SK, 2), F(163, 16))
check("skew law m3", cm(SK, 3), F(2157, 32))
check("skew law m4", cm(SK, 4), F(149461, 256))
check("skew law kurt", cm(SK, 4) / cm(SK, 2) ** 2, F(149461, 26569))
check("skew law skew^2", cm(SK, 3) ** 2 / cm(SK, 2) ** 3, F(18610596, 4330747))
check("term 10 alone", (F(33, 4)) ** 3 * F(1, 8), F(35937, 512))
check("the other three terms", (F(-7, 4)) ** 3 * F(1, 2) + (F(-3, 4)) ** 3 * F(1, 4) + (F(1, 4)) ** 3 * F(1, 8), F(-1425, 512))

# ---- L03 section 4 law ----
S4 = ((-2, F(2, 5)), (1, F(1, 2)), (3, F(1, 10)))
check("S4 mean", mean(S4), 0)
check("S4 m2", cm(S4, 2), 3)
check("S4 m3", cm(S4, 3), 0)
check("S4 m4", cm(S4, 4), 15)
check("S4 kurt", cm(S4, 4) / cm(S4, 2) ** 2, F(5, 3))
check("S4 reflection of -2 about 0 is 2 with prob 0", sum(p for v, p in S4 if v == 2), 0)

# ---- L03 Prop 2.8: numeric spot check of the Gaussian moments ----
def phi(z):
    return math.exp(-z * z / 2) / math.sqrt(2 * math.pi)


def integ(f, a=-40.0, b=40.0, n=400000):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


m0 = integ(phi)
m2n = integ(lambda z: z * z * phi(z))
m4n = integ(lambda z: z**4 * phi(z))
print(f"numeric int phi = {m0:.12f}, int z^2 phi = {m2n:.12f}, int z^4 phi = {m4n:.12f}")
assert abs(m0 - 1) < 1e-9 and abs(m2n - 1) < 1e-9 and abs(m4n - 3) < 1e-8

# ---- L01 quantile and CDF table (Example 3.6 and lab) ----
L1 = ((-2, F(1, 10)), (-1, F(2, 10)), (0, F(3, 10)), (1, F(2, 10)), (2, F(1, 10)), (3, F(1, 10)))
def cdf(x):
    return sum(p for v, p in L1 if v <= x)
check("F values", [cdf(x) for x in range(-2, 4)], [F(1, 10), F(3, 10), F(3, 5), F(4, 5), F(9, 10), 1])
def Q(p):
    return min(v for v, _ in L1 if cdf(v) >= p)
for p, want in [(F(1, 2), 0), (F(3, 5), 0), (F(61, 100), 1), (F(9, 10), 2), (F(99, 100), 3), (F(11, 100), -1), (F(1, 10), -2), (F(91, 100), 3), (F(1), 3)]:
    check(f"Q({p})", Q(p), want)
grid = [F(j, 100) for j in range(1, 101)]
check("F(Q(p))>=p on grid", sum(cdf(Q(p)) >= p for p in grid), 100)
check("index 0.99*150", math.ceil(F(99, 100) * 150), 149)
check("index 0.99*200", math.ceil(F(99, 100) * 200), 198)
check("148/150 < 0.99", F(148, 150) < F(99, 100), True)
check("150 values 148/150 = 74/75", F(148, 150), F(74, 75))
check("strict rule Q^s(3/5)=1", min(v for v, _ in L1 if cdf(v) > F(3, 5)), 1)
check("M2 quantile 0.7 (values 2,5,7)", min(v for v, _ in ((2, F(1, 5)), (5, F(1, 2)), (7, F(3, 10))) if sum(p for w, p in ((2, F(1, 5)), (5, F(1, 2)), (7, F(3, 10))) if w <= v) >= F(7, 10)), 5)
check("40 values index 0.901", math.ceil(F(901, 1000) * 40), 37)

# ---- L02 die and loss ----
DIE = tuple((k, F(1, 6)) for k in range(1, 7))
LOSS = ((0, F(19, 20)), (250000, F(1, 20)))
check("die E", mean(DIE), F(7, 2))
check("die E[X^2]", sum(v * v * p for v, p in DIE), F(91, 6))
check("die Var", cm(DIE, 2), F(35, 12))
check("die Var(2X)", cm(tuple((2 * v, p) for v, p in DIE), 2), F(35, 3))
check("loss E", mean(LOSS), 12500)
check("loss E[L^2]", sum(v * v * p for v, p in LOSS), 3125000000)
check("loss Var", cm(LOSS, 2), 2968750000)
check("loss sd", round(math.sqrt(2968750000), 2), 54486.24)
check("D=L/100 variance", cm(tuple((F(v, 100), p) for v, p in LOSS), 2), F(296875))
check("sd of 2-point 0/50000 at 9/10,1/10", cm(((0, F(9, 10)), (50000, F(1, 10))), 2) ** 0.5, 15000.0)
check("Var(3X-2) = 36 for Var 4", 9 * 4, 36)
check("E[X^2] of two-valued +-1", sum(v * v * p for v, p in ((-1, F(1, 2)), (1, F(1, 2)))), 1)
check("E[X]=0 for +-1", mean(((-1, F(1, 2)), (1, F(1, 2)))), 0)
check("indicator Var 3/10", cm(((0, F(7, 10)), (1, F(3, 10))), 2), F(21, 100))
check("E[L] M2", mean(((0, F(9, 10)), (50000, F(1, 10)))), 5000)

# ---- L02 P3: U=+-1, V=-U ----
U = ((-1, F(1, 2)), (1, F(1, 2)))
V = tuple((-u, p) for u, p in U)
UV = ((0, F(1)),)
check("P3 Var U + Var V", cm(U, 2) + cm(V, 2), 2)
check("P3 Var(U+V)", cm(UV, 2), 0)

# ---- L04 tables ----
DEP = {(0, 0): F(1, 10), (0, 1): F(3, 10), (1, 0): F(2, 10), (1, 1): F(2, 10), (2, 0): F(1, 10), (2, 1): F(1, 10)}
px = {x: sum(p for (a, b), p in DEP.items() if a == x) for x in (0, 1, 2)}
py = {y: sum(p for (a, b), p in DEP.items() if b == y) for y in (0, 1)}
check("DEP px", px, {0: F(2, 5), 1: F(2, 5), 2: F(1, 5)})
check("DEP py", py, {0: F(2, 5), 1: F(3, 5)})
check("DEP E[X]", sum(x * p for x, p in px.items()), F(4, 5))
check("DEP E[X|Y=0]", sum(x * DEP[(x, 0)] for x in (0, 1, 2)) / py[0], 1)
check("DEP E[X|Y=1]", sum(x * DEP[(x, 1)] for x in (0, 1, 2)) / py[1], F(2, 3))
check("DEP total", F(2, 5) * 1 + F(3, 5) * F(2, 3), F(4, 5))
check("DEP cell00 product", px[0] * py[0], F(4, 25))
check("DEP ratio 5/8", DEP[(0, 0)] / (px[0] * py[0]), F(5, 8))
PROD_X = {0: F(1, 5), 1: F(2, 5), 2: F(2, 5)}
PROD_Y = {0: F(3, 10), 1: F(7, 10)}
check("PROD cell00", PROD_X[0] * PROD_Y[0], F(3, 50))
check("uniform Y=X^2 cell00 product", F(1, 3) * F(1, 3), F(1, 9))
check("uniform E[Y]", F(2, 3), F(2, 3))
check("uniform E[XY]", sum(x * x * x for x in (-1, 0, 1)) * F(1, 3), 0)
check("R1 Y=|X| E[Y]", sum(abs(x) for x in (-1, 0, 1)) * F(1, 3), F(2, 3))
check("M1 L04 p(0,0)=0.1 vs 0.3*0.4=0.12", F(3, 10) * F(4, 10), F(12, 100))
check("M2 L04 E[X|Y=1]", F(4, 10) / F(6, 10), F(2, 3))
check("M3 L04 E[XY]", F(1, 4) * F(1, 2), F(1, 8))
check("E3 L04 ratio 5/8", F(1, 10) / F(4, 25), F(5, 8))
check("Cov disjoint -ab", 0 - F(1, 3) * F(1, 4), -F(1, 12))

# ---- Hub placement arithmetic ----
check("placement rung 2 s^2", 1 / (F(5, 3)), F(3, 5))
check("placement rung 1 quantile", F(1, 4) < F(1, 2) <= F(3, 4), True)
check("hours 10 x 9 + 30 = 120", 10 * 9 + 30, 120)
check("hours split 90/120 = 75%", F(90, 120), F(3, 4))
check("placement geometric sum", sum(F(1, 2**k) for k in range(4)), F(15, 8))

print(f"OK {len(OK)}  BAD {len(BAD)}")
for b in BAD:
    print("BAD", b)
