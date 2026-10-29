"""Duplicate and coverage scan of course/modules/M/M4/cards.json (verifier script, round 1)."""
import json, re, sys
from collections import Counter
path = "course/modules/M/M4/cards.json"
cards = json.load(open(path, encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)) == len(ids))
per = Counter(c["lesson"] for c in cards)
print("per lesson:", dict(sorted(per.items())))
def norm(s):
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()
def bigrams(ws):
    return set(zip(ws, ws[1:]))
pairs = []
for i in range(len(cards)):
    bi = bigrams(norm(cards[i]["front"] + " " + cards[i]["back"]))
    for j in range(i + 1, len(cards)):
        bj = bigrams(norm(cards[j]["front"] + " " + cards[j]["back"]))
        if not bi or not bj:
            continue
        jac = len(bi & bj) / len(bi | bj)
        if jac >= 0.35 or norm(cards[i]["front"]) == norm(cards[j]["front"]):
            pairs.append((round(jac, 2), cards[i]["id"], cards[j]["id"], cards[i]["front"][:70], cards[j]["front"][:70]))
for p in sorted(pairs, reverse=True):
    print(p)
print("pairs >= 0.35 bigram Jaccard:", len(pairs))
for c in cards:
    if c["grade"] != "T" and "basis" not in c:
        print("NO BASIS", c["id"])
    if c["grade"] == "T" and "basis" in c:
        print("T with basis", c["id"])
