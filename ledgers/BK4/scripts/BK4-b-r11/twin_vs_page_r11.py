"""Compare each BK4 slice-b lab twin with the page code block and the page expected block.

Usage: python -I -W error twin_vs_page_r11.py <repo_root> <scratch_dir>
Prints one line per check and a final RESULT line.
"""

import html
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
scratch = pathlib.Path(sys.argv[2])
ok = True
pairs = [("L04", "course/modules/BK/BK4/L04.html", "tests/labs/BK4/lab-BK4-L04-1.py"),
         ("L05", "course/modules/BK/BK4/L05.html", "tests/labs/BK4/lab-BK4-L05-1.py")]
for name, page, twin in pairs:
    text = (root / page).read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    twin_text = (root / twin).read_text(encoding="utf-8")
    page_code = html.unescape(code.group(1))
    page_expected = html.unescape(expected.group(1))
    same_code = page_code.rstrip("\n") == twin_text.rstrip("\n")
    print(f"{name} page code == twin: {same_code} (page {len(page_code)} chars, twin {len(twin_text)} chars)")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / twin)], cwd=scratch,
                         capture_output=True, text=True)
    print(f"{name} twin exit {run.returncode}, stderr bytes {len(run.stderr.encode())}")
    same_out = run.stdout.rstrip("\n") == page_expected.rstrip("\n")
    print(f"{name} page expected == twin stdout: {same_out} (stdout lines {len(run.stdout.splitlines())})")
    (scratch / f"{name}_stdout.txt").write_text(run.stdout, encoding="utf-8")
    ok = ok and same_code and same_out and run.returncode == 0 and not run.stderr
print("RESULT:", "PASS" if ok else "FAIL")
