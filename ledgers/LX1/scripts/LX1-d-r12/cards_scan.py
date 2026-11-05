"""Scan LX1 cards.json for duplicate ids, near-duplicate fronts, process words and banned strings.

Run with: python3 -I -W error ledgers/LX1/scripts/LX1-d-r12/cards_scan.py course/modules/LX/LX1/cards.json
"""

import difflib
import json
import re
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)))
print("missing ids c001-c082:", [f"LX1-c{i:03d}" for i in range(1, 83) if f"LX1-c{i:03d}" not in ids])
print("keys:", sorted({k for c in cards for k in c}))
print("lessons:", {l: sum(1 for c in cards if c["lesson"] == l) for l in ("L01", "L02", "L03", "L04")})
print("grades:", {g: sum(1 for c in cards if c.get("grade") == g) for g in ("T", "C", None)})
pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1 :]:
        r = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        rb = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
        if r > 0.5 or rb > 0.5:
            pairs.append((round(r, 2), round(rb, 2), a["id"], b["id"]))
print("near-duplicate pairs (front>0.5 or back>0.5):")
for p in sorted(pairs, reverse=True)[:25]:
    print("  ", p)
text = "\n".join(c["front"] + " " + c["back"] for c in cards)
banned = r"\b(round\s*\d*|batch|fix(ed|es)?|revis\w*|verifier|builder|previous round|we|our|us|I|TODO|TBD|lorem|omitted|beyond the scope|obviously|clearly|it is important|well known|studies show|experts agree)\b"
hits = sorted({m.group(0) for m in re.finditer(banned, text, flags=re.IGNORECASE)})
print("process/banned word hits:", hits)
for c in cards:
    for m in re.finditer(banned, c["front"] + " " + c["back"], flags=re.IGNORECASE):
        print("   hit", c["id"], m.group(0), "|", (c["front"] + " " + c["back"])[max(0, m.start()-50): m.end()+30])
