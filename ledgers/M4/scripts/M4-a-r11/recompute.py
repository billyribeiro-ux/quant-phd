"""Round 11 M4 slice a: independent recomputation of the exact numbers printed or stated in L01-L04 and the hub.

Written from the mathematics, not from the lab code. Run: python3 -I ledgers/M4/scripts/M4-a-r11/recompute.py
"""

import math
import random
from fractions import Fraction as Fr

def q_inf(law, p):
    # Q(p) = inf{x : F(x) >= p} over the support (finite law)
    return min(x for x, _ in law if sum(w for y, w in law if y <= x) >= p)

def F(law, x):
    return sum(w for y, w in law if y <= x)

# ---- L01 ----
L01 = [(-2, Fr(1, 10)), (-1, Fr(2, 10)), (0, Fr(3, 10)), (1, Fr(2, 10)), (2, Fr(1, 10)), (3, Fr(1, 10))]
print("L01 F:", [str(F(L01, x)) for x, _ in L01])
for p in [Fr(1, 20), Fr(1, 10), Fr(11, 100), Fr(1, 2), Fr(3, 5), Fr(61, 100), Fr(9, 10), Fr(91, 100), Fr(99, 100), Fr(1)]:
    print("L01 Q", p, "=", q_inf(L01, p))
ok_grid = all(F(L01, q_inf(L01, Fr(j, 100))) >= Fr(j, 100) for j in range(1, 101))
print("L01 F(Q(p))>=p on grid:", ok_grid)
# Prop 3.4 index check, n=150 and 200 and 40
print("ceil(0.99*150)=", math.ceil(Fr(99, 100) * 150), " ceil(0.99*200)=", math.ceil(Fr(99, 100) * 200))
print("ceil(40*0.9)=", math.ceil(Fr(9, 10) * 40), " ceil(40*0.901)=", math.ceil(Fr(901, 1000) * 40))
print("0.987 check 148/150 =", float(Fr(148, 150)))
# Prop 2.2 / Example 1.3
print("Ex1.3 P(X<=1)=", Fr(1, 2) + Fr(1, 3))
# strict-rule example R1
print("Qs(3/5): least x with F>3/5 =", min(x for x, _ in L01 if F(L01, x) > Fr(3, 5)))
# L01 mech-2: values 2,5,7 probs 1/5,1/2,3/10
M2 = [(2, Fr(1, 5)), (5, Fr(1, 2)), (7, Fr(3, 10))]
print("mech2 F(5)=", F(M2, 5), " Q(7/10)=", q_inf(M2, Fr(7, 10)), " Q(71/100)=", q_inf(M2, Fr(71, 100)))

# ---- L02 ----
die = [(k, Fr(1, 6)) for k in range(1, 7)]
loss = [(0, Fr(19, 20)), (250000, Fr(1, 20))]
def E(law, g=lambda x: x):
    return sum(g(x) * w for x, w in law)
mu = E(die); ex2 = E(die, lambda x: x * x)
print("die E", mu, "E[X2]", ex2, "Var", ex2 - mu * mu, "sd", float(ex2 - mu * mu) ** 0.5)
print("die Var(2X)=", E([(2 * x, w) for x, w in die], lambda x: x * x) - E([(2 * x, w) for x, w in die]) ** 2)
mu_l = E(loss); ex2_l = E(loss, lambda x: x * x)
print("loss E", mu_l, "E[L2]", ex2_l, "Var", ex2_l - mu_l * mu_l, "sd", round(math.sqrt(ex2_l - mu_l * mu_l), 2), math.sqrt(2968750000))
print("mech2 L: E", E([(0, Fr(9, 10)), (50000, Fr(1, 10))]), "Var", E([(0, Fr(9, 10)), (50000, Fr(1, 10))], lambda x: x*x) - 5000**2, "sd", math.sqrt(2.25e8))
print("R2 Var(D)=", Fr(2968750000, 10000), " sqrt(296875)=", math.sqrt(296875), " sqrt(2968750000)/100=", math.sqrt(2968750000) / 100)
print("E-count 10000/20=", Fr(10000, 20), " 489 vs 500 diff", 500 - 489)
print("Ex2.5 E[X2]=", Fr(91, 6), "Var=", Fr(91, 6) - Fr(7, 2) ** 2, "sd float", math.sqrt(35 / 12))
print("L02 2.6 sqrt", math.sqrt(2968750000))
print("mean-of-L01-Ex3.6 =", E(L01), " Q(1/2)=", q_inf(L01, Fr(1, 2)))
# sum check for the 3/10 expectation text
print("(-2*1-1*2+0*3+1*2+2*1+3*1)/10 =", Fr(-2 * 1 - 1 * 2 + 0 * 3 + 1 * 2 + 2 * 1 + 3 * 1, 10))

# ---- L03 ----
sk = [(0, Fr(1, 2)), (1, Fr(1, 4)), (2, Fr(1, 8)), (10, Fr(1, 8))]
mu3 = E(sk)
def cm(law, k):
    m = E(law)
    return sum(((x - m) ** k) * w for x, w in law)
