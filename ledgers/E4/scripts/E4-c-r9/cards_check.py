"""Round 9, slice E4-c: card numbers vs own lesson text, card duplicate scan, card inventory for L07-L09."""
import json
import html
import re
from collections import Counter

BASE = "/Users/billyribeiro/.fanout/wt/verifyE9-E4-c/course/modules/E/E4/"
cards = json.load(open(BASE + "cards.json", encoding="utf-8"))
pages = {}
for lesson in ("L07", "L08", "L09"):
    s = open(BASE + lesson + ".html", encoding="utf-8").read()
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    pages[lesson] = s
sel = [c for c in cards if c["lesson"] in pages]
num_re = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?(?:e-?\d+)?(?![\d])")
missing = []
for c in sel:
    for n in set(num_re.findall(c["front"] + " " + c["back"])):
        if n not in pages[c["lesson"]] and n not in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"}:
            missing.append((c["id"], n))
print("ids", len(cards), "duplicate ids", len(cards) - len({c["id"] for c in cards}))
print("L07-L09 cards", len(sel), dict(Counter(c["lesson"] for c in sel)))
print("card numbers not found in own lesson text:", missing)
print("cards with grade None (definitions/assumptions):", sum(1 for c in sel if c.get("grade") is None))
toks = lambda s: set(re.findall(r"[a-zA-Z]+|\d+", s.lower()))
pairs = []
for i, a in enumerate(cards):
    ta = toks(a["front"] + " " + a["back"])
    for b in cards[i + 1:]:
        tb = toks(b["front"] + " " + b["back"])
        j = len(ta & tb) / max(1, len(ta | tb))
        if j > 0.55:
            pairs.append((round(j, 2), a["id"], b["id"]))
print("near-duplicate pairs (Jaccard > 0.55) over all cards:", len(pairs))
for p in sorted(pairs, reverse=True):
    print("  ", p)
