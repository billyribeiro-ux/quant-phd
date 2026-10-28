"""Verifier check (CS2-d round 2): every theorem-like reference on a card must name a label that its own lesson defines.

Usage: python -I card_refs_check.py <checkout>
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/CS/CS2"
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
pat = re.compile(r"\b(Theorem|Corollary|Proposition|Lemma|Definition|Example|Remark|Problem|Lab|Assumption)\s+(\d+\.\d+|\d+)")
bad: list[str] = []
count = 0
for card in cards:
    text = re.sub(r"<[^>]+>", " ", (root / f"{card['lesson']}.html").read_text(encoding="utf-8"))
    text = re.sub(r"\s+", " ", html.unescape(text))
    for field in ("front", "back"):
        for m in pat.finditer(card[field]):
            count += 1
            label = f"{m.group(1)} {m.group(2)}"
            if label not in text:
                bad.append(f"{card['id']} {field}: '{label}' not in {card['lesson']}")
print("theorem-like references on cards:", count)
print("references not found in own lesson:", len(bad))
for b in bad:
    print(" ", b)
