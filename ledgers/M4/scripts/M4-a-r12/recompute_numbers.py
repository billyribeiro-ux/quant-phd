"""Independent recomputation of every displayed number in M4 slice a (L01-L04, hub). Standard library only.

Method differs from the twins: brute-force enumeration over outcomes, Fraction arithmetic, and float checks.
"""
import math
import random
from fractions import Fraction as Fr

def F_of(law, x):
    return sum((p for v, p in law if v <= x), Fr(0))

def Q_of(law, p):
    cands = [v for v, _ in law if F_of(law, v) >= p]
    return min(cands)

print("== L01")
law = [(-2, Fr(1, 10)), (-1, Fr(2, 10)), (0, Fr(3, 10)), (1, Fr(2, 10)), (2, Fr(1, 10)), (3, Fr(1, 10))]
print("F at support:", [str(F_of(law, v)) for v, _ in law])
for p in [Fr(1, 20), Fr(1, 10), Fr(11, 100), Fr(1, 2), Fr(3, 5), Fr(61, 100), Fr(9, 10), Fr(91, 100), Fr(99, 100), Fr(1)]:
    print("Q(%s)=%d" % (p, Q_of(law, p)), end="; ")
print()
# Q by inf over a fine grid of reals, as a cross-check of the support-point formula
def Q_grid(law, p):
    xs = [i / 1000 for i in range(-3000, 4001)]
    return min(x for x in xs if F_of(law, Fr(x).limit_denominator(10**6)) >= p)
print("grid inf check (x step 1e-3):", [Q_grid(law, p) for p in [Fr(1, 2), Fr(3, 5), Fr(61, 100), Fr(99, 100)]])
print("n=150 index ceil(0.99*150)=", math.ceil(Fr(99, 100) * 150), " pn=", float(Fr(99, 100) * 150), " 148/150=", float(Fr(148, 150)), "74/75=", float(Fr(74, 75)))
print("n=200 ceil(0.99*200)=", math.ceil(Fr(99, 100) * 200))
print("40 values: 40*0.9=", 40 * 0.9, " 40*0.901=", 40 * 0.901, " ceil=", math.ceil(40 * 0.901))
# M1, M2, M3 of L01 page
print("M1 law: P(X=0)=1/2 ->", Q_of([(0, Fr(1, 2)), (1, Fr(1, 2))], Fr(1, 2)))
print("M2 law: F(5)=", F_of([(2, Fr(1, 5)), (5, Fr(1, 2)), (7, Fr(3, 10))], 5), " Q(7/10)=", Q_of([(2, Fr(1, 5)), (5, Fr(1, 2)), (7, Fr(3, 10))], Fr(7, 10)), " Q(71/100)=", Q_of([(2, Fr(1, 5)), (5, Fr(1, 2)), (7, Fr(3, 10))], Fr(71, 100)))
print("Example 1.3 P(X<=1)=", F_of([(0, Fr(1, 2)), (1, Fr(1, 3)), (3, Fr(1, 6))], 1))
print("L01 quiz: law 1/4,1/2,1/4 Q(1/2)=", Q_of([(0, Fr(1, 4)), (1, Fr(1, 2)), (2, Fr(1, 4))], Fr(1, 2)))

print("== L02")
die = [(k, Fr(1, 6)) for k in range(1, 7)]
loss = [(0, Fr(19, 20)), (250000, Fr(1, 20))]
def E(law, g=lambda v: v):
    return sum((g(v) * p for v, p in law), Fr(0))
mu = E(die); print("die E", mu, "E[X2]", E(die, lambda v: v * v), "Var", E(die, lambda v: (v - mu) ** 2), "Var(2X)", E([(2 * v, p) for v, p in die], lambda v: (v - 2 * mu) ** 2))
ml = E(loss); print("loss E", ml, "E[L2]", E(loss, lambda v: v * v), "Var", E(loss, lambda v: (v - ml) ** 2))
print("sd loss", math.sqrt(2968750000), "sd die", math.sqrt(35 / 12), "E[X2]die float", float(E(die, lambda v: v * v)), "Var die float", float(E(die, lambda v: (v - mu) ** 2)))
print("D=L/100 Var", E([(Fr(v, 100), p) for v, p in loss], lambda v: (v - Fr(ml, 100)) ** 2), " sd", math.sqrt(296875), " 54486.24/100", 54486.24 / 100)
print("L02 E3X-1 with E[X]=2: 3*2-1 =", 3 * 2 - 1)
print("M3 L02: Var(3X-2) with Var 4 =", 9 * 4)