m2, m3, m4 = cm(sk, 2), cm(sk, 3), cm(sk, 4)
print("L03 mu", mu3, "m2", m2, "m3", m3, "m4", m4)
print("L03 m3^2/m2^3", m3 * m3 / m2 ** 3, float(m3 * m3 / m2 ** 3) ** 0.5, "kurt", m4 / m2 ** 2, float(m4 / m2 ** 2))
pq = Fr(9, 100); p = Fr(1, 10)
print("Bern 1/10 gamma3^2", (1 - 2 * p) ** 2 / pq, " gamma4", (1 - 3 * pq) / pq)
print("p=1/4 gamma4", (1 - 3 * Fr(3, 16)) / Fr(3, 16), " gamma3 p=1/4 =", (1 - 2 * Fr(1, 4)) / math.sqrt(3 / 16))
print("canon law: mu", E([(-2, Fr(2, 5)), (1, Fr(1, 2)), (3, Fr(1, 10))]), "m2", cm([(-2, Fr(2, 5)), (1, Fr(1, 2)), (3, Fr(1, 10))], 2),
      "m3", cm([(-2, Fr(2, 5)), (1, Fr(1, 2)), (3, Fr(1, 10))], 3), "m4", cm([(-2, Fr(2, 5)), (1, Fr(1, 2)), (3, Fr(1, 10))], 4))
print("p=(1-1/sqrt3)/2 pq=", ((1 - 1 / math.sqrt(3)) / 2) * ((1 + 1 / math.sqrt(3)) / 2))
print("Bern p=1/10 skew, 8/3 =", (1 - 2 * p) / math.sqrt(pq), 8 / 3)
print("R1 probability check of E[Z^4]: symmetric two point ->1")
print("mech L03 M1 p=1/4 gamma3=", (1 - 2 * Fr(1, 4)) / math.sqrt(3 / 16), 2 / math.sqrt(3))
print("M2 L03 two-point 0,2 mean 1: m3=", cm([(0, Fr(1, 2)), (2, Fr(1, 2))], 3), "m4=", cm([(0, Fr(1, 2)), (2, Fr(1, 2))], 4))

# seeded sample reproductions (independent code path: cumulative weights with random())
rng = random.Random(2026)
vals = [0, 1, 2, 10]; cw = [4, 6, 7, 8]
draws = []
for _ in range(20000):
    u = rng.random() * 8
    for v, c in zip(vals, cw):
        if u < c:
            draws.append(v)
            break
n = len(draws); mean = sum(draws) / n
s2 = sum((x - mean) ** 2 for x in draws) / n
s3 = sum((x - mean) ** 3 for x in draws) / n
s4 = sum((x - mean) ** 4 for x in draws) / n
print("independent sample skew (cumulative method, may differ from choices):", round(s3 / s2 ** 1.5, 3), round(s4 / s2 ** 2, 3))
rng2 = random.Random(2026)
draws2 = rng2.choices(vals, weights=[4, 2, 1, 1], k=20000)
n = len(draws2); mean = sum(draws2) / n
s2 = sum((x - mean) ** 2 for x in draws2) / n
s3 = sum((x - mean) ** 3 for x in draws2) / n
s4 = sum((x - mean) ** 4 for x in draws2) / n
print("choices-based sample skew, kurt:", round(s3 / s2 ** 1.5, 3), round(s4 / s2 ** 2, 3))

# ---- L04 ----
DEP = {(0, 0): Fr(1, 10), (0, 1): Fr(3, 10), (1, 0): Fr(2, 10), (1, 1): Fr(2, 10), (2, 0): Fr(1, 10), (2, 1): Fr(1, 10)}
PX = {}; PY = {}
for (x, y), w in DEP.items():
    PX[x] = PX.get(x, 0) + w; PY[y] = PY.get(y, 0) + w
print("L04 sum", sum(DEP.values()), "PX", PX, "PY", PY)
EX = sum(x * w for (x, y), w in DEP.items())
print("L04 E[X]=", EX)
for y in (0, 1):
    num = sum(x * w for (x, yy), w in DEP.items() if yy == y)
    print("E[X|Y=%d]=" % y, num / PY[y], "total part", num)
print("total", sum(sum(x * w for (x, yy), w in DEP.items() if yy == y) for y in (0, 1)))
print("cell00 dep", DEP[(0, 0)], "prod", PX[0] * PY[0], "ratio", DEP[(0, 0)] / (PX[0] * PY[0]))
PROD = {(x, y): Fr(1, 5) * 0 for x in (0,)}
PXp = {0: Fr(1, 5), 1: Fr(2, 5), 2: Fr(2, 5)}; PYp = {0: Fr(3, 10), 1: Fr(7, 10)}
print("product (0,0) =", PXp[0] * PYp[0], "sum PXp", sum(PXp.values()), "sum PYp", sum(PYp.values()))
U = {(x, x * x): Fr(1, 3) for x in (-1, 0, 1)}
ex = sum(x * w for (x, y), w in U.items()); ey = sum(y * w for (x, y), w in U.items()); exy = sum(x * y * w for (x, y), w in U.items())
print("Part B E[X],E[Y],E[XY],cov:", ex, ey, exy, exy - ex * ey)
print("R1 |X| cov: E[XY] with Y=|X|:", sum(x * abs(x) * Fr(1, 3) for x in (-1, 0, 1)))
print("E2 ratio", Fr(1, 3) / Fr(1, 9), " E3 ratio", Fr(1, 10) / Fr(4, 25), float(Fr(1, 10) / Fr(4, 25)))
print("M3 L04 table cells", Fr(1, 4) * Fr(1, 2), Fr(3, 4) * Fr(1, 2))
print("M1 L04 table: E[X|Y=1]=", Fr(4, 10) / Fr(6, 10), " P(Y=1)", Fr(6, 10))
print("L04 M1 table cell (0,0) product", Fr(3, 10) * Fr(4, 10))
print("Canon: marginal example p(0,0)=1/2 vs 1/4")
