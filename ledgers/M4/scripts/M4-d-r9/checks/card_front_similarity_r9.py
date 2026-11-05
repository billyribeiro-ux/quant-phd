"""Round-9 check: near-duplicate card fronts (difflib ratio >= 0.8) in course/modules/M/M4/cards.json.
Usage: python -I <this file> from the checkout root."""
import difflib
import itertools
import json
import pathlib

cards = json.loads(pathlib.Path("course/modules/M/M4/cards.json").read_text(encoding="utf-8"))
pairs = []
for a, b in itertools.combinations(cards, 2):
    r = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
    if r >= 0.8:
        pairs.append((round(r, 2), a["id"], b["id"], a["front"][:70], b["front"][:70]))
for p in sorted(pairs, reverse=True):
    print(p)
print("pairs >= 0.8 front similarity:", len(pairs))
