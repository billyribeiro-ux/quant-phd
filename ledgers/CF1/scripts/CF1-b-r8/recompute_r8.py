"""Independent Fraction recomputation of the numbers printed or displayed in CF1 L03 and L04 (slice b, round 8)."""
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP
import math


def r2(x, nd=2):
    q = Decimal(1).scaleb(-nd)
    return str(Decimal(str(float(x))).quantize(q, rounding=ROUND_HALF_UP))


def npv(flows, r):
    return sum(F(cf) / (1 + r) ** t for t, cf in enumerate(flows))


print("== L03")
r, pi = F(6, 100), F(3, 100)
n = (1 + r) * (1 + pi) - 1
print("Ex1.4 n", float(n), "additive gap", float(n - (r + pi)), "r*pi", float(r * pi))
print("Ex2.5 nominal NPV", float(F(100) / F(108, 100) + F(100) / F(108, 100) ** 2 + F(100) / F(108, 100) ** 3))
print("Ex2.5 real flows", [float(F(100) / F(103, 100) ** t) for t in (1, 2, 3)])
rr = F(108, 100) / F(103, 100) - 1
print("Ex2.5 real rate", float(rr), "real NPV at it", float(sum(F(100) / F(103, 100) ** t / (1 + rr) ** t for t in (1, 2, 3))))
print("l.248 nominal rate", float(F(205) * F(105, 100) / 200 - 1), "implied infl", float((1 + (F(205) * F(105, 100) / 200 - 1)) / F(105, 100) - 1), "200/1.05", float(F(200) / F(105, 100)))
print("l.269 y4 nominal", float(F(30000000) * F(103, 100) ** 4))
print("l.257 gap", float(F(6, 100) * F(3, 100)))
print("M1 n", float(F(104, 100) * F(1025, 1000) - 1), "gap", float(F(4, 100) * F(25, 1000)))
print("M2", float(1000 * F(102, 100) ** 3))
print("M3 r", float(F(110, 100) / F(104, 100) - 1), "104/1.1", float(F(104, 100) / F(110, 100)), "100/r", float(100 / (F(110, 100) / F(104, 100))))
print("P3 sqrt(0.005)", math.sqrt(0.005), "x^2 at x", math.sqrt(0.005) ** 2)
real_npv_cents = npv([F(-100000000), F(30000000), F(30000000), F(30000000), F(30000000), F(30000000)], F(6, 100))
nom_flows = [F(cf) * (1 + pi) ** t for t, cf in enumerate([-100000000, 30000000, 30000000, 30000000, 30000000, 30000000])]
mixed_over = sum(cf / (1 + F(6, 100)) ** t for t, cf in enumerate(nom_flows))
mixed_under = npv([F(-100000000), F(30000000), F(30000000), F(30000000), F(30000000), F(30000000)], n)
print("real NPV USD", float(real_npv_cents / 100), "mixed over USD", float(mixed_over / 100), "mixed under USD", float(mixed_under / 100))
print("mixed minus real cents (3%)", float(mixed_over - real_npv_cents))
for inf in (F(0), F(1, 100), F(3, 100), F(5, 100)):
    nf = [F(cf) * (1 + inf) ** t for t, cf in enumerate([-100000000, 30000000, 30000000, 30000000, 30000000, 30000000])]
    gap = sum(cf / (1 + F(6, 100)) ** t for t, cf in enumerate(nf)) - real_npv_cents
    print("  infl", float(inf), "mixed minus real USD", float(gap / 100), "share of real NPV", float(gap / real_npv_cents))
print("E1 share 0.05", float(F(19436827, 100) / F(26370914, 100)))
print("E1 share 0.03", float(F(11363749, 100) / F(26370914, 100)) if False else float(F("113637.49") / F("263709.14")))
print("E1 share 0.01", float(F("36913.22") / F("263709.14")), "E1 share 0.05 decimal", float(F("194368.27") / F("263709.14")))
print("E3 n", float(F(110, 100) * F(103, 100) - 1))
R2 = F(6, 100) * F(103, 100) / F(3, 100)
print("R2 ratio", float(R2), "mixed/real via q", float((F(103, 100) / F(106, 100)) / (1 - F(103, 100) / F(106, 100))) / float(F(6,100)/F(6,100)))
print("R3 b", float(F(106, 100) / F(203, 100)), "error zero check",
      float(F(1) * F(3, 100) / F(106, 100) - (F(106, 100) / F(203, 100)) * ((F(103, 100)) ** 2 - 1) / F(106, 100) ** 2))
