"""Round 5 FC2-d: extract project lab code and expected blocks from project.html, compare to twins, run twins alone."""
import html
import re
import subprocess
import sys
import tempfile
import shutil
import os

ROOT = "/Users/billyribeiro/.fanout/wt/verifyC5-FC2-d"
page = open(f"{ROOT}/course/modules/FC/FC2/project.html", encoding="utf-8").read()
sections = re.findall(r'<section class="lab[^"]*" id="(lab-FC2-project-\d)".*?</section>', page, flags=re.S)
blocks = re.finditer(r'<section class="lab[^"]*" id="(lab-FC2-project-\d)".*?</section>', page, flags=re.S)
for m in blocks:
    lab = m.group(1)
    body = m.group(0)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, flags=re.S).group(1)
    code = html.unescape(code)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, flags=re.S).group(1)
    exp = html.unescape(exp)
    twin = open(f"{ROOT}/tests/labs/FC2/{lab}.py", encoding="utf-8").read()
    same = code.rstrip("\n") == twin.rstrip("\n")
    w = tempfile.mkdtemp(prefix="fc2d-r5-lab.")
    shutil.copy(f"{ROOT}/tests/labs/FC2/{lab}.py", os.path.join(w, "lab.py"))
    r = subprocess.run([f"{ROOT}/.venv/bin/python", "-I", "-W", "error", os.path.join(w, "lab.py")],
                       capture_output=True, text=True, cwd=w, timeout=60)
    shutil.rmtree(w)
    out_eq = r.stdout.rstrip(chr(10)) == exp.rstrip(chr(10))
    print(f"{lab}: page_code_eq_twin={same} rc={r.returncode} stderr={r.stderr!r} stdout_eq_expected={out_eq}")
    if not out_eq:
        print("EXPECTED:\n" + exp + "\nGOT:\n" + r.stdout)

# Lab 2: every page line equals the twin line or contains a blank
m = re.search(r'<section class="lab completion" id="lab-FC2-project-2".*?</section>', page, flags=re.S)
pc = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', m.group(0), flags=re.S).group(1)).splitlines()
tw = open(f'{ROOT}/tests/labs/FC2/lab-FC2-project-2.py', encoding='utf-8').read().splitlines()
print('lab2 line counts', len(pc), len(tw))
bad = [(i, a, b) for i, (a, b) in enumerate(zip(pc, tw)) if a != b and '___' not in a]
print('lab2 non-blank mismatches:', bad)
print('lab2 blank lines:', [a.strip() for a in pc if '___' in a])
