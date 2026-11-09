"""Round-7 card scan for CS2 L09-L11 cards (verifier-written, reads only the checkout files)."""

import difflib
import json
import re
import sys
from collections import Counter

ROOT = sys.argv[1]
cards = json.load(open(f"{ROOT}/course/modules/CS/CS2/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards total", len(cards), "duplicate ids", len(ids) - len(set(ids)))
print("grades (whole deck)", dict(Counter(c["grade"] for c in cards)))
sub = [c for c in cards if c["lesson"] in ("L09", "L10", "L11")]
print("L09-L11 cards", len(sub), dict(Counter(c["lesson"] for c in sub)), dict(Counter(c["grade"] for c in sub)))
for c in sub:
    if c["grade"] == "C" and not c.get("basis"):
        print("C card without basis", c["id"])
    if c["grade"] != "C" and "basis" in c:
        print("non-C card with basis", c["id"])
    if set(c) - {"id", "lesson", "front", "back", "grade", "basis"}:
        print("extra fields", c["id"], set(c))
    if not c["id"].startswith("CS2-c"):
        print("bad id", c["id"])

# numbers on the changed and new cards must appear in their lesson text
html = {L: open(f"{ROOT}/course/modules/CS/CS2/{L}.html", encoding="utf-8").read() for L in ("L09", "L10", "L11")}
changed = ["CS2-c125", "CS2-c139", "CS2-c194", "CS2-c200", "CS2-c244", "CS2-c245"]
num_re = re.compile(r"\d[\d.]*(?:e-?\d+)?")
for c in cards:
    if c["id"] in changed:
        toks = sorted(set(num_re.findall(c["front"] + " " + c["back"])))
        present = {t: (t in html[c["lesson"]]) for t in toks}
        print(c["id"], c["lesson"], c["grade"], "numbers:", present)

# near-duplicate scan across the whole deck (front+back), ratio >= 0.55
texts = [(c["id"], c["front"] + " " + c["back"]) for c in cards]
hits = []
for i in range(len(texts)):
    for j in range(i + 1, len(texts)):
        r = difflib.SequenceMatcher(None, texts[i][1], texts[j][1]).quick_ratio()
        if r >= 0.55:
            r = difflib.SequenceMatcher(None, texts[i][1], texts[j][1]).ratio()
            if r >= 0.55:
                hits.append((round(r, 3), texts[i][0], texts[j][0]))
hits.sort(reverse=True)
print("near-duplicate pairs (ratio >= 0.55):", len(hits))
for h in hits[:40]:
    print(h)
