# E1-b round 5 verifier script: re-derive every number changed or cited by the round-5 delta (exact Fractions).
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP

def half_up(x, places):
    q = Decimal(1).scaleb(-places)
    return Decimal(x.numerator) / Decimal(x.denominator) if False else (Decimal(x.numerator) / Decimal(x.denominator)).quantize(q, rounding=ROUND_HALF_UP)

a, b, c = F(120), F(1), F(20)
d = a - b * c
print("d =", d)
# Monopoly (Prop 1.4 / Example 1.5): Q = d/2, fee (a+bc)/(2b), profit d^2/(4b)
Qm, fm, pim = d / 2, (a + b * c) / (2 * b), d * d / (4 * b)
print("monopoly", Qm, fm, pim)
# Cournot (Thm 2.5): each q = d/3 ; total 2d/3 ; fee (a+2bc)/(3b) ; each profit d^2/(9b) ; industry 2 d^2/(9b)
q = d / 3
Qc, fc, each, ind = 2 * q, (a + 2 * b * c) / (3 * b), d * d / (9 * b), 2 * d * d / (9 * b)
print("cournot", Qc, fc, each, ind, "half-up volume", half_up(Qc, 2), "fee", half_up(fc, 2), "industry whole cents", half_up(ind, 0), "each whole cents", half_up(each, 0))
# Brute-force Cournot by best-response iteration with exact fractions (independent of the closed form)
def R(x):
    D = d - x
    return max(F(0), D / 2)
x1, x2 = F(0), F(0)
for _ in range(200):
    x1, x2 = R(x2), R(x1)
print("iteration after 200 steps", float(x1), float(x2), "gap to d/3", float(x1 - d / 3))
# Bertrand (Thm 3.3): fee c, volume d, zero profit
print("bertrand volume", d, "fee", c, "profit", (c - c) * d)
# Prop 4.1 differences
print("diffs", Qc - Qm, d - Qc, fm - fc, fc - c, ind - pim, pim - ind)
print("table rounding: 20000/9 ->", half_up(ind, 0), " 10000/9 ->", half_up(each, 0), " 2500 ->", half_up(pim, 0))
# Prop 2.8: closed form equals iteration for t = 0..30 (exact)
x = F(0)
ok = True
for t in range(31):
    closed = d / 3 * (1 - F(-1, 2) ** t)
    ok &= (x == closed)
    x = R(x)
print("Prop 2.8 closed form == iteration t=0..30:", ok)
# first t with |x_t - d/3| <= 1e-6 at reference case
x = F(0)
t = 0
while abs(x - d / 3) > F(1, 10**6):
    x = R(x)
    t += 1
print("first t with error <= 1e-6 (reference):", t)
# Lab 1 Part A/B derivatives (L04): p(a) = sqrt(1+a)-1 at a = 120 => p = 10, dp/da = 1/22, elasticity (a/p)(dp/da) = 6/11
from decimal import getcontext
getcontext().prec = 60
A = Decimal(120)
p = (1 + A).sqrt() - 1
dp = 1 / (2 * (1 + A).sqrt())
print("p", p, "dp/da - 1/22 =", dp - Decimal(1) / 22, "(a/p)(dp/da) - 6/11 =", (A / p) * dp - Decimal(6) / 11)
# c050: dQ*/da = S'(p*) dp*/da = 20/22 = 10/11 at p=10 (S=p^2)
print("dQ/da - 10/11 =", Decimal(20) * dp - Decimal(10) / 11)
# Prop 1.4 check on a grid: |eps| > 1 iff p > a/(2b), linear demand, a=120,b=1 and b=3, a=60,b=3
bad = []
for (aa, bb) in [(F(120), F(1)), (F(60), F(3)), (F(200), F(4))]:
    for k in range(1, 4000):
        pp = aa / bb * F(k, 4000)
        eps = -bb * pp / (aa - bb * pp)
        if (abs(eps) > 1) != (pp > aa / (2 * bb)) and pp != aa / (2 * bb):
            bad.append((aa, bb, pp))
print("Prop 1.4 grid mismatches:", bad)
# Lemma 3.2 / Remark 3.4: undercut at g just below r earns h(g) -> h(r) = 2 * sharing profit
r = F(60)
h = lambda g: (g - c) * (a - b * g)
print("h(r)/2 vs sharing (r-c)(a-br)/2:", h(r) / 2 == (r - c) * (a - b * r) / 2)
# Monopoly profit identity pi(p) = (a-bc)^2/(4b) - b(p-pm)^2 on a grid
pm = (a + b * c) / (2 * b)
print("completing-square identity holds on grid:", all((p - c) * (a - b * p) == d * d / (4 * b) - b * (p - pm) ** 2 for p in [F(k, 7) for k in range(-50, 300)]))
# Monopoly price minus a/(2b) equals c/2 (Remark 5.3), Lerner index (a-bc)/(a+bc), |eps(p_m)|
print("p_m - a/(2b) - c/2 =", pm - a / (2 * b) - c / 2, " Lerner", (pm - c) / pm - (a - b * c) / (a + b * c))
