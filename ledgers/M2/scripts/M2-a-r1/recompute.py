# Independent recomputation (exact fractions) of the displayed numbers in the M2 hub and lessons L01-L06.
# Usage: .venv/bin/python -I ledgers/M2/scripts/M2-a-r1/recompute.py
from fractions import Fraction as F
import math
print("hub 6/8 =", F(6, 8), " 7/8 =", F(7, 8), " 0.8*8 =", F(4, 5) * 8)
print("L01 N for mech-1 (eps 0.01):", min(n for n in range(1, 2000) if F(13, n + 4) < F(1, 100)))
print("L01 least N eps 1e-4:", min(n for n in range(1, 20000) if F(1, 10000) > F(1, n + 1) and all(F(1, m + 1) < F(1, 10000) for m in range(n, n + 50))))
print("L01 a_1000 =", float(F(2001, 1001)), " 1/1001 =", float(F(1, 1001)), " a_9 error =", F(1, 10))
print("L02 sum err n=10 =", F(12, 110), " product err n=100 =", F(302, 10100), " quotient err n=1000 =", float(F(5004, 1001 * 1002)))
print("L02 closed-form quotient error at n=1 =", F(9, 6), " direct |a1/b1-2| =", abs(F(3, 2) / 3 - 2))
print("L03 gap h=0.001 =", float(1 + 4 * F(1, 1000) - F(1, 10**6)), " f(1-h)=", float((1 - F(1, 1000)) ** 2))
print("L04 (3h+h^2)/h at 1e-6 =", float((3 * F(1, 10**6) + F(1, 10**12)) / F(1, 10**6)))
print("L05 p' =", 2 * 1.5 * 1.5**3 + (1.5**2 + 1) * 3 * 1.5**2, " q' =", F(29, 49), " c' =", 6 * 1.5 * (1.5**2 + 1) ** 2)
print("L05 E1 h^2 p'''/6 =", 1e-8 * (60 * 1.5**2 + 6) / 6, " lab sizes 2.35e-7, 8.55e-7 vs h^2 =", 1e-8)
print("L06 1/sqrt3 =", 1 / math.sqrt(3), " 2/sqrt3 =", 2 / math.sqrt(3), " f(-2)=", (-2) ** 3 - 3 * (-2))
