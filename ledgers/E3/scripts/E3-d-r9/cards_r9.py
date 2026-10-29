# Verifier r8: cards.json structure, duplicate fronts, and whether each card's numbers appear in its lesson text.
import json, re, sys, html
from collections import Counter
base = "course/modules/E/E3/"
cards = json.load(open(base + "cards.json"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)))
print("dup ids", [k for k, v in Counter(ids).items() if v > 1])
fr = Counter(c["front"].strip().lower() for c in cards)
print("dup fronts", [k for k, v in fr.items() if v > 1])
txt = {}
for L in sorted({c["lesson"] for c in cards}):
    raw = open(base + L + ".html", encoding="utf-8").read()
    raw = re.sub(r"<[^>]+>", " ", raw)
    txt[L] = re.sub(r"\s+", " ", html.unescape(raw))
miss = []
for c in cards:
    for field in ("front", "back"):
        for n in re.findall(r"\d+(?:\.\d+)?", c[field]):
            if len(n) < 2:
                continue
            if n not in txt[c["lesson"]]:
                miss.append((c["id"], field, n))
print("card numbers (>=2 digits) absent from own lesson:", miss)
for rid in ("E3-c092", "E3-c114", "E3-c156"):
    print("removed", rid, "present:", rid in ids)
