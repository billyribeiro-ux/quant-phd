"""Round-1 near-duplicate scan over the L01-L03 card fronts (Jaccard on word sets). Read-only."""
import json
import re
import sys

cards = json.load(open(f"{sys.argv[1]}/course/modules/FC/FC1/cards.json", encoding="utf-8"))
sl = [c for c in cards if c.get("lesson") in ("L01", "L02", "L03")]
def toks(s):
    return set(re.findall(r"[a-z0-9]+", s.lower()))
pairs = []
for i in range(len(sl)):
    for j in range(i + 1, len(sl)):
        a, b = toks(sl[i]["front"] + " " + sl[i]["back"]), toks(sl[j]["front"] + " " + sl[j]["back"])
        jac = len(a & b) / max(1, len(a | b))
        pairs.append((jac, sl[i]["id"], sl[j]["id"]))
pairs.sort(reverse=True)
print("cards", len(sl))
for p in pairs[:8]:
    print(round(p[0], 3), p[1], p[2])
fr = []
for i in range(len(sl)):
    for j in range(i + 1, len(sl)):
        a, b = toks(sl[i]["front"]), toks(sl[j]["front"])
        fr.append((len(a & b) / max(1, len(a | b)), sl[i]["id"], sl[j]["id"]))
fr.sort(reverse=True)
print("front-only top pairs")
for p in fr[:6]:
    print(round(p[0], 3), p[1], p[2])
