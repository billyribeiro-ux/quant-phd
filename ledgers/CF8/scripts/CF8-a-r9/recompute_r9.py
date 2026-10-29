"""Exact recomputation of the round-9 changed claims: quiz L02q3, Remark 2.2 rows, Prop 2.1 at gaps below and at 365, and the L01 Part C release."""
from fractions import Fraction as F
import math

def simple(d, gap):
    return F(d) / (1 - F(d)) * F(365, gap)

def compounded(d, gap):
    q = F(365, gap)
    x = F(d) / (1 - F(d))
    # (1/(1-d))^q with q rational: exact check via float for display only
    return (1 / (1 - float(d))) ** float(q) - 1, float(simple(d, gap))

rows = [("2/10 net 30", F(2, 100), 20), ("1/10 net 30", F(1, 100), 20), ("2/10 net 60", F(2, 100), 50), ("3/15 net 45", F(3, 100), 30)]
for name, d, gap in rows:
    c, s = compounded(d, gap)
    print(f"{name}: gap={gap} simple={100*s:.4f}% compounded={100*c:.4f}% compounded_larger={c > s}")
# Prop 2.1 boundary: gap exactly 365 -> q = 1, equality
for d in [F(1, 10), F(1, 2), F(9, 10)]:
    x = d / (1 - d)
    q = F(1)
    print("gap 365, d", d, "h(x) =", (1 + x) ** 1 - 1 - q * x, "(exact zero)")
# Gap below 365: q>1 strict
for gap in [364, 300, 20]:
    d = F(1, 10); q = F(365, gap); x = d / (1 - d)
    print("gap", gap, "h(x) positive:", (1 + x) ** 0 * 0 + (1 + float(x)) ** float(q) - 1 - float(q * x) > 0)
# L01 Part C
rel = F(9_000_000_000 * 5, 365)
print("release exact cents:", float(rel), "4dp:", f"{float(rel):.4f}", "half-up cents:", math.floor(rel + F(1, 2)))
print("receivables after:", f"{float(F(1_200_000_000) - rel):.4f}")
