"""Check cards for L01-L03: duplicates across all of cards.json, and every cited block/problem/misconception exists in its lesson page."""
import collections
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M3/cards.json").read_text(encoding="utf-8"))
ids = collections.Counter(c["id"] for c in cards)
print("duplicate ids:", [k for k, v in ids.items() if v > 1])
norm = collections.Counter(re.sub(r"\W+", " ", c["front"].lower()).strip() for c in cards)
print("duplicate fronts (normalised):", [k for k, v in norm.items() if v > 1])
pages = {lid: (root / f"course/modules/M/M3/{lid}.html").read_text(encoding="utf-8") for lid in ["L01", "L02", "L03"]}
pat = re.compile(r"(Definition|Proposition|Lemma|Theorem|Corollary|Example|Remark) (\d+\.\d+)")
problems = []
for c in cards:
    if c["lesson"] not in pages:
        continue
    page = pages[c["lesson"]]
    text = c["front"] + " " + c["back"]
    for kind, num in pat.findall(text):
        if not re.search(rf"{kind} {re.escape(num)}\b", page):
            problems.append((c["id"], kind, num))
    for m in re.findall(r"Misconception (\d)", text):
        if "Misconception " + m not in page:
            problems.append((c["id"], "misconception", m))
    for m in re.findall(r"Problem ([A-Z]\d)", text):
        if f'<span class="problem-title">{m} ' not in page:
            problems.append((c["id"], "problem", m))
    for m in re.findall(r"Lesson (\d)", text):
        pass
print("unresolved citations:", problems)
print("slice cards checked:", sum(1 for c in cards if c["lesson"] in pages))
