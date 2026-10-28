"""Compare each E5 slice lab page with its twin and with a fresh run of the twin (run with python -I -W error)."""

import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PAIRS = [
    ("course/modules/E/E5/L07.html", "tests/labs/E5/lab-E5-L07-1.py"),
    ("course/modules/E/E5/L08.html", "tests/labs/E5/lab-E5-L08-1.py"),
]
for page, twin in PAIRS:
    text = (ROOT / page).read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', text, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1))
    twin_src = (ROOT / twin).read_text(encoding="utf-8")
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(ROOT / twin)], capture_output=True, text=True, check=False
    )
    print(f"{twin}: rc={run.returncode} code_equals_twin={code.strip() == twin_src.strip()}")
    print(f"  embedded_output_equals_run={expected.strip() == run.stdout.strip()}")
    if expected.strip() != run.stdout.strip():
        print("\n".join(difflib.unified_diff(expected.splitlines(), run.stdout.splitlines(), lineterm="")))
