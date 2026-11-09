"""Round-2: every multi-digit number or decimal on a L09-L11 card back appears in its lesson page (tags stripped, entities unescaped)."""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
cards = json.loads((ROOT / "course/modules/CS/CS2/cards.json").read_text(encoding="utf-8"))
lessons = {}
for page in ("L09", "L10", "L11"):
    raw = (ROOT / f"course/modules/CS/CS2/{page}.html").read_text(encoding="utf-8")
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    lessons[page] = re.sub(r"\s+", " ", text)
misses = []
checked = 0
for c in cards:
    if c["lesson"] not in lessons:
        continue
    nums = set(re.findall(r"\d+(?:\.\d+)?(?:e-?\d+)?", c["back"] + " " + c["front"]))
    for n in sorted(nums):
        if len(n.replace(".", "")) < 2 and "." not in n:
            continue  # single digits are structural (k=1,2,...), checked by reading
        checked += 1
        if n not in lessons[c["lesson"]]:
            misses.append((c["id"], c["lesson"], n))
print("numbers checked:", checked)
print("numbers not found verbatim in the lesson text:", len(misses))
for m in misses:
    print("  ", m)
