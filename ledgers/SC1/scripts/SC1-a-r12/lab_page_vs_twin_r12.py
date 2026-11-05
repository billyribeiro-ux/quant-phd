"""Compares each slice-a lab's page code and expected block with its twin and with the twin's observed stdout.

Usage: python -I lab_page_vs_twin_r12.py <checkout>
Reads course/modules/SC/SC1/L01..L03.html and tests/labs/SC1/lab-SC1-L0n-1.py; runs each twin with the same
interpreter under -I -W error from an empty scratch cwd; prints PASS/FAIL per lab.
"""
import html
import os
import re
import subprocess
import sys
import tempfile

root = sys.argv[1]
exe = sys.executable
ok_all = True
for n in ("01", "02", "03"):
    page = open(os.path.join(root, f"course/modules/SC/SC1/L{n}.html"), encoding="utf-8").read()
    twin_path = os.path.join(root, f"tests/labs/SC1/lab-SC1-L{n}-1.py")
    twin = open(twin_path, encoding="utf-8").read()
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code_txt = html.unescape(code.group(1))
    exp_txt = html.unescape(expected.group(1))
    with tempfile.TemporaryDirectory() as scratch:
        proc = subprocess.run([exe, "-I", "-W", "error", twin_path], cwd=scratch, capture_output=True, text=True)
    out = proc.stdout
    code_eq = code_txt.rstrip("\n") == twin.rstrip("\n")
    exp_eq = exp_txt.rstrip("\n") == out.rstrip("\n")
    ok = code_eq and exp_eq and proc.returncode == 0 and proc.stderr == ""
    ok_all = ok_all and ok
    print(f"L{n}: page_code_equals_twin={code_eq} expected_equals_stdout={exp_eq} exit={proc.returncode} "
          f"stderr_bytes={len(proc.stderr)} -> {'PASS' if ok else 'FAIL'}")
    if not exp_eq:
        import difflib
        print("\n".join(difflib.unified_diff(exp_txt.splitlines(), out.splitlines(), lineterm="")))
print("ALL PASS" if ok_all else "SOME FAIL")
