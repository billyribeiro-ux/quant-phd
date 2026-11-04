"""Round-3 check: each page's data-run code equals its twin, and each expected block equals the twin's printed stdout.

Stdout is produced by running the twin with python -I -W error in a scratch copy of its directory (no file reads).
"""
import html
import re
import subprocess
import sys
import tempfile
import shutil
import os

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE3-LX1-a/"
PY = ROOT + ".venv/bin/python"
pairs = [("course/modules/LX/LX1/L01.html", "tests/labs/LX1/lab-LX1-L01-1.py", "lab-LX1-L01-1"),
         ("course/modules/LX/LX1/L02.html", "tests/labs/LX1/lab-LX1-L02-1.py", "lab-LX1-L02-1")]
ok = True
for page, twin, lab_id in pairs:
    t = open(ROOT + page, encoding="utf-8").read()
    sec = re.search(r'<section class="lab" id="%s".*?</section>' % lab_id, t, re.S).group(0)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin_src = open(ROOT + twin, encoding="utf-8").read()
    same_code = code.rstrip("\n") == twin_src.rstrip("\n")
    print(lab_id, "page code == twin:", same_code, "| len", len(code), len(twin_src))
    ok &= same_code
    d = tempfile.mkdtemp(prefix="lx1r3_")
    shutil.copy(ROOT + twin, os.path.join(d, "twin.py"))
    r = subprocess.run([PY, "-I", "-W", "error", os.path.join(d, "twin.py")], capture_output=True, text=True, cwd=d)
    print("  exit", r.returncode, "stderr bytes", len(r.stderr.encode()))
    same_out = r.stdout.rstrip("\n") == expected.rstrip("\n")
    print("  expected block == twin stdout:", same_out, "| stdout lines", len(r.stdout.splitlines()), "expected lines", len(expected.splitlines()))
    ok &= same_out and r.returncode == 0 and not r.stderr
    shutil.rmtree(d)
    # data-files and data-runtime attributes
    print("  section attrs:", re.search(r'<section class="lab"[^>]*>', sec).group(0))
print("ALL OK" if ok else "MISMATCH")
