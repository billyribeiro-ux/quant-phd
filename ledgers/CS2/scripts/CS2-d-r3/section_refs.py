"""List every 'Section N' / 'Problem X' / 'Misconception N' mention in the CS2 lesson texts, and the cards citing them.

Usage: python -I section_refs.py <repo_root> <text dir>
"""

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
tdir = Path(sys.argv[2])
pat = re.compile(r"(Section|Problem|Misconception|Part|Lab)\s+([A-Z]?\d+[A-Za-z]?(?:\.\d+)?)")
for lid in ("L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09", "L10", "L11"):
    txt = (tdir / f"{lid}.txt").read_text(encoding="utf-8")
    found = sorted({f"{a} {b}" for a, b in pat.findall(txt)})
    print(lid, "lesson mentions:", found)
cards = json.loads((root / "course/modules/CS/CS2/cards.json").read_text(encoding="utf-8"))
for c in cards:
    for field in ("front", "back", "basis"):
        for a, b in pat.findall(c.get(field, "")):
            print(c["id"], c["lesson"], field, f"{a} {b}")
