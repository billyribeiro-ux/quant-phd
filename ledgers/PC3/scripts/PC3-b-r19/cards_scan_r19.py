"""Round 19 PC3-b card scan: schema keys, duplicates, cite lists, grades, and numbers in each card that must appear in its lesson."""
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1])
cards = json.loads((ROOT / "course/modules/PC/PC3/cards.json").read_text(encoding="utf-8"))
print("cards", len(cards))
keys = Counter(tuple(sorted(c.keys())) for c in cards)
for k, n in keys.items():
    print("keyset", n, k)
print("grades", Counter(c.get("grade") for c in cards))
print("cite nonempty", [c["id"] for c in cards if c.get("cite")])
norm = lambda s: re.sub(r"\s+", " ", s.strip().lower())  # noqa: E731
print("dup ids", [i for i, n in Counter(c["id"] for c in cards).items() if n > 1])
print("dup fronts", [i for i, n in Counter(norm(c["front"]) for c in cards).items() if n > 1])
print("dup backs", [i for i, n in Counter(norm(c["back"]) for c in cards).items() if n > 1])
lessons = {}
for L in ("L04", "L05", "L06"):
    raw = (ROOT / f"course/modules/PC/PC3/{L}.html").read_text(encoding="utf-8")
    txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    lessons[L] = re.sub(r"\s+", " ", txt)
for c in cards:
    if c["lesson"] not in lessons:
        continue
    text = c["front"] + " " + c["back"]
    nums = set(re.findall(r"\d+(?:\.\d+)?", text))
    missing = [n for n in sorted(nums) if n not in lessons[c["lesson"]] and n not in ("1", "2", "3", "0")]
    if missing:
        print("NUM-NOT-IN-LESSON", c["id"], c["lesson"], missing)
ids = [c["id"] for c in cards if c["lesson"] in lessons]
print("L04-L06 cards", len(ids), Counter(c["lesson"] for c in cards if c["lesson"] in lessons))
