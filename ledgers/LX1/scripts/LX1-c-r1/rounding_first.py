"""Rung-1 worked step 3 claim: rounding the period-5 real value before the next computation would move the answer
in the last printed cent (LX1-c round 1). Computes the rounded-first routes exactly. Usage: python3 -I rounding_first.py"""
from fractions import Fraction
import math

def half_up(x):
    m = math.floor(abs(x) + Fraction(1, 2))
    return m if x >= 0 else -m

D = Fraction(10_000_000)  # cents
falling5 = Fraction(85, 100); rising5 = Fraction(115, 100)
V5f = D / falling5; V5r = D / rising5
print("exact V5 falling cents:", float(V5f), " rounded to whole cent:", half_up(V5f))
# Route 1 (page): exact difference, then round once
d_exact = V5f - V5r
print("route exact diff cents:", float(d_exact), "printed dollars:", half_up(d_exact) / 100)
# Route 2: round each real value to the cent first, then difference
d_rf = Fraction(half_up(V5f)) - Fraction(half_up(V5r))
print("route rounded-first diff cents:", d_rf, "printed dollars:", d_rf / 100, "->", half_up(d_rf) / 100)
# Route 3: burden change from rounded real value (period 5) vs exact
V0 = D
b_exact = 100 * (V5f / V0 - 1)
b_rf = 100 * (Fraction(half_up(V5f)) / V0 - 1)
print("burden exact:", float(b_exact), "printed", half_up(b_exact * 100) / 100)
print("burden from rounded real value:", float(b_rf), "printed", half_up(b_rf * 100) / 100)
# Route 4: the page's own claim for the difference: 'the difference of the two printed values'
print("difference of printed values dollars:", (half_up(V5f) - half_up(V5r)) / 100)
