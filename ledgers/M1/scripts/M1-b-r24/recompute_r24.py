# Independent recomputation of the numbers in the changed L05 Example 3.1 and misconception, and the L04 R3 claim.
from decimal import Decimal, getcontext
import math
getcontext().prec = 50
r = Decimal("0.05")
print("annual PV", Decimal(1000000) * (1 + r) ** -5, "-> whole cents", round(Decimal(1000000) * (1 + r) ** -5))
print("semi factor", 1 / (1 + r / 2) ** 10, "PV", Decimal(1000000) / (1 + r / 2) ** 10)
print("cont factor", math.exp(-0.25), "PV", 1000000 * math.exp(-0.25))
print("spread cents", 783526 - 778801)
for t in [0.5, 1, 2, 5, 10]:
    print("annual factor t=%s" % t, 1.05 ** -t, "in (0,1):", 0 < 1.05 ** -t < 1)
print("R3 r_12 for r=0.05", 12 * (math.exp(0.05 / 12) - 1))
print("counterexample Prop 1.4 sign check at r=-0.5 t=1:", 0.5 ** -1)
