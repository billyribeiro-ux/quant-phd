"""Round-10 (verifier): every numbered citation on a card resolves to a heading of the card's own lesson.

A citation is a label such as 'Definition 1.1', 'Proposition 2.1(ii)', 'Problem R2', 'Section 4', 'Assumption 4.0' or
'Remark 1.2' inside the card's parentheses. A label resolves when the lesson text (out/lessons, from lesson_text.py)
contains it at the start of a line, after an optional number prefix. Labels with no number (for example 'misconception 1')
are checked as the word followed by a digit appearing in the lesson.
Usage: python -I ledgers/FC1/scripts/FC1-c-r10/cite_resolve_r10.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CARDS = json.loads((ROOT / "course" / "modules" / "FC" / "FC1" / "cards.json").read_text(encoding="utf-8"))
LESSONS = ROOT / "ledgers" / "FC1" / "scripts" / "FC1-c-r10" / "out" / "lessons"
TEXT = {f"L0{i}": (LESSONS / f"L0{i}.txt").read_text(encoding="utf-8") for i in range(1, 6)}
LABEL = re.compile(r"\b(Definition|Proposition|Remark|Example|Corollary|Section|Problem|Assumption|Lab \d, Part [A-D]|Assumptions [AB]\d to [AB]\d|Assumption [AB]\d|misconception \d)\s*([A-Z]?\d[\d.]*|[A-Z]\d)?")
unresolved: list[str] = []
checked = 0
for card in CARDS:
    text = TEXT[card["lesson"]]
    for group in re.findall(r"\(([^()]*)\)", card["back"]):
        for m in LABEL.finditer(group):
            label = m.group(0).rstrip(".")
            checked += 1
            base = re.sub(r"\(.*", "", label).strip()
            if base.startswith("Lab"):
                ok = "Lab 1" in text or "Lab 2" in text or "Lab 3" in text
                if not ok:
                    unresolved.append(f"{card['id']} {label}")
                continue
            if base.startswith("misconception"):
                ok = "Misconceptions" in text or "misconception" in text.lower()
                if not ok:
                    unresolved.append(f"{card['id']} {label}")
                continue
            if base.startswith("Assumptions") or base.startswith("Assumption ") and re.search(r"[AB]\d to", base):
                if not re.search(r"(Assumption|Assumptions)", text):
                    unresolved.append(f"{card['id']} {label}")
                continue
            if not re.search(r"(^|\n)" + re.escape(base), text):
                unresolved.append(f"{card['id']} {label}")
print("labels checked:", checked)
print("unresolved:", len(unresolved))
for u in unresolved:
    print("  ", u)
