"""Structure and duplicate scan for BK4 cards.json, and label cross-references against the card's lesson text.

Usage: python -I card_structure.py <cards.json> <lesson_text_dir>
"""
import difflib
import json
import re
import sys
from collections import Counter

cards = json.load(open(sys.argv[1], encoding="utf-8"))
textdir = sys.argv[2]
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)))
print("id sequence gaps:", sorted(set(f"c{n:03d}" for n in range(1, int(max(i[-3:] for i in ids)) + 1)) - {i[-4:] for i in ids}))
print("per lesson:", dict(sorted(Counter(c["lesson"] for c in cards).items())))
print("grades:", dict(Counter(c.get("grade") for c in cards)))
print("keys:", sorted({k for c in cards for k in c}))
print("fronts unique:", len({c["front"] for c in cards}), "backs unique:", len({c["back"] for c in cards}))
pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        rf = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        rb = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
        if rf > 0.6 or rb > 0.6:
            pairs.append((round(rf, 2), round(rb, 2), a["id"], b["id"]))
print("near-duplicate pairs (front>0.6 or back>0.6):", len(pairs))
for p in sorted(pairs, reverse=True)[:20]:
    print("  ", p)
lab = re.compile(r"\b(Definition|Proposition|Example|Remark|Problem|Corollary|Assumption|Section|Lab)\s+((?:\d+(?:\.\d+)?)|[A-Z]\d+|\d)")
bad = 0
texts = {}
for c in cards:
    lid = c["lesson"]
    if lid not in texts:
        texts[lid] = open(f"{textdir}/{lid}.txt", encoding="utf-8").read()
    for m in lab.finditer(c["front"] + " " + c["back"]):
        kind, ident = m.group(1), m.group(2)
        if kind == "Lab" and ident == "1":
            continue
        pat = re.escape(f"{kind} {ident}")
        if not re.search(pat, texts[lid]) and not any(re.search(pat, texts[o]) for o in texts):
            bad += 1
            print("  label not found anywhere:", c["id"], f"{kind} {ident}")
        elif not re.search(pat, texts[lid]):
            print("  label found only in another lesson:", c["id"], lid, f"{kind} {ident}")
print("label cross-reference misses:", bad)
