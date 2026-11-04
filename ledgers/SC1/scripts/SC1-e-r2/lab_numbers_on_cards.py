"""For each card whose basis names a lab, list numeric tokens in its back that do not occur in that lab's
actual stdout (from python -I -W error run, saved under /tmp/sc1e_out). Tokens absent from stdout are
either rounded forms, derived values, or wrong; each is judged by hand in the ledger.
Usage: lab_numbers_on_cards.py <cards.json> <stdout dir>
"""
import json
import re
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
out_dir = sys.argv[2]
NUM = re.compile(r"(?<![A-Za-z_\-])\d+(?:\.\d+)?")
for c in cards:
    basis = c.get("basis", "")
    if "Lab" not in basis:
        continue
    lesson = c["lesson"]
    if "Lab 1" in basis or "lab" in basis.lower():
        stem = f"lab-SC1-{lesson}-1"
    else:
        continue
    stdout = open(f"{out_dir}/{stem}.stdout", encoding="utf-8").read()
    toks = sorted(set(NUM.findall(c["back"])))
    absent = [t for t in toks if t not in stdout]
    if absent:
        print(c["id"], lesson, "absent from stdout:", absent)
