"""Re-derive the card numbers that are not printed verbatim by a lab, from first principles.

Run with: python3 -I -W error ledgers/LX1/scripts/LX1-d-r12/card_claims_check.py
"""

import math
from fractions import Fraction

# LX1 L01 card c011 and Proposition 2.2 witness.
d1, r = 400, Fraction(9, 100)
f1 = Fraction(d1) / (r - Fraction(1, 100))
f3 = Fraction(d1) / (r - Fraction(3, 100))
print("c011 F(1%) =", f1, "F(3%) =", f3, "P=6000 above under 1%:", 6000 > f1, "below under 3%:", 6000 < f3)
# c012: present value of 400 at date 1 only, at 9 percent.
pv = Fraction(400) / (1 + r)
print("c012 PV =", pv, "=", float(pv), "rounds to", math.floor(pv + Fraction(1, 2)))
# c061 / c001 style check of ln 1.1.
print("c061 ln 1.1 =", round(math.log(1.1), 6), "simple minus log =", round(0.1 - math.log(1.1), 6))
# c082: N_t = N_0 + D - V_t because V_0 = D; V_m < N_0 + D is Assumption 1.2.
N0, D, delta, m = 4_000_000, 1_000_000, Fraction(1, 50), 4
Vm = D / (1 - delta) ** m
print("c082 V_m =", float(Vm), "< N0+D:", Vm < N0 + D)
# c037 / c038 / c039 depth closed form (Proposition 3.2(b)) with phi = beta = 1.
def depth(mm):
    Vm = Fraction(D) / (1 - delta) ** mm
    return Vm / (N0 + D - Vm) - Fraction(D, N0)
dx, dy = depth(12), depth(4)
print("c037 depth X =", float(dx) * 100, "c038 depth Y =", float(dy) * 100, "c039 ratio =", float(dx / dy))
# c067 ratio is free of beta*phi by construction (factor cancels).
print("c067 ratio with beta*phi scaling:", float(dx * Fraction(1, 2) / (dy * Fraction(1, 2))))
