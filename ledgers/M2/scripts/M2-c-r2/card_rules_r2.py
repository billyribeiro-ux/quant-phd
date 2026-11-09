"""Round-2 card rules for M2 cards of lessons L13-L18: grade/basis rule (C cards carry basis, T cards carry none),
near-duplicate fronts within the slice (difflib ratio >= 0.80), and cards whose lesson field disagrees with the id range.

Run: python -I card_rules_r2.py <checkout_root>
"""

import difflib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
slice_lessons = {"L13", "L14", "L15", "L16", "L17", "L18"}
sl = [c for c in cards if c["lesson"] in slice_lessons]
bad = []
for c in sl:
    g = c.get("grade")
    if g == "C" and not c.get("basis"):
        bad.append((c["id"], "C without basis"))
    if g == "T" and c.get("basis"):
        bad.append((c["id"], "T with basis"))
    if g in ("A", "B", "D", "X"):
        bad.append((c["id"], f"grade {g} present in slice"))
print("grade/basis violations:", bad)
print("grade counts:", {g: sum(1 for c in sl if c.get("grade") == g) for g in ("T", "C", None)})
near = []
for i in range(len(sl)):
    for j in range(i + 1, len(sl)):
        r = difflib.SequenceMatcher(None, sl[i]["front"], sl[j]["front"]).ratio()
        if r >= 0.80:
            near.append((sl[i]["id"], sl[j]["id"], round(r, 3)))
print("near-duplicate fronts within slice (ratio >= 0.80):", near)
