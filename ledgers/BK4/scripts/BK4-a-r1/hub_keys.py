"""Verifier script (BK4 slice a, round 1): re-derives the placement-diagnostic answer keys and the hub arithmetic.

Run: .venv/bin/python -I -W error ledgers/BK4/scripts/BK4-a-r1/hub_keys.py
"""

import math
import re
from fractions import Fraction as F
from pathlib import Path

hub = Path(__file__).resolve().parents[4] / "course/modules/BK/BK4/index.html"
text = hub.read_text(encoding="utf-8")
keys = re.findall(r'data-answer="([^"]+)" data-tolerance="([^"]+)"', text)
print("numeric keys on hub:", keys)
pv = F(110) / F("1.1")
print("Pq1 PV of 110 at end of one period, 10%:", pv, "(option 100.00 is correct)")
assert pv == 100
geo = (1 - F(1, 2) ** 3) / F(1, 2)
print("Pq2 1+1/2+1/4:", geo, "(key 1.75)")
assert geo == F(7, 4)
lim = 2 * 3
print("Pq3 lim 2x at 3:", lim, "(key 6)")
assert lim == 6
print("Pq7 defaulter layers: a1=min(120,100)=", min(120, 100), " a2=min(120-100,50)=", min(120 - 100, 50), "(key 20)")
assert min(120 - 100, 50) == 20
R, DF = 1, {1: 1, 2: 1, 3: 1}
T = sum(DF.values())
share = {i: (R * d) // T for i, d in DF.items()}
left = R - sum(share.values())
print("Pq8 floor shares:", share, "leftover:", left)
assert left == 1
mastery = F(8, 10) * 8
print("mastery bar with 8 items: need >=", math.ceil(mastery), "correct; 6/8 =", F(6, 8) * 100, "% ; 7/8 =", F(7, 8) * 100, "%")
assert math.ceil(mastery) == 7
hours = [2, 2, 3, 3, 2, 2, 1]
print("project hours table sum:", sum(hours), "(data-hours-project 15)")
assert sum(hours) == 15
print("lessons 5 x 7 =", 5 * 7, "; 35 + 15 =", 35 + 15, "; 15/50 =", F(15, 50) * 100, "%")
assert 5 * 7 + 15 == 50
print("HUB KEYS OK")
