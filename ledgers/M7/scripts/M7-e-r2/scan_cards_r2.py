"""Slice-e scans of cards.json (round 2): banned/process strings, SIMULATED labelling of lab-result cards,
grade honesty (T cards must not carry lab-printed values), and the card-count/id checks.

Usage: python3 -I scan_cards_r2.py <cards.json>
"""
import json
import re
import sys
from collections import Counter

cards = json.load(open(sys.argv[1], encoding="utf-8"))
print("cards:", len(cards), "unique ids:", len({c["id"] for c in cards}))
print("grades:", dict(Counter(c["grade"] for c in cards)))
ban = re.compile(r"TODO|TBD|lorem|for brevity|beyond the scope|left as an exercise|obviously|clearly|it is important|well known|experts agree|studies show|you can add|it can be shown|\bwe\b|\bour\b|let us", re.I)
hits = [(c["id"], m.group(0)) for c in cards for f in ("front", "back") for m in [ban.search(c[f])] if m]
print("banned/process hits:", hits)
ell = [c["id"] for c in cards for f in ("front", "back") if re.search(r"\.\.\.|…", c[f])]
print("ellipsis uses (math ranges such as a_t, ..., a_{H-1}; checked by hand, not omitted content):", sorted(set(ell)))
lab_c = [c for c in cards if "Lab" in c["back"] + " " + c["front"] + " " + c.get("basis", "")]
bad_sim = [c["id"] for c in lab_c if c["grade"] == "C" and "SIMULATED" not in c.get("basis", "") + c["back"]]
print("C-graded lab-result cards without a SIMULATED label:", bad_sim)
t_lab_numbers = []
printed = ["2573", "3125", "552", "184", "1089", "27951", "1331", "378", "13.948890", "0.590490", "0.558861",
           "0.572254", "0.820002", "1.392257", "177/110", "177/55", "13/19", "551/722", "817/722", "0.763", "0.113798",
           "0.123809", "0.106241", "0.115780", "0.084794", "0.184631", "2.7400", "2.466", "2.2194", "1.99746"]
for c in cards:
    if c["grade"] == "T":
        t = c["front"] + " " + c["back"]
        h = [p for p in printed if p in t]
        if h:
            t_lab_numbers.append((c["id"], h))
print("T-graded cards carrying lab-printed values:", t_lab_numbers)
print("T-graded cards that name Lab:", [c["id"] for c in cards if c["grade"] == "T" and "Lab" in c["front"] + c["back"]])
