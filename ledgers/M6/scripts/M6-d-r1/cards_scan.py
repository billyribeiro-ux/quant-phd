"""Card checks for M6 (verifier round 1): duplicate scan by word overlap, and cited statement headings present in the lesson.

Usage: <checkout>/.venv/bin/python ledgers/M6/scripts/M6-d-r1/cards_scan.py <checkout>
"""

from __future__ import annotations

import html
import itertools
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
mod = root / "course" / "modules" / "M" / "M6"
cards = json.loads((mod / "cards.json").read_text(encoding="utf-8"))

WORD = re.compile(r"[a-z0-9]+")


def words(text: str) -> set[str]:
    return set(WORD.findall(text.lower())) - {"the", "a", "of", "is", "and", "to", "in", "for", "on", "what", "does", "it"}


print(f"cards: {len(cards)}")
pairs = []
for a, b in itertools.combinations(cards, 2):
    wa, wb = words(a["front"] + " " + a["back"]), words(b["front"] + " " + b["back"])
    jac = len(wa & wb) / len(wa | wb)
    if jac >= 0.30:
        pairs.append((round(jac, 2), a["id"], b["id"], a["front"][:70], b["front"][:70]))
print(f"pairs with word Jaccard >= 0.30: {len(pairs)}")
for p in sorted(pairs, reverse=True):
    print(p)

texts: dict[str, str] = {}
pat = re.compile(r"\b(Definition|Proposition|Theorem|Example|Lemma|Corollary|Remark|Result)\s+([A-Z]?\d+\.\d+)")
missing = []
for c in cards:
    if c["lesson"] not in texts:
        raw = (mod / f"{c['lesson']}.html").read_text(encoding="utf-8")
        texts[c["lesson"]] = html.unescape(re.sub(r"<[^>]+>", "", raw))
    for m in pat.finditer(c["front"] + " " + c["back"]):
        kind, num = m.group(1), m.group(2)
        if not re.search(rf"{kind} {re.escape(num)}\s*[\(\.:]", texts[c["lesson"]]):
            missing.append((c["id"], c["lesson"], kind, num))
print(f"cited statement headings not found in the card's own lesson: {missing}")
