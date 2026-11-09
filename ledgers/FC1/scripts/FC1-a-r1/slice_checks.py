"""Round-1 FC1-a checks: card grade/basis consistency, key-results grades, why-it-matters word counts, structure counts,
process words and banned phrases on the hub and L01-L03 pages and twins.

Run from the checkout root: .venv/bin/python -I ledgers/FC1/scripts/FC1-a-r1/slice_checks.py
"""

from __future__ import annotations

import html
import json
import pathlib
import re
from collections import Counter

ROOT = pathlib.Path(".").resolve()
UNIT = ROOT / "course/modules/FC/FC1"
LESSONS = ["L01", "L02", "L03"]

cards = json.loads((UNIT / "cards.json").read_text(encoding="utf-8"))
mine = [c for c in cards if c["lesson"] in LESSONS]
print("cards L01-L03:", len(mine), Counter(c["lesson"] for c in mine))
print("cards L01-L03 by (grade, basis):", Counter((c.get("grade"), bool(c.get("basis"))) for c in mine))
print("T-graded cards whose basis names a lab (ruling 13 requires C naming the lab):")
for c in mine:
    if c.get("grade") == "T" and c.get("basis") and "Lab" in c["basis"]:
        print("   ", c["id"], "|", c["basis"], "|", c["front"][:90])
print("C-graded cards with a lab or hand basis:", [c["id"] for c in mine if c.get("grade") == "C"])
dupes = Counter(c["front"] for c in cards)
print("duplicate fronts across unit:", [f for f, n in dupes.items() if n > 1])

for page in ["index"] + LESSONS:
    t = (UNIT / f"{page}.html").read_text(encoding="utf-8")
    if page != "index":
        kr = re.search(r'<table class="key-results">.*?</table>', t, re.S)
        rows = re.findall(r"<tr><td>(.*?)</td><td><span class=\"grade\" data-grade=\"(\w)\">\w</span></td><td>(.*?)</td></tr>", kr.group(0), re.S)
        for text, grade, source in rows:
            if re.search(r"Lab \d", source) and grade == "T":
                print(page, "key-results T row with lab basis:", re.sub(r"<[^>]+>", "", text)[:90], "|", re.sub(r"<[^>]+>", "", source)[:90])
        wim = re.search(r'<p class="why-it-matters">(.*?)</p>', t, re.S)
        prose = html.unescape(re.sub(r"<[^>]+>", " ", wim.group(1)))
        print(page, "why-it-matters words:", len(prose.split()))
        print(page, "misconceptions:", t.count('class="misconception"'), "| solutions:", t.count('<details class="solution"'),
              "| quiz items:", t.count('class="item"'), "| labs:", t.count('class="lab"'))
    text = html.unescape(re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", t, flags=re.S))
    text = re.sub(r"\s+", " ", text)
    for pat in [r"\bbuilders?\b", r"\bverifiers?\b", r"\bplanner\b", r"\barchitect\b", r"\bledger\b", r"\bTODO\b", r"\bTBD\b",
                r"lorem", r"for brevity", r"details omitted", r"beyond the scope", r"left as an exercise", r"you can add more",
                r"studies show", r"experts agree", r"well known", r"\bobviously\b", r"\bclearly\b",
                r"it is important to note", r"it can be shown", r"checked directly"]:
        if re.search(pat, text, re.I):
            print(page, "BANNED/PROCESS hit:", pat)
    if "…" in text:
        print(page, "ellipsis character present")
for f in ["tests/labs/FC1/lab-FC1-L01-1.py", "tests/labs/FC1/lab-FC1-L02-1.py", "tests/labs/FC1/lab-FC1-L03-1.py"]:
    t = (ROOT / f).read_text(encoding="utf-8")
    for pat in [r"\bbuilders?\b", r"\bverifiers?\b", r"\bplanner\b", r"\bround\b", r"\bTODO\b", r"\bTBD\b"]:
        if re.search(pat, t, re.I):
            print(f, "PROCESS hit:", pat)
print("slice_checks done")
