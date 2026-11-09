"""Round-12 verifier (M3 slice d): full scan of course/modules/M/M3/cards.json for duplicate ids, duplicate or
near-duplicate fronts and backs, field sets, grade/basis rules (BUILDER_RULES 7), and cards-to-lesson mapping.
Run from the checkout root."""

import difflib
import itertools
import json
import re
from collections import Counter

cards = json.load(open("course/modules/M/M3/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "distinct ids:", len(set(ids)))
print("duplicate ids:", [k for k, v in Counter(ids).items() if v > 1])
print("ids sorted ascending:", ids == sorted(ids, key=lambda s: int(s.rsplit("c", 1)[1])))
print("field sets:", Counter(tuple(sorted(c)) for c in cards))
bad_grade = [c["id"] for c in cards if c.get("grade") not in (None, "T", "C")]
print("grades outside {T, C, absent}:", bad_grade)
no_basis_C = [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis")]
basis_not_C = [c["id"] for c in cards if c.get("grade") != "C" and "basis" in c]
print("grade C without basis:", no_basis_C, "| basis without grade C:", basis_not_C)
def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
fronts = Counter(norm(c["front"]) for c in cards)
print("duplicate normalised fronts:", [k for k, v in fronts.items() if v > 1])
backs = Counter(norm(c["back"]) for c in cards)
print("duplicate normalised backs:", [k for k, v in backs.items() if v > 1])
pairs = []
for a, b in itertools.combinations(cards, 2):
    r = difflib.SequenceMatcher(None, norm(a["front"] + " " + a["back"]), norm(b["front"] + " " + b["back"])).ratio()
    if r >= 0.8:
        pairs.append((round(r, 3), a["id"], b["id"]))
print("pairs with combined front+back similarity >= 0.80:", sorted(pairs, reverse=True)[:20], "count", len(pairs))
lessons = Counter(c["lesson"] for c in cards)
print("per lesson:", dict(sorted(lessons.items())))
for c in cards:
    if c["lesson"] not in {f"L0{i}" for i in range(1, 10)}:
        print("unexpected lesson:", c["id"], c["lesson"])
print("c211 record:", json.dumps([c for c in cards if c["id"] == "M3-c211"][0], ensure_ascii=False))
