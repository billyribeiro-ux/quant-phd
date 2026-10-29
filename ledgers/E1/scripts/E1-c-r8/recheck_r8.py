"""Round-8 re-derivations for E1 slice c (L07-L09). Reads only the checkout; prints evidence."""
import json
import re
import sys
from fractions import Fraction

ROOT = sys.argv[1]
# 1. L08 Part C: every printed improvement has a non-integer amount (lab output lines 311-320 of L08.html)
html = open(f"{ROOT}/course/modules/E/E1/L08.html", encoding="utf-8").read()
block = html.split('<pre class="expected" data-tolerance="1e-6">', 1)[1].split("</pre>", 1)[0]
lines = [l for l in block.splitlines() if l.startswith("part C: from")]
bad = 0
for l in lines:
    amounts = re.findall(r"A = \(([^)]*)\)", l)[0].split(", ")
    fracs = [Fraction(a) for a in amounts]
    nonint = any(f.denominator != 1 for f in fracs)
    bad += (not nonint)
    print(f"{len(lines)} part C rows; amounts {amounts} non-integer={nonint}")
print("part C rows without a non-integer amount:", bad)
# 2. L08 part E / A numbers from the grid (re-derived independently)
X, Y = 8, 4
grid = [(x, y) for x in range(X + 1) for y in range(Y + 1)]
def u(x, y):
    return (Fraction(x) * Fraction(y), Fraction((X - x)) * Fraction((Y - y)))
def dominated(z, w):
    a, b = u(*z); c, d = u(*w)
    return a >= c and b >= d and (a > c or b > d)
eff = [w for w in grid if not any(dominated(z, w) for z in grid)]
print("grid-efficient count", len(eff), "interior", len([w for w in eff if 0 < w[0] < X and 0 < w[1] < Y]))
eq = [w for w in grid if 4 * u(*w)[0] * u(*w)[1] == (X * Y - sum(u(*w)))**2]
print("equality points", eq)
# 3. L07 Example 2.2 and Prop 2.3 numbers (exact)
a, b, c = 120, Fraction(1), 20
d = a - b * c
dwl = {"M": Fraction(d, 2) ** 2 / (2 * b), "C": (Fraction(2 * d, 3)) and (Fraction(d, 3)) ** 2 / (2 * b)}
print("DWL_M", dwl["M"], "DWL_C", dwl["C"], "ratio_M", dwl["M"] / (Fraction(d * d) / (2 * b)), "ratio_C", dwl["C"] / (Fraction(d * d) / (2 * b)))
print("5d^2/(72b)", Fraction(5 * d * d, 72) / b, "7/72 CS shift", Fraction(2, 9) - Fraction(1, 8), "PS shift", Fraction(1, 4) - Fraction(2, 9))
# 4. L09 quiz numbers
print("q_p", (1000 - 200) // 10, "q_s", (1000 - 200 - 120) // 10, "DWL", Fraction(120 ** 2, 20), "tax100 qty", (1000 - 200 - 100) / 10)
print("R2 quantity", (800 - 5 * 80) / 10)
# 5. Cards: L07-L09 count, uniqueness, grades
cards = json.load(open(f"{ROOT}/course/modules/E/E1/cards.json", encoding="utf-8"))
sub = [k for k in cards if k["lesson"] in ("L07", "L08", "L09")]
ids = [k["id"] for k in sub]
print("L07-L09 cards", len(sub), "unique", len(set(ids)) == len(ids), "ids", ids[0], ids[-1])
print("C-graded without basis", [k["id"] for k in sub if k.get("grade") == "C" and not k.get("basis")])
