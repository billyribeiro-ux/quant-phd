"""Independent check of L06 numbers (PC3-b round 6), exact fractions, own formulas from the page (Props 1.1-3.2)."""
from fractions import Fraction as F
import math

def A(r):
    return sum(F(1) / (1 + r) ** t for t in range(1, 4))

def npv(u, r, outlay=15_000_000, m=5000):
    return -outlay + sum(F(u * m) / (1 + r) ** t for t in range(1, 4))

def disp(x, places):
    s = 10 ** places
    n = math.floor(x * s + F(1, 2))
    return n / s if places else n

A10 = A(F(1, 10))
print("A10", A10, "== 3310/1331:", A10 == F(3310, 1331))
be = {r: F(15_000_000, 5000) / A(r) for r in (F(8, 100), F(1, 10), F(12, 100))}
for r, v in be.items():
    print("rate", r, "break-even exact", float(v), "display", float(disp(v, 2)))
print("unrounded to 4dp:", {str(r): round(float(v), 4) for r, v in be.items()})
d_8_10 = be[F(1, 10)] - be[F(8, 100)]
d_10_12 = be[F(12, 100)] - be[F(1, 10)]
print("diff 8->10", float(d_8_10), float(disp(d_8_10, 2)), " diff 10->12", float(d_10_12), float(disp(d_10_12, 2)))
print("printed-value diffs: 1206.34-1164.10 =", F("1206.34") - F("1164.10"), " 1249.05-1206.34 =", F("1249.05") - F("1206.34"))
width = be[F(12, 100)] - be[F(8, 100)]
print("E3 width", float(width), float(disp(width, 2)), " per point", float(width / 4), float(disp(width / 4, 2)))
print("E3 1249.0469-1164.1005 =", float(F("1249.0469") - F("1164.1005")))
print("E3 1206.3444-1164.1005 =", float(F("1206.3444") - F("1164.1005")), " 1249.0469-1206.3444 =", float(F("1249.0469") - F("1206.3444")))
# NPV values
for r in (F(8, 100), F(1, 10), F(12, 100)):
    lo, hi = npv(200, r), npv(1600, r)
    print("rate", r, "NPV lower", float(lo), disp(lo, 0), "upper", float(hi), disp(hi, 0))
print("grid NPV at 1200 (10%):", npv(1200, F(1, 10)), float(npv(1200, F(1, 10))), "closed -105000000/1331:", float(F(-105000000, 1331)))
print("grid NPV at 1300 (10%):", float(npv(1300, F(1, 10))), "1550000000/1331 =", float(F(1550000000, 1331)))
print("grid >0 count:", sum(1 for u in range(200, 1601, 100) if npv(u, F(1, 10)) > 0), "largest negative grid point:", max(u for u in range(200, 1601, 100) if npv(u, F(1, 10)) < 0))
print("grid increasing:", all(npv(a, F(1, 10)) < npv(a + 100, F(1, 10)) for a in range(200, 1500, 100)))
print("E1 annuity 12%:", float(A(F(12, 100))), "3000/A =", float(3000 / A(F(12, 100))))
print("M2 NPV:", npv_small := (-100 + F(60) / F(11, 10) + F(60) / F(121, 100)), float(npv_small), F(500, 121) == npv_small)
print("M3 break-even:", F(100000, 400) / A10, "33275/331 =", F(33275, 331), float(F(33275, 331)))
print("R1 log widths", math.log(4000 / 2000), math.log(2 / 1), math.log((1 / 5) / (1 / 10)), math.log(2))
mstar = F(15_000_000, 1600) / A10
print("R3 m*", float(mstar), float(mstar / 5000), "fall %", float((5000 - mstar) / 5000 * 100))
print("Example 4.2 breakeven exact", float(F(399300, 331)), "matches 3000/A:", F(399300, 331) == F(15_000_000, 5000) / A10)
print("Fermi bounds product:", 2000 * 1 * F(1, 10), 4000 * 2 * F(1, 5))
print("Prop 2.1 (i) check at S=9700 D=97/100 F=10100:", F(10100) - F(9700) / F(97, 100))
print("forward no-arb 9700/0.97 =", F(9700) / F(97, 100))
print("L06 M1 4900/0.98 =", F(4900) / F(98, 100), " payoff", F(5050) - F(4900) / F(98, 100))
