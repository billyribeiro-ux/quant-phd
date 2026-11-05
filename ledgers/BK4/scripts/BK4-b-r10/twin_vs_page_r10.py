"""Round 10 check for BK4 slice b: page code block equals lab twin; page expected block equals twin stdout.

Run as: python3 -I -W error ledgers/BK4/scripts/BK4-b-r10/twin_vs_page_r10.py  (from the checkout root).
Twins are executed from a scratch directory, never from the checkout, so no twin imports a checkout module.
"""

import html
import os
import re
import subprocess
import sys

ROOT = os.getcwd()
SCRATCH = "/tmp/bk4b_r10_scratch"
PAIRS = [
    ("L04", "lab-BK4-L04-1"),
    ("L05", "lab-BK4-L05-1"),
]
ok = True
os.makedirs(SCRATCH, exist_ok=True)
for page, lab in PAIRS:
    with open(os.path.join(ROOT, f"course/modules/BK/BK4/{page}.html"), encoding="utf-8") as fh:
        page_html = fh.read()
    section = re.search(r'<section class="lab" id="%s".*?</section>' % lab, page_html, re.S).group(0)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', section, re.S).group(1)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section, re.S).group(1)
    code = html.unescape(code)
    expected = html.unescape(expected)
    twin_path = os.path.join(ROOT, f"tests/labs/BK4/{lab}.py")
    with open(twin_path, encoding="utf-8") as fh:
        twin = fh.read()
    same_code = code.rstrip() == twin.rstrip()
    scratch_twin = os.path.join(SCRATCH, f"{lab}-r10.py")
    with open(scratch_twin, "w", encoding="utf-8") as fh:
        fh.write(twin)
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", scratch_twin], capture_output=True, text=True, cwd=SCRATCH
    )
    same_out = run.stdout.rstrip() == expected.rstrip()
    print(f"{page} {lab}: page code == twin: {same_code}; twin exit {run.returncode}; "
          f"stderr bytes {len(run.stderr.encode())}; page expected == twin stdout: {same_out}")
    if not (same_code and run.returncode == 0 and not run.stderr and same_out):
        ok = False
    if not same_code:
        print("  first differing line of code:")
        a, b = code.rstrip().splitlines(), twin.rstrip().splitlines()
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                print(f"  line {i+1}: page={x!r} twin={y!r}")
                break
        else:
            print(f"  length page={len(a)} twin={len(b)}")
    if not same_out:
        a, b = expected.rstrip().splitlines(), run.stdout.rstrip().splitlines()
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                print(f"  line {i+1}: page={x!r} stdout={y!r}")
                break
        else:
            print(f"  length page={len(a)} stdout={len(b)}")
print("RESULT:", "PASS" if ok else "FAIL")
