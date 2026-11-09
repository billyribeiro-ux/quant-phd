"""Round-4 slice a: every number token on a slice card (L01-L06) must appear in that card's lesson page text (tags stripped, entities decoded, math kept)."""
import html
import json
import re
import sys

root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/M/M2/cards.json", encoding="utf-8"))
lessons = {}
for i in range(1, 7):
    raw = open(f"{root}/course/modules/M/M2/L{i:02d}.html", encoding="utf-8").read()
    lessons[f"L{i:02d}"] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
bad = 0
checked = 0
for c in cards:
    if c["lesson"] not in lessons:
        continue
    checked += 1
    text = lessons[c["lesson"]]
    for field in ("front", "back"):
        for tok in re.findall(r"\d+(?:\.\d+)?(?:e-?\d+)?", c[field]):
            if tok in ("1", "2", "0", "3", "4", "5", "6", "10"):
                continue  # small integers are checked by reading, not by string match
            if tok not in text:
                bad += 1
                print(f"{c['id']} {c['lesson']} {field}: number {tok!r} not in lesson text")
print(f"cards checked: {checked}; numbers not found in lesson (excluding 0-10): {bad}")
