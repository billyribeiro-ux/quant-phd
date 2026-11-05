"""Every decimal or multi-digit number on an M4 card must appear in its lesson's text (or, for a basis card, in the
printed output of that lesson's lab twin, saved at /tmp/m4d11_labs). Prints each card number not found. Standard library."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(".")
cards = json.loads((ROOT / "course/modules/M/M4/cards.json").read_text(encoding="utf-8"))
labs = Path(sys.argv[1])
NUM = re.compile(r"(?<![A-Za-z_])(\d+\.\d+|\d{2,}(?:[,]\d{3})*|\d+\.\d+e[-+]?\d+)")
text_cache: dict[str, str] = {}


def lesson_text(lesson: str) -> str:
    if lesson not in text_cache:
        raw = (ROOT / f"course/modules/M/M4/{lesson}.html").read_text(encoding="utf-8")
        text_cache[lesson] = re.sub(r"<[^>]+>", " ", raw)
    return text_cache[lesson]


missing = []
for c in cards:
    hay = lesson_text(c["lesson"])
    if "basis" in c:
        for lab in labs.glob(f"lab-M4-{c['lesson']}*.out"):
            hay += lab.read_text(encoding="utf-8")
    for m in NUM.finditer(c["back"]):
        tok = m.group(1).replace(",", "")
        bare = tok.rstrip("0") if "." in tok and tok.endswith("0") and False else tok
        if bare not in hay and tok not in hay:
            missing.append((c["id"], c["lesson"], c["grade"], tok))
for row in missing:
    print(*row)
print("numbers not found:", len(missing))
