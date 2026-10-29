"""Round 8: independent recomputation of the Lab 3 expected block (a = 120 and a = 121, b = 1, c = 20)."""
import math
from fractions import Fraction

def half_up(x):
    return math.floor(x + Fraction(1, 2))

def outcome(structure, a, b, c):
    d = Fraction(a - b * c)
    if structure == "monopoly":
        q, f = d / 2, Fraction(a + b * c, 2 * b)
    elif structure == "cournot":
        q, f = 2 * d / 3, Fraction(a + 2 * b * c, 3 * b)
    else:
        q, f = d, Fraction(c)
    profit = (f - c) * q
    cs = q * q / (2 * b)
    w = cs + profit
    dwl = (d - q) ** 2 / (2 * b)
    return [half_up(v) for v in (q, f, profit, cs, w, dwl)]

expected = {
    120: {"monopoly": [50, 70, 2500, 1250, 3750, 1250], "cournot": [67, 53, 2222, 2222, 4444, 556],
          "bertrand": [100, 20, 0, 5000, 5000, 0]},
    121: {"monopoly": [51, 71, 2550, 1275, 3825, 1275], "cournot": [67, 54, 2267, 2267, 4534, 567],
          "bertrand": [101, 20, 0, 5101, 5101, 0]},
}
ok = True
for a in (120, 121):
    for s in ("monopoly", "cournot", "bertrand"):
        got = outcome(s, a, 1, 20)
        print(a, s, got, "match" if got == expected[a][s] else "MISMATCH")
        ok &= got == expected[a][s]
print("all 6 rows match the page expected block:", ok)
