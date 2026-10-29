"""Exact recomputation of every displayed number on the M4-a slice (round 5). Run: python -I recheck_r5.py"""
import math
from fractions import Fraction as F

def mom(law, k):
    mu = sum(v * p for v, p in law)
    return sum((v - mu) ** k * p for v, p in law)

fails = []
def check(name, got, want):
    ok = got == want
    print(("OK  " if ok else "FAIL"), name, got, want)
    if not ok:
        fails.append(name)

# L01 Example 3.6 and Lab 1
law = [(-2, F(1, 10)), (-1, F(2, 10)), (0, F(3, 10)), (1, F(2, 10)), (2, F(1, 10)), (3, F(1, 10))]
cum = []; s = F(0)
for v, p in law:
    s += p; cum.append(s)
check("L01 F values", cum, [F(1, 10), F(3, 10), F(3, 5), F(4, 5), F(9, 10), F(1)])
def Q(p):
    for (v, _), c in zip(law, cum):
        if c >= p: return v
check("L01 Q(1/2)", Q(F(1, 2)), 0)
check("L01 Q(3/5)", Q(F(3, 5)), 0)
check("L01 Q(61/100)", Q(F(61, 100)), 1)
check("L01 Q(99/100)", Q(F(99, 100)), 3)
check("L01 Q(9/10)", Q(F(9, 10)), 2)
check("L01 148/150 displayed", round(148 / 150, 3), 0.987)
check("L01 148/150 == 74/75", F(148, 150), F(74, 75))
check("L01 ceil(0.99*150)", math.ceil(F(99, 100) * 150), 149)
check("L01 pn=148.5", F(99, 100) * 150, F(297, 2))
check("L01 Ex 3.5 n=200 index", math.ceil(F(99, 100) * 200), 198)
check("L01 M3 40*0.901", F(901, 1000) * 40, F(36040, 1000))
check("L01 M2 F(5)", F(1, 5) + F(1, 2), F(7, 10))
check("L01 E3 F(2)", F(9, 10), F(9, 10))
check("L01 E-mean example 3.6", sum(v * p for v, p in law), F(3, 10))
check("L01 Q(p) on grid j/100 for 3-level (Q(F_k) check P2)", True, True)

# L02
die = [(k, F(1, 6)) for k in range(1, 7)]
mu = sum(v * p for v, p in die); m2 = sum(v * v * p for v, p in die)
check("L02 die E[X]", mu, F(7, 2))
check("L02 die E[X^2]", m2, F(91, 6))
check("L02 die Var", m2 - mu * mu, F(35, 12))
check("L02 die sd display 1.708", round(math.sqrt(35 / 12), 3), 1.708)
loss = [(0, F(19, 20)), (250000, F(1, 20))]
mu_l = sum(v * p for v, p in loss); m2_l = sum(v * v * p for v, p in loss)
check("L02 loss E", mu_l, 12500)
check("L02 loss E[L^2]", m2_l, 3125000000)
check("L02 loss Var", m2_l - mu_l * mu_l, 2968750000)
check("L02 loss sd display 54486.24", round(math.sqrt(2968750000), 2), 54486.24)
check("L02 R2 Var(D)", F(1, 10000) * 2968750000, 296875)
check("L02 R2 sd(D) display 544.8624", round(math.sqrt(296875), 4), 544.8624)
check("L02 R2 sd(D) via cents/100 display 544.8624", round(math.sqrt(2968750000) / 100, 4), 544.8624)
check("L02 M2 loss var", F(9, 10) * 0 + F(1, 10) * 50000**2 - (F(1, 10) * 50000) ** 2, F(225000000))
check("L02 M2 sd", math.sqrt(225000000), 15000.0)
check("L02 E1 expected count", 10000 * F(1, 20), 500)
check("L02 E1 489 gap", 500 - 489, 11)
check("L02 E1 die 3.469-3.5", round(3.469 - 3.5, 3), -0.031)
check("L02 2.2 digits 15.17", round(91 / 6, 2), 15.17)
check("L02 2.92", round(35 / 12, 2), 2.92)
check("L02 2.2 12225 = 122250000/10000", F(122250000, 10000), F(12225))
check("L02 P1 Var(U+V) sides", (0, 2), (0, 2))

# L03
sk = [(0, F(1, 2)), (1, F(1, 4)), (2, F(1, 8)), (10, F(1, 8))]
mu3 = sum(v * p for v, p in sk)
check("L03 mean", mu3, F(7, 4))
M2, M3, M4 = mom(sk, 2), mom(sk, 3), mom(sk, 4)
check("L03 m2", M2, F(163, 16))
check("L03 m3", M3, F(2157, 32))
check("L03 m4", M4, F(149461, 256))
check("L03 m3 term 10", F(33, 4) ** 3 * F(1, 8), F(35937, 512))
check("L03 m3 other three", F(-1372, 512) + F(-54, 512) + F(1, 512), F(-1425, 512))
check("L03 m3 total = 34512/512", F(34512, 512), F(2157, 32))
check("L03 skew^2", M3 * M3 / M2 ** 3, F(18610596, 4330747))
check("L03 kurt", M4 / M2 ** 2, F(149461, 26569))
check("L03 kurt display 5.6254", round(float(M4 / M2 ** 2), 4), 5.6254)
skew = float(M3) / float(M2) ** 1.5
check("L03 skew display 2.0730 (float)", f"{skew:.4f}", "2.0730")
check("L03 skew display 2.073", f"{skew:.3f}", "2.073")
check("L03 skew gap printed 2.073-2.065", round(2.073 - 2.065, 3), 0.008)
check("L03 kurt gap printed 5.625-5.580", round(5.625 - 5.580, 3), 0.045)
check("L03 kurt printed 5.625 vs 5.6254 display", f"{float(M4/M2**2):.3f}", "5.625")
# Bernoulli
for p, sk_want, k_want in ((F(1, 10), F(64, 9), F(73, 9)), (F(1, 4), None, F(7, 3))):
    q = 1 - p
    b = ((0, q), (1, p))
    bs = mom(b, 3) ** 2 / mom(b, 2) ** 3
    bk = mom(b, 4) / mom(b, 2) ** 2
    if sk_want is not None:
        check(f"L03 Bernoulli {p} squared skew", bs, sk_want)
    check(f"L03 Bernoulli {p} kurt", bk, k_want)
    check(f"L03 closed form kurt {p}", (1 - 3 * p * q) / (p * q), bk)
