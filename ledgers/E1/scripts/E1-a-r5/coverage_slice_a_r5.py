"""Coverage of L01-L03 definitions, propositions, theorems and misconceptions by slice-a cards (round 5).

Each block title 'Definition X.Y' / 'Proposition X.Y' / 'Theorem X.Y' / 'Lemma X.Y' on a lesson page is looked up
in the card texts of that lesson (cards cite them by number); misconceptions are counted per lesson and matched to
cards that name a misconception. Prints the matrix so every item can be read.
"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/E/E1/cards.json").read_text(encoding="utf-8"))
for lid in ("L01", "L02", "L03"):
    page = (root / f"course/modules/E/E1/{lid}.html").read_text(encoding="utf-8")
    titles = re.findall(r'<span class="block-title[^"]*"[^>]*>((?:Definition|Proposition|Theorem|Lemma|Corollary) \d+\.\d+)', page)
    titles = list(dict.fromkeys(titles))
    lesson_cards = [c for c in cards if c["lesson"] == lid]
    miss = len(re.findall(r'<li class="misconception">', page))
    miss_cards = [c["id"] for c in lesson_cards if "misconception" in c["back"].lower()]
    print(f"{lid}: blocks {len(titles)}; misconceptions on page {miss}; cards naming a misconception {miss_cards}")
    uncovered = []
    for t in titles:
        hits = [c["id"] for c in cards if re.search(re.escape(t) + r"(?!\d)", c["front"] + " " + c["back"])]
        status = "covered by " + ",".join(hits) if hits else "NOT COVERED"
        if not hits:
            uncovered.append(t)
        print(f"  {t}: {status}")
    print(f"  uncovered blocks: {uncovered}")
