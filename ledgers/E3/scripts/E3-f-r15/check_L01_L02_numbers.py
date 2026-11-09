"""Round-14 independent re-derivation of every number in L01 and L02 prose (E3 slice f).

Uses mpmath-free exact Fractions and the decimal module for 40-digit roots. Prints each quantity so the
verifier can compare it with the page text.
"""
from fractions import Fraction
from decimal import Decimal, getcontext
import math

getcontext().prec = 50

def dsqrt(x):
    return Decimal(x).sqrt()

# L01 Example 1.4 and Misconception 1, Problem M1, R3, E1, E3
A = [(0, Fraction(1, 4)), (100, Fraction(1, 2)), (400, Fraction(1, 4))]
ev = lambda L, f: sum((p * f(x) for x, p in L), Fraction(0))
print("L01 Ex1.4 E X", ev(A, lambda x: Fraction(x)), "E X^2", ev(A, lambda x: Fraction(x * x)))
print("L01 M1 EX", ev([(20, Fraction(1, 5)), (50, Fraction(3, 10)), (80, Fraction(1, 2))], lambda x: Fraction(x)),
      "Eu", ev([(20, Fraction(1, 5)), (50, Fraction(3, 10)), (80, Fraction(1, 2))], lambda x: Fraction(x * x)))
print("L01 M2 Eu(L)", ev([(0, Fraction(1, 2)), (100, Fraction(1, 2))], lambda x: Fraction(x)),
      "Eu(M)", ev([(100, Fraction(1, 4)), (200, Fraction(3, 4))], lambda x: Fraction(x)))
print("L01 Ex3.4 C quad", ev([(0, Fraction(1, 3)), (150, Fraction(1, 3)), (300, Fraction(1, 3))], lambda x: Fraction(x * x)))
print("L01 R3 X quad", ev([(100, Fraction(1, 2)), (200, Fraction(1, 2))], lambda x: Fraction(x * x)), "Y quad", Fraction(150 * 150))
print("L01 quiz 5/12:", Fraction(1, 3) * Fraction(1, 4) + Fraction(2, 3) * Fraction(1, 2))

# L02 Example 1.5
EU = Decimal(40).sqrt() / 4 + Decimal(10) / 2 + Decimal(160).sqrt() / 4
print("L02 Ex1.5 EU sqrt unrounded", EU)
print("L02 Ex1.5 EU rounded 6dp", EU.quantize(Decimal("0.000001")))
CE = EU * EU
print("L02 Ex1.5 CE unrounded", CE, " CE from printed 9.743416 squared:", Decimal("9.743416") ** 2)
print("L02 Ex1.5 premium", 100 - CE, " cents CE", CE * 100, " cents premium", (100 - CE) * 100)

# L02 Section 3 lab: exact quantities at eps scales
X = [(-60, Fraction(1, 4)), (0, Fraction(1, 2)), (60, Fraction(1, 4))]
var = ev(X, lambda x: Fraction(x * x))
print("L02 var X", var)
w = 100
def ce_sqrt(eps):
    e = Decimal(0)
    for x, p in X:
        e += Decimal(p.numerator) / Decimal(p.denominator) * (Decimal(w) + Decimal(eps) * x).sqrt()
    return e * e
limit = Decimal(1) / 2 * (Decimal(1) / (2 * w)) * Decimal(1800)
print("limit", limit)
for eps in ("1", "0.5", "0.25", "0.1", "0.01"):
    prem = w - ce_sqrt(Decimal(eps))
    ratio = prem / (Decimal(eps) ** 2)
    print("eps", eps, "prem", prem, "ratio", ratio, "gap", abs(ratio - limit))
print("L02 E2 share of premium:", (Decimal("5.065835") - Decimal("4.5")) / Decimal("5.065835"),
      " share of approx:", (Decimal("5.065835") - Decimal("4.5")) / Decimal("4.5"))
print("L02 E1 ratio 0.028811/0.004565", Decimal("0.028811") / Decimal("0.004565"))
print("L02 M1 CE of 4/16 sqrt", (Decimal(2) + Decimal(4)) / 2)
print("L02 Ex2.3 r_A(100)", Decimal(1) / (2 * 100))
