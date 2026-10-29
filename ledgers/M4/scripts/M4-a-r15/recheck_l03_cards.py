"""Round-15 recheck of the L03 skewed-law and Bernoulli numbers and the L02 die/loss numbers used by changed cards."""
import math
from fractions import Fraction as F

law = [(0, F(1, 2)), (1, F(1, 4)), (2, F(1, 8)), (10, F(1, 8))]
mu = sum(x * p for x, p in law)


def m(k: int) -> F:
    return sum((x - mu) ** k * p for x, p in law)


print("skewed law mu", mu, "m2", m(2), "m3", m(3), "m4", m(4), "g4", m(4) / m(2) ** 2, float(m(4) / m(2) ** 2))
three = [(-2, F(2, 5)), (1, F(1, 2)), (3, F(1, 10))]
mu3 = sum(x * p for x, p in three)
mm = lambda k: sum((x - mu3) ** k * p for x, p in three)  # noqa: E731
print("three-point mean", mu3, "m2", mm(2), "m3", mm(3), "m4", mm(4), "g4", mm(4) / mm(2) ** 2)
for p in (F(1, 10), F(1, 4)):
    q = 1 - p
    print("Bernoulli", p, "g3^2", (1 - 2 * p) ** 2 / (p * q), "g4", (1 - 3 * p * q) / (p * q))
print("loss sd", round(math.sqrt(2968750000), 2), "E[L^2]", 250000**2 * F(1, 20), "Var", 3125000000 - 12500**2)
print("die losses expected", 10000 * F(1, 20))
