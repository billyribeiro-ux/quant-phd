"""Independent re-derivation (E3 slice f, round 12) of the numbers printed in L01-L04 prose, cards and lab output.

Uses decimal (50 digits) and fractions only; does not import the lab code.
"""
from decimal import Decimal, getcontext, ROUND_HALF_UP
from fractions import Fraction as F
import math

getcontext().prec = 50
D = Decimal


def half_up(x: Decimal) -> int:
    return int(x.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def show(label, value):
    print(f"{label}: {value}")


# L01 Example 1.4, Misconception 1, M1, M3-ish, Example 3.4, E1, R3
A = [(0, F(1, 4)), (100, F(1, 2)), (400, F(1, 4))]
show("L01 EX1.4 E X CU", sum(p * x for x, p in A))
show("L01 EX1.4 E x^2 CU^2", sum(p * x * x for x, p in A))
show("L01 MisC1 u(EX)=150^2", 150 * 150)
C = [(0, F(1, 3)), (150, F(1, 3)), (300, F(1, 3))]
show("L01 EX3.4 E x^2 for C", sum(p * x * x for x, p in C))
show("L01 M1 E X", sum(p * x for x, p in [(20, F(1, 5)), (50, F(3, 10)), (80, F(1, 2))]))
show("L01 M1 E x^2", sum(p * x * x for x, p in [(20, F(1, 5)), (50, F(3, 10)), (80, F(1, 2))]))
show("L01 M1 u(59)", 59 * 59)
show("L01 M2 E u(L) and E u(M) and rhs", (F(1, 2) * 0 + F(1, 2) * 100, F(1, 4) * 100 + F(3, 4) * 200, F(1, 3) * (F(1, 2) * 0 + F(1, 2) * 100) + F(2, 3) * (F(1, 4) * 100 + F(3, 4) * 200)))
show("L01 M3 E v(X), E v(Y)", (F(5) + 3 * 20, F(5) + 3 * 30))
show("L01 R1/R3 E u(X), E u(Y) with x^2", (F(1, 2) * 100**2 + F(1, 2) * 200**2, F(150**2)))
show("L01 E1 diff", 45000 - 37500)
show("L01 E2 line", F(1, 3) * 45000 + F(2, 3) * 37500)
show("L01 E3 sum 5/6", F(1, 2) + F(1, 3))
show("L01 q7 mixture prob 0", F(1, 3) * F(1, 4) + F(2, 3) * F(1, 2))
show("L01 Lab B quadratic EU (cents, x^2/10000)", F(5000**2, 10000) * F(1, 2) + F(20000**2, 10000) * F(1, 2))
show("L01 Lab C quadratic EU", (F(15000**2, 10000) + F(30000**2, 10000)) / 3)
show("L01 Lab A quadratic EU", F(10000**2, 10000) / 2 + F(40000**2, 10000) / 4)

# L02 Example 1.5 (sqrt wealth)
W = [(40, F(1, 4)), (100, F(1, 2)), (160, F(1, 4))]
EW = sum(p * x for x, p in W)
show("L02 EX1.5 E W", EW)
EU = D(1) / 4 * D(40).sqrt() + D(1) / 2 * D(100).sqrt() + D(1) / 4 * D(160).sqrt()
show("L02 EX1.5 E sqrt(W) (50dp)", EU)
CE = EU * EU
show("L02 EX1.5 CE (50dp)", CE)
show("L02 EX1.5 premium (50dp)", D(100) - CE)
show("L02 EX1.5 premium cents unrounded", (D(100) - CE) * 100)
show("L02 EX1.5 premium cents half_up", half_up((D(100) - CE) * 100))
show("L02 EX1.5 CE cents unrounded", CE * 100)
show("L02 EX1.5 CE cents half_up", half_up(CE * 100))
# Example 2.3
show("L02 EX2.3 r_A(100)", D(1) / (2 * 100))
# Section 3 / Lab: variance 1800, pratt approx
show("L02 approx 0.5*0.005*1800", D("0.5") * D("0.005") * 1800)
show("L02 half variance", F(1800, 2))
ex = D("5.065835")
ap = D("4.5")
show("L02 error (E2 basis)", ex - ap)
show("L02 error / exact premium (percent)", (ex - ap) / ex * 100)
show("L02 error / approx (percent)", (ex - ap) / ap * 100)
show("L02 E1 gap 0.1 and ratio", (D("4.504565") - D("4.5"), D("0.028811") / D("0.004565")))
show("L02 eps^2 factor (0.25/0.1)^2", (D("0.25") / D("0.1")) ** 2)
show("L02 M1 CE two point", (D(1) / 2 * D(4).sqrt() + D(1) / 2 * D(16).sqrt()) ** 2)

# Lab L02 floats: replicate the lab's exact formula with float and decimal
import math as m
WEALTH = 100.0
G = [(-60, 0.25), (0, 0.5), (60, 0.25)]
def ce_sqrt(eps):
    e = sum(p * m.sqrt(WEALTH + eps * x) for x, p in G)
    return e * e
for eps in (1.0, 0.5, 0.25, 0.1, 0.01):
    prem = WEALTH - ce_sqrt(eps)
    print(f"L02 lab recompute eps {eps}: premium/eps^2 = {prem / eps**2:.6f}, gap {abs(prem/eps**2 - 4.5):.6f}")
print("L02 lab recompute CE(eps=1) cents", round(ce_sqrt(1.0) * 100, 4))

# L03
PR = [5000, 10000, 20000]
PB = [F(1, 4), F(1, 2), F(1, 4)]
show("L03 expected prize", sum(p * x for p, x in zip(PB, PR)))
def ce_crra(g):
    if g == 1:
        return m.exp(sum(float(p) * m.log(x) for p, x in zip(PB, PR)))
    s = 1 - g
    M = sum(float(p) * x ** s for p, x in zip(PB, PR))
    return M ** (1 / s)
for g in (0, 0.25, 0.5, 1, 2, 4):
    v = ce_crra(g)
    print(f"L03 CE gamma {g}: {v:.4f} rounded {math.floor(v + 0.5)}")
M2 = sum(F(p) * F(1, x) for p, x in zip(PB, PR))
show("L03 gamma2 exact 1/M", 1 / M2)
show("L03 gamma2 exact float", float(1 / M2))
show("L03 geometric mean exact check: (5000*20000)^(1/4)*10000^(1/2)", (D(5000) * D(20000)) ** D("0.25") * D(10000).sqrt())
show("L03 E2 M", F(1, 4) * F(1, 5000) + F(1, 2) * F(1, 10000) + F(1, 4) * F(1, 20000))
show("L03 Ex2.5 gamma2 M", F(1, 2) * F(1, 1000) + F(1, 2) * F(1, 4000))
show("L03 Ex2.5 gamma1", m.exp(0.5 * m.log(1000) + 0.5 * m.log(4000)))
show("L03 M2 gamma2 M", F(1, 4) * F(1, 1000) + F(3, 4) * F(1, 9000))
show("L03 M3 3X M", F(1, 4) * F(1, 3000) + F(3, 4) * F(1, 27000))
show("L03 E3 bound (10+1)/2", F(11, 2))
show("L03 M1 r_A(4) gamma1/2", F(1, 2) / 4)
# L03 homogeneity and remark bound
for k in (2, 3, 10):
    for g in (0, 0.25, 0.5, 2, 4):
        a = ce_crra(g)
        # scaled CE via power identity
        if g == 1:
            b = m.exp(sum(float(p) * m.log(k * x) for p, x in zip(PB, PR)))
        else:
            s = 1 - g
            b = (sum(float(p) * (k * x) ** s for p, x in zip(PB, PR))) ** (1 / s)
        assert abs(b / (k * a) - 1) < 1e-12, (k, g)
print("L03 homogeneity recompute: ok for k=2,3,10 and listed gammas")

# L04 integrated values
S = [1000, 2000, 3000, 4000, 5000]
def I(pmf, t):
    return sum(p * max(t - x, 0) for x, p in pmf)
X_A = [(2000, F(1, 2)), (4000, F(1, 2))]
Y_A = [(1000, F(1, 4)), (3000, F(1, 2)), (5000, F(1, 4))]
print("L04 Ex2.5 I_X", [I(X_A, t) for t in S])
print("L04 Ex2.5 I_Y", [I(Y_A, t) for t in S])
Y_B = [(3000, F(1, 2)), (4000, F(1, 2))]
print("L04 pair B I_Y", [I(Y_B, t) for t in S], "I_X", [I(X_A, t) for t in S])
C_X = [(1000, F(1, 2)), (5000, F(1, 2))]
C_Y = [(3000, F(1))]
print("L04 pair C I_X", [I(C_X, t) for t in S], "I_Y", [I(C_Y, t) for t in S])
print("L04 Ex1.7 means", sum(p * x for x, p in X_A), sum(p * x for x, p in Y_B))
print("L04 Ex2.5 means", sum(p * x for x, p in X_A), sum(p * x for x, p in Y_A))
print("L04 Ex2.6 means", sum(p * x for x, p in C_X), sum(p * x for x, p in C_Y))
print("L04 M1 means (X 1000/4000, Y 2000)", sum(p * x for x, p in [(1000, F(1, 2)), (4000, F(1, 2))]), 2000)
print("L04 M3 I(3000)", I([(1000, F(1, 4)), (5000, F(3, 4))], 3000))
print("L04 E1 I_Y(4000) pair B", I(Y_B, 4000))
print("L04 Ex2.6 I_X at support", [I(C_X, t) for t in S])
