"""Card checks for M5 L08-L10: schema, grade/basis, duplicates over the whole file, and numbers on each card.

For each card of lesson L08-L10, every number-like token in front and back must appear in the lesson's
text (tags stripped, entities unescaped, LaTeX kept). Misses are printed for manual reading.
Usage: python3 -I cards_check.py <repo-root>
"""

import html
import json
import pathlib
import re
import sys
from collections import Counter

root = pathlib.Path(sys.argv[1]) / "course/modules/M/M5"
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
print("cards total", len(cards))
ids = Counter(c["id"] for c in cards)
print("duplicate ids", [i for i, n in ids.items() if n > 1])
fronts = Counter(c["front"].strip().lower() for c in cards)
backs = Counter(c["back"].strip().lower() for c in cards)
print("duplicate fronts", [f for f, n in fronts.items() if n > 1])
print("duplicate backs", [b for b, n in backs.items() if n > 1])
keys = {"id", "lesson", "front", "back", "grade", "basis", "cite"}
print("unexpected keys", sorted({k for c in cards for k in c} - keys))
print("grades", Counter(c.get("grade") for c in cards))
print("T without basis or cite", [c["id"] for c in cards if c.get("grade") == "T" and not (c.get("basis") or c.get("cite"))])
print("C without basis", [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis")])
print("cards with cite", [c["id"] for c in cards if c.get("cite")])
print("prefix ok", all(c["id"].startswith("M5-c") for c in cards))

NUM = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?")
def lesson_text(name: str) -> str:
    s = (root / name).read_text(encoding="utf-8")
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(s)

for lesson in ("L08", "L09", "L10"):
    text = lesson_text(f"{lesson}.html")
    text_nospace = re.sub(r"\s+", "", text)
    lc = [c for c in cards if c["lesson"] == lesson]
    misses = []
    for c in lc:
        for field in ("front", "back"):
            for tok in NUM.findall(c[field]):
                if tok not in text and tok.rstrip("0") not in text_nospace and tok not in text_nospace:
                    misses.append((c["id"], field, tok))
    print(lesson, "cards", len(lc), "number tokens not found verbatim in lesson text:", misses)
