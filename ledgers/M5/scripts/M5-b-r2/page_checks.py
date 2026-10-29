"""Round-2 checks for M5 slice b (L05-L07): raw less-than scan, math spans, lab output presence.

Run: <checkout>/.venv/bin/python -I ledgers/M5/scripts/M5-b-r2/page_checks.py
"""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
PAGES = ["L05", "L06", "L07"]
LABS = {"L05": "tests/labs/M5/lab-M5-L05-1.py", "L06": "tests/labs/M5/lab-M5-L06-1.py", "L07": "tests/labs/M5/lab-M5-L07-1.py"}

for name in PAGES:
    text = (ROOT / f"course/modules/M/M5/{name}.html").read_text(encoding="utf-8")
    tag_hits = [m.start() for m in re.finditer(r"<([A-Za-z][A-Za-z0-9-]*)([^A-Za-z0-9\-\s/>])", text)]
    math_lt = [s for s in re.findall(r"\\\((.*?)\\\)", text, flags=re.S) if re.search(r"<[A-Za-z]", s)]
    print(f"{name}: raw tag-like '<letter' sites={len(tag_hits)} math spans with raw '<letter'={len(math_lt)}")
    out = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(ROOT / LABS[name])], capture_output=True, text=True, check=False
    ).stdout.splitlines()
    missing = [line for line in out if html.escape(line, quote=False) not in text and line not in text]
    print(f"{name}: lab rc-run lines={len(out)} lines missing from page={len(missing)}")
