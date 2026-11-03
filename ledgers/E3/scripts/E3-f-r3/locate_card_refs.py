"""Locate every lesson locator cited on an E3 L01-L04 card (Definition, Proposition, Lemma, Theorem, Remark, Example,
Problem, Assumption, Lab, section) in its lesson HTML, and print file:line for the first block-title occurrence.

Used by make_fragment.py to put a file:line citation on every card row. Run with -I.
Usage: locate_card_refs.py <cards.json> <lesson_dir> [--json out.json]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

cards_path, lesson_dir = Path(sys.argv[1]), Path(sys.argv[2])
out_json = Path(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[3] == "--json" else None
cards = json.loads(cards_path.read_text(encoding="utf-8"))
lessons = {p: (lesson_dir / f"{p}.html").read_text(encoding="utf-8").split("\n") for p in ("L01", "L02", "L03", "L04")}

REF = re.compile(
    r"\b(Definitions?|Propositions?|Lemma|Theorem|Remark|Example|Problem|Assumptions?|Corollary|Lab|section)\s+"
    r"((?:\d+\.\d+|[A-Z]\d+|\d+)(?:\([a-z]\))?)"
)
TITLE = {
    "Definition": "Definition",
    "Proposition": "Proposition",
    "Lemma": "Lemma",
    "Theorem": "Theorem",
    "Remark": "Remark",
    "Example": "Example",
    "Corollary": "Corollary",
    "Assumption": "Assumption",
    "Assumptions": "Assumption",
}


def find_line(lesson: str, kind: str, num: str) -> int | None:
    lines = lessons[lesson]
    if kind in TITLE:
        pat = re.compile(rf"block-title[^>]*>\s*(?:<span[^>]*>)?\s*{TITLE[kind]}\s+{re.escape(num)}\b")
        for i, line in enumerate(lines, 1):
            if pat.search(line):
                return i
        return None
    if kind == "Problem":
        pat = re.compile(rf'class="problem-title">\s*{re.escape(num)}\s')
        for i, line in enumerate(lines, 1):
            if pat.search(line) or (f'id="{num}"' in line):
                return i
        return None
    if kind == "section":
        pat = re.compile(rf'<h2 id="s{re.escape(num)}">')
        for i, line in enumerate(lines, 1):
            if pat.search(line):
                return i
        return None
    if kind == "Lab":
        for i, line in enumerate(lines, 1):
            if 'class="lab"' in line:
                return i
        return None
    return None


result = {}
for c in cards:
    if c["lesson"] not in lessons:
        continue
    refs = []
    for kind, num in REF.findall(f"{c['back']} {c['front']}"):
        line = find_line(c["lesson"], kind, num)
        refs.append({"ref": f"{kind} {num}", "line": line})
    result[c["id"]] = {"lesson": c["lesson"], "refs": refs}
    shown = ", ".join(f"{r['ref']}={'L' + c['lesson'][1:] + '.html:' + str(r['line']) if r['line'] else 'NOT FOUND'}" for r in refs)
    print(f"{c['id']} {c['lesson']}: {shown}")

if out_json:
    out_json.write_text(json.dumps(result, indent=1), encoding="utf-8")
