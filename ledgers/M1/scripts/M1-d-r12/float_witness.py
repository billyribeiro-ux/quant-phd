import math, random
from fractions import Fraction
random.seed(12)
found = []
for trial in range(400000):
    rate = round(random.uniform(0.001, 0.25), random.choice([2,3,4,5]))
    i_exact = Fraction(repr(rate)) / 12
    i_float = float(i_exact)
    opening = random.randint(1, 10**9)
    exact = math.floor(opening * i_exact + Fraction(1, 2))
    flt = math.floor(float(opening) * i_float + 0.5)
    if exact != flt:
        found.append((rate, opening, exact, flt))
        if len(found) >= 5: break
print("trials done; mismatches:", len(found))
for f in found: print("rate", f[0], "opening_cents", f[1], "exact_interest", f[2], "float_interest", f[3])
