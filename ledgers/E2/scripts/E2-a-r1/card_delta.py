"""Delta check for E2 slice a cards (round 1, pin 95f3f8cb vs base pin f618cf1).

Lists per-id card differences between the two pins, then for every changed or new card whose lesson is
L01-L03 checks that each number in its front/back appears in that lesson's HTML text.
Usage (repository root): python -I ledgers/E2/scripts/E2-a-r1/card_delta.py
"""

import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path.cwd()
PAGES = ROOT / "course" / "modules" / "E" / "E2"


def cards_at(rev: str) -> dict[str, dict[str, object]]:
    raw = subprocess.run(
        ["git", "show", f"{rev}:course/modules/E/E2/cards.json"], capture_output=True, text=True, check=True
    ).stdout
    data = json.loads(raw)
    items = data if isinstance(data, list) else data["cards"]
    return {c["id"]: c for c in items}


base = cards_at("f618cf1")
head = cards_at("HEAD")
changed = sorted(i for i in head if i not in base or base[i] != head[i])
removed = sorted(i for i in base if i not in head)
print("cards base", len(base), "head", len(head), "removed", removed)
print("changed or new", changed)
print("unchanged slice-a ids c016 c017 c022 c027:",
      [(i, base.get(i) == head.get(i)) for i in ("E2-c016", "E2-c017", "E2-c022", "E2-c027")])

lesson_text: dict[str, str] = {}
for n in ("L01", "L02", "L03"):
    raw = (PAGES / f"{n}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<[^>]+>", " ", raw)
    lesson_text[n] = html.unescape(raw)

for cid in changed:
    c = head[cid]
    lesson = str(c["lesson"])
    if lesson not in lesson_text:
        continue
    text = f'{c["front"]} {c["back"]}'
    nums = sorted(set(re.findall(r"\d[\d,]*(?:\.\d+)?", text)))
    missing = [x for x in nums if x.rstrip(",") not in lesson_text[lesson]]
    print(cid, lesson, "numbers:", nums, "missing from lesson text:", missing)
