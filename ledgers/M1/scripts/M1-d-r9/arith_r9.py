"""Round-9 recomputation of the numbers the delta sentences state (M1-d): run with python -I."""
import math
from fractions import Fraction as F

# new test at project grader line 307-313: annual rate 1e-7, 100,000,000 cents, 12 months
i = F("1e-7") / 12
exact = 100_000_000 * i / (1 - (1 + i) ** -12)
print("tiny-rate exact payment (cents):", float(exact), "loan over months:", 100_000_000 / 12, "correction:", float(exact - F(100_000_000, 12)), "rounded:", math.floor(exact + F(1, 2)))
# comment at grader lines 334-335: 499999999999 at annual 1.2e-11 (monthly 1e-12), one month
x = F(499999999999) * (1 + F(1, 10**12))
from decimal import Decimal, getcontext
getcontext().prec = 40
print("1.2e-11 case exact value (decimal):", Decimal(499999999999) * (1 + Decimal("1e-12")))
# Lab 3 bound and perpetuity error
n, ii = 300, 0.00375
print("bound n(1+i)^n+1:", round(n * (1 + ii) ** n + 1, 4))
v = 1 / 1.05
print("perpetuity error at 344 payments:", v**344 / 0.05, "at 345:", v**345 / 0.05)
print("5e-8 = 1e-6/20:", 1e-6 / 20)
print("(1+0.00375)^12 =", (1 + ii) ** 12, "> 1.045:", (1 + ii) ** 12 > 1.045)
print("tail q^400/(r-g):", ((1.02) / 1.05) ** 400 / 0.03)
