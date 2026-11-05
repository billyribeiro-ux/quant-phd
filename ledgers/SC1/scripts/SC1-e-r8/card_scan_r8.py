"""Structural and duplicate scans of cards.json.

Usage: python -I card_scan_r8.py <cards.json>
Checks: unique ids; id prefix; lesson in L01..L08; cite empty; grade in T/A/B/C/D/X or absent; basis present when
grade present; assumption words in a card that name A3/A4/A1/A2/A5 also name them in basis; near-duplicate pairs.
"""
import difflib
import json
import re
import sys
from collections import Counter

cards = json.load(open(sys.argv[1], encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "distinct ids:", len(set(ids)))
print("id prefix ok:", all(i.startswith("SC1-c") for i in ids))
print("lessons:", sorted(Counter(c["lesson"] for c in cards).items()))
print("cite non-empty:", [c["id"] for c in cards if c["cite"]])
print("bad grade:", [c["id"] for c in cards if "grade" in c and c["grade"] not in "TABCDX"])
print("grade without basis:", [c["id"] for c in cards if "grade" in c and not c.get("basis")])
print("keys:", Counter(tuple(sorted(c)) for c in cards))
asm = re.compile(r"\bA([1-5])\b|Assumption[s]? A?([1-5])|Assum")
miss = []
for c in cards:
    body = c["front"] + " " + c["back"]
    if re.search(r"\bA3\b|Assumptions? A3", body):
        if not re.search(r"A3", c.get("basis", "")):
            miss.append((c["id"], "A3 in text, not in basis"))
    if re.search(r"\bA4\b|A4\(", body) and not re.search(r"A4", c.get("basis", "")):
        miss.append((c["id"], "A4 in text, not in basis"))
print("assumption naming gaps:", miss)
dups = []
for i in range(len(cards)):
    a = cards[i]
    fa = a["front"] + " || " + a["back"]
    for j in range(i + 1, len(cards)):
        b = cards[j]
        if a["front"] == b["front"] or a["back"] == b["back"]:
            dups.append(("identical field", a["id"], b["id"]))
            continue
        fb = b["front"] + " || " + b["back"]
        r = difflib.SequenceMatcher(None, fa, fb, autojunk=False).quick_ratio()
        if r >= 0.6:
            ratio = difflib.SequenceMatcher(None, fa, fb, autojunk=False).ratio()
            if ratio >= 0.6:
                dups.append((round(ratio, 3), a["id"], b["id"]))
print("pairs with ratio >= 0.6:", dups)
