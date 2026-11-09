"""Lesson-restricted coverage of L01-L03 blocks by slice-a cards, and misconception quotes (round 5)."""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/E/E1/cards.json").read_text(encoding="utf-8"))
for lid in ("L01", "L02", "L03"):
    page = (root / f"course/modules/E/E1/{lid}.html").read_text(encoding="utf-8")
    titles = list(dict.fromkeys(re.findall(r'<span class="block-title[^"]*"[^>]*>((?:Definition|Proposition|Theorem|Lemma|Corollary) \d+\.\d+)', page)))
    lc = [c for c in cards if c["lesson"] == lid]
    print(lid, "blocks:")
    for t in titles:
        hits = [c["id"] for c in lc if re.search(re.escape(t) + r"(?!\d)", c["front"] + " " + c["back"])]
        print("  ", t, "->", hits or "NONE IN LESSON CARDS")
    print(lid, "misconceptions:")
    for q in re.findall(r'<p class="wrong">“(.*?)”</p>', page):
        print("   WRONG:", q)
