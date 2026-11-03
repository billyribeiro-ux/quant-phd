"""Verifier r4: page code equals twin; page expected block equals twin stdout (twin run alone, python -I -W error, empty cwd)."""
import hashlib
import html
import os
import re
import subprocess
import sys
import tempfile

ROOT = sys.argv[1]
PAGES = {"L07": "lab-M3-L07-1", "L08": "lab-M3-L08-1", "L09": "lab-M3-L09-1"}
for page, lab in PAGES.items():
    text = open(os.path.join(ROOT, f"course/modules/M/M3/{page}.html"), encoding="utf-8").read()
    twin_path = os.path.join(ROOT, f"tests/labs/M3/{lab}.py")
    twin = open(twin_path, encoding="utf-8").read()
    sha = hashlib.sha256(twin.encode()).hexdigest()[:16]
    m = re.search(r'<section class="lab" id="lab-M3-%s-1".*?</section>' % page, text, re.S)
    assert m, page
    sec = m.group(0)
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', sec, re.S)
    code_txt = html.unescape(code.group(1))
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S)
    exp_txt = html.unescape(exp.group(1))
    print(page, "twin sha256", sha, "| page code == twin (rstrip):", code_txt.rstrip() == twin.rstrip(),
          "| len page", len(code_txt), "len twin", len(twin))
    with tempfile.TemporaryDirectory(prefix=f"v4-{page}-", dir="/private/tmp") as scratch:
        r = subprocess.run([sys.executable, "-I", "-W", "error", twin_path], cwd=scratch, capture_output=True, text=True)
        print(page, "twin alone exit", r.returncode, "stderr bytes", len(r.stderr.encode()))
        print(page, "expected == stdout (rstrip):", exp_txt.rstrip() == r.stdout.rstrip())
        print("---- STDOUT", page)
        print(r.stdout, end="")
        print("---- END", page)
