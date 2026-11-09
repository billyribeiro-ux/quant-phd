"""Independent re-derivation of the numbers in the FC1-b cards changed or re-read in round 8."""
from fractions import Fraction as F
import datetime
import math
import random


def cents(x):
    return math.floor(x * 100 + F(1, 2))


print("c010 total after stage 10, cents:", cents(1000 * (1 - F(9, 10) ** 11) / F(1, 10)), "expect 686189")
print("c011 limit with phi=1/2, cents:", cents(F(1000) / (1 - F(45, 100))), "expect 181818")
print("c092 half-share stage 10, cents:", cents(F(1000) * (1 - F(45, 100) ** 11) / F(55, 100)), "expect 181790")
print("c084 net/gross ratio:", float(F(14282414, 68398886)), "expect 0.20881062..., rounds to 0.209")
print("c082/c172 consideration 216*10060:", 216 * 10060, "expect 2172960")
print("c083 weekdays:", datetime.date(2026, 10, 28).strftime("%A"), datetime.date(2026, 10, 30).strftime("%A"))
ok = True
for rho in [F(1, 10), F(1, 3), F(1, 2), F(99, 100), F(1)]:
    for n in range(60):
        m = (1 - (1 - rho) ** (n + 1)) / rho
        ok = ok and ((m < 1 / rho) if rho < 1 else (m == 1 / rho))
print("c016 multiplier strictly below 1/rho for rho<1, equal at rho=1, n<60:", ok)
print("c016 stage 10 multiplier rho=1/10:", float((1 - F(9, 10) ** 11) / F(1, 10)), "expect 6.8618940391")
eq = True
for rho in [F(k, 12) for k in range(1, 13)]:
    for phi in [F(k, 12) for k in range(0, 13)]:
        eq = eq and ((1 / (1 - phi * (1 - rho)) == 1 / rho) == (phi == 1 or rho == 1))
print("c153 limit equals d/rho iff phi=1 or rho=1 on a 12x13 grid (d=1):", eq)
random.seed(8)
ok = True
for _ in range(300):
    rho = F(random.randint(1, 20), 20)
    d = F(random.randint(1, 1000))
    N = random.randint(0, 30)
    D = [d * (1 - rho) ** t for t in range(N + 1)]
    X = [rho * x for x in D]
    L = [x - y for x, y in zip(D, X)]
    ok = ok and sum(X) + sum(L) == sum(D)
print("c103 cumulative identity on 300 random (rho, d, n):", ok)
print("c050 (k-1)N > kN/2 iff k > 2, k in 3..49:", all(((k - 1) > F(k, 2)) == (k > 2) for k in range(3, 50)))
print("c037 quoted spread 5015-4985, relative 30/5000:", 5015 - 4985, F(30, 5000), float(F(30, 5000)))
print("c043 h*V = 2*200:", 2 * 200, "c139 mid-move:", -1 * 100 * (10000 - 9990), "c140 P:", 400 - 1000)
print("c061/c171 cost and average:", 60 * 1000 + 90 * 1100, (60 * 1000 + 90 * 1100) / 150)
print("c153/c152 check at phi=1/2, rho=1/10: limit", float(1 / (1 - F(1, 2) * F(9, 10))), "d/rho", 10)
