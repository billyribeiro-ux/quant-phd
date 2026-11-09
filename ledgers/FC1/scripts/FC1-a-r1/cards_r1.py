"""Round-1 closing delta card scan for FC1-a (L01-L03 cards). Read-only."""
import html
import json
import re
import sys
from collections import Counter

ROOT = sys.argv[1]
base = f"{ROOT}/course/modules/FC/FC1"
cards = json.load(open(f"{base}/cards.json", encoding="utf-8"))
print("total cards", len(cards))
ids = [c["id"] for c in cards]
dups = [k for k, v in Counter(ids).items() if v > 1]
print("duplicate ids:", dups)
fronts = Counter(c["front"] for c in cards)
backs = Counter(c["back"] for c in cards)
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
print("duplicate backs:", [k for k, v in backs.items() if v > 1])
slice_cards = [c for c in cards if c.get("lesson") in ("L01", "L02", "L03")]
print("L01-L03 cards:", len(slice_cards))
print("L01-L03 ids:", sorted(c["id"] for c in slice_cards)[0], "..", sorted(c["id"] for c in slice_cards)[-1])
print("missing ids in 001-172 (all cards):", sorted(set(f"FC1-c{i:03d}" for i in range(1, 173)) - set(ids)))
# grade / basis convention
bad = []
for c in cards:
    g = c.get("grade")
    if (g == "C") != ("basis" in c):
        bad.append((c["id"], g, "basis" in c))
print("grade/basis mismatches:", bad)
# lesson text
lesson_text = {}
for L in ("L01", "L02", "L03"):
    raw = open(f"{base}/{L}.html", encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    lesson_text[L] = re.sub(r"\s+", " ", txt)
num_re = re.compile(r"\d+(?:\.\d+)?")
for c in slice_cards:
    L = c["lesson"]
    missing = []
    for field in ("front", "back"):
        for n in set(num_re.findall(c[field])):
            if n not in lesson_text[L]:
                missing.append((field, n))
    if missing:
        print("NUMBER NOT IN LESSON", c["id"], L, missing)
# lab mentions in T cards
for c in cards:
    if c["lesson"] in ("L01", "L02", "L03") and c.get("grade") == "T" and re.search(r"Lab|SIMULATED|prints", c["back"] + c["front"]):
        print("T card with lab mention:", c["id"], "|", c["back"][:200])
for cid in ("FC1-c016", "FC1-c050", "FC1-c103", "FC1-c105", "FC1-c153"):
    c = next(x for x in cards if x["id"] == cid)
    print(json.dumps(c, ensure_ascii=False))
