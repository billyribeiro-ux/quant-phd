"""Verifier E1-c round 2: every numeric token on an L07-L09 card (front or back) appears in its lesson page text."""
import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/E/E1/cards.json").read_text(encoding="utf-8"))
texts = {}
for lesson in ("L07", "L08", "L09"):
    raw = (root / f"course/modules/E/E1/{lesson}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<[^>]+>", " ", raw)
    texts[lesson] = html.unescape(raw).replace(",", "")
missing = []
for c in cards:
    if c["lesson"] not in texts:
        continue
    text = texts[c["lesson"]]
    for field in ("front", "back"):
        for tok in re.findall(r"\d+(?:\.\d+)?(?:/\d+)?", c[field].replace(",", "")):
            if tok not in text:
                missing.append((c["id"], field, tok))
print("cards checked:", sum(1 for c in cards if c["lesson"] in texts))
print("numeric tokens not found verbatim in lesson:", missing)
