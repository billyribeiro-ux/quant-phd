"""Structure counts and slice-card checks for M2 slice c (L13-L18), round 4.

Prints: why-it-matters word counts, misconception and problem counts, quiz item counts, key-results row
counts, slice-card grade counts, C-card basis check, exact and near-duplicate slice fronts across the unit,
and the card-id set of the slice. Run: .venv/bin/python -I <this file> <checkout root>.
"""
import difflib
import json
import re
import sys

ROOT = sys.argv[1]
PAGES = ["L13", "L14", "L15", "L16", "L17", "L18"]
for p in PAGES:
    s = open(f"{ROOT}/course/modules/M/M2/{p}.html", encoding="utf-8").read()
    why = [len(re.sub(r"<[^>]+>", " ", m).split()) for m in re.findall(r'<p class="why-it-matters">(.*?)</p>', s, re.S)]
    mis = len(re.findall(r'<li class="misconception">', s))
    probs = re.findall(r'<span class="problem-title">([A-Z][0-9]) ', s)
    quiz = len(re.findall(r'<li class="item"', s))
    kr = len(re.findall(r'<tr><td>', s))
    solutions = len(re.findall(r'<details class="solution">', s))
    print(f"{p}: why_words={why} misconceptions={mis} problem_ids={probs} quiz_items={quiz} key_result_rows_(all_tr_td)={kr} solutions={solutions}")

cards = json.load(open(f"{ROOT}/course/modules/M/M2/cards.json", encoding="utf-8"))
sl = [c for c in cards if c["lesson"] in PAGES]
print("slice cards:", len(sl), "ids:", sl[0]["id"], "...", sl[-1]["id"])
print("grades:", {g: sum(1 for c in sl if c.get("grade") == g) for g in ["T", "C", None]})
print("C cards without basis:", [c["id"] for c in sl if c.get("grade") == "C" and not c.get("basis")])
print("T cards with basis field:", [c["id"] for c in sl if c.get("grade") == "T" and c.get("basis")])
fronts = [(c["id"], c["front"]) for c in cards]
exact = [i for i, (cid, f) in enumerate(fronts) if sum(1 for _, g in fronts if g.strip().lower() == f.strip().lower()) > 1]
print("exact duplicate fronts unit-wide:", exact)
near = []
for a in range(len(sl)):
    for b in range(a + 1, len(sl)):
        r = difflib.SequenceMatcher(None, sl[a]["front"], sl[b]["front"]).ratio()
        if r >= 0.80:
            near.append((round(r, 2), sl[a]["id"], sl[b]["id"]))
print("near-duplicate slice front pairs (ratio >= 0.80):", near)
for c in sl:
    if c["id"] in ("M2-c212", "M2-c225"):
        nums = re.findall(r"\d+\.\d{3,}|\d+e-\d+", c["front"] + " " + c["back"])
        print(c["id"], "numbers with >=3 decimals or sci notation:", nums)
