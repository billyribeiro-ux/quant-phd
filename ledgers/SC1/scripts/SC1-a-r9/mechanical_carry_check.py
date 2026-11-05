"""SC1 slice a, round 9: mechanical byte-identity check for carried rows.

Reads the round-8 fragment, parses each row's location for file:line tokens, and reports which rows cite a line that
changed between the round-8 pin (0dee921a) and the round-9 pin (c93dd52) in the slice files. A row that cites no changed
line is eligible for carrying; a row that cites one must be re-verified.

Run from the checkout root: .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r9/mechanical_carry_check.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
OLD = "0dee921a33dc1275ff9b1babc6c2fdf3daac62c3"
NEW = "c93dd526025c6dffd34c54cd2c89eb62a890f885"
SLICE_FILES = [
    "course/modules/SC/SC1/index.html",
    "course/modules/SC/SC1/L01.html",
    "course/modules/SC/SC1/L02.html",
    "course/modules/SC/SC1/L03.html",
    "tests/labs/SC1/lab-SC1-L01-1.py",
    "tests/labs/SC1/lab-SC1-L02-1.py",
    "tests/labs/SC1/lab-SC1-L03-1.py",
]
diff = subprocess.run(
    ["git", "-C", str(ROOT), "diff", "-U0", OLD, NEW, "--"] + SLICE_FILES, capture_output=True, text=True, check=True
).stdout
changed: dict[str, set[int]] = {}
current = ""
for line in diff.splitlines():
    if line.startswith("+++ b/"):
        current = line[6:]
    m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
    if m and current:
        start, count = int(m.group(1)), int(m.group(2) or 1)
        changed.setdefault(current, set()).update(range(start, start + max(count, 1)))
print("changed lines in slice files (new numbering):")
for f in sorted(changed):
    print(f"  {f}: {sorted(changed[f])}")

FILE_RE = re.compile(r"((?:course/modules/SC/SC1/)?(?:index|L0[1-8]|project)\.html|lab-SC1-L0[1-3]-1\.py)")
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-SC1-a.round8.json").read_text(encoding="utf-8"))


def cited(location: str) -> list[tuple[str, int, int]]:
    out: list[tuple[str, int, int]] = []
    for clause in location.split(";"):
        files = [(m.start(), m.group(1)) for m in FILE_RE.finditer(clause)]
        for m in re.finditer(r":(\d+)(?:\s*-\s*(\d+))?", clause):
            name = None
            for pos, fname in files:
                if pos < m.start():
                    name = fname
            if name is None and files:
                name = files[0][1]
            if name is None:
                continue
            a = int(m.group(1))
            b = int(m.group(2) or a)
            out.append((name, a, b))
    return out


def hits(location: str) -> list[tuple[str, int, int]]:
    result = []
    for name, a, b in cited(location):
        for full, lines in changed.items():
            if full.split("/")[-1] == name.split("/")[-1] and any(a <= n <= b for n in lines):
                result.append((name, a, b))
    return result


for row in prev["rows"]:
    h = hits(row["location"])
    print(f"{row['id']:42s} {row['status']:4s} blocked={bool(h)} {h if h else ''}")
