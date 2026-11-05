"""Every numbered label a card names (Definition/Theorem/Proposition/Corollary/Remark/Example/Assumption A#/Problem X#)
must exist as a block title or problem heading of the card's own lesson, unless the card names another lesson.
Usage: python -I label_refs_r7.py <checkout>. Prints each card's labels and whether the lesson has them.
"""
import html
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
cards = json.loads((root / "course/modules/PC/PC3/cards.json").read_text(encoding="utf-8"))
blocks = {}
for n in range(1, 7):
    lid = f"L{n:02d}"
    page = (root / f"course/modules/PC/PC3/{lid}.html").read_text(encoding="utf-8")
    found = set()
    for t in re.findall(r'<span class="block-title[^"]*"[^>]*>(.*?)</span>', page, flags=re.S):
        t = html.unescape(re.sub(r"<[^>]+>", " ", t))
        t = re.sub(r"\s+", " ", t).strip()
        m = re.match(r"(Definition|Theorem|Proposition|Corollary|Assumption|Remark|Example|Problem)\s+([A-Z]?[0-9]+(?:\.[0-9]+)?)", t)
        if m:
            found.add(f"{m.group(1)} {m.group(2)}")
    for t in re.findall(r"<h3[^>]*>(.*?)</h3>", page, flags=re.S) + re.findall(r"<h4[^>]*>(.*?)</h4>", page, flags=re.S):
        t = html.unescape(re.sub(r"<[^>]+>", " ", t))
        m = re.match(r"\s*([MEPR][0-9]+)\s", t)
        if m:
            found.add(f"Problem {m.group(1)}")
    # problem headings appear as "M1 · ..." inside a span or p; scan the plain text too
    plain = html.unescape(re.sub(r"<[^>]+>", "\n", page))
    for m in re.finditer(r"(?m)^\s*([MEPR][0-9]+) · ", plain):
        found.add(f"Problem {m.group(1)}")
    for m in re.finditer(r"(?m)^\s*(A[0-9]) \(", plain):
        found.add(f"Assumption {m.group(1)}")
    blocks[lid] = found
pat = re.compile(r"\b(Definition|Theorem|Proposition|Corollary|Assumption|Remark|Example|Problem) ([A-Z]?[0-9]+(?:\.[0-9]+)?)\b")
bad = 0
for c in cards:
    text = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    labs = sorted(set(f"{a} {b}" for a, b in pat.findall(text)))
    own = blocks[c["lesson"]]
    missing = [l for l in labs if l not in own]
    flag = "" if not missing else "  <-- not a block of " + c["lesson"]
    if missing:
        bad += 1
    print(f"{c['id']} {c['lesson']} {labs}{flag}")
print("cards naming a label absent from their own lesson:", bad)
for lid in sorted(blocks):
    print(lid, sorted(blocks[lid]))
