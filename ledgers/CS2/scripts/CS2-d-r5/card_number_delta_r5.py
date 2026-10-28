"""Verifier CS2-d round 5: which card backs quote a number that the current lesson text has but the round-4 pin did not.

usage: card_number_delta_r5.py <cards.json> <current-lesson-txt-dir> <old-lesson-txt-dir>
A card is flagged for re-reading when any number in its back is absent from the old lesson text.
"""
import json, re, sys
from pathlib import Path

cards = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
new = Path(sys.argv[2]); old = Path(sys.argv[3])
for c in cards:
    ntxt = (new / f"{c['lesson']}.txt").read_text(encoding="utf-8")
    otxt = (old / f"{c['lesson']}.txt").read_text(encoding="utf-8")
    toks = set(re.findall(r"\d[\d,.]*\d|\d", c["back"] + " " + c["front"]))
    fresh = [t for t in sorted(toks) if t.rstrip(".,") not in otxt and t.replace(",", "") not in otxt]
    if fresh:
        print(c["id"], c["lesson"], "numbers new in lesson text:", fresh)
print("done")
