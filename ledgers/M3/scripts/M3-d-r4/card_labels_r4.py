"""Round-4 verifier: every numbered result a card cites ("Theorem 2.2", "Proposition 3.3(a)", "Remark 1.4", ...)
must appear as a heading in the lesson the card names (ledgers/M3/scripts/M3-d-r4/out/text/L0n.txt). Prints the
cards whose cited labels are absent from their own lesson, and the labels that exist only in another lesson.

Usage (from the checkout root): .venv/bin/python -I ledgers/M3/scripts/M3-d-r4/card_labels_r4.py
"""

import json
import re
from pathlib import Path

ROOT = Path.cwd()
TEXT = ROOT / "ledgers/M3/scripts/M3-d-r4/out/text"
cards = json.loads((ROOT / "course/modules/M/M3/cards.json").read_text(encoding="utf-8"))
texts = {f.stem: f.read_text(encoding="utf-8") for f in TEXT.glob("L0*.txt")}
PAT = re.compile(r"\b(Definition|Theorem|Proposition|Lemma|Corollary|Remark|Example|Fact|Problem|Assumption)s? (\d+\.\d+[a-z]?)")
SECTION = re.compile(r"\bSection (\d)\b")
missing_here = []
elsewhere = []
total = 0
for card in cards:
    lesson = card["lesson"]
    refs = set()
    for field in ("front", "back", "basis"):
        s = card.get(field, "") or ""
        refs |= {f"{k} {v}" for k, v in PAT.findall(s)}
    for label in sorted(refs):
        total += 1
        own = texts[lesson]
        # a heading in the lesson text looks like "Definition 1.1 (orthogonal matrix)" or "Theorem 2.3 (...)" or "Example 2.5"
        head = re.compile(rf"(^|\n)\s*{re.escape(label)}(\s|\(|\.|:|$)", re.M)
        if not head.search(own) and label.split()[0] not in ("Problem", "Assumption"):
            where = [name for name, t in texts.items() if head.search(t)]
            (elsewhere if where else missing_here).append((card["id"], lesson, label, where))
print(f"labels checked: {total}")
print("labels absent from the card's own lesson, present in another lesson:")
for row in elsewhere:
    print("  ", row)
print("labels absent from every lesson:")
for row in missing_here:
    print("  ", row)
