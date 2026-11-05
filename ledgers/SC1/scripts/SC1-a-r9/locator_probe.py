"""SC1 slice a, round 9: print the content at every file:line locator cited by the round-8 rows (first 110 chars).

Used to confirm that carried rows point at the content they claim. Run from the checkout root.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path.cwd()
FILE_RE = re.compile(r"((?:course/modules/SC/SC1/)?(?:index|L0[1-8]|project)\.html|lab-SC1-L0[1-3]-1\.py|lab-SC1-project-[1-3]\.py)")
prev = json.loads(Path("/Users/billyribeiro/.fanout/frags/E-SC1-a.round8.json").read_text(encoding="utf-8"))
seen: set[tuple[str, int]] = set()
for row in prev["rows"]:
    loc = row["location"]
    for clause in loc.split(";"):
        files = [(m.start(), m.group(1)) for m in FILE_RE.finditer(clause)]
        for m in re.finditer(r":(\d+)(?:\s*-\s*(\d+))?", clause):
            name = None
            for pos, fn in files:
                if pos < m.start():
                    name = fn
            if name is None and files:
                name = files[0][1]
            if name is None:
                continue
            path = ROOT / (name if name.startswith("course") or name.startswith("tests") else
                           ("course/modules/SC/SC1/" + name if name.endswith(".html") else "tests/labs/SC1/" + name))
            a = int(m.group(1))
            b = int(m.group(2) or a)
            for n in range(a, min(b, a + 1) + 1):
                if (str(path), n) in seen:
                    continue
                seen.add((str(path), n))
                lines = path.read_text(encoding="utf-8").split("\n")
                text = lines[n - 1].strip() if n - 1 < len(lines) else "<EOF>"
                print(f"{row['id'][:34]:34s} {path.name}:{n}: {text[:110]}")
