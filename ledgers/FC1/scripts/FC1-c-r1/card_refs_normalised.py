"""Second, normalised pass over the block citations in cards.json (after card_refs_in_lessons.py).

Normalisation: a trailing full stop is dropped; 'Lab 1, Part B' matches 'Lab 1 Part B'; 'Assumption X' also matches the
bare label 'X' (lessons label items such as 'B1 (two dealers)'); 'misconception n' matches when the lesson has at least
n <li class="misconception"> items (they are numbered by order). A citation is UNRESOLVED when none of these holds.
Usage: python -I card_refs_normalised.py <module dir>
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

module = Path(sys.argv[1])
cards = json.loads((module / "cards.json").read_text(encoding="utf-8"))
texts: dict[str, str] = {}
counts: dict[str, int] = {}
for lesson in ("L01", "L02", "L03", "L04", "L05"):
    raw = (module / f"{lesson}.html").read_text(encoding="utf-8")
    counts[lesson] = len(re.findall(r'<li class="misconception"', raw))
    texts[lesson] = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw)))
pattern = re.compile(
    r"\b(Definition|Proposition|Remark|Example|Problem|Corollary|Assumption|Section|misconception|Lab \d, Part)\s?"
    r"([A-Z]?\d[\d.]*(?:\([ivx]+\))?|[A-Z]\d|[A-Z]\b)?"
)
unresolved = []
total = 0
for card in cards:
    lesson = card["lesson"]
    text = texts[lesson]
    for match in pattern.finditer(card["front"] + " " + card["back"]):
        label = match.group(0).rstrip(".").strip()
        total += 1
        kind, _, rest = label.partition(" ")
        if label.startswith("misconception"):
            number = int(label.split()[-1])
            ok = counts[lesson] >= number
        elif label.startswith("Lab "):
            ok = label in text or label.replace(", Part", " Part") in text
        elif label.startswith("Assumption ") or label.startswith("Problem ") or label.startswith("Section "):
            bare = label.split(" ", 1)[1]
            ok = label in text or (kind == "Assumption" and re.search(rf"\({bare}\)|\b{re.escape(bare)}\b", text) is not None)
            if not ok and kind == "Problem":
                ok = label in text
        else:
            ok = label in text
        if not ok:
            unresolved.append(f"{card['id']} ({lesson}): '{label}'")
for item in unresolved:
    print("UNRESOLVED", item)
print(f"citations={total} unresolved={len(unresolved)}")
