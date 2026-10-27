"""AC2 L05-L06 round-8 recomputation. Run: .venv/bin/python -I ledgers/AC2/scripts/L05-L06-r8/recompute.py (from the checkout)."""
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
AC2 = ROOT / "course" / "modules" / "AC" / "AC2"

# Card arithmetic (c075, c123, c122, c125, c082, c084, c085, c086, c124)
d, s = 0.00223495, 0.0113137
se = s / math.sqrt(120)
print("se_120", round(se, 7), "quotient_full_precision", round(d / se, 5), "-> 2.164 (c123)")
print("quotient_displayed_SD", round(0.0022350 / (0.01131 / math.sqrt(120)), 4), "-> 2.1647 (c123)")
z = 1.959964 + 0.841621
print("n_for_80pct_power", round((z * s / d) ** 2, 2), "-> about 201 (c075)")
q = -0.841621  # Phi^-1(0.2)
phi = math.exp(-q * q / 2) / math.sqrt(2 * math.pi)
print("quintile_gap_analytic", round(-2 * phi / 0.2, 4), "-> -2.800 (c122, Prop 2.3)")
print("c125 ratio", round(0.2781 * math.sqrt(1800 / 57600), 4), "vs printed 0.0489")
print("c082/c085 flags: strong TP 197 of 200; weak TP 0.355*200 =", 0.355 * 200, "; strong TP 0.985*200 =", 0.985 * 200)
print("c070 SE of rate from 200 draws", round(math.sqrt(0.05 * 0.95 / 200), 4), "-> about 0.015")

# Hours (index hub, data-hours)
index = (AC2 / "index.html").read_text(encoding="utf-8")
kick = [int(m) for m in re.findall(r'card-kicker">L\d\d · (\d+) h', index)]
print("hub lesson hours", kick, "sum", sum(kick), "data-hours-lessons=76 in index:", 'data-hours-lessons="76"' in index)
print("L05 data-hours", re.search(r'data-page="L05" data-hours="(\d+)"', (AC2 / "L05.html").read_text()).group(1))
print("L06 data-hours", re.search(r'data-page="L06" data-hours="(\d+)"', (AC2 / "L06.html").read_text()).group(1))

# Cards integrity
cards = json.loads((AC2 / "cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique", len(set(ids)) == len(ids), "sequential", ids == [f"AC2-c{i:03d}" for i in range(1, 141)])
fronts = [c["front"] for c in cards]
backs = [c["back"] for c in cards]
print("duplicate fronts", len(fronts) - len(set(fronts)), "duplicate backs", len(backs) - len(set(backs)))
print("L05 cards", [c["id"][-4:] for c in cards if c["lesson"] == "L05"])
print("L06 cards", [c["id"][-4:] for c in cards if c["lesson"] == "L06"])

# c072 wording against the lesson text (Sloan claim and no-finding statement)
l05 = (AC2 / "L05.html").read_text(encoding="utf-8")
print("L05 states no finding of Sloan:", "The lesson states no finding of that paper" in l05)
print("L05 lab docstring: does not reproduce Sloan:", "does not reproduce Sloan (1996)" in l05)
print("L05 section 3 question wording:", "The question Sloan (1996) asks" in l05)
print("hub L05 title:", re.search(r'<span class="card-title">([^<]*)</span>', index.split('href="L05.html"')[1]).group(1))
