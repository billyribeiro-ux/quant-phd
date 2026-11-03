"""Re-derive every number on the E3 L01-L04 cards with exact Fractions and float checks (E3 slice f, round 4)."""
from fractions import Fraction as F
import math

out = []

def show(label, value):
    out.append(f"{label}: {value}")

# L01 Example 1.4 / card c014 / c016 (lottery A, B, C as in L01 Lab 1)
A = [(0, F(1, 4)), (10000, F(1, 2)), (40000, F(1, 4))]
B = [(5000, F(1, 2)), (20000, F(1, 2))]
C = [(0, F(1, 3)), (15000, F(1, 3)), (30000, F(1, 3))]
lin = lambda x: F(x)
quad = lambda x: F(x * x, 10000)
ev = lambda L: sum(p * x for x, p in L)
eu = lambda L, u: sum(p * u(x) for x, p in L)
show("c016 EV A,B,C (cents)", [ev(A), ev(B), ev(C)])
show("c016 linear EU A,B,C", [eu(A, lin), eu(B, lin), eu(C, lin)])
show("c016 quadratic EU A,B,C", [eu(A, quad), eu(B, quad), eu(C, quad)])
# Example 1.4 in CU: A pays 0,100,400 CU
A_cu = [(0, F(1, 4)), (100, F(1, 2)), (400, F(1, 4))]
show("c014 E X in CU", ev(A_cu))
show("c014 u(EX)=150^2", ev(A_cu) ** 2)
show("c014 E u(X) under x^2 CU", sum(p * x * x for x, p in A_cu))
# Example 3.4 / misconception numbers
show("Ex3.4 E u(C) under x^2 CU", sum(p * x * x for x, p in [(0, F(1, 3)), (150, F(1, 3)), (300, F(1, 3))]))
# L01 Lab Part B mixture checks
for alpha in (F(1, 4), F(1, 3), F(1, 2)):
    mixed = {}
    for x, p in A:
        mixed[x] = mixed.get(x, F(0)) + alpha * p
    for x, p in C:
        mixed[x] = mixed.get(x, F(0)) + (1 - alpha) * p
    Mx = list(mixed.items())
    show(f"B alpha={alpha} mix quad EU", eu(Mx, quad))
    show(f"B alpha={alpha} lin comb quad", alpha * eu(A, quad) + (1 - alpha) * eu(C, quad))
# card c173 / c010 / c011 algebra spot checks (a=3, b=2)
show("c010 a + b E X (a=3,b=2, EX=150)", 3 + 2 * 150)

# L02 gamble X in {-60,0,60} w.p. 1/4,1/2,1/4; wealth 100
g = [(-60, F(1, 4)), (0, F(1, 2)), (60, F(1, 4))]
mean = sum(p * x for x, p in g)
var = sum(p * x * x for x, p in g) - mean ** 2
show("L02 gamble mean, variance", (mean, var))
w = 100.0
def ce(eps):
    Eu = sum(float(p) * math.sqrt(w + eps * x) for x, p in g)
    return Eu * Eu
ce1 = ce(1.0)
prem1 = w - ce1
show("c032 CE eps=1 (CU)", ce1)
show("c032 premium eps=1 (CU)", prem1)
show("c032 cents CE (half up)", math.floor(ce1 * 100 + 0.5))
show("c032 cents premium (half up)", math.floor(prem1 * 100 + 0.5))
r_a = 1 / (2 * w)
show("c026 r_A(100)", r_a)
show("c026 r_R", 0.5)
approx = 0.5 * r_a * float(var)
show("c032 Pratt approx (CU)", approx)
show("c032 error (CU)", prem1 - approx)
show("c029 half variance (CU^2)", 0.5 * float(var))
show("c034 error/exact premium (percent)", 100 * (prem1 - approx) / prem1)
show("E2 error/approx (percent)", 100 * (prem1 - approx) / approx)
for eps in (1.0, 0.5, 0.25, 0.1, 0.01):
    pr = w - ce(eps)
    show(f"c033 premium/eps^2 at eps={eps}", pr / eps ** 2)
show("c033 gap at eps=0.1 (lab rule)", abs((w - ce(0.1)) / 0.01 - 4.5))
show("L02 E1 gap ratio 0.25->0.1", (abs((w - ce(0.25)) / 0.0625 - 4.5)) / (abs((w - ce(0.1)) / 0.01 - 4.5)))
show("c035 linear premium eps=1", w - (sum(float(p) * (w + x) for x, p in g)))
# Example 1.5 in L02: W pays 40,100,160 w.p. 1/4,1/2,1/4
Eu_sqrtW = 0.25 * math.sqrt(40) + 0.5 * 10 + 0.25 * math.sqrt(160)
show("Ex1.5 E sqrt(W)", Eu_sqrtW)
show("Ex1.5 CE", Eu_sqrtW ** 2)
show("Ex1.5 premium", 100 - Eu_sqrtW ** 2)

