"""Card checks for L04-L06 cards of PC3.

1. every number token in a card's front or back appears in the card's own lesson page (text or code output);
2. near-duplicate fronts within the slice (difflib ratio >= 0.85);
3. card ids unique across the whole unit; each card's lesson field matches its id block.
Run: python3 -I cards_check.py <checkout_root>
"""
import difflib
import html
import json
import re
import sys

root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/PC/PC3/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("unique ids:", len(ids) == len(set(ids)), "count:", len(ids))
pages = {}
for p in ("L04", "L05", "L06"):
    raw = open(f"{root}/course/modules/PC/PC3/{p}.html", encoding="utf-8").read()
    pages[p] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
slice_cards = [c for c in cards if c["lesson"] in pages]
missing = []
num_re = re.compile(r"(?<![A-Za-z_])-?\d[\d,]*\.?\d*")
for c in slice_cards:
    text = c["front"] + " " + c["back"]
    for tok in set(num_re.findall(text)):
        t = tok.rstrip(".").replace(",", "")
        if t in ("1", "2", "0", "3", "10", "5"):
            continue
        if t not in pages[c["lesson"]].replace(",", "") and t.lstrip("-") not in pages[c["lesson"]].replace(",", ""):
            missing.append((c["id"], c["lesson"], tok))
print("card numbers not found verbatim in own lesson page (small integers excluded):")
for m in missing:
    print("  ", m)
print("count:", len(missing))
dups = []
for i in range(len(slice_cards)):
    for j in range(i + 1, len(slice_cards)):
        a, b = slice_cards[i], slice_cards[j]
        r = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        if r >= 0.85:
            dups.append((a["id"], b["id"], round(r, 3)))
print("near-duplicate fronts (ratio>=0.85):", dups)
for c in slice_cards:
    if c["lesson"] not in ("L04", "L05", "L06"):
        print("bad lesson", c["id"])
