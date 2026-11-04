"""(1) Pairwise similarity of card fronts and backs (difflib). (2) Every number token on a card must occur in its lesson text
or in the lab stdout of the lesson. Usage: dup_and_numbers.py <cards.json> <outdir-with-L0n.txt> <labs-stdout-dir>"""
import difflib
import json
import re
import sys
from pathlib import Path

cards = json.load(open(sys.argv[1], encoding="utf-8"))
out = Path(sys.argv[2])
labs = Path(sys.argv[3])
print("== near-duplicate pairs (front ratio >= 0.5 or back ratio >= 0.5 or joined >= 0.55)")
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        rf = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        rb = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
        rj = difflib.SequenceMatcher(None, a["front"] + " " + a["back"], b["front"] + " " + b["back"]).ratio()
        if rf >= 0.5 or rb >= 0.5 or rj >= 0.55:
            print(f"{a['id']}({a['lesson']}) {b['id']}({b['lesson']}) front={rf:.2f} back={rb:.2f} joined={rj:.2f}")
print("== number tokens not found in lesson text or lab stdout")
lesson_text = {}
for n in ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08"]:
    lesson_text[n] = (out / f"{n}.txt").read_text(encoding="utf-8")
allnums = []
for c in cards:
    toks = re.findall(r"\d+(?:\.\d+)?", c["front"] + " " + c["back"])
    for t in toks:
        allnums.append(t)
        lab = ""
        for f in labs.glob(f"lab-SC1-{c['lesson']}-*.stdout"):
            lab += f.read_text(encoding="utf-8")
        if t not in lesson_text[c["lesson"]] and t not in lab:
            print(f"{c['id']} {c['lesson']} token {t!r} not in its lesson or lab stdout")
print("number tokens checked:", len(allnums))
