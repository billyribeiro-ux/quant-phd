"""Re-derive the prose and docstring numbers of the FC1 project page, its grader docstrings and sampled cards (exact Fractions and float probes)."""
from fractions import Fraction as F
import datetime

def half_away(x):
    m = abs(x)
    w = (2 * m.numerator + m.denominator) // (2 * m.denominator)
    return w if x >= 0 else -w

print("lab1 exact PV", float(sum(F(a) / (1 + F(400, 10000)) ** t for t, a in [(1, 5000), (2, 5000), (3, 105000)])), "price", half_away(sum(F(a) / (1 + F(400, 10000)) ** t for t, a in [(1, 5000), (2, 5000), (3, 105000)])))
y = F(400, 10000); ev = [(1, 500), (2, 500), (3, 10500)]
print("rounding fixture exact PV", float(sum(F(a) / (1 + y) ** t for t, a in ev)), "terms", [float(F(a) / (1 + y) ** t) for t, a in ev], "rounded terms sum", sum(half_away(F(a) / (1 + y) ** t) for t, a in ev))
print("fixture B exact", float(F(10500) / F(95, 100)), half_away(F(10500) / F(95, 100)))
print("496 bps exact", F(1734792) / F(10496, 10000), "coupon", float(F(1704285 * 179, 10000)))
print("2**40+1 times 9851", (2**40 + 1) * 9851, "odd", ((2**40 + 1) * 9851) % 2, "above 2**53", (2**40 + 1) * 9851 > 2**53)
for n in (12, 13, 14, 15):
    e = [(t, 500) for t in range(1, n + 1)]; e[-1] = (n, 10500)
    print("par check n", n, sum(F(a) / (1 + F(500, 10000)) ** t for t, a in e))
print("c010", float(1000 * (1 - F(9, 10) ** 11) / F(1, 10)), "c011", float(F(1000) / (1 - F(45, 100))), "c012", float(1000 * F(68619, 10000)))
print("c084", float(F(14282414, 68398886)))
print("c092 half redeposit stage 10", float(1000 * sum(F(45, 100) ** k for k in range(11))))
print("c083 weekday", datetime.date(2026, 10, 28).strftime("%A"), datetime.date(2026, 10, 30).strftime("%A"))
print("c061", 60 * 1000 + 90 * 1100, (60 * 1000 + 90 * 1100) / 150)
print("c082", 216 * 10060, "c097/c098", 4000 - 545)
print("float 13/(1+0.04)", repr(13 / (1 + 0.04)), "-> rounds to", int(13 / (1 + 0.04) + 0.5))
print("float 13*(1+0.04)**-1", repr(13 * (1 + 0.04) ** -1), "-> half-away rounds to", int(13 * (1 + 0.04) ** -1 + 0.5))
print("float 1734792/(1+0.0496)", repr(1734792 / (1 + 0.0496)))
