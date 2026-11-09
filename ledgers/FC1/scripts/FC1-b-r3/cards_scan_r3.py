"""Verifier (FC1-b r3): full-scan duplicate check over all FC1 cards, and numbers on L04/L05 cards present in their lessons."""
import json
import re
import sys
from itertools import combinations
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/FC/FC1/cards.json").read_text(encoding="utf-8"))
print("cards", len(cards), "unique ids", len({c["id"] for c in cards}), "unique fronts", len({c["front"].strip().lower() for c in cards}))


def toks(s):
    return set(re.findall(r"[a-z0-9]+", s.lower())) - {"the", "a", "an", "of", "is", "to", "and", "in", "it", "what", "does", "do", "for", "on", "by", "at"}


pairs = []
for a, b in combinations(cards, 2):
    ta, tb = toks(a["front"] + " " + a["back"]), toks(b["front"] + " " + b["back"])
    j = len(ta & tb) / max(1, len(ta | tb))
    if j >= 0.45:
        pairs.append((round(j, 2), a["id"], b["id"], a["front"][:70], b["front"][:70]))
print("near-duplicate pairs (jaccard >= 0.45):", len(pairs))
for p in sorted(pairs, reverse=True)[:20]:
    print(" ", p)

lessons = {"L04": (root / "course/modules/FC/FC1/L04.html").read_text(encoding="utf-8"),
           "L05": (root / "course/modules/FC/FC1/L05.html").read_text(encoding="utf-8")}
import html as h
for L, text in lessons.items():
    plain = h.unescape(re.sub(r"<[^>]+>", " ", text))
    missing = []
    for c in cards:
        if c["lesson"] != L:
            continue
        for num in re.findall(r"\b\d[\d,]*\b", c["front"] + " " + c["back"]):
            n = num.replace(",", "")
            if n not in plain:
                missing.append((c["id"], num))
    print(L, "card numbers not found in lesson text:", missing)
