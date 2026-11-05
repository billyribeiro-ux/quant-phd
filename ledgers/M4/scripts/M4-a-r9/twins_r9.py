"""Round 9 slice a: page code == twin, twin runs alone under python -I -W error, expected block == stdout.

Run: .venv/bin/python -I ledgers/M4/scripts/M4-a-r9/twins_r9.py <checkout-root>
Writes one line per lab. Exit 1 on any mismatch.
"""

import html
import os
import re
import subprocess
import sys
import tempfile

root = os.path.abspath(sys.argv[1])
fail = False
for lesson in ("L01", "L02", "L03", "L04"):
    page_path = os.path.join(root, "course", "modules", "M", "M4", f"{lesson}.html")
    text = open(page_path, encoding="utf-8").read()
    m_code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    m_exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    code = html.unescape(m_code.group(1))
    expected = html.unescape(m_exp.group(1))
    twin_path = os.path.join(root, "tests", "labs", "M4", f"lab-M4-{lesson}-1.py")
    twin = open(twin_path, encoding="utf-8").read()
    code_eq = code.rstrip("\n") == twin.rstrip("\n")
    with tempfile.TemporaryDirectory() as scratch:
        proc = subprocess.run(
            [sys.executable, "-I", "-W", "error", twin_path],
            cwd=scratch, capture_output=True, text=True, timeout=60,
        )
    out_eq = proc.stdout.rstrip("\n") == expected.rstrip("\n")
    ok = code_eq and out_eq and proc.returncode == 0 and proc.stderr == ""
    fail = fail or not ok
    print(f"{lesson}: exit={proc.returncode} stdout_lines={len(proc.stdout.splitlines())} stderr_len={len(proc.stderr)} "
          f"code_equals_twin={code_eq} expected_equals_stdout={out_eq} ok={ok}")
    if not out_eq:
        print("  expected:", expected.splitlines()[:3], "...")
        print("  stdout:", proc.stdout.splitlines()[:3], "...")
sys.exit(1 if fail else 0)
