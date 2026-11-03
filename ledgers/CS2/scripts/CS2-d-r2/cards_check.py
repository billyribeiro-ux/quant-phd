"""Check every CS2 card against its lesson page: every number and every cited label must appear in that lesson
(or, for a number quoted from a lab, in the lab's printed output on the page). Prints mismatches, one per line.

Usage: python -I cards_check.py <repo_root>
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve() / "course/modules/CS/CS2"
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))


def text_of(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"(?s)<script.*?</script>", " ", raw)
    raw = re.sub(r"(?s)<style.*?</style>", " ", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    return re.sub(r"\s+", " ", raw)


lesson_text: dict[str, str] = {}
for c in cards:
    lid = c["lesson"]
    if lid not in lesson_text:
        lesson_text[lid] = text_of(root / f"{lid}.html")

label_re = re.compile(r"\b(Proposition|Lemma|Remark|Example|Corollary|Definition|Theorem|Assumption|Problem|Section|Lab|Part|Exercise|Table|Figure)\s+([A-Z]?\d+(?:\.\d+)?|[A-Z]\d+)")
num_re = re.compile(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)(?![\w])")
problems = 0
for c in cards:
    lid = c["lesson"]
    body = lesson_text[lid]
    for field in ("front", "back", "basis"):
        s = c.get(field, "")
        for lab in label_re.finditer(s):
            token = f"{lab.group(1)} {lab.group(2)}"
            if token not in body:
                problems += 1
                print(f"LABEL {c['id']} {lid} {field}: '{token}' not in lesson text")
        for num in num_re.finditer(s):
            n = num.group(1).replace(",", "")
            if n in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
                continue
            if n not in body:
                problems += 1
                print(f"NUMBER {c['id']} {lid} {field}: '{n}' not in lesson text")
print(f"cards={len(cards)} mismatches={problems}")
