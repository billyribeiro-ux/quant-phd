"""FC1-a round 4: card integrity for L01-L03 cards: unique ids, unique fronts, numbers on each card appear in its lesson text."""

from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()
MOD = ROOT / "course/modules/FC/FC1"
cards = json.loads((MOD / "cards.json").read_text(encoding="utf-8"))
ids = Counter(c["id"] for c in cards)
print("duplicate ids:", [k for k, v in ids.items() if v > 1])
fronts = Counter(c["front"].strip().lower() for c in cards)
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
lesson_text = {}
for L in ["L01", "L02", "L03"]:
    raw = (MOD / f"{L}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    lesson_text[L] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
sl = [c for c in cards if c["lesson"] in ("L01", "L02", "L03")]
print("slice cards:", len(sl), "ids", sl[0]["id"], "..", sl[-1]["id"])
missing = []
for c in sl:
    text = c["front"] + " " + c["back"]
    nums = set(re.findall(r"\d[\d,]*\.?\d*", text))
    for n in sorted(nums):
        token = n.rstrip(".").replace(",", "")
        if token in {"1", "2", "3", "0", "4"}:
            continue
        if token not in lesson_text[c["lesson"]].replace(",", ""):
            missing.append((c["id"], c["lesson"], token))
print("numbers on a card not found in its lesson text (after removing thousands commas):", missing)
# near duplicates: same back text
backs = Counter(c["back"].strip().lower() for c in cards)
print("duplicate backs:", [k[:60] for k, v in backs.items() if v > 1])
