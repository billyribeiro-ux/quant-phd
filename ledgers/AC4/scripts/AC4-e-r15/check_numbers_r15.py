from fractions import Fraction
import random, math
print("7600000/1400 =", round(7600000/1400, 2), "| exact", Fraction(7600000, 1400), float(Fraction(7600000, 1400)))
print("3142857 vs exact flexed profit gap:", Fraction(2600000 * 1500, 1400) - 3142857 if False else "see below")
worst = Fraction(0)
def half_up(x): return math.floor(x + Fraction(1, 2))
random.seed(15)
for _ in range(200000):
    a = Fraction(random.randint(0, 10**7), random.randint(1, 3000))
    b = Fraction(random.randint(0, 10**7), random.randint(1, 3000))
    e = abs(Fraction(half_up(a) - half_up(b)) - (a - b))
    worst = max(worst, e)
print("max |(rounded a - rounded b) - (a - b)| over 200000 random pairs:", float(worst), "< 1:", worst < 1)
# a - b with a exact half and b just below half is the extreme
a = Fraction(1, 2); b = Fraction(1, 2) - Fraction(1, 10**9)
print("extreme pair:", float(Fraction(half_up(a) - half_up(b)) - (a - b)))
