from fractions import Fraction as F
D = 365
def dso(ar, rev): return F(ar * D) / rev
def dio(inv, cogs): return F(inv * D) / cogs
def dpo(ap, pur): return F(ap * D) / pur
f = lambda x: f"{float(x):.6f}"
# Example 3.3 / M1 / M2 / Remark 3.4
print("M1 DSO", f(dso(300_000, 2_400_000)), "DIO", f(dio(250_000, 1_500_000)), "DPO", f(dpo(200_000, 1_600_000)))
print("M1 CCC", f(dso(300_000, 2_400_000) + dio(250_000, 1_500_000) - dpo(200_000, 1_600_000)))
print("TWC", 300_000 + 250_000 - 200_000)
print("M2 release", f(F(2_400_000 * 10, D)), "one day", f(F(2_400_000, D)))
# M3 (1,460,000 purchases, 30 -> 45 days)
print("M3 dAP", F(15 * 1_460_000, D), float(F(15 * 1_460_000, D)))
# E1 2025/2026
y25 = (dso(600_000, 5_000_000), dio(480_000, 3_000_000), dpo(400_000, 3_200_000))
y26 = (dso(840_000, 6_000_000), dio(585_000, 3_900_000), dpo(480_000, 4_000_000))
c25 = y25[0] + y25[1] - y25[2]; c26 = y26[0] + y26[1] - y26[2]
print("E1 2025", [f(x) for x in y25], "cycle", f(c25))
print("E1 2026", [f(x) for x in y26], "cycle", f(c26))
print("E1 dCycle", f(c26 - c25), "parts", f(y26[0]-y25[0]), f(y26[1]-y25[1]), f(-(y26[2]-y25[2])))
# E3 average basis
print("E3 avg DSO", f(dso(720_000, 6_000_000)), "diff", f(dso(720_000, 6_000_000) - y26[0]), "P4.1", f(F((600_000 - 840_000) * D, 2 * 6_000_000)))
# Example 4.2 (cents)
print("Ex4.2 year-end", f(dso(1_200_000_000, 9_000_000_000)), "avg", f(dso(F(1_050_000_000 + 1_200_000_000, 2), 9_000_000_000)), "diff", f(F((1_050_000_000 - 1_200_000_000) * D, 2 * 9_000_000_000)))
# R2/R3 quoted equations: AR = DSO*Rev/D proportional to revenue
print("R3 AR ratio (same DSO) ", f(F(1) * F(2_400_000) / F(1)), "identity AR=DSO*Rev/D check", dso(300_000, 2_400_000) * 2_400_000 / D == 300_000)
