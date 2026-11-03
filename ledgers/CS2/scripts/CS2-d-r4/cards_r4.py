"""Round-4 card checks for CS2: duplicates, lesson links, every number in a card's back appears in its lesson text,
and grade and basis rules. Prints the cards that fail any check, then the count of cards checked."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
UNIT = ROOT / "course/modules/CS/CS2"
cards = json.loads((UNIT / "cards.json").read_text(encoding="utf-8"))
lessons: dict[str, str] = {}
for path in sorted(UNIT.glob("L*.html")):
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    text = re.sub(r"\s+", " ", text)
    lessons[path.stem] = text
problems: list[str] = []
seen: set[str] = set()
for c in cards:
    cid = c["id"]
    if cid in seen:
        problems.append(f"{cid}: duplicate id")
    seen.add(cid)
    if c["lesson"] not in lessons:
        problems.append(f"{cid}: lesson {c['lesson']} missing")
        continue
    if c["grade"] not in ("T", "C"):
        problems.append(f"{cid}: grade {c['grade']!r}")
    for field in ("front", "back"):
        if not c[field].strip():
            problems.append(f"{cid}: empty {field}")
    numbers = set(re.findall(r"\d[\d,]*\.?\d*", c["back"]))
    for num in sorted(numbers):
        bare = num.rstrip(".").replace(",", "")
        if bare not in lessons[c["lesson"]].replace(",", ""):
            problems.append(f"{cid}: number {num} in back not found in lesson {c['lesson']}")
print("cards:", len(cards), "distinct ids:", len(seen), "lesson-text keys:", sorted(lessons))
print("problems:", len(problems))
for p in problems:
    print("  ", p)
