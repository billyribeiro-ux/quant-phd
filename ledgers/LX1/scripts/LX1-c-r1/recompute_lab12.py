"""Independent recomputation of the rung-1 and rung-2 numbers on project.html (LX1-c round 1). Usage: python3 -I recompute_lab12.py
Exact Fractions; half-up rounding to the cent (dollars) and to two decimals (percent)."""
from fractions import Fraction as F
import math

def hu(x):
    m = math.floor(abs(x) + F(1, 2))
    return m if x >= 0 else -m

def dollars(cents_fraction):
    return hu(cents_fraction) / 100

D1 = 10_000_000  # cents, rung 1
falling = [F(p, 100) for p in (100, 97, 94, 91, 88, 85)]
rising = [F(p, 100) for p in (100, 103, 106, 109, 112, 115)]
print("rung1 falling real debt $:", [f"{dollars(F(D1) / p):.2f}" for p in falling])
print("rung1 rising real debt $:", [f"{dollars(F(D1) / p):.2f}" for p in rising])
bf = 100 * (falling[0] / falling[-1] - 1); br = 100 * (rising[0] / rising[-1] - 1)
print("rung1 burden change % falling:", hu(bf * 100) / 100, " rising:", hu(br * 100) / 100)
diff = F(D1) / falling[-1] - F(D1) / rising[-1]
print("rung1 period-5 difference cents exact:", float(diff), " printed $:", dollars(diff))
print("rung1 falling period-5 real value cents exact:", float(F(D1) / falling[-1]))
print("rung1 rising period-5 real value cents exact:", float(F(D1) / rising[-1]))

D2 = 4_000_000  # cents, rung 2
path = [F(p, 100) for p in (100, 99, 98, 96, 95, 93)]
print("rung2 real debt $:", [f"{dollars(F(D2) / p):.2f}" for p in path])
b2 = 100 * (path[0] / path[-1] - 1)
print("rung2 burden change %:", hu(b2 * 100) / 100)
print("rung2 wrong-inverted burden %:", hu(100 * (path[-1] / path[0] - 1) * 100) / 100)
print("rung2 no-division real debt $ each period:", dollars(F(D2)))
