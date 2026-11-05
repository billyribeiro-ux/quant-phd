"""For each L05..L08 card of E3, list each number (decimal or fraction) on the card that does not occur in its lesson text
(L0x.txt from strip.py, which includes the lab code and printed output). Also list duplicate card fronts."""
import json
import re
import sys

D = "ledgers/E3/scripts/E3-g-r11"
cards = json.load(open("course/modules/E/E3/cards.json", encoding="utf-8"))
texts = {L: open(f"{D}/{L}.txt", encoding="utf-8").read() for L in ("L05", "L06", "L07", "L08")}
pat = re.compile(r"(?<![A-Za-z_])(\d+(?:\.\d+)?(?:/\d+)?(?:e-?\d+)?)")
norm = lambda s: s.replace(" ", "")
bad = 0
checked = 0
for c in cards:
    L = c["lesson"]
    if L not in texts:
        continue
    checked += 1
    text = norm(texts[L])
    body = c["front"] + " " + c["back"]
    for tok in set(pat.findall(body)):
        if tok in ("1", "0", "2", "3", "4", "5"):
            continue
        if norm(tok) not in text:
            # try the numerator/denominator form of a fraction, and the eight-decimal forms
            bad += 1
            print(f"{c['id']} {L}: '{tok}' not found in lesson text")
print(f"cards checked {checked}; numbers not found {bad}")
fronts = [c["front"] for c in cards]
dups = {f for f in fronts if fronts.count(f) > 1}
print("duplicate fronts across the unit:", len(dups))
ids = [c["id"] for c in cards]
print("duplicate ids:", len(ids) - len(set(ids)))
