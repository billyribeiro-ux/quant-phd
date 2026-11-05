"""Find every numeric token in cards.json and report whether it appears verbatim in its own lesson text
(rendered from the page) or in that lesson's lab stdout. Usage: python -I card_numbers_r8.py <cards.json> <out_dir>
"""
import json
import os
import re
import sys

cards_path, out_dir = sys.argv[1], sys.argv[2]
cards = json.load(open(cards_path, encoding="utf-8"))
NUM = re.compile(r"(?<![A-Za-z_\w])(\d+(?:\.\d+)?(?:/\d+)?(?:\s?×\s?10\^\(?-?\d+\)?)?)")
texts: dict[str, str] = {}
for lesson in ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08"]:
    t = open(os.path.join(out_dir, f"{lesson}.txt"), encoding="utf-8").read()
    stdout = open(os.path.join(out_dir, "labs", f"lab-SC1-{lesson}-1.stdout"), encoding="utf-8").read()
    texts[lesson] = t + "\n" + stdout
missing = []
total = 0
for c in cards:
    lesson = c["lesson"]
    body = c["front"] + " " + c["back"]
    for tok in NUM.findall(body):
        t = tok.strip()
        if t in ("0", "1", "2", "3", "4"):
            continue
        total += 1
        if t not in texts[lesson]:
            missing.append((c["id"], lesson, t))
print(f"numeric tokens (excluding 0..4): {total}; not verbatim in own lesson text or stdout: {len(missing)}")
for m in missing:
    print("  ", m)
