"""For each BK4 lab twin, check every output line of the twin (run under python -I -W error) occurs in its lesson page.

Usage: python3 -I ledgers/BK4/scripts/BK4-d-r1/lab_output_in_lesson.py <repo-root> <output-dir-with-twin-outs>
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
outdir = Path(sys.argv[2])
pairs = {"lab-BK4-L01-1": "L01", "lab-BK4-L02-1": "L02", "lab-BK4-L03-1": "L03", "lab-BK4-L04-1": "L04", "lab-BK4-L05-1": "L05"}
for twin, page in pairs.items():
    src = (root / f"tests/labs/BK4/{twin}.py")
    res = subprocess.run([sys.executable, "-I", "-W", "error", str(src)], capture_output=True, text=True)
    lines = [l for l in res.stdout.splitlines() if l.strip()]
    raw = (root / f"course/modules/BK/BK4/{page}.html").read_text(encoding="utf-8")
    body = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", raw)).split())
    missing = [l for l in lines if " ".join(l.split()) not in body]
    print(f"{twin}: exit={res.returncode} output_lines={len(lines)} lines_not_in_{page}={len(missing)}")
    for m in missing[:20]:
        print("   MISSING:", m)
