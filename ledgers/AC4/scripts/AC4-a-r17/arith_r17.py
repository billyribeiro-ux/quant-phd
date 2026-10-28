from fractions import Fraction as F
import math
step = lambda h: 0 if h == 0 else math.ceil(h / 400) * 4000
v = F(12000, 1200)
err = max((abs(step(h) - v * h), h) for h in range(0, 1201))
print("R3 max err", err, float(err[0] / 4000))
print("R2", float(-F(120000, 1350**2) * 100), float(F(120000, 1450) - F(120000, 1350)))
print("L02 DOL", float(F(1350 * 2500, 555000)), "margin", float(F(2500) - F(2820000, 1350)))
print("c018 witness: OI over 0..5000 max at 5000 =", 1350 * 5000 - 2820000)
