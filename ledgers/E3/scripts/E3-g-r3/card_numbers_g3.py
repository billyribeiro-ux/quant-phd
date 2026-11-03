"""For each L05-L08 card, list every number token in its front and back and say whether the
same token occurs in its own lesson text dump (text/Lnn.txt, produced by dump_text_g3.py).
Also reports duplicate fronts/backs and near-duplicates across the whole E3 card file.

Usage: python -I card_numbers_g3.py <unit_dir_with_cards.json> <scripts_dir>
"""
import difflib
import json
import re
import sys

NUM = re.compile(r"(?<![A-Za-z_])-?\d+(?:\.\d+)?(?:e-?\d+)?")

cards_path, scripts = sys.argv[1], sys.argv[2]
cards = json.load(open(cards_path, encoding="utf-8"))
texts = {}
for L in ("L05", "L06", "L07", "L08"):
    raw = open(f"{scripts}/text/{L}.txt", encoding="utf-8").read()
    texts[L] = re.sub(r"^\d{4}\| ", "", raw, flags=re.M).replace(",", "")
missing = 0
for c in cards:
    if c["lesson"] not in texts:
        continue
    toks = set(NUM.findall((c["front"] + " " + c["back"]).replace(",", "")))
    absent = [t for t in sorted(toks) if t.lstrip("-") not in texts[c["lesson"]] and t not in texts[c["lesson"]]]
    if absent:
        missing += 1
        print(f"{c['id']} {c['lesson']}: numbers not in own lesson text: {absent}")
print(f"cards with a number absent from their own lesson: {missing}")

seen_f, seen_b = {}, {}
for c in cards:
    seen_f.setdefault(c["front"].strip().lower(), []).append(c["id"])
    seen_b.setdefault(c["back"].strip().lower(), []).append(c["id"])
print("exact duplicate fronts:", {k: v for k, v in seen_f.items() if len(v) > 1})
print("exact duplicate backs:", {k: v for k, v in seen_b.items() if len(v) > 1})
l58 = [c for c in cards if c["lesson"] in ("L05", "L06", "L07", "L08")]
pairs = []
for i, a in enumerate(l58):
    for b in l58[i + 1:]:
        rf = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        rb = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
        if rf > 0.6 or rb > 0.6:
            pairs.append((round(rf, 2), round(rb, 2), a["id"], b["id"]))
print("L05-L08 pairs with front or back similarity > 0.6 (front ratio, back ratio, a, b):")
for p in sorted(pairs, reverse=True):
    print("  ", p)
ids = sorted(int(c["id"].split("-c")[1]) for c in cards)
gaps = [n for n in range(1, max(ids) + 1) if n not in ids]
print("missing ids in the sequence c001..c", max(ids), ":", gaps)
