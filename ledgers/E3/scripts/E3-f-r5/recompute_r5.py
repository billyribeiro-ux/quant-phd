# Independent recomputation of every number the slice (L01-L04 pages and their cards) states.
from fractions import Fraction as F
import math
from decimal import Decimal, ROUND_HALF_UP

def line(label, value):
    print(f"{label}: {value}")

# ---- L01 ----
A = [(0, F(1, 4)), (100, F(1, 2)), (400, F(1, 4))]  # CU
line("L01 Ex1.4 E X (CU)", sum(p * x for x, p in A))
line("L01 Ex1.4 E u(X) u=x^2 (CU^2)", sum(p * x * x for x, p in A))
LA = [(0, F(1, 4)), (10000, F(1, 2)), (40000, F(1, 4))]
LB = [(5000, F(1, 2)), (20000, F(1, 2))]
LC = [(0, F(1, 3)), (15000, F(1, 3)), (30000, F(1, 3))]
ev = lambda L: sum(p * x for x, p in L)
eq = lambda L: sum(p * F(x * x, 10000) for x, p in L)
line("L01 lab EV cents A,B,C", [ev(LA), ev(LB), ev(LC)])
line("L01 lab quadratic EU A,B,C", [eq(LA), eq(LB), eq(LC)])
line("L01 u(EX)=150^2 (CU^2)", 150 ** 2)
line("L01 M1 E X, E u(X) u=x^2, u(EX)", (sum(p*x for x,p in [(20,F(1,5)),(50,F(3,10)),(80,F(1,2))]), sum(p*x*x for x,p in [(20,F(1,5)),(50,F(3,10)),(80,F(1,2))]), 59**2))
line("L01 E2 1/3*45000+2/3*37500", F(1,3)*45000 + F(2,3)*37500)
line("L01 Ex3.4 E u(C) u=x^2 CU^2", (0 + 150**2 + 300**2) / F(3))
line("L01 R3 E u(X), E u(Y) CU^2", (F(100**2) * F(1,2) + F(200**2)*F(1,2), F(150**2)))
line("L01 Q7 5/12", F(1,3)*F(1,4) + F(2,3)*F(1,2))
# ---- L02 ----
gamble = [(-60, F(1, 4)), (0, F(1, 2)), (60, F(1, 4))]
mean = sum(p * x for x, p in gamble); var = sum(p * x * x for x, p in gamble) - mean ** 2
line("L02 gamble mean, variance", (mean, var))
W = [(40, F(1,4)), (100, F(1,2)), (160, F(1,4))]
EU = sum(float(p) * math.sqrt(x) for x, p in W)
CE = EU ** 2
line("L02 Ex1.5 E sqrt(W)", f"{EU:.9f}")
line("L02 Ex1.5 CE", f"{CE:.9f}")
line("L02 Ex1.5 premium", f"{100 - CE:.9f}")
def half_up(x):
    return int(Decimal(x).quantize(Decimal(1), rounding=ROUND_HALF_UP))
line("L02 CE cents", half_up(CE * 100))
line("L02 premium cents", half_up((100 - CE) * 100))
rA = 0.005; rR = 0.5
approx = 0.5 * rA * float(var)
line("L02 Pratt approx CU (0.5*0.005*1800)", approx)
line("L02 half variance (CU^2)", 0.5 * float(var))
exact = 100 - CE
line("L02 error CU", exact - approx)
line("L02 error share of exact (%)", 100 * (exact - approx) / exact)
line("L02 error share of approx (%)", 100 * (exact - approx) / approx)
line("L02 E1 gap 0.1 and 0.25 ratio", (0.028811/0.004565, 0.25**2/0.1**2))
# Part B premium/eps^2 at five scales, u = sqrt, gamble X at w = 100
def ce_sqrt(eps):
    e = sum(float(p) * math.sqrt(100 + eps * float(x)) for x, p in gamble)
    return e * e
limit = 0.5 * rA * float(var)
for eps in (1.0, 0.5, 0.25, 0.1, 0.01):
    ratio = (100 - ce_sqrt(eps)) / eps ** 2
    line(f"L02 Part B eps={eps}", f"ratio={ratio:.6f} gap={abs(ratio-limit):.6f}")
line("L02 Part A linear CE", 100)
# R3/M1 L02: W in {4,16}
line("L02 M1 CE", (0.5*2 + 0.5*4)**2)
# M3 L02 exponential
# ---- L03 ----
prizes = (5000, 10000, 20000); probs = (0.25, 0.5, 0.25)
def ce(g, pr=prizes):
    if g == 1.0:
        return math.exp(sum(p * math.log(x) for p, x in zip(probs, pr)))
    s = 1 - g
    return sum(p * x ** s for p, x in zip(probs, pr)) ** (1 / s)
for g in (0.0, 0.25, 0.5, 1.0, 2.0, 4.0):
    line(f"L03 CE gamma={g}", f"{ce(g):.4f}  rounded {math.floor(ce(g)+0.5)}")
line("L03 80000/9", 80000/9)
line("L03 geometric mean", ce(1.0))
line("L03 M for gamma 2", sum(F(1,4)*F(1,5000)+F(1,2)*F(1,10000)+F(1,4)*F(1,20000) for _ in [0]))
line("L03 Ex2.5 CE gamma 2 (1000,4000)", 1/(0.5/1000 + 0.5/4000))
line("L03 Ex2.5 CE gamma 1 (1000,4000)", math.exp(0.5*math.log(1000)+0.5*math.log(4000)))
line("L03 M2 CE", 1/(0.25/1000 + 0.75/9000))
line("L03 M3 CE 3X", 1/(0.25/3000 + 0.75/27000))
line("L03 E2 M", F(1,4)*F(1,5000)+F(1,2)*F(1,10000)+F(1,4)*F(1,20000))
line("L03 E3 bound", (10+1)/2)
line("L03 M1 r_A(4), r_R(4) u_{1/2}", (F(1,2)/4, F(1,2)))
line("L03 Ex1.5 u_2(w)=1-1/w check w=2", (2**-1 - 1)/(-1))
# L03 E1 CE at 0.5 cents
line("L03 E1 CE gamma0.5 cents", f"{ce(0.5):.4f} -> {math.floor(ce(0.5)+0.5)}")
# ---- L04 ----
X = {2000: F(1,2), 4000: F(1,2)}
Y = {1000: F(1,4), 3000: F(1,2), 5000: F(1,4)}
def I(pmf, t):
    return sum(p * max(t - x, 0) for x, p in pmf.items())
for name, pmf in (("X", X), ("Y", Y)):
    line(f"L04 Ex2.5 I_{name} at 1000..5000", [str(I(pmf, t)) for t in (1000,2000,3000,4000,5000)])
Y2 = {3000: F(1,2), 4000: F(1,2)}
line("L04 pair B I_Y(4000)", I(Y2, 4000))
Z = {1000: F(1,2), 5000: F(1,2)}; Z2 = {3000: F(1)}
line("L04 Ex2.6 I_X", [str(I(Z,t)) for t in (1000,3000,5000)], )
line("L04 Ex2.6 I_Y", [str(I(Z2,t)) for t in (1000,3000,5000)])
line("L04 M2 I_X(3000) and I_Y(3000) (Ex2.5 pair)", (I(X,3000), I(Y,3000)))
line("L04 M3 I_X(3000) integral", F(1,4)*2000)
