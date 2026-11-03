"""Check the project page's worked example: q = 0.1, n = 20, epsilon = 0.05 gives exact target 2 and a 64-bit float target 1;
also q = 0.2500004 on n = 20, epsilon 0.05: qn = 5.000008, exact target 5, and q rounded to six places gives target 4."""
import math
from fractions import Fraction
n, q, e = 20, 0.1, 0.05
exact_target = math.ceil(Fraction(q) * n - Fraction(e) * n)
float_target = math.ceil(q * n - e * n)
print("exact diff - 1 > 0:", Fraction(q) * n - Fraction(e) * n - 1 > 0, "| exact target:", exact_target, "| float target:", float_target)
q2 = 0.2500004
print("qn =", float(Fraction(q2) * 20), "| exact target:", math.ceil(Fraction(q2) * 20 - Fraction(e) * 20),
      "| six-place q target:", math.ceil(Fraction(round(q2, 6)) * 20 - Fraction(e) * 20))
