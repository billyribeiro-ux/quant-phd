"""Verifier round 5: every number token in a slice card back (L07-L09) must occur in its lesson HTML (tags stripped)."""
import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/E/E1"
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
text = {}
for L in ("L07", "L08", "L09"):
    raw = (root / f"{L}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<[^>]+>", " ", raw)
    text[L] = html.unescape(raw)
bad = 0
n = 0
for c in cards:
    if c["lesson"] not in text:
        continue
    nums = re.findall(r"\d+(?:\.\d+)?", c["back"])
    missing = [x for x in nums if x not in text[c["lesson"]]]
    n += 1
    if missing:
        bad += 1
        print(c["id"], c["lesson"], "numbers not in lesson text:", sorted(set(missing)))
print("slice cards checked:", n, "cards with a number absent from their lesson:", bad)
