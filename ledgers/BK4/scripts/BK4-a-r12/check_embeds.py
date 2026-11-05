"""Round 12 verifier check for BK4 slice a: twin vs page code, and expected block vs twin output.

Usage: python3 -I check_embeds.py <checkout_root>
Reads the three lesson pages and twins, runs each twin alone under python -I -W error from /tmp,
and compares (1) the page <code data-run> block with the twin file (trailing newline stripped), and
(2) the page <pre class="expected"> block with the twin stdout (trailing newline stripped).
"""

import html
import os
import re
import subprocess
import sys

root = sys.argv[1]
ok_all = True
for n in ("L01", "L02", "L03"):
    page = open(os.path.join(root, "course/modules/BK/BK4", f"{n}.html"), encoding="utf-8").read()
    twin_path = os.path.join(root, "tests/labs/BK4", f"lab-BK4-{n}-1.py")
    twin = open(twin_path, encoding="utf-8").read()
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code_text = html.unescape(code.group(1))
    exp_text = html.unescape(exp.group(1))
    twin_norm = twin.rstrip("\n")
    code_norm = code_text.rstrip("\n")
    code_eq = twin_norm == code_norm
    run = subprocess.run(
        ["python3", "-I", "-W", "error", twin_path],
        cwd="/tmp",
        capture_output=True,
        text=True,
    )
    out = run.stdout
    exp_eq = exp_text.rstrip("\n") == out.rstrip("\n")
    print(f"{n}: exit={run.returncode} page_code_equals_twin={code_eq} expected_equals_output={exp_eq}")
    if not code_eq:
        import difflib

        for line in list(difflib.unified_diff(twin_norm.splitlines(), code_norm.splitlines(), lineterm=""))[:20]:
            print("  code-diff:", line)
    if not exp_eq:
        import difflib

        for line in list(difflib.unified_diff(out.rstrip("\n").splitlines(), exp_text.rstrip("\n").splitlines(), lineterm=""))[:20]:
            print("  exp-diff:", line)
    ok_all = ok_all and code_eq and exp_eq and run.returncode == 0
print("ALL_OK" if ok_all else "MISMATCH")