print("== L03")
sk = [(0, Fr(1, 2)), (1, Fr(1, 4)), (2, Fr(1, 8)), (10, Fr(1, 8))]
m = E(sk); print("mean", m)
mom = {k: E(sk, lambda v, k=k: (v - m) ** k) for k in (2, 3, 4)}
print("m2", mom[2], "m3", mom[3], "m4", mom[4])
print("skew^2", mom[3] ** 2 / mom[2] ** 3, float(mom[3] ** 2 / mom[2] ** 3), " skew", float(mom[3]) / float(mom[2]) ** 1.5, " kurt", mom[4] / mom[2] ** 2, float(mom[4] / mom[2] ** 2))
print("terms m3:", [str((v - m) ** 3 * p) for v, p in sk], "sum*512", mom[3] * 512, " 10-term", (10 - m) ** 3 / 8, " others", mom[3] - (10 - m) ** 3 / 8)
print("terms-of-sum check (k/512):", [float(((v - m) ** 3 * p) * 512) for v, p in sk])
for p in (Fr(1, 10), Fr(1, 4)):
    b = [(0, 1 - p), (1, p)]
    mb = {k: E(b, lambda v, k=k: (v - p) ** k) for k in (2, 3, 4)}
    q = 1 - p
    print("Bernoulli p=", p, "skew^2", mb[3] ** 2 / mb[2] ** 3, "kurt", mb[4] / mb[2] ** 2, " closed skew^2", (1 - 2 * p) ** 2 / (p * q), " closed kurt", (1 - 3 * p * q) / (p * q), " gamma3", float((1 - 2 * p) / math.sqrt(p * q)))
pp = (1 - 1 / math.sqrt(3)) / 2
print("p with pq=1/6:", pp, pp * (1 - pp), " kurt", (1 - 3 * pp * (1 - pp)) / (pp * (1 - pp)))
print("Bernoulli p=1/4 gamma3 2/sqrt3 =", 2 / math.sqrt(3))
law3 = [(-2, Fr(2, 5)), (1, Fr(1, 2)), (3, Fr(1, 10))]
m3l = E(law3); print("zero-skew law mean", m3l, "m2", E(law3, lambda v: (v - m3l) ** 2), "m3", E(law3, lambda v: (v - m3l) ** 3), "m4", E(law3, lambda v: (v - m3l) ** 4), "kurt", E(law3, lambda v: v ** 4) / E(law3, lambda v: v * v) ** 2)
print("L03 E1 gaps: 2.073-2.065=", round(2.073 - 2.065, 3), " 5.625-5.580=", round(5.625 - 5.580, 3))
print("R1 Bernoulli kurt p=1/10 =", 73 / 9, " 8.11 check", round(73 / 9, 2))
print("L03 Example 2.6 gamma3 p=1/10 = 8/3:", Fr(4, 5) / Fr(3, 10), float(Fr(4, 5) / Fr(3, 10)))
# sample check, independent sampler: inverse-CDF on uniform
rng = random.Random(2026)
vals = [0, 1, 2, 10]; cum = [4, 6, 7, 8]
draws = []
for _ in range(20000):
    u = rng.randrange(8)
    draws.append(vals[next(i for i, c in enumerate(cum) if u < c)])
mean = sum(draws) / len(draws)
s2 = sum((x - mean) ** 2 for x in draws) / len(draws)
s3 = sum((x - mean) ** 3 for x in draws) / len(draws)
s4 = sum((x - mean) ** 4 for x in draws) / len(draws)
print("independent sampler (not the lab's stream): skew", s3 / s2 ** 1.5, "kurt", s4 / s2 ** 2)

print("== L04")
dep = {(0, 0): Fr(1, 10), (0, 1): Fr(3, 10), (1, 0): Fr(2, 10), (1, 1): Fr(2, 10), (2, 0): Fr(1, 10), (2, 1): Fr(1, 10)}
px = {x: sum(p for (a, b), p in dep.items() if a == x) for x in range(3)}
py = {y: sum(p for (a, b), p in dep.items() if b == y) for y in range(2)}
print("dep marginals X", px, "Y", py, "sum", sum(dep.values()))
print("cond E[X|Y=0]", sum(x * p for (x, y), p in dep.items() if y == 0) / py[0], " E[X|Y=1]", sum(x * p for (x, y), p in dep.items() if y == 1) / py[1], " E[X]", sum(x * p for (x, y), p in dep.items()))
print("ratio cell (0,0)", dep[(0, 0)] / (px[0] * py[0]), " 3/50 product check")
prod = {(x, y): Fr(1, 5) if x == 0 else (Fr(2, 5) if x in (1, 2) else 0) for x in range(3) for y in range(2)}
pyv = {0: Fr(3, 10), 1: Fr(7, 10)}
print("product (0,0)=", Fr(1, 5) * Fr(3, 10))
print("E[XY] for Y=X^2 uniform:", sum(Fr(1, 3) * x * x * x for x in (-1, 0, 1)), " E[X]", sum(Fr(1, 3) * x for x in (-1, 0, 1)))
print("R1 Y=|X|: E[XY]", sum(Fr(1, 3) * x * abs(x) for x in (-1, 0, 1)))
print("M1 L04: 0.1 vs 0.12; M2 0.4/0.6 =", Fr(4, 6))
print("E1 L04 P(Y=1) from table:", Fr(3, 10) + Fr(2, 10) + Fr(1, 10))
print("E2 L04 ratio", (Fr(1, 3)) / (Fr(1, 9)), " E3 ratio", Fr(1, 10) / Fr(4, 25), float(Fr(1, 10) / Fr(4, 25)))
print("hub skill 2: s^2 = 3/5 =", Fr(3, 5), " Var t5 = 5/3 ->", Fr(5, 3) * Fr(3, 5))
print("hub skill 1 Q(1/2) for 1/4,1/2,1/4 table:", Q_of([(0, Fr(1, 4)), (1, Fr(1, 2)), (2, Fr(1, 4))], Fr(1, 2)))