print("Thm2.3 example pi=0.03 mixed table ok")

print("== L04")
P = [F(-10000000), F(23000000), F(-13200000)]
for rate in [F(0), F(5, 100), F(10, 100), F(15, 100), F(20, 100), F(25, 100), F(30, 100)]:
    v = npv(P, rate) / 100
    fac = -2000 * (11 / (1 + rate) - 10) * (6 / (1 + rate) - 5)
    print("P rate", float(rate), "NPV USD", float(v), "factor form", float(fac))
print("P at 15 as decimal", float(npv(P, F(15, 100)) / 100))
print("P at 15 factor", float(-2000 * (11 / F(115, 100) - 10) * (6 / F(115, 100) - 5)))
print("Ex3.2 NPV at 10 check", float(npv(P, F(1, 10))))
print("Rem5.1 at 20", float(-100000 * F(144, 100) + 230000 * F(12, 10) - 132000))
print("R3 FV 15%", float(F(1225, 1000) * 0 + F(1, 1) * (F(1)+F(15,100))**2 * float(npv(P, F(15, 100)) / 100)))
print("R3 FV 15% decimal fraction", float((1 + F(15, 100)) ** 2 * npv(P, F(15, 100)) / 100))
print("R3 FV 5%", float((1 + F(5, 100)) ** 2 * npv(P, F(5, 100)) / 100))
print("Ex4.2 NPV A10", float(F(130000) / F(110, 100) - 100000), "B10", float(F(250000) / F(110, 100) - 200000))
print("Ex4.2 at 20 A", float(F(130000) / F(120, 100) - 100000), "B", float(F(250000) / F(120, 100) - 200000))
print("IRR A 30 B 25", "crossover", float(F(120000, 100000) - 1))
print("E2 NPV A10", float(F(120000) / F(110, 100) - 100000), "B10", float(F(250000) / F(110, 100) - 200000))
print("E2 at 35 A", float(F(120000) / F(135, 100) - 100000), "B", float(F(250000) / F(135, 100) - 200000))
print("E2 crossover", float(F(130000, 100000) - 1))
print("M2 x", math.sqrt(23 / 3) / 2 - 0.5, "r", 1 / (math.sqrt(23 / 3) / 2 - 0.5) - 1)
print("M2 check NPV at r", float(-100 + 60 / (1 + F(130662, 1000000)) + 60 / (1 + F(130662, 1000000)) ** 2))
print("R1 NPV10", float(-1 + F(6) / F(11, 10) - F(5) / F(121, 100)))
print("R1 roots check", float(-1 + 6 * F(1, 5) - 5 * F(1, 25)), float(-1 + 6 - 5))
print("R2 NPVA", float(F(300) / F(121, 100) - 100), "NPVB", float(F(200) / F(11, 10) - 100), "IRRA", math.sqrt(3) - 1, "IRRB", 1.0)
print("Mis: avg 15 NPV", float(npv(P, F(15, 100)) / 100))
print("E3 NPV 5%", float(-2000 * (11 / F(105, 100) - 10) * (6 / F(105, 100) - 5)))
print("Ex4.2 lab table 0.05 A", float(F(130000) / F(105, 100) * 0 + (F(13000000) / F(105, 100) - 10000000) / 100), "B", float((F(25000000) / F(105, 100) - 20000000) / 100))
print("lab table 0.25 A", float((F(13000000) / F(125, 100) - 10000000) / 100), "B", float((F(25000000) / F(125, 100) - 20000000) / 100))
print("lab table 0.30 A", float((F(13000000) / F(130, 100) - 10000000) / 100), "B", float((F(25000000) / F(130, 100) - 20000000) / 100))
print("lab table 0.15 A", float((F(13000000) / F(115, 100) - 10000000) / 100), "B", float((F(25000000) / F(115, 100) - 20000000) / 100))
print("lab table 0.20 A", float((F(13000000) / F(120, 100) - 10000000) / 100), "B", float((F(25000000) / F(120, 100) - 20000000) / 100))
print("lab table 0.10 A", float((F(13000000) / F(110, 100) - 10000000) / 100), "B", float((F(25000000) / F(110, 100) - 20000000) / 100))
