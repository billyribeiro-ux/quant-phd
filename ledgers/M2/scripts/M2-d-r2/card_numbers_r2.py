"""Verifier round 2: every decimal or scientific number on a slice card (M2-c280..c377) must occur in its lesson text.
Usage: python -I card_numbers_r2.py <checkout>. Read-only; prints cards whose numbers are absent from the lesson."""
import json
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
texts = {}
for L in ("L19", "L20", "L21", "L22", "L23", "L24"):
    raw = (root / f"course/modules/M/M2/{L}.html").read_text(encoding="utf-8")
    plain = re.sub(r"<[^>]+>", " ", raw)
    texts[L] = plain.replace("&minus;", "-")
for c in cards:
    k = int(c["id"].split("c")[-1])
    if not 280 <= k <= 377 or c["lesson"] not in texts:
        continue
    nums = set(re.findall(r"\d+\.\d+(?:e[-+]?\d+)?|\d+e-\d+|\d+\.\d+e-\d+", c["back"] + " " + c["front"]))
    missing = [n for n in nums if n not in texts[c["lesson"]] and n not in texts[c["lesson"]].replace(",", "")]
    if missing:
        print(c["id"], c["lesson"], "numbers not in lesson text:", sorted(missing))
print("scan done")
