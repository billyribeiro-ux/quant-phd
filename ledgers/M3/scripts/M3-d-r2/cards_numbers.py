"""For every M3 card, check each numbered label it cites ('Definition 1.2a', 'Theorem 2.2', ...) appears in the card's own lesson page.

Labels cited with 'Lesson N' or 'Lesson N, <label>' are checked in lesson N instead. Prints every citation and its status.
"""
import json
import re
import sys

root = sys.argv[1]
M3 = f"{root}/course/modules/M/M3"
cards = json.load(open(f"{M3}/cards.json", encoding="utf-8"))
pages = {}
for n in range(1, 10):
    pages[f"L{n:02d}"] = open(f"{M3}/L{n:02d}.html", encoding="utf-8").read()
label = re.compile(r"\b(Definition|Proposition|Theorem|Lemma|Remark|Fact|Problem|Misconception|Example|Assumption)\s+(\d+\.\d+[a-z]?)")
problems = 0
checked = 0
for c in cards:
    text = c["front"] + " " + c["back"]
    for kind, num in label.findall(text):
        checked += 1
        ok = f"{kind} {num}" in pages[c["lesson"]]
        if not ok:
            # the citation may name another lesson, e.g. 'Lesson 4, Theorem 2.3' or 'Theorem 2.3 of Lesson 4'
            m = re.search(r"Lesson (\d)", text)
            other = f"L0{m.group(1)}" if m else None
            ok = bool(other and f"{kind} {num}" in pages.get(other, ""))
            where = other if ok else None
        else:
            where = c["lesson"]
        if not ok:
            problems += 1
            print("MISSING", c["id"], c["lesson"], f"{kind} {num}", "|", text[:120])
        else:
            print("ok", c["id"], f"{kind} {num}", "in", where)
print("citations checked:", checked, "missing:", problems)
