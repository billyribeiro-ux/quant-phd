"""Check the L09 claim: at offset 1e9 the rounding error of the running sums exceeds the 174.5 being estimated."""
import random
from fractions import Fraction
rng = random.Random(90)
xs = [1e9 + rng.random() for _ in range(2000)]
t = 0.0; q = 0.0
for x in xs:
    t += x; q += x * x
exact_q = sum(Fraction(x) * Fraction(x) for x in xs)
exact_t = sum(Fraction(x) for x in xs)
print("abs error of computed sum of squares:", float(abs(Fraction(q) - exact_q)))
print("abs error of computed sum:", float(abs(Fraction(t) - exact_t)))
print("true S_n ~ 174.47; ratio of sum-of-squares error to S_n:", float(abs(Fraction(q) - exact_q) / Fraction(174.47)))
