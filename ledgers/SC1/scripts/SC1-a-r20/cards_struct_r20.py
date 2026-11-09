"""SC1-a round 20: structural checks on the L01-L03 cards of cards.json (duplicates, grade/basis pairing, grade values,
numbered references in each card that must occur in the lesson the card names, and card ids present in the file)."""

import collections
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
SC1 = os.path.join(ROOT, "course", "modules", "SC", "SC1")
cards = json.load(open(os.path.join(SC1, "cards.json"), encoding="utf-8"))
mine = [c for c in cards if c["lesson"] in ("L01", "L02", "L03")]
print("L01-L03 cards:", len(mine), "per lesson:", dict(collections.Counter(c["lesson"] for c in mine)))
print("all cards:", len(cards), "distinct ids:", len({c["id"] for c in cards}))
fronts = collections.Counter(c["front"].strip() for c in cards)
print("exact duplicate fronts (all cards):", [f for f, n in fronts.items() if n > 1])
backs = collections.Counter(c["back"].strip() for c in cards)
print("exact duplicate backs (all cards):", [b[:60] for b, n in backs.items() if n > 1])
print("grade values:", collections.Counter(c.get("grade") for c in mine))
bad = [c["id"] for c in mine if (c.get("grade") is None) != (c.get("basis") is None)]
print("grade/basis not paired:", bad)
print("cite non-empty (L01-L03):", [c["id"] for c in mine if c.get("cite")])
pages = {n: open(os.path.join(SC1, f"{n}.html"), encoding="utf-8").read() for n in ("L01", "L02", "L03")}
pages["index"] = open(os.path.join(SC1, "index.html"), encoding="utf-8").read()
pat = re.compile(r"\b(Lemma|Proposition|Theorem|Remark|Example|Corollary|Definition|Problem|Assumption|Lab) (\d+(?:\.\d+)?|[A-Z]\d)(\([a-z]\))?")
missing = []
for c in mine:
    text = c["front"] + " " + c["back"] + " " + (c.get("basis") or "")
    for m in pat.finditer(text):
        kind, num = m.group(1), m.group(2)
        token = f"{kind} {num}"
        home = pages[c["lesson"]]
        if token not in home and not any(token in p for p in pages.values()):
            missing.append((c["id"], token))
        elif token not in home:
            missing.append((c["id"], token + " (not in its own lesson " + c["lesson"] + ")"))
print("numbered references not found in the card's own lesson:", missing)
