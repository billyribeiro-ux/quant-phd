"""Compare each L09-L12 lab twin's printed output (python -I -W error run) with the expected block embedded in its page.

Run from the checkout root: .venv/bin/python -I ledgers/M6/scripts/M6-c-r1/compare_outputs_c.py
"""

import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PYTHON = str(ROOT / ".venv" / "bin" / "python")
ok = True
for page in ("L09", "L10", "L11", "L12"):
    html_text = (ROOT / "course/modules/M/M6" / f"{page}.html").read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', html_text, re.S).group(1))
    twin = (ROOT / "tests/labs/M6" / f"lab-M6-{page}-1.py").read_text(encoding="utf-8")
    expected = html.unescape(re.sub(r"<[^>]+>", "", re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', html_text, re.S).group(1)))
    run = subprocess.run([PYTHON, "-I", "-W", "error", str(ROOT / "tests/labs/M6" / f"lab-M6-{page}-1.py")],
                         capture_output=True, text=True, check=False)
    same_code = code.strip() == twin.strip()
    same_out = run.stdout.strip() == expected.strip()
    print(f"{page}: exit={run.returncode} page_code_equals_twin={same_code} output_equals_embedded={same_out}")
    if not same_out:
        ok = False
        print("\n".join(list(difflib.unified_diff(expected.strip().splitlines(), run.stdout.strip().splitlines(), lineterm=""))[:20]))
    ok = ok and run.returncode == 0 and same_code
sys.exit(0 if ok else 1)
