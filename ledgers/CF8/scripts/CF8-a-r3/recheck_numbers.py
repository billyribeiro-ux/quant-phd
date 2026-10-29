"""CF8-a round 3: independent exact recomputation of every number quoted in the hub, L01 and L02 prose and quiz."""
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F
import math


def hu(x, nd=2):
    """Half-up rounding of an exact value to nd decimals, returned as a string."""
    q = Decimal(x.numerator) / Decimal(x.denominator) if isinstance(x, F) else Decimal(str(x))
    return str(q.quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))


def fl(x):
    return float(x)


D = 365
print("== hub placement")
print("0.8*9 =", F(4, 5) * 9, "; 7/9 =", hu(F(700, 9) / 100, 1), "%")  # 77.8
print("110/1.1 =", F(110) / F("1.1"), "; 1/1.05^2 =", hu(1 / F(105, 100) ** 2, 4), "; -1000+1200/1.1 =", hu(-1000 + F(1200) / F("1.1")))
print("hub split 40/50 =", F(40, 50) * 100, "% ; 10/50 =", F(10, 50) * 100, "%")
print("skill1 shortfall:", 20000 - (30000 + 40000 - 120000), " skill2 draw:", min(20000 - (-50000), 50000 - 20000), " shortfall left:", (20000 + 50000) - min(70000, 30000))

print("== L01")
rev, cogs, pur, ar, inv, ap = 2_400_000, 1_500_000, 1_600_000, 300_000, 250_000, 200_000
dso = F(ar * D, rev); dio = F(inv * D, cogs); dpo = F(ap * D, pur)
print("M1 DSO", dso, hu(dso), "DIO", float(dio), hu(dio), "DPO", dso and hu(dpo), "CCC", float(dso + dio - dpo), hu(dso + dio - dpo))
print("TWC", ar + inv - ap)
rel = F(rev * 10, D)
print("release 10 days", float(rel), hu(rel), "exact4", hu(rel, 4), "per day", hu(F(rev, D)))
print("E1 2025 DSO", hu(F(600000 * D, 5000000)), "DIO", hu(F(480000 * D, 3000000)), "DPO", float(F(400000 * D, 3200000)), hu(F(400000 * D, 3200000)))
c25 = F(600000 * D, 5000000) + F(480000 * D, 3000000) - F(400000 * D, 3200000)
c26 = F(840000 * D, 6000000) + F(585000 * D, 3900000) - F(480000 * D, 4000000)
print("E1 CCC25", float(c25), hu(c25), "CCC26", float(c26), hu(c26), "chg", float(c26 - c25), hu(c26 - c25))
print("E1 parts dDSO", float(F(840000 * D, 6000000) - F(600000 * D, 5000000)), "dDIO", float(F(585000 * D, 3900000) - F(480000 * D, 3000000)), "-dDPO", float(-(F(480000 * D, 4000000) - F(400000 * D, 3200000))), hu(-(F(480000 * D, 4000000) - F(400000 * D, 3200000))))
print("E3 avg DSO", float(F(720000 * D, 6000000)), "E3 Prop4.1", float(F((600000 - 840000) * D, 2 * 6000000)))
prev, end, revx = 1_050_000_000, 1_200_000_000, 9_000_000_000
print("Ex4.2 yr-end", float(F(end * D, revx)), hu(F(end * D, revx)), "avg", float(F((prev + end) * D, 2 * revx)), hu(F((prev + end) * D, 2 * revx)), "diff", float(F((prev - end) * D, 2 * revx)), hu(F((prev - end) * D, 2 * revx), 4))
print("Remark 4.3 360/365 check", float(F(360, 365)))
print("Ex4.2 diff of printed 48.67-45.63 =", F("48.67") - F("45.63"))
print("M3 DPO change: 15*1460000/365 =", F(15 * 1_460_000, D))
print("Remark 3.4 release check", hu(F(2_400_000, D)))
print("M2 release exact", float(F(2_400_000 * 10, D)), hu(F(2_400_000 * 10, D)))

print("== L02")
def simple(d, days):
    return d / (1 - d) * F(D, days)
def comp(d, days):
    return float(1 / (1 - d)) ** (D / days) - 1
print("Ex1.4 simple", float(simple(F(2, 100), 20)), hu(simple(F(2, 100), 20) * 100), "comp", comp(0.02, 20) * 100)
for d, g in [(F(2, 100), 20), (F(1, 100), 20), (F(2, 100), 50), (F(3, 100), 30)]:
    print("  table row simple%", hu(simple(d, g) * 100), "comp%", round(comp(float(d), g) * 100, 4))
print("M1 1/15 net 45", float(simple(F(1, 100), 30)), hu(simple(F(1, 100), 30) * 100))
print("E1 2/10 net 60", float(simple(F(2, 100), 50)), hu(simple(F(2, 100), 50) * 100))
print("financed 0.5% 50 days", hu(simple(F(5, 1000), 50) * 100))

def npv(m, rev_x, inv_, n, r=F(1, 10)):
    A = sum((1 / (1 + r)) ** t for t in range(1, n + 1))
    return -inv_ + m * rev_x * A + inv_ / (1 + r) ** n, A

r = F(1, 10)
rev0, n0, n1, drev = 12_000_000, 30, 45, 1_500_000
dI = F((rev0 + drev) * n1 - rev0 * n0, D)
print("Ex3.4 dI", float(dI), hu(dI), "m*", float(r * dI / drev), hu(r * dI / drev * 100))
v, A5 = npv(F(5, 100), drev, dI, 5)
print("Ex3.4 NPV at 5% over 5y", float(v), hu(v), "A5", float(A5))
v0, _ = npv(r * dI / drev, drev, dI, 5)
print("NPV at m* exact zero:", v0 == 0)

# E2
r9 = F(9, 100)
dI2 = F(22_000_000 * 45 - 20_000_000 * 30, D)
mstar2 = r9 * dI2 / 2_000_000
v2, A3 = npv(F(6, 100), 2_000_000, dI2, 3, r9)
print("E2 dI", float(dI2), hu(dI2), "m*", float(mstar2), hu(mstar2 * 100), "NPV(0.06)", float(v2), hu(v2), "A(0.09,3)", float(A3))

# M2/M3/R1
rr = F(8, 100)
dI3 = F(6_600_000 * 60 - 6_000_000 * 30, D)
m3 = rr * dI3 / 600_000
print("M2 dI", float(dI3), hu(dI3), "m*", float(m3), hu(m3 * 100))
v3, A4 = npv(F(10, 100), 600_000, dI3, 4, rr)
print("M3 A(0.08,4)", float(A4), "term1", hu(-dI3), "term2", hu(F(10, 100) * 600_000 * A4), "term3", hu(dI3 / (1 + rr) ** 4), "sum exact", float(v3), hu(v3, 4), hu(v3))
print("M3 term2 exact", float(F(10, 100) * 600_000 * A4))
mnr = dI3 / (600_000 * A4)
print("R1 m_nr", float(mnr), hu(mnr * 100), "ratio", float(mnr / m3), hu(mnr / m3))
print("R1 closed form check", float(m3 / (1 - (1 + rr) ** -4)))
print("M2 horizon independence check:", [float(npv(m3, 600_000, dI3, n, rr)[0]) for n in (1, 4)])
print("E3 Part D printed numbers reproduce? (see lab)")
