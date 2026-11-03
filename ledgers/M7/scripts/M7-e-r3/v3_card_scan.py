"""Scan all M7 cards for banned phrases, process words, duplicates, grade/basis rules and SIMULATED labels.

Usage: python -I v3_card_scan.py  (verifier round 3, slice e; reads course/modules/M/M7/cards.json)
"""
import json
import re
from collections import Counter

cards = json.load(open("course/modules/M/M7/cards.json", encoding="utf-8"))
print("cards", len(cards), "ids unique", len({c["id"] for c in cards}) == len(cards))
ids = sorted(int(c["id"].split("c")[1]) for c in cards)
print("id range", ids[0], ids[-1], "missing numbers in range:", sorted(set(range(ids[0], ids[-1] + 1)) - set(ids)))
banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "...", "…", "round", "builder", "verifier", "fixer", "predicted", "prediction"]
hits = []
for c in cards:
    text = (c["front"] + " " + c["back"] + " " + c.get("basis", "")).lower()
    for b in banned:
        if b.lower() in text:
            hits.append((c["id"], b))
print("banned/process hits:", hits)
print("keys:", Counter(tuple(sorted(c.keys())) for c in cards))
print("grades:", Counter(c["grade"] for c in cards))
bad_basis = [c["id"] for c in cards if c["grade"] == "C" and not c.get("basis")]
print("C cards without basis:", bad_basis)
t_with_basis = [c["id"] for c in cards if c["grade"] == "T" and c.get("basis")]
print("T cards carrying basis:", t_with_basis)
sim_needed = {"L01", "L02", "L03", "L04", "L06", "L07", "L08"}
c_no_sim = [(c["id"], c["lesson"], c["basis"]) for c in cards
            if c["grade"] == "C" and c["lesson"] in sim_needed and "SIMULATED" not in c.get("basis", "")]
print("C cards from SIMULATED-lab lessons without SIMULATED in basis:", c_no_sim)
c_l05 = [(c["id"], c["basis"]) for c in cards if c["grade"] == "C" and c["lesson"] == "L05"]
print("L05 C cards:", c_l05)
# duplicate fronts (normalised) and near-duplicates by token Jaccard
def toks(s):
    return set(re.findall(r"[a-z0-9]+", s.lower()))
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = toks(cards[i]["front"]), toks(cards[j]["front"])
        if not a or not b:
            continue
        jac = len(a & b) / len(a | b)
        if jac >= 0.5:
            pairs.append((round(jac, 2), cards[i]["id"], cards[j]["id"], cards[i]["front"][:70], cards[j]["front"][:70]))
print("front near-duplicates (jaccard>=0.5):")
for p in sorted(pairs, reverse=True):
    print("  ", p)
bk = [(c["id"], c["back"][:60]) for c in cards]
seen = Counter(b for _, b in bk)
print("identical backs:", [x for x in seen.items() if x[1] > 1])
lesson_counts = Counter(c["lesson"] for c in cards)
print("cards per lesson:", dict(sorted(lesson_counts.items())))
