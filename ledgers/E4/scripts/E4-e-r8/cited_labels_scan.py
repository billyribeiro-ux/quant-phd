"""Round 8, slice e: every numbered result cited on a card must exist in E4 lesson text (scratch/txt/Lxx.txt, rendered by html_to_text.py).

Usage: python -I cited_labels_scan.py <cards.json> <txt dir>
"""
import json
import os
import re
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
txt = {i: open(os.path.join(sys.argv[2], f"L{i:02d}.txt"), encoding="utf-8").read() for i in range(1, 10)}
pat = re.compile(r"\b(Proposition|Lemma|Corollary|Definition|Remark|Example|Assumption|Problem|Fact|Theorem|Lab \d)\s*([A-Z]?\d+(?:\.\d+)?)")
missing = []
checked = 0
for c in cards:
    body = c["front"] + " " + c["back"]
    own = txt[int(c["lesson"][1:])]
    for kind, num in set(pat.findall(body)):
        lab = f"{kind} {num}"
        checked += 1
        if re.search(re.escape(lab) + r"(?![\d.])", own):
            continue
        if any(re.search(re.escape(lab) + r"(?![\d.])", t) for t in txt.values()):
            print("found in another lesson:", c["id"], c["lesson"], lab)
        else:
            missing.append((c["id"], c["lesson"], lab))
print("labels checked", checked, "not found anywhere", len(missing))
for m in sorted(missing):
    print("  NOT FOUND", m)
