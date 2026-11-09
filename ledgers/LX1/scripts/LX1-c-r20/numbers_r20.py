"""LX1-c round 20: independent re-derivation of every printed number in project.html (labs 1, 2, 3 and the prose).
Uses only the standard library; does not import the lab code. Run: python -I numbers_r20.py <repo-root>"""
import csv
import math
import statistics
import sys
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

root = sys.argv[1]


def r2(x):  # x is an exact Decimal or float; half-up to 2 places
    return Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def r2exact(fr):  # Fraction -> half-up 2 places via exact arithmetic
    q = fr * 100
    n = math.floor(abs(q) + Fraction(1, 2))
    return (n if q >= 0 else -n) / 100


# ---- Lab 1 ----
D = Fraction(10_000_000)  # cents
falling = [Fraction(p, 100) for p in (100, 97, 94, 91, 88, 85)]
rising = [Fraction(p, 100) for p in (100, 103, 106, 109, 112, 115)]
for name, path in (("falling", falling), ("rising", rising)):
    vals = [D / p for p in path]
    print("L1", name, [f"{float(v)/100:.6f}" for v in vals])
    print("L1", name, "burden %", float(100 * (path[0] / path[-1] - 1)), "rounded", r2exact(100 * (path[0] / path[-1] - 1)))
diff = D / falling[-1] - D / rising[-1]
print("L1 difference cents", float(diff), "dollars", float(diff) / 100, "rounded dollars", r2exact(diff / 100))
print("L1 ratio check 1/0.85 =", float(1 / Fraction(85, 100)))

# ---- Lab 2 ----
D2 = Fraction(4_000_000)
path2 = [Fraction(p, 100) for p in (100, 99, 98, 96, 95, 93)]
print("L2 real dollars", [str(D2 / p / 100) for p in path2])
print("L2 real rounded", [float(D2 / p / 100) for p in path2][-1])
print("L2 burden", float(100 * (path2[0] / path2[-1] - 1)), "rounded", r2exact(100 * (path2[0] / path2[-1] - 1)))
print("L2 inverted burden", r2exact(100 * (path2[-1] / path2[0] - 1)))

# ---- Lab 3 ----
rows = []
with open(f"{root}/course/assets/data/market/fx_monthly.csv", encoding="utf-8", newline="") as h:
    for row in csv.DictReader(h):
        rows.append((row["month"], row["GBP"]))
print("months", len(rows), rows[0][0], rows[-1][0], "blank GBP", sum(1 for _, v in rows if v.strip() == ""))
# independent month check
def idx(m):
    y, mm = m.split("-")
    return int(y) * 12 + int(mm)
assert all(idx(rows[i][0]) == idx(rows[i - 1][0]) + 1 for i in range(1, len(rows)))
changes = []
for i in range(1, len(rows)):
    s0 = Decimal(rows[i - 1][1]); s1 = Decimal(rows[i][1])
    changes.append((rows[i][0], math.log(s1 / s0)))  # float log of exact ratio
def window(start=None, end=None):
    return [(m, c) for m, c in changes if (start is None or m >= start) and (end is None or m <= end)]
W1 = window(); W2 = window("2000-01"); W3 = window("2025-10")
out = {}
for name, W in (("W1", W1), ("W2", W2), ("W3", W3)):
    vals = [c for _, c in W]
    sd = statistics.stdev(vals)  # sample, n-1
    zeros = sum(1 for v in vals if v == 0.0)
    big = max(W, key=lambda t: abs(t[1]))
    pop = statistics.pstdev(vals)
    out[name] = sd
    print(name, "first", W[0][0], "last", W[-1][0], "n", len(vals), "zeros", zeros,
          "sd%", 100 * sd, "->", r2(100 * sd), "| popsd%", 100 * pop, "| largest", big[0], 100 * big[1], "->", r2(100 * big[1]))
print("ratio W2/W1", out["W2"] / out["W1"], "->", r2(out["W2"] / out["W1"]))
print("diff W1-W2 %/month", 100 * (out["W1"] - out["W2"]), "->", r2(100 * (out["W1"] - out["W2"])))
print("diff from rounded sds", r2(100 * out["W1"]) - r2(100 * out["W2"]))
print("sd W1 decimal 6dp", f"{out['W1']:.6f}", "sd W2", f"{out['W2']:.6f}")
print("largest abs overall", max(changes, key=lambda t: abs(t[1])))
print("zero-change months W1", [m for m, c in W1 if c == 0.0])
print("zero-change months W2", [m for m, c in W2 if c == 0.0])
print("W1 changes with |c|<1e-4 (sensitivity)", sum(1 for _, c in W1 if abs(c) < 1e-4))
