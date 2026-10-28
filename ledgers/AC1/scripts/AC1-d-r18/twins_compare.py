"""Compares each project lab's expected block on project.html with the twin's run output (python -I -W error).
Usage: python3 -I twins_compare.py <checkout>
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
src = (root / "course/modules/AC/AC1/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    lab = f"lab-AC1-project-{n}"
    m = re.search(rf'id="{lab}".*?<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected = html.unescape(m.group(1)).rstrip("\n")
    run = subprocess.run(
        [str(root / ".venv/bin/python"), "-I", "-W", "error", str(root / f"tests/labs/AC1/{lab}.py")],
        capture_output=True, text=True, check=False,
    )
    got = run.stdout.rstrip("\n")
    print(lab, "exit", run.returncode, "identical" if got == expected else "DIFFERENT", "lines", len(got.splitlines()))
