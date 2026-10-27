"""Round-2 duplicate and structure scan of AC2 cards.json (all cards), with the L03/L04 subset."""
import difflib
import json
import re
import sys
from collections import Counter
from pathlib import Path

cards = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)), "ids c001..c130 present:", sorted(ids) == [f"AC2-c{i:03d}" for i in range(1, 131)])
norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        fr = difflib.SequenceMatcher(None, norm(a["front"]), norm(b["front"])).ratio()
        bk = difflib.SequenceMatcher(None, norm(a["back"]), norm(b["back"])).ratio()
        if fr > 0.75 or bk > 0.75 or (fr > 0.6 and bk > 0.6):
            pairs.append((round(fr, 2), round(bk, 2), a["id"], b["id"]))
print("near-duplicate pairs (front>0.75 or back>0.75 or both>0.6):", len(pairs))
for p in pairs:
    print(" ", p)
print("front duplicates:", [k for k, v in Counter(norm(c["front"]) for c in cards).items() if v > 1])
print("back duplicates:", [k[:60] for k, v in Counter(norm(c["back"]) for c in cards).items() if v > 1])
keys = Counter(tuple(sorted(c.keys())) for c in cards)
print("key sets:", dict(keys))
print("grades:", Counter(c.get("grade") for c in cards))
bad = [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis") and not c.get("cite")]
print("C-graded cards without basis or cite:", bad)
sub = [c for c in cards if c["lesson"] in ("L03", "L04")]
print("L03 cards:", [c["id"] for c in sub if c["lesson"] == "L03"])
print("L04 cards:", [c["id"] for c in sub if c["lesson"] == "L04"])
