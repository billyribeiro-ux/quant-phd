"""Round-4 card checks for FC2 L07 and L08 (run from the checkout root).

1. Every numeric token in a card's front or back appears in its own lesson's visible text (or its twin).
2. No duplicate ids; ids unique across all cards.
3. Each card's lesson is L07 or L08 for the slice.
4. Grade and basis keys: prints every card with its grade and basis for manual review.
"""

from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(".").resolve()
cards = json.loads((ROOT / "course/modules/FC/FC2/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)), "duplicate ids", [k for k, v in Counter(ids).items() if v > 1])


def visible(path: Path) -> str:
    t = path.read_text(encoding="utf-8")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t)


text = {
    "L07": visible(ROOT / "course/modules/FC/FC2/L07.html") + " " + (ROOT / "tests/labs/FC2/lab-FC2-L07-1.py").read_text(),
    "L08": visible(ROOT / "course/modules/FC/FC2/L08.html") + " " + (ROOT / "tests/labs/FC2/lab-FC2-L08-1.py").read_text(),
}
missing: list[str] = []
for c in cards:
    if c["lesson"] not in ("L07", "L08"):
        continue
    for field in ("front", "back"):
        for tok in re.findall(r"\d+(?:\.\d+)?", c[field]):
            if tok not in text[c["lesson"]]:
                missing.append(f"{c['id']} {field} token {tok!r}")
print("numeric tokens not found in own lesson (or twin):", missing if missing else "none")
for c in cards:
    if c["lesson"] in ("L07", "L08"):
        print(c["id"], c["lesson"], c.get("grade"), c.get("basis"), "|", c["front"][:70])