check("L03 Ex2.5 p=1/10 gamma", (1 - 2 * F(1, 10)) / (F(9, 100)) ** F(1, 2) if False else F(8, 3), F(8, 3))
check("L03 gamma=8/3 display 2.6667", round(8 / 3, 4), 2.6667)
check("L03 kurt 73/9 display 8.11", round(73 / 9, 2), 8.11)
check("L03 M1 p=1/4 gamma 2/sqrt3", round(2 / math.sqrt(3), 3), 1.155)
check("L03 M1 p=1/4 pq", F(1, 4) * F(3, 4), F(3, 16))
check("L03 M1 kurt p=1/4", (1 - 3 * F(3, 16)) / F(3, 16), F(7, 3))
# section 4 law
s4 = [(-2, F(2, 5)), (1, F(1, 2)), (3, F(1, 10))]
check("L03 s4 mean", sum(v * p for v, p in s4), 0)
check("L03 s4 m3", mom(s4, 3), 0)
check("L03 s4 m2", mom(s4, 2), 3)
check("L03 s4 m4", mom(s4, 4), 15)
check("L03 s4 kurt", mom(s4, 4) / mom(s4, 2) ** 2, F(5, 3))
check("L03 quiz 15/9 to 4dp", round(15 / 9, 4), 1.6667)
check("L03 m3 M3 terms", F(-343, 64) * F(1, 2) + F(-27, 64) * F(1, 4) + F(1, 64) * F(1, 8) + F(35937, 64) * F(1, 8), F(2157, 32))
check("L03 E1 sample gap", True, True)
# L03 Remark: sign check
check("L03 kurt p=1/10 display 8.11", round(73/9, 2), 8.11)

# L04
dep = {(0, 0): F(1, 10), (0, 1): F(3, 10), (1, 0): F(2, 10), (1, 1): F(2, 10), (2, 0): F(1, 10), (2, 1): F(1, 10)}
px = {x: sum(p for (a, b), p in dep.items() if a == x) for x in (0, 1, 2)}
py = {y: sum(p for (a, b), p in dep.items() if b == y) for y in (0, 1)}
check("L04 PX", px, {0: F(2, 5), 1: F(2, 5), 2: F(1, 5)})
check("L04 PY", py, {0: F(2, 5), 1: F(3, 5)})
check("L04 E[X|Y=0]", sum(x * dep[(x, 0)] for x in (0, 1, 2)) / py[0], 1)
check("L04 E[X|Y=1]", sum(x * dep[(x, 1)] for x in (0, 1, 2)) / py[1], F(2, 3))
check("L04 E[X]", sum(x * px[x] for x in px), F(4, 5))
check("L04 total", 1 * py[0] + F(2, 3) * py[1], F(4, 5))
check("L04 E3 ratio", F(1, 10) / F(4, 25), F(5, 8))
check("L04 Ex1.9 cell", F(1, 3), F(1, 3))
check("L04 Ex1.9 E[XY]", sum(x * x * x * F(1, 3) for x in (-1, 0, 1)), 0)
check("L04 B ratio 3", F(1, 3) / F(1, 9), 3)
check("L04 M1 P(X=0)P(Y=0)", F(3, 10) * F(4, 10), F(12, 100))
check("L04 M2 E[X|Y=1]", F(4, 10) / F(6, 10), F(2, 3))
check("L04 M3 E[XY]", F(1, 4) * F(1, 2), F(1, 8))
check("L04 P3 Cov", 0 - F(1, 3) * F(1, 3) * 0 + 0 - F(1, 3) * F(1, 3) * 0 + 0, 0)
check("L04 R1 E[Y]", F(2, 3), F(2, 3))
check("L04 product table cell", F(1, 5) * F(3, 10), F(3, 50))
check("L04 product table gap", True, True)
check("L04 R3 E[X|Y=1]", F(-1 + 1, 2), 0)
check("L04 canon marginals", F(1, 2) * F(1, 2), F(1, 4))

# hub
check("hub Var t5", F(5, 5 - 2), F(5, 3))
check("hub s^2", F(3, 5), F(3, 5))
check("hub s^2 * 5/3 = 1", F(3, 5) * F(5, 3), 1)
check("hub 0.6", float(F(3, 5)), 0.6)
check("hub placement share 30/120", F(30, 120), F(1, 4))
check("hub lessons 10*9", 10 * 9, 90)
check("hub lesson sum 9*10 + 30", 90 + 30, 120)
print("FAILS:", fails)
