"""Verifier round 4: slice cards (L05-L08) checked mechanically.

Usage: python3 -I cards_r4.py <checkout>
Prints: slice card count, duplicate ids and fronts across the whole unit file, and for each slice card
every number token in its back that does not occur in its lesson page's visible text (stripped of tags).
Hand-checked semantics are recorded in the fragment, not here.
"""
import html
import json
import re
import sys
from collections import Counter

root = sys.argv[1]
unit = f"{root}/course/modules/CS/CS2"
cards = json.load(open(f"{unit}/cards.json", encoding="utf-8"))
ids = Counter(c["id"] for c in cards)
fronts = Counter(c["front"] for c in cards)
print("unit cards:", len(cards), "duplicate ids:", [k for k, v in ids.items() if v > 1], "duplicate fronts:", [k for k, v in fronts.items() if v > 1])
slice_cards = [c for c in cards if c["lesson"] in ("L05", "L06", "L07", "L08")]
print("slice cards:", len(slice_cards), {l: sum(1 for c in slice_cards if c["lesson"] == l) for l in ("L05", "L06", "L07", "L08")})
text = {}
for l in ("L05", "L06", "L07", "L08"):
    src = open(f"{unit}/{l}.html", encoding="utf-8").read()
    src = re.sub(r"<script.*?</script>|<style.*?</style>", " ", src, flags=re.S)
    text[l] = html.unescape(re.sub(r"<[^>]+>", " ", src))
    text[l] = re.sub(r"\s+", " ", text[l])
missing = []
for c in slice_cards:
    for num in re.findall(r"\d[\d,]*\.?\d*", c["back"]):
        n = num.rstrip(".,")
        if n and n not in text[c["lesson"]] and n.replace(",", "") not in text[c["lesson"]]:
            missing.append((c["id"], c["lesson"], n))
print("card numbers not found verbatim in own lesson text:", missing)
for c in slice_cards:
    if c["grade"] not in ("T", "A", "B", "C", "D", "X"):
        print("bad grade", c["id"], c["grade"])
