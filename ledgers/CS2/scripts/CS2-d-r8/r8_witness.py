"""Round 8: rank-target witnesses and the wide-epsilon claims on project.html, exact vs float."""
import math
from fractions import Fraction
print("q=0.1 n=20 eps=0.05: exact qn-en =", float(Fraction(0.1) * 20 - Fraction(0.05) * 20), "> 1:", Fraction(0.1) * 20 - Fraction(0.05) * 20 > 1,
      "exact ceil", math.ceil(Fraction(0.1) * 20 - Fraction(0.05) * 20), "float ceil", math.ceil(0.1 * 20 - 0.05 * 20))
print("q=0.2500004 n=20 eps=0.05: qn =", float(Fraction(0.2500004) * 20), "exact target", math.ceil(Fraction(0.2500004) * 20 - Fraction(0.05) * 20),
      "q=0.25 target", math.ceil(Fraction(0.25) * 20 - Fraction(0.05) * 20), "needed at_or_below >=", float(Fraction(0.2500004) * 20 - Fraction(0.05) * 20))
print("wide eps 0.3 n=2 q=1: qn-en =", float(Fraction(2) - Fraction("0.3") * 2), "exact fraction of 0.3 float:", float(Fraction(0.3) * 2))
print("Lab3 qn-en", Fraction(1, 2) * 11 - Fraction("0.1") * 11, "ceil", math.ceil(Fraction(1, 2) * 11 - Fraction("0.1") * 11))
