"""Round-9 lab check for BK4-c: page code equals twin, twin runs alone under python -I -W error, expected block equals output.

Usage: python lab_twin_check_r9.py <repo_root>
"""

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/BK/BK4/project.html").read_text(encoding="utf-8")
labs = {"lab-BK4-project-1": "lab-BK4-project-1.py", "lab-BK4-project-2": "lab-BK4-project-2.py", "lab-BK4-project-3": "lab-BK4-project-3.py"}
ok = True
for lab_id, twin_name in labs.items():
    m = re.search(r'<section class="lab[^"]*" id="' + lab_id + r'".*?</section>', page, re.S)
    body = m.group(0)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1))
    twin = (root / "tests/labs/BK4" / twin_name).read_text(encoding="utf-8")
    twin_eq = code.strip() == twin.strip()
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / "tests/labs/BK4" / twin_name)],
                         capture_output=True, text=True, cwd="/tmp")
    out_eq = run.stdout.strip() == expected.strip()
    print(f"{lab_id}: page_code_equals_twin={twin_eq} exit={run.returncode} stderr_bytes={len(run.stderr)} expected_equals_output={out_eq}")
    if not out_eq:
        print("--- expected\n" + expected + "\n--- output\n" + run.stdout)
    if not (twin_eq and run.returncode == 0 and not run.stderr and out_eq):
        ok = False
    if not twin_eq:
        import difflib
        print("\n".join(difflib.unified_diff(twin.strip().splitlines(), code.strip().splitlines(), "twin", "page", lineterm="")))
print("ALL PASS" if ok else "FAIL")
