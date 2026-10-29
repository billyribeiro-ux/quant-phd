# Full duplicate scan of course/modules/M/M2/cards.json (pin 1817191): exact front duplicates and near-duplicate fronts.
# Usage: .venv/bin/python -I ledgers/M2/scripts/M2-a-r2/card_dupes.py
import json, re, difflib, itertools
cards = json.load(open("course/modules/M/M2/cards.json", encoding="utf-8"))
def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", s.lower())).strip()
print("cards:", len(cards), "unique ids:", len({c["id"] for c in cards}))
fronts = {}
for c in cards:
    fronts.setdefault(norm(c["front"]), []).append(c["id"] + "(" + c["lesson"] + ")")
for k, v in fronts.items():
    if len(v) > 1:
        print("EXACT DUPLICATE FRONT:", v, "|", k)
pairs = []
for a, b in itertools.combinations(cards, 2):
    r = difflib.SequenceMatcher(None, norm(a["front"]), norm(b["front"])).ratio()
    if r >= 0.8:
        pairs.append((round(r, 3), a["id"], a["lesson"], b["id"], b["lesson"], a["front"][:70], b["front"][:70]))
for p in sorted(pairs, reverse=True):
    print("NEAR (ratio>=0.8):", p)
bk = {}
for c in cards:
    bk.setdefault(norm(c["back"]), []).append(c["id"])
for k, v in bk.items():
    if len(v) > 1:
        print("EXACT DUPLICATE BACK:", v)
