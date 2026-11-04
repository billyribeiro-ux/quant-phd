"""BK4-b round 4: run each lab twin alone under python -I -W error, compare with its page.

Usage: python -I ledgers/BK4/scripts/BK4-b-r4/twin_and_page.py <repo-root> <venv-python>
"""

import html
import os
import re
import shutil
import subprocess
import sys
import tempfile

root = os.path.abspath(sys.argv[1])
py = sys.argv[2]
pages = {"L04": "course/modules/BK/BK4/L04.html", "L05": "course/modules/BK/BK4/L05.html"}
ok = True
for lab, page in pages.items():
    twin_path = os.path.join(root, "tests/labs/BK4", f"lab-BK4-{lab}-1.py")
    with open(twin_path, encoding="utf-8") as fh:
        twin = fh.read()
    with open(os.path.join(root, page), encoding="utf-8") as fh:
        text = fh.read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    page_code = html.unescape(code.group(1))
    page_expected = html.unescape(expected.group(1))
    tmp = tempfile.mkdtemp(prefix=f"bk4b-r4-{lab}-")
    shutil.copy(twin_path, os.path.join(tmp, os.path.basename(twin_path)))
    proc = subprocess.run(
        [py, "-I", "-W", "error", os.path.basename(twin_path)],
        cwd=tmp,
        capture_output=True,
        text=True,
        timeout=60,
    )
    code_eq = page_code.rstrip() == twin.rstrip()
    exp_eq = page_expected.rstrip() == proc.stdout.rstrip()
    print(f"{lab}: exit={proc.returncode} stderr_bytes={len(proc.stderr)} page_code==twin {code_eq} "
          f"page_expected==stdout {exp_eq} stdout_lines={proc.stdout.count(chr(10))}")
    ok = ok and proc.returncode == 0 and code_eq and exp_eq
    out_path = os.path.join("/tmp/bk4b-r4", f"{lab}-stdout.txt")
    os.makedirs("/tmp/bk4b-r4", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(proc.stdout)
print("ALL OK" if ok else "MISMATCH")
