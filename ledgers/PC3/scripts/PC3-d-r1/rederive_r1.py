"""Independent re-derivation of every number in the changed cards and the changed lesson hunks (PC3 slice d, round 1)."""
from fractions import Fraction as F
import math

def A(r):
    return sum((F(1) / (1 + r) ** t for t in range(1, 4)), F(0))

def npv(units, r, margin=5000, outlay=15000000):
    return -outlay + sum(F(units * margin) / (1 + r) ** t for t in range(1, 4))

def display(x, places):
    scale = 10 ** places
    n = math.floor(x * scale + F(1, 2))
    if places == 0:
        return str(n)
    whole, frac = divmod(abs(n), scale)
    return ("-" if n < 0 else "") + f"{whole}.{frac:0{places}d}"

r8, r10, r12 = F(8, 100), F(10, 100), F(12, 100)
print("A(8%) =", A(r8), "=", display(A(r8), 7), " A(10%) =", A(r10), "=", display(A(r10), 7), " A(12%) =", A(r12), "=", display(A(r12), 7))
print("A(10%) == 3310/1331:", A(r10) == F(3310, 1331))
for name, r in (("8", r8), ("10", r10), ("12", r12)):
    be = F(3000) / A(r)
    print(f"break-even at {name}%: exact {float(be):.6f}  display2 {display(be, 2)}  display4 {display(be, 4)}")
be8, be10, be12 = F(3000) / A(r8), F(3000) / A(r10), F(3000) / A(r12)
print("u* exact 10% == 399300/331:", F(3000) / A(r10) == F(399300, 331))
print("diff 8->10 (unrounded, display 2):", display(F(1164.1005) * 0 + (F(3000) / A(r10) - F(3000) / A(r8)), 4), "per 4dp values", F(12064344, 10000) - F(11641005, 10000))
print("width 8->12 exact:", float(be12 - be8), "avg per point exact:", float((be12 - be8) / 4))
print("4dp-rounded diff 8->10:", round(float(F(1206.3444) - F(1164.1005)), 4), " 10->12:", round(float(F(1249.0469) - F(1206.3444)), 4))
print("avg per point from 4dp:", round(float((F(1249.0469) - F(1164.1005)) / 4), 4))
print("printed diffs 1206.34-1164.10 =", F(120634, 100) - F(116410, 100), " 1249.05-1206.34 =", F(124905, 100) - F(120634, 100))
print()
print("NPV at 200 units, 10%: exact", npv(200, r10), " display0", display(npv(200, r10), 0), " -16655000000/1331 =", F(-16655000000, 1331), display(F(-16655000000, 1331), 0))
print("NPV at 1600 units, 10%:", display(npv(1600, r10), 0), "exact", npv(1600, r10))
print("NPV at 1200, 10%: exact", npv(1200, r10), "=", float(npv(1200, r10)), " == -105000000/1331:", npv(1200, r10) == F(-105000000, 1331))
print("NPV at 1300, 10%: exact", npv(1300, r10), "=", float(npv(1300, r10)), " == 1550000000/1331:", npv(1300, r10) == F(1550000000, 1331))
print("NPV at 200 and 1600 at 8%:", display(npv(200, r8), 0), display(npv(1600, r8), 0), " 12%:", display(npv(200, r12), 0), display(npv(1600, r12), 0))
print("NPV at 200 signs 8,10,12:", [npv(200, r) < 0 for r in (r8, r10, r12)], " 1600 signs:", [npv(1600, r) > 0 for r in (r8, r10, r12)])
print("NPV(1200) at 8% positive:", npv(1200, r8) > 0, " 1200 vs be8:", 1200 > be8)
print("1200 < be10:", 1200 < be10, " 1300 > be10:", 1300 > be10)
print("grid points positive at 10%:", [u for u in range(200, 1601, 100) if npv(u, r10) > 0])
print()
print("M2 NPV -100,60,60 at 10%:", -100 + F(60) / F(11, 10) + F(60) / F(121, 100), "== 500/121:", -100 + F(60) / F(11, 10) + F(60) / F(121, 100) == F(500, 121), float(F(500, 121)))
print("M3 u* 100000/(400 A10):", F(100000) / (400 * A(r10)), "== 33275/331:", F(100000) / (400 * A(r10)) == F(33275, 331), float(F(33275, 331)))
m_star = F(15000000) / (1600 * A(r10))
print("R3 m* =", float(m_star), " ratio =", float(m_star / 5000), " fall % =", float((1 - m_star / 5000) * 100))
print("E3 break-even 1600 check: npv at 1600 after m*=", float(F(-15000000) + sum(F(1600) * m_star / (1 + r10) ** t for t in range(1, 4))))
print()
print("Example 4.2 factor range checks: lower", F(2000) * 1 * F(1, 10), " upper", F(4000) * 2 * F(1, 5))
print("Fermi ratio 1600/200 =", F(1600, 200), "; each factor ratio:", F(4000, 2000), F(2, 1), F(1, 5) / F(1, 10))
print()
print("Remark 4.3 A check: 3000/A(8%) display4 =", display(F(3000) / A(r8), 4), " A(12%) =", display(A(r12), 7))
print("E1 3000/A(12) =", float(F(3000) / A(r12)))
print("4dp check 1249.0469 vs exact", float(F(3000) / A(r12)))
print("E3 average, exact", float((F(3000)/A(r12) - F(3000)/A(r8))/4), "displays", display((F(3000)/A(r12) - F(3000)/A(r8))/4, 2))
