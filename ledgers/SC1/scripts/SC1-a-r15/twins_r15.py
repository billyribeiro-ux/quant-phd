"""Round-15 twin check for SC1 lab pages L01-L03 (slice a).

For each page: (1) the data-run code block, HTML-unescaped and stripped, equals the twin file;
(2) the twin runs alone under python -I -W error from an empty directory, rc 0, empty stderr;
(3) the expected block (HTML-unescaped) equals the twin's stdout line by line.
Usage: python3 -I twins_r15.py <checkout-root>
"""
import html
import os
import re
import subprocess
import sys
import tempfile

root = sys.argv[1]
pairs = {
    "L01": ("course/modules/SC/SC1/L01.html", "tests/labs/SC1/lab-SC1-L01-1.py"),
    "L02": ("course/modules/SC/SC1/L02.html", "tests/labs/SC1/lab-SC1-L02-1.py"),
    "L03": ("course/modules/SC/SC1/L03.html", "tests/labs/SC1/lab-SC1-L03-1.py"),
}
py = os.path.join(root, ".venv/bin/python")
ok_all = True
for lid, (page_rel, twin_rel) in pairs.items():
    page = open(os.path.join(root, page_rel), encoding="utf-8").read()
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = open(os.path.join(root, twin_rel), encoding="utf-8").read()
    same_code = code.strip() == twin.strip()
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1)).strip()
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([py, "-I", "-W", "error", os.path.join(root, twin_rel)], cwd=d,
                           capture_output=True, text=True)
    out = r.stdout.strip()
    same_out = out.splitlines() == expected.splitlines()
    print(f"{lid}: page code == twin: {same_code}; rc={r.returncode}; stderr empty: {r.stderr == ''}; "
          f"expected == stdout: {same_out}; lines={len(out.splitlines())}")
    if not (same_code and r.returncode == 0 and r.stderr == "" and same_out):
        ok_all = False
        print("DIFF expected:\n" + expected + "\nDIFF stdout:\n" + out + "\nstderr:\n" + r.stderr)
print("ALL TWINS OK" if ok_all else "TWIN FAILURE")
