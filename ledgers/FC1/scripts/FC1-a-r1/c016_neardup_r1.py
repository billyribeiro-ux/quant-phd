# Near-duplicate scan for the changed card FC1-c016 against the other L01-L03 cards (word Jaccard on front+back).
import json
import pathlib
import re
import sys

cards = json.loads((pathlib.Path(sys.argv[1]) / "course/modules/FC/FC1/cards.json").read_text(encoding="utf-8"))
def words(c):
    return set(re.findall(r"\w+", (c["front"] + " " + c["back"]).lower()))
target = next(c for c in cards if c["id"] == "FC1-c016")
scored = []
for c in cards:
    if c["id"] == target["id"]:
        continue
    a, b = words(target), words(c)
    scored.append((len(a & b) / len(a | b), c["id"], c["lesson"]))
scored.sort(reverse=True)
for s in scored[:5]:
    print(f"{s[0]:.3f} {s[1]} {s[2]}")