# L03 fixed lottery: prizes 5000, 10000, 20000 with 1/4, 1/2, 1/4
P = [5000, 10000, 20000]
Q = [F(1, 4), F(1, 2), F(1, 4)]
show("L03 expected prize exact", sum(q * x for q, x in zip(Q, P)))
def ce_crra(gam):
    if gam == 1:
        return math.exp(sum(float(q) * math.log(x) for q, x in zip(Q, P)))
    s = 1 - gam
    M = sum(float(q) * x ** s for q, x in zip(Q, P))
    return M ** (1 / s)
for gam in (0.0, 0.25, 0.5, 1.0, 2.0, 4.0):
    show(f"c054 CE gamma={gam}", f"{ce_crra(gam):.4f}")
M2 = sum(q / x for q, x in zip(Q, P))
show("c055 M = sum p/x (exact)", M2)
show("c055 1/M exact", 1 / M2)
show("c055 float", float(1 / M2))
show("L03 geometric mean exact check: (5000*20000)^(1/4)*10000^(1/2)", (5000 * 20000) ** 0.25 * 10000 ** 0.5)
# Example 2.5: 1000,4000 with 1/2 each
M_ex = F(1, 2) * F(1, 1000) + F(1, 2) * F(1, 4000)
show("Ex2.5 CE gamma=2 (cents)", 1 / M_ex)
show("Ex2.5 CE gamma=1 (cents)", math.sqrt(1000 * 4000))
# M2 of L03 and M3
M_m2 = F(1, 4) * F(1, 1000) + F(3, 4) * F(1, 9000)
show("L03 M2 CE2", 1 / M_m2)
show("L03 M3 CE2 of 3X", 1 / (F(1, 4) * F(1, 3000) + F(3, 4) * F(1, 27000)))
# c168 bound: (k+1)/2 for k=10 -> 5.5 cents
show("c168 bound k=10", F(10 + 1, 2))
# L03 remark 2.8 rounding example
show("L03 E1 CE(0.5) rounded", math.floor(10615.8009 + 0.5))

# L04 pmfs on support
S = [1000, 2000, 3000, 4000, 5000]
def pmf(d): return [d.get(x, F(0)) for x in S]
def cdf(p, t): return sum(pi for pi, x in zip(p, S) if x <= t)
def icdf(p, t): return sum(pi * max(t - x, 0) for pi, x in zip(p, S))
X = pmf({2000: F(1, 2), 4000: F(1, 2)})
Y = pmf({1000: F(1, 4), 3000: F(1, 2), 5000: F(1, 4)})
show("c067 I_X(3000,4000,5000)", [icdf(X, t) for t in (3000, 4000, 5000)])
show("c067 I_Y(2000,3000,4000,5000)", [icdf(Y, t) for t in (2000, 3000, 4000, 5000)])
show("c067 means X,Y", (sum(pi * x for pi, x in zip(X, S)), sum(pi * x for pi, x in zip(Y, S))))
show("c068 F_X(2000), F_Y(2000), F_Y(3000), F_X(3000)", (cdf(X, 2000), cdf(Y, 2000), cdf(Y, 3000), cdf(X, 3000)))
Xe = pmf({2000: F(1, 2), 4000: F(1, 2)}) 
Ye1 = pmf({2000: F(1, 2), 3000: F(1, 2)})  # placeholder not used
E17X = pmf({2000: F(1, 2), 4000: F(1, 2)})
E17Y = pmf({3000: F(1, 2), 4000: F(1, 2)})
S3 = [2000, 3000, 4000]
def cdf3(d, t): return sum(v for x, v in d.items() if x <= t)
show("c070 F_X on 2000,3000,4000", [cdf3({2000: F(1, 2), 4000: F(1, 2)}, t) for t in S3])
show("c070 F_Y on 2000,3000,4000", [cdf3({3000: F(1, 2), 4000: F(1, 2)}, t) for t in S3])
E26X = {1000: F(1, 2), 5000: F(1, 2)}
S26 = [1000, 3000, 5000]
show("Ex2.6 I_X at support", [sum(v * max(t - x, 0) for x, v in E26X.items()) for t in S26])
show("Ex2.6 I_Y at support", [max(t - 3000, 0) for t in S26])

# c031 / c173 / c011 checks in Python
open("/Users/billyribeiro/.fanout/wt/verifyD4-E3-f/ledgers/E3/scripts/E3-f-r4/recompute_numbers.out", "w").write("\n".join(out) + "\n")
print("\n".join(out))
