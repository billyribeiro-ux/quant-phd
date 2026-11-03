"""Check the L23 E3 claim: the float yield used by the lab differs from the exact 5 percent by about 2.8e-18, moving the price by about 2.1e-12 cents."""
from fractions import Fraction
import sys
ns = {}
src = open(sys.argv[1], encoding="utf-8").read().replace("\nmain()\n", "\n")
exec(compile(src, "twin_L23_nomain", "exec"), ns)
float_yield = 0.04 + 0.01
exact_offset = Fraction(float_yield) - Fraction(5, 100)
print("float yield", repr(float_yield), "exact 5% offset (float - exact):", float(exact_offset))
d1 = ns["price_first_derivative"](float_yield)
print("P'(float yield) =", d1)
print("price change from offset, cents:", d1 * float(exact_offset))
print("unrounded price at float yield minus 100000:", float(ns["price"](float_yield) - 100000))
print("integer price at float yield:", ns["price_cents"](float_yield))
