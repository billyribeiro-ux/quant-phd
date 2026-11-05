"""Full scan of FC2 cards: unique ids and fronts, near-duplicate fronts, card numbers present in the cited lesson."""
import difflib
import json
import re
import sys

root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/FC/FC2/cards.json", encoding="utf-8"))
print("cards:", len(cards))
ids = [c["id"] for c in cards]
fronts = [c["front"] for c in cards]
print("unique ids:", len(set(ids)) == len(ids), "unique fronts:", len(set(fronts)) == len(fronts))
print("keys:", sorted({k for c in cards for k in c}))
print("grades:", sorted({c.get("grade", "-") for c in cards}))
lessons = {}
for c in cards:
    lessons.setdefault(c["lesson"], open(f"{root}/course/modules/FC/FC2/{c['lesson']}.html", encoding="utf-8").read())
bad = []
for c in cards:
    text = lessons[c["lesson"]]
    refs = set(re.findall(r"(Theorem|Lemma|Proposition|Definition|Remark|Example|Assumption|A)\s?(\d+\.\d+|\d+)", c["back"] + " " + c["front"]))
    for kind, num in refs:
        if kind == "A" and not re.fullmatch(r"\d", num):
            continue
        pat = f"{kind} {num}" if kind != "A" else f"A{num}"
        if pat not in text:
            bad.append((c["id"], c["lesson"], pat))
print("numbered references not found in cited lesson:", bad[:20], len(bad))
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        r = difflib.SequenceMatcher(None, cards[i]["front"], cards[j]["front"]).ratio()
        if r > 0.75:
            pairs.append((round(r, 2), cards[i]["id"], cards[j]["id"]))
print("near-duplicate fronts (ratio > 0.75):", sorted(pairs, reverse=True)[:30])
