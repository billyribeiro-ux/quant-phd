"""Classify round-6 PASS rows for round 7: carry (cited lines byte-identical since pin 4bd8cb9) or re-verify.

Run from the checkout root: .venv/bin/python ledgers/E4/scripts/E4-b-r7/classify_prev_rows.py
Reads the round-6 fragment, the git diff between pins, and prints one line per row."""

import json
import re
import subprocess

OLD, NEW = "4bd8cb94", "06994db1"
PREV = "/Users/billyribeiro/.fanout/frags/E-E4-b.round6.json"
FILES = {
    "L04": "course/modules/E/E4/L04.html",
    "L05": "course/modules/E/E4/L05.html",
    "L06": "course/modules/E/E4/L06.html",
    "twin04": "tests/labs/E4/lab-E4-L04-1.py",
    "twin05": "tests/labs/E4/lab-E4-L05-1.py",
    "twin06": "tests/labs/E4/lab-E4-L06-1.py",
    "index": "course/modules/E/E4/index.html",
}


def lines_of(rev, path):
    out = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
    return out.split("\n")


def changed_lines(path):
    """1-based line numbers (new numbering) that differ between the two pins, from a unified diff."""
    d = subprocess.run(["git", "diff", "-U0", OLD, NEW, "--", path], capture_output=True, text=True, check=True).stdout
    res = set()
    for m in re.finditer(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", d, flags=re.M):
        start = int(m.group(3))
        cnt = int(m.group(4)) if m.group(4) is not None else 1
        res.update(range(start, start + cnt))
    return res


changed = {k: changed_lines(p) for k, p in FILES.items()}
prev = json.load(open(PREV))
for r in prev["rows"]:
    text = r["location"] + " " + r["evidence"]
    hits = set()
    whole = []
    for m in re.finditer(r"(L0[456]|index)\.html:(\d+)(?:-(\d+))?", text):
        key = m.group(1)
        a = int(m.group(2))
        b = int(m.group(3)) if m.group(3) else a
        ch = [x for x in range(a, b + 1) if x in changed[key]]
        if ch:
            hits.add(f"{key}:{ch}")
    for m in re.finditer(r"(L0[456]\.html)(?!:)", text):
        whole.append(m.group(1))
    for key in ("twin04", "twin05", "twin06"):
        if FILES[key].split("/")[-1] in text and changed[key]:
            hits.add(key)
    tag = "CHANGED" if hits else ("WHOLE-PAGE" if whole else "BYTE-IDENT")
    print(f"{tag:11s} {r['status']:4s} {r['id']:44s} hits={sorted(hits)} whole={sorted(set(whole))}")
