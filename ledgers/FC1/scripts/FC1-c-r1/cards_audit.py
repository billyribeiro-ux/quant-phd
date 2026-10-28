"""Verifier audit of course/modules/FC/FC1/cards.json: counts, grades, notation, duplicates (read-only)."""
import difflib
import json
import re
import sys

path = sys.argv[1]
cards = json.load(open(path, encoding="utf-8"))
print("cards", len(cards))
print("per lesson", {l: sum(1 for c in cards if c["lesson"] == l) for l in ["L01", "L02", "L03", "L04", "L05"]})
print("ids sequential", [c["id"] for c in cards] == [f"FC1-c{i:03d}" for i in range(1, len(cards) + 1)])
print("no grade field:", [c["id"] for c in cards if "grade" not in c])
print("grade T with basis only (no cite):", [(c["id"], c.get("basis")) for c in cards if c.get("grade") == "T" and c.get("basis")])
print("plain Q used as a symbol:", [c["id"] for c in cards if re.search(r"(?<![A-Za-z\\])Q(?![a-z])", c["front"] + " " + c["back"])])
fr = [c["front"] for c in cards]
bk = [c["back"] for c in cards]
print("exact duplicate fronts/backs:", len(fr) - len(set(fr)), len(bk) - len(set(bk)))
near = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a = difflib.SequenceMatcher(None, bk[i].lower(), bk[j].lower()).ratio()
        if a > 0.6:
            near.append((round(a, 2), cards[i]["id"], cards[j]["id"]))
print("back similarity > 0.6:", sorted(near, reverse=True))
