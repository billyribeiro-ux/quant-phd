"""Hub (index.html) numbers and placement tolerances, recomputed with math and Fraction.

Run: python -I -W error ledgers/E1/scripts/E1-a-r2/hub_numbers.py
"""

import math
from fractions import Fraction as Fr

ok = True


def show(name, got, want, tol=None):
    global ok
    good = abs(got - want) <= tol if tol is not None else got == want
    ok = ok and good
    print(("PASS " if good else "FAIL ") + f"{name}: {got} vs {want}" + (f" tol {tol}" if tol is not None else ""))


show("7/9 as percent", float(round(100 * Fr(7, 9), 1)), 77.8, 1e-9)
show("8/9 as percent", float(round(100 * Fr(8, 9), 1)), 88.9, 1e-9)
show("8 of 9 items clears 80 percent", Fr(8, 9) >= Fr(8, 10), True)
show("7 of 9 does not clear 80 percent", Fr(7, 9) >= Fr(8, 10), False)
import re
with open("course/modules/E/E1/index.html", encoding="utf-8") as fh:
    html = fh.read()
sec = html[html.index('id="placement"'): html.index('id="lessons"')]
show("placement items on hub", len(re.findall(r'<li class="item"', sec)), 9)
show("placement skill items (data-skill)", len(re.findall(r'data-skill', sec)), 2)
show("placement mastery bar 0.8", 'data-mastery="0.8"' in sec, True)
show("e^0.5 vs placement 1.6487 tol 0.00005", math.exp(0.5), 1.6487, 0.00005)
show("100 e^-0.1 vs placement 90.48 tol 0.005", 100 * math.exp(-0.1), 90.48, 0.005)
show("implicit dy/dx at (3,1) for y^2+x=4", -1 / (2 * 1), -0.5, 1e-12)
show("partial df/dx of x^2 y at (1,3) = 2xy", 2 * 1 * 3, 6)
show("hours: 9 x 10 = 90 lessons", 9 * 10, 90)
show("hours: 90 + 30 = 120", 90 + 30, 120)
show("project share 30/120 = 25 percent", round(100 * Fr(30, 120)), 25)
show("lessons width 75 percent", round(100 * Fr(90, 120)), 75)
print("ALL PASS" if ok else "SOME FAILED")
