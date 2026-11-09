"""Re-derive the float and hand-number claims in grader/test_project.py docstrings (FC1 slice c, round 12)."""
from fractions import Fraction as F
import math

print("496bps float, 1/1.0496 path:", repr(1734792 / 1.0496), " (1+0.0496)**-1 path:", repr(1734792 * (1 + 0.0496) ** -1))
print("496bps exact:", F(1734792) / F(10496, 10000), "== 3305625/2:", F(1734792) / F(10496, 10000) == F(3305625, 2))
print("13 at 400bps float (1+0.04)**-1*13:", repr(13 * (1 + 0.04) ** -1), " 13/1.04 float:", repr(13 / 1.04))
print("exact 13/1.04:", F(13) / F(104, 100))
print("hand terms exact:", float(F(500) / (F(104, 100)) ** 1), float(F(500) / (F(104, 100)) ** 2), float(F(10500) / (F(104, 100)) ** 3))
# just-under-half fixture: Bond(300075005,0,3) at 1 bps
y = F(1, 10000)
pv = F(300075005) / (1 + y) ** 3
print("hair-under: pv float", float(pv), "floor", math.floor(pv), "frac - 1/2", pv - math.floor(pv) - F(1, 2))
print("claimed: 299985000 + 1/2 - 1/(2*1000300030001)", F(299985000) + F(1, 2) - F(1, 2 * 1000300030001))
print("pv == claimed:", pv == F(299985000) + F(1, 2) - F(1, 2 * 1000300030001))
print("half_away", math.floor(pv + F(1, 2)))
# 10500/101 and 10500/1001 and 10500/21
print("10500/101 =", float(F(10500, 101)), " 10500/1001 =", float(F(10500, 1001)), " 10500/21 =", F(10500, 21), " 10500/2.5 =", F(10500) / F(5, 2), " 10500/4 =", F(10500, 4))
print("fixture B 210000/19 =", float(F(210000, 19)))
print("10001*50% =", F(10001, 2))
print("ROUNDING_CASE coupons check on make_instance(6) later")
