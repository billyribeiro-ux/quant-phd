import math
from decimal import Decimal, ROUND_HALF_UP
# L03 Example 2.3 / Remark 2.4 (values as cited on the page)
P6 = 1068160 + 530408 - 1138473
print("L03 P6", P6, "Dr6", 1000000 - P6, "avail", 4000000 - (1000000 - P6))
# L04 Example 2.3, 2.4, 2.5
print("L04 const", 1200000 + 1200000 - 1800000, "U11", 1200000 + 1200000 - 1800000 - 1488640)
print("L04 peak-shortfall", 1288640 - 1288639)
x = 5 * 1234567 / 7
print("L04 slip exact", x, "half_up", int(Decimal(5 * 1234567) / Decimal(7)).__class__ and (Decimal(5*1234567)/Decimal(7)).quantize(Decimal(1), rounding=ROUND_HALF_UP))
# L05 Remark 2.4, E1, E2, M2, R3
k = math.ceil(0.05 * 2000)
print("L05 k", k, "99/2000", 99 / 2000, "k-1", k - 1)
print("L05 E1", 1676 - 356, "E2", 365525 / 100, "2000-1676", 2000 - 1676)
p = 356 / 2000
print("L05 p", p, "p(1-p)", p * (1 - p), "SE250k", math.sqrt(p * (1 - p) / 2000))
print("L05 R3 N", p * (1 - p) / 0.002 ** 2, "0.0086/0.002", 0.0086 / 0.002)
print("L05 SE from 0.146316/2000 sqrt", math.sqrt(0.146316 / 2000))
