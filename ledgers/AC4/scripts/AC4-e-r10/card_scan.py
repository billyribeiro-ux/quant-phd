"""Duplicate and structure scan of AC4 cards.json (argv[1]); prints near-duplicate fronts and checks grade/basis fields."""
import difflib
import json
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
keys = {"id", "lesson", "front", "back", "grade", "basis"}
bad = [c["id"] for c in cards if set(c) - keys or not {"id", "lesson", "front", "back"} <= set(c)]
print("structure problems:", bad)
print("grade without basis:", [c["id"] for c in cards if c.get("grade") and not c.get("basis")])
print("basis without grade:", [c["id"] for c in cards if c.get("basis") and not c.get("grade")])
print("grade values:", sorted({str(c.get("grade")) for c in cards}))
print("ids sequential:", [c["id"] for c in cards] == [f"AC4-c{i:03d}" for i in range(1, len(cards) + 1)])
print("duplicate fronts:", [f for f in {c["front"] for c in cards} if sum(c["front"] == f for c in cards) > 1])
print("duplicate backs:", [b[:40] for b in {c["back"] for c in cards} if sum(c["back"] == b for c in cards) > 1])
pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1 :]:
        r = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
        if r >= 0.75:
            pairs.append((round(r, 2), a["id"], b["id"], a["front"], b["front"]))
for p in sorted(pairs, reverse=True):
    print("NEAR", *p)
print("lesson counts:", {l: sum(c["lesson"] == l for c in cards) for l in sorted({c["lesson"] for c in cards})})
print("T-grade cards:", sum(c.get("grade") == "T" for c in cards), "C:", sum(c.get("grade") == "C" for c in cards), "ungraded:", sum("grade" not in c for c in cards))
