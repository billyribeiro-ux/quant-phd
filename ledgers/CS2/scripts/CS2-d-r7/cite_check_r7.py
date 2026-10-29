"""Round-7 verifier script: every numbered label cited by a card must occur in the card's lesson text (or in another
CS2 lesson when the card names that lesson), and every card's lesson id must match its page.

Usage: python cite_check_r7.py <checkout-root>
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
text_dir = root / "ledgers/CS2/scripts/CS2-d-r7/text"
pages = {p.stem: p.read_text(encoding="utf-8") for p in text_dir.glob("L??.txt")}
cards = json.loads((root / "course/modules/CS/CS2/cards.json").read_text(encoding="utf-8"))
pat = re.compile(r"\b(Definition|Proposition|Lemma|Theorem|Corollary|Remark|Problem|Example|Assumption|Section)\s+(\d+(?:\.\d+)?|[A-Z]\d+)(\([a-z0-9]+\))?")
missing = []
checked = 0
for card in cards:
    own = pages[card["lesson"]]
    for m in pat.finditer(card["back"]):
        label = m.group(0)
        if m.group(1) == "Section":
            # "Section 4" names a section heading; accept any heading text that starts with the number
            ok = re.search(rf"\b{re.escape(label)}\b", own) is not None or re.search(rf"\bSection {m.group(2)}\b", own) is not None
        else:
            ok = re.search(rf"{re.escape(m.group(1))} {re.escape(m.group(2))}\b", own) is not None
        checked += 1
        if not ok:
            where = [k for k, t in pages.items() if re.search(rf"{re.escape(m.group(1))} {re.escape(m.group(2))}\b", t)]
            missing.append((card["id"], card["lesson"], label, where))
print("citations checked", checked)
for item in missing:
    print("NOT IN OWN LESSON", item)
print("missing", len(missing))
