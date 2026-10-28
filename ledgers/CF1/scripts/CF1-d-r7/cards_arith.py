from fractions import Fraction as F
import math
# c009: exact discounted sum of 3000..3800 at 8 percent, outlay 10000
s = sum(F(c) / F(108, 100) ** t for t, c in zip(range(1, 6), [3000, 3200, 3400, 3600, 3800]))
print("c009 exact sum", float(s), "npv exact", float(s - 10000), "to cents", round(float(s - 10000), 4))
print("c009 exact npv as fraction decimal:", float(s - 10000))
# c011: NPV at 20 percent of -1000, 600, 600
print("c011 npv20", -1000 + 600 / 1.2 + 600 / 1.2 ** 2)
# c016: -1 at 0, 1.05 at 1 at 6% and 3%
print("c016 6%", -1 + 1.05 / 1.06, "3%", -1 + 1.05 / 1.03)
# c017: A (-100,0,130), B (-100,120,0): NPV_A - NPV_B = (1+r)^-2 (10-120r)? check at r=1/12
r = 1 / 12
print("c017 diff at 1/12", (-100 + 130 / (1 + r) ** 2) - (-100 + 120 / (1 + r)), "formula", (1 + r) ** -2 * (10 - 120 * r))
# c032: working-capital flows 1..4 at 8%
pv = -690 / 1.08 + 10 / 1.08 ** 2 + 0 / 1.08 ** 3 + 680 / 1.08 ** 4
print("c032 pv", pv, "sum", -690 + 10 + 0 + 680)
# c043: nominal rate
print("c043 nominal", 1.06 * 1.03 - 1, "additive", 0.06 + 0.03)
# c046: 30,000,000 cents growing at 3 percent
print("c046 y1", 30000000 * 1.03, "y4", 30000000 * 1.03 ** 4)
# c053/c058: NPV at 5 percent of P, cents -> dollars
npv = lambda r: -100000 + 230000 / (1 + r) - 132000 / (1 + r) ** 2
print("c058 npv5", npv(0.05), "c060 npv15", npv(0.15), "avg irr", npv(0.15))
# c054/c093/c094 A and B NPV at 10%: B (-200000,250000,...)? check via lab numbers
print("c053 factor check", [round(-2000 * (11 * x - 10) * (6 * x - 5) - (-100000 + 230000 * x - 132000 * x * x), 9) for x in (0.3, 0.7)])
# c055 IRRs
print("c055 A irr", -1 + 130000 / 100000, "B irr", -1 + 250000 / 200000 - 0.0)
# c097: A minus B NPV at 10 percent, cents, and PV of A years 4 to 6
A = [-1000000, 300000, 400000, 400000, 300000, 200000, 100000]
B = [-1000000, 300000, 400000, 400000, 0, 0, 0]
g = sum(a / 1.1 ** t for t, a in enumerate(A)) - sum(b / 1.1 ** t for t, b in enumerate(B))
pv46 = sum(A[t] / 1.1 ** t for t in (4, 5, 6))
print("c097 gap", g, "PV years4-6", pv46)
# c082 ratio and c081 z score
print("c081 z", (79216.82 - 79078.68) / 221.01, "c082 ratio", 49419.62 / 49379.84)
# c083 binomial se
p = 0.0552
print("c083 se", math.sqrt(p * (1 - p) / 50000))
# c068/c074 paybacks
print("c068 disc payback A at 10", end=" ")
d = [f / 1.1 ** t for t, f in enumerate(A)]
cum = d[0]
for t in range(1, 7):
    if cum + d[t] >= 0:
        print(t - 1 + (-cum) / d[t]); break
    cum += d[t]
# c094: NPV at 10 for B and A in $ of L04 projects
A4 = (-100000, 130000); B4 = (-200000, 250000)
print("c094 A", -100000 + 130000 / 1.1, "B", -200000 + 250000 / 1.1)
# c088/c044 etc: 1 + n for real 0.06 pi 0.03 done
# c057 terminal value zero: trivially
# c081: closed form inside lab; c063 etc n/a
# c013 NPV at 0 and 20 percent of lab A
A1 = [-10000, 3000, 3200, 3400, 3600, 3800]
print("c013", sum(A1), sum(c / 1.2 ** t for t, c in enumerate(A1)))
