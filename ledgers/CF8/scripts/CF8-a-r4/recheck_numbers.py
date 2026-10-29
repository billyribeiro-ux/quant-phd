"""Independent recomputation of prose numbers in CF8 hub, L01 and L02 (run with python -I)."""
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP
import math

def r2(x):
    return Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) if not isinstance(x, F) else \
        (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def npv(m, base, inv, n, r=F(1, 10)):
    A = sum((1 / (1 + r)) ** t for t in range(1, n + 1))
    return -inv + m * base * A + inv / (1 + r) ** n

# L02 M2/M3
dI = F((6_600_000 * 60 - 6_000_000 * 30), 365)
print("L02 M2 dI", float(dI), r2(dI), "m*", float(F(8, 100) * dI / 600_000), r2(F(8, 100) * dI / 600_000 * 100))
A84 = sum(F(1, 1) / F(108, 100) ** t for t in range(1, 5))
print("A(0.08,4)", float(A84))
t1 = -dI
t2 = F(10, 100) * 600_000 * A84
t3 = dI / F(108, 100) ** 4
print("M3 terms", float(t1), float(t2), float(t3), "sum", float(t1 + t2 + t3), r2(t1), r2(t2), r2(t3), r2(t1 + t2 + t3))
print("M3 check exact sum", float(npv(F(10, 100), 600_000, dI, 4, F(8, 100))))
# R1 M2
mnr = dI / (600_000 * A84)
print("m_nr", float(mnr), "ratio", float(mnr / (F(8, 100) * dI / 600_000)), "1/(1-1.08^-4)", float(1 / (1 - F(100, 108) ** 4)))
# E2 L02
dI2 = F(22_000_000 * 45 - 20_000_000 * 30, 365)
m2 = F(9, 100) * dI2 / 2_000_000
A93 = sum(F(1, 1) / F(109, 100) ** t for t in range(1, 4))
print("E2 dI", float(dI2), r2(dI2), "m*", float(m2), r2(m2 * 100), "A(0.09,3)", float(A93))
print("E2 NPV(0.06)", float(npv(F(6, 100), 2_000_000, dI2, 3, F(9, 100))), r2(npv(F(6, 100), 2_000_000, dI2, 3, F(9, 100))))
# L02 Example 3.4
dI3 = F(13_500_000 * 45 - 12_000_000 * 30, 365)
m3 = F(1, 10) * dI3 / 1_500_000
print("Ex3.4 dI", float(dI3), r2(dI3), "m*", float(m3), "NPV 5pct", float(npv(F(5, 100), 1_500_000, dI3, 5)), r2(npv(F(5, 100), 1_500_000, dI3, 5)))
# L02 Example 1.4 and E1
d = F(2, 100)
c = d / (1 - d) * F(365, 20)
print("Ex1.4 simple", float(c), "compound", (1 / (1 - d)) ** (365 / 20) - 1)
print("E1 bank: 1/15 net45", float(F(1, 100) / (1 - F(1, 100)) * F(365, 30)), " 2/10 net60", float(c.__class__(2,100)/(1-F(2,100))*F(365,50)))
# L01 numbers
print("L01 Ex3.3 cycle", float(F(300000*365, 2400000) + F(250000*365,1500000) - F(200000*365,1600000)))
print("L01 Ex4.2", float(F((1050000000-1200000000)*365, 2*9000000000)), float(F(1200000000*365, 9000000000)), float(F(1125000000*365,9000000000)))
print("L01 E1 2025/2026", [float(x) for x in (F(600000*365,5000000), F(480000*365,3000000), F(400000*365,3200000))],
      [float(x) for x in (F(840000*365,6000000), F(585000*365,3900000), F(480000*365,4000000))])
print("L01 E1 cycle25", float(F(600000*365,5000000)+F(480000*365,3000000)-F(400000*365,3200000)), "cycle26", float(F(840000*365,6000000)+F(585000*365,3900000)-F(480000*365,4000000)))
print("L01 E3 avg", float(F((600000+840000)*365, 2*6000000)), float(F(-240000*365, 12000000)))
print("L01 M3", float(F(60000 * 0 + 15 * 1460000, 365)))
print("L01 M2 release", float(F(2400000*10, 365)), "per day", float(F(2400000, 365)))
print("hub 7/9", float(F(7, 9)*100), "7.2 bar", 0.8*9)
print("hub 40/50 10/50", 40/50*100, 10/50*100)
print("hub 30000 rung2 availability", 50000-20000, "draw", min(70000, 50000-20000))
print("hub PV 110/1.1", 110/1.1, "DF", 1/1.05**2, "NPV", -1000+1200/1.1)
