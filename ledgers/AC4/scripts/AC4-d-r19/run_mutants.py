"""Run every AC4-d lab mutant against the current twin expectations and report killed or survived.

A mutant is killed when it exits non-zero or its printed output differs from the embedded expected block
of its page. Lab mutants are demonstrations, so a survivor is recorded, not a grader finding (architect ruling).
Usage: python -I run_mutants.py <checkout>.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
expected: dict[str, str] = {}
for page in ("L07", "L08"):
    text = (root / f"course/modules/AC/AC4/{page}.html").read_text(encoding="utf-8")
    expected[page] = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1)).strip()

mut_dirs = [root / "ledgers/AC4/mutants/AC4-d-r17", root / "ledgers/AC4/mutants/AC4-d-r18"]
for d in mut_dirs:
    for f in sorted(d.glob("*.py")):
        page = "L08" if "L08" in f.name else "L07"
        proc = subprocess.run([sys.executable, "-I", "-W", "error", str(f)], capture_output=True, text=True, timeout=60)
        out = proc.stdout.strip()
        if proc.returncode != 0:
            verdict = f"KILLED rc={proc.returncode} ({proc.stderr.strip().splitlines()[-1][:90] if proc.stderr.strip() else ''})"
        elif out != expected[page]:
            verdict = "KILLED output-differs"
        else:
            verdict = "SURVIVED (rc 0, output identical to expected)"
        print(f"{f.parent.name}/{f.name}: {verdict}")
