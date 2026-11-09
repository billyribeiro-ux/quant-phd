"""Duplicate and id scan over all M7 cards, and a check that each L07/L08 card's bare numbers appear in its lesson page.

Run: python3 -I ledgers/M7/scripts/M7-c-r1/cards_scan.py <checkout>
"""
import html
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M7/cards.json").read_text(encoding="utf-8"))
ids = Counter(c["id"] for c in cards)
print("total cards", len(cards), "duplicate ids", [i for i, n in ids.items() if n > 1])
norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()
fronts = defaultdict(list)
backs = defaultdict(list)
for c in cards:
    fronts[norm(c["front"])].append(c["id"])
    backs[norm(c["back"])].append(c["id"])
print("duplicate fronts", {k: v for k, v in fronts.items() if len(v) > 1})
print("duplicate backs", {k: v for k, v in backs.items() if len(v) > 1})
# shared 8-word shingles between cards (near-duplicate probe)
def shingles(s, n=8):
    w = norm(s).split()
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}
pairs = []
sel = [c for c in cards if c["lesson"] in ("L07", "L08")]
for i, a in enumerate(sel):
    for b in sel[i + 1:]:
        common = shingles(a["front"] + " " + a["back"]) & shingles(b["front"] + " " + b["back"])
        if len(common) >= 3:
            pairs.append((a["id"], b["id"], sorted(common)[:3]))
print("L07/L08 card pairs sharing >=3 eight-word runs:", pairs)
# number check: every number token in card text must occur in its lesson page text
for lid in ("L07", "L08"):
    page = html.unescape((root / f"course/modules/M/M7/{lid}.html").read_text(encoding="utf-8"))
    ptxt = re.sub(r"<[^>]+>", " ", page)
    for c in sel:
        if c["lesson"] != lid:
            continue
        txt = c["front"] + " " + c["back"]
        nums = set(re.findall(r"(?<![\w.])\d+(?:\.\d+)?", txt))
        missing = [n for n in nums if not re.search(r"(?<![\w.])" + re.escape(n) + r"(?![\w])", ptxt)]
        if missing:
            print(c["id"], "numbers not on lesson page:", missing)
print("number-presence scan done")
