"""Round-8 recomputation of the changed sentences in AC4 L05 and L06 and the card duplicate scan. Run with -I."""

import json
import re
import sys
from fractions import Fraction as F
from pathlib import Path

co = Path(sys.argv[1])
# L06 interpretation sentence (line 259)
print("share actual A", float(F(650, 1150) * 100), "round1", round(float(F(650, 1150) * 100), 1))
print("share budget A", F(600, 1000) * 100, "gap exact", F(60) - F(650, 1150) * 100, float(F(60) - F(650, 1150) * 100))
print("mix", 1500 * (650 - 1150 * F(600, 1000)) + 1900 * (500 - 1150 * F(400, 1000)))
print("volume 150*1660", 150 * 1660, "budget kg std", 2 * 650 + 3 * 500, "actual kg", 1350 + 1600)
# L06 P3 one-product identity, numeric: p_b=2500 p_a=2400 s=2 pi=500 q_b=600 q_a=650 kg_a=1350
pb, pa, s, pi, qb, qa, kg = 2500, 2400, 2, 500, 600, 650, 1350
CM = pb - s * pi
SP = (pa - pb) * qa
V = (qa - qb) * CM
M = CM * (qa - qa * 1)
E = -pi * (kg - s * qa)
T = (pa * qa - pi * kg) - CM * qb
print("P3 one product", SP, V, M, E, "sum SP+V+E", SP + V + E, "T", T, "identity", SP + V + E == T)
# L05 bullet-1 claim is conditional; no number. Card scan:
d = json.loads((co / "course/modules/AC/AC4/cards.json").read_text(encoding="utf-8"))
cards = d if isinstance(d, list) else d.get("cards", d)
ids = [c["id"] for c in cards]
fronts = [re.sub(r"\W+", " ", c["front"].lower()).strip() for c in cards]
print("cards", len(cards), "dup ids", len(ids) - len(set(ids)), "dup fronts", len(fronts) - len(set(fronts)))
l5l6 = [c for c in cards if c.get("lesson") in ("L05", "L06")]
print("L05/L06 cards", len(l5l6), sorted(c["id"] for c in l5l6)[:3], "...")
