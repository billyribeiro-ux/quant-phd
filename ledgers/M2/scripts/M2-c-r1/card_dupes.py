"""Near-duplicate scan over all M2 cards (fronts and backs), and card-number-in-lesson check (verifier scratch, round 1)."""
import difflib
import json
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
cards = json.load(open(f"{ROOT}/course/modules/M/M2/cards.json", encoding="utf-8"))
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower())
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        r = difflib.SequenceMatcher(None, norm(a["front"]), norm(b["front"])).ratio()
        if r >= 0.80:
            pairs.append((round(r, 3), a["id"], a["lesson"], b["id"], b["lesson"], a["front"][:70], b["front"][:70]))
print(f"cards={len(cards)} front-near-duplicate pairs (ratio>=0.80): {len(pairs)}")
for p in sorted(pairs, reverse=True)[:30]:
    print(p)
# card numbers appearing in their lesson text
for n in range(13, 19):
    txt = open(f"{ROOT}/course/modules/M/M2/L{n}.html", encoding="utf-8").read()
    txt = re.sub(r"<[^>]+>", " ", txt)
    missing = []
    for c in cards:
        if c["lesson"] != f"L{n}":
            continue
        for num in re.findall(r"\d+\.\d+|\d+e-?\d+|\d+ ?times", c["back"]):
            pass
        for num in set(re.findall(r"\b\d+\.\d{3,}\b", c["back"])):
            if num not in txt:
                missing.append((c["id"], num))
    print(f"L{n} card decimals absent from lesson text: {missing}")
