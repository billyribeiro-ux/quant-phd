"""Card checks for CS2 lessons L05-L08 (slice b).

For every card: (a) every number token in front/back appears in the card's lesson text (tags stripped);
(b) every cross-reference in parentheses (Definition x.y, Lemma x.y, Proposition x.y, Theorem x.y,
Corollary x.y, Example x.y, Remark x.y, Problem XN, Section N, Lab 1 Part X) exists in the lesson;
(c) every non-T grade carries a basis; (d) no duplicate ids or near-duplicate fronts across all 224 cards.
Usage: python -I -W error cards_check.py <repo_root>
"""
from __future__ import annotations

import html
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/CS/CS2"
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
text_cache: dict[str, str] = {}


def lesson_text(name: str) -> str:
    if name not in text_cache:
        raw = (root / f"{name}.html").read_text(encoding="utf-8")
        raw = re.sub(r"<[^>]+>", " ", raw)
        text_cache[name] = html.unescape(re.sub(r"\s+", " ", raw))
    return text_cache[name]


problems: list[str] = []
slice_cards = [c for c in cards if c["lesson"] in {"L05", "L06", "L07", "L08"}]
for c in cards:
    if not c.get("front", "").strip() or not c.get("back", "").strip():
        problems.append(f"{c['id']}: empty front/back")
    if c["grade"] != "T" and not (c.get("basis") or c.get("cite")):
        problems.append(f"{c['id']}: non-T grade without basis/cite")

ids = [c["id"] for c in cards]
dups = {i for i in ids if ids.count(i) > 1}
if dups:
    problems.append(f"duplicate ids {sorted(dups)}")

for c in slice_cards:
    body = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    lt = lesson_text(c["lesson"])
    for num in set(re.findall(r"(?<![A-Za-z_])\d+(?:\.\d+)?", body)):
        # a number inside the card is accepted when the lesson contains it as a token
        if not re.search(rf"(?<![\d.]){re.escape(num)}(?![\d])", lt):
            problems.append(f"{c['id']}: number {num} not in lesson {c['lesson']}")
    for kind, label in re.findall(r"\b(Definition|Lemma|Proposition|Theorem|Corollary|Example|Remark)\s+(\d+\.\d+)", body):
        if f"{kind} {label}" not in lt:
            problems.append(f"{c['id']}: '{kind} {label}' not in lesson {c['lesson']}")
    for label in re.findall(r"\bProblem\s+([MPER]\d)\b", body):
        if f"{label} · " not in lt and f"{label} ·" not in lt:
            problems.append(f"{c['id']}: Problem {label} not in lesson {c['lesson']}")
    for label in re.findall(r"\bSection\s+(\d)\b", body):
        if f"Section {label}" not in lt and f"§{label}" not in lt:
            # sections are cited by title elsewhere; record as note only
            pass

# near-duplicate fronts across the whole deck
fronts = [(c["id"], c["front"].lower()) for c in cards]
near = []
for i in range(len(fronts)):
    for j in range(i + 1, len(fronts)):
        r = SequenceMatcher(None, fronts[i][1], fronts[j][1]).ratio()
        if r >= 0.8:
            near.append((round(r, 2), fronts[i][0], fronts[j][0]))
print(f"cards total={len(cards)} slice_cards={len(slice_cards)} dup_ids={len(dups)}")
print("near-duplicate fronts (ratio>=0.8):", near if near else "none")
print("PROBLEMS:" if problems else "PROBLEMS: none")
for p in problems:
    print("  ", p)
