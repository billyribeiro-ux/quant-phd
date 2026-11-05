"""For each SC1 card, list every number token (decimal, fraction, or integer of 2+ digits) that is absent from the
card's own lesson text (plain text from lesson_text.py) and from that lesson's lab stdout.

Usage: python -I card_numbers_r7.py <cards.json> <out dir with L0n.txt and labs/lab-SC1-L0n-1.stdout>.
"""
import json
import re
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
out = sys.argv[2]
texts = {}
for n in range(1, 9):
    lesson = open(f"{out}/L0{n}.txt", encoding="utf-8").read()
    lab = open(f"{out}/labs/lab-SC1-L0{n}-1.stdout", encoding="utf-8").read()
    texts[f"L0{n}"] = lesson + "\n" + lab
TOK = re.compile(r"\d+\.\d+|\d+/\d+|\d{2,}")
total = 0
missing = []
for c in cards:
    body = c["front"] + " " + c["back"]
    toks = set(TOK.findall(body))
    total += len(toks)
    hay = texts[c["lesson"]].replace(" ", " ")
    for t in toks:
        if t not in hay:
            missing.append((c["id"], c["lesson"], t))
print("distinct number tokens over cards:", total)
print("absent from own lesson text + lab stdout:", len(missing))
for cid, les, t in missing:
    print(f"  {cid} {les}: {t}")
