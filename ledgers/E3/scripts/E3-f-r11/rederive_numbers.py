"""E3 slice f round 11: independent re-derivation of the numbers quoted in cards and lesson prose for L01-L04.

Uses Fraction and decimal (high precision), not the lab code. Run: python3 -I ledgers/E3/scripts/E3-f-r11/rederive_numbers.py
"""
from decimal import Decimal, getcontext
from fractions import Fraction
import math

getcontext().prec = 50
D = Decimal

# L01 Example 1.4 and lab A, B, C (cents, exact)
A = [(0, Fraction(1, 4)), (10000, Fraction(1, 2)), (40000, Fraction(1, 4))]
B = [(5000, Fraction(1, 2)), (20000, Fraction(1, 2))]
C = [(0, Fraction(1, 3)), (15000, Fraction(1, 3)), (30000, Fraction(1, 3))]
ev = lambda L: sum(p * x for x, p in L)
eu2 = lambda L: sum(p * Fraction(x * x, 10000) for x, p in L)
print("L01 EV A,B,C", [str(ev(L)) for L in (A, B, C)], "EU quad", [str(eu2(L)) for L in (A, B, C)])
# L01 Example 3.4 C under x^2 (CU): outcomes 0,150,300 CU
print("L01 Ex3.4 E u(C) CU^2", sum(Fraction(1, 3) * v for v in (0, 150**2, 300**2)))
# L01 M1 and R3
print("L01 M1 EX, Eu", sum(p * x for p, x in [(Fraction(1, 5), 20), (Fraction(3, 10), 50), (Fraction(1, 2), 80)]),
      sum(p * x * x for p, x in [(Fraction(1, 5), 20), (Fraction(3, 10), 50), (Fraction(1, 2), 80)]))
print("L01 R3 Eu(X), Eu(Y)", Fraction(100**2 + 200**2, 2), Fraction(150**2))
# L02 Example 1.5 and Lab 1 part A
EU = D(40).sqrt() / 4 + D(5) + D(160).sqrt() / 4
CE = EU * EU
print("L02 E sqrt(W)", EU.quantize(D("0.000001")), "CE", CE.quantize(D("0.000001")), "premium", (D(100) - CE).quantize(D("0.000001")))
var = Fraction(1, 4) * 60 * 60 + Fraction(1, 4) * 60 * 60
print("L02 var(X)", var)
rA = D(1) / (2 * D(100))
rR = D(100) * rA
approx = rA / 2 * D(1800)
print("L02 rA(100), rR, approx", rA, rR, approx, "error", ((D(100) - CE) - approx).quantize(D("0.000001")))
print("L02 error share", ((D(100) - CE) - approx) / (D(100) - CE))
# L02 Lab Part B exact premium/eps^2 at eps=0.1 and 0.01 (CE(eps) = (E sqrt(100+eps X))^2)
def prem(eps):
    e = (D(100 - 60 * eps).sqrt() / 4) + (D(100).sqrt() / 2) + (D(100 + 60 * eps).sqrt() / 4)
    return D(100) - e * e
for eps in ("1", "0.5", "0.25", "0.1", "0.01"):
    e = D(eps)
    print("L02 eps", eps, "premium/eps^2", (prem(e) / (e * e)).quantize(D("0.000001")))
# L03 CE values at gammas (CE = (sum p x^s)^(1/s))
P = [(Fraction(1, 4), 5000), (Fraction(1, 2), 10000), (Fraction(1, 4), 20000)]
def ce(g):
    s = 1 - D(str(g))
    if s == 0:
        return math.exp(sum(float(p) * math.log(x) for p, x in P))
    M = sum(D(p.numerator) / D(p.denominator) * (D(x) ** s) for p, x in P)
    return M ** (1 / s)
for g in ("0", "0.25", "0.5", "1", "2", "4"):
    if g == "1":
        print("L03 gamma 1 geometric mean", (D(5000) ** D("0.25") * D(10000) ** D("0.5") * D(20000) ** D("0.25")).quantize(D("0.0001")))
    else:
        print("L03 gamma", g, "CE", ce(g).quantize(D("0.0001")))
M2 = Fraction(1, 4) * Fraction(1, 5000) + Fraction(1, 2) * Fraction(1, 10000) + Fraction(1, 4) * Fraction(1, 20000)
print("L03 M(gamma2)", M2, "CE", 1 / M2, float(1 / M2))
print("L03 Ex2.5 CE2", 1 / (Fraction(1, 2) / 1000 + Fraction(1, 2) / 4000), "CE1", math.exp(0.5 * math.log(1000) + 0.5 * math.log(4000)))
print("L03 M2 CE2", 1 / (Fraction(1, 4) / 1000 + Fraction(3, 4) / 9000), "M3 CE2(3X)", 1 / (Fraction(1, 4) / 3000 + Fraction(3, 4) / 27000))
print("L03 M1 gamma 1/2 at w=4 rA", Fraction(1, 2) / 4)
print("L03 E1 cents bound k=10", Fraction(11, 2))
# L04 Example 2.5 integrated values
def I(pmf, t):
    return sum(p * max(t - x, 0) for x, p in pmf)
X25 = [(2000, Fraction(1, 2)), (4000, Fraction(1, 2))]
Y25 = [(1000, Fraction(1, 4)), (3000, Fraction(1, 2)), (5000, Fraction(1, 4))]
print("L04 I_X", [str(I(X25, t)) for t in (1000, 2000, 3000, 4000, 5000)])
print("L04 I_Y", [str(I(Y25, t)) for t in (1000, 2000, 3000, 4000, 5000)])
def F(pmf, t):
    return sum(p for x, p in pmf if x <= t)
print("L04 F_X(2000), F_Y(2000), F_Y(3000), F_X(3000)", F(X25, 2000), F(Y25, 2000), F(Y25, 3000), F(X25, 3000))
Y26 = [(3000, Fraction(1))]
X26 = [(1000, Fraction(1, 2)), (5000, Fraction(1, 2))]
print("L04 Ex2.6 I_X", [str(I(X26, t)) for t in (1000, 3000, 5000)], "I_Y", [str(I(Y26, t)) for t in (1000, 3000, 5000)])
print("L04 M2 I_X(3000)", I(X25, 3000), "I_Y(3000) Ex2.5", I(Y25, 3000))
print("L04 M1 F", F([(Fraction(1, 2), 1000), (Fraction(1, 2), 4000)], 2000))
print("L04 Ex1.7 F_X", [str(F([(Fraction(1, 2), 2000), (Fraction(1, 2), 4000)], t)) for t in (2000, 3000, 4000)],
      "F_Y", [str(F([(Fraction(1, 2), 3000), (Fraction(1, 2), 4000)], t)) for t in (2000, 3000, 4000)])
print("L04 E1 I_Y(4000) pair B", I([(Fraction(1, 2), 3000), (Fraction(1, 2), 4000)], 4000))
print("L04 E2 counts sum", 3 + 10 + 1 + 10)
