"""Run each project lab twin under python -I -W error and compare stdout with the page's expected block (verifier round 1)."""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
page = (ROOT / "course/modules/M/M4/project.html").read_text(encoding="utf-8")
for lab in ("lab-M4-project-1", "lab-M4-project-2", "lab-M4-project-3"):
    m = re.search(rf'<section class="lab[^"]*" id="{lab}".*?<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(m.group(1)).strip()
    twin = ROOT / "tests/labs/M4" / f"{lab}.py"
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd="/tmp")
    got = run.stdout.strip()
    print(lab, "rc", run.returncode, "match" if got == expected else "MISMATCH")
    if got != expected:
        print("--- got\n" + got + "\n--- expected\n" + expected)
    code = html.unescape(re.search(rf'<section class="lab[^"]*" id="{lab}".*?<code[^>]*data-run>(.*?)</code>', page, re.S).group(1))
    print("  page code equals twin:", code.strip() == twin.read_text(encoding="utf-8").strip())
