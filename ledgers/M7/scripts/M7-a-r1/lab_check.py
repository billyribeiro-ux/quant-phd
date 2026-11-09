"""M7-a round 1 witness: page code == twin, expected block == twin output, twin run under python -I -W error.

Usage: python3 -I ledgers/M7/scripts/M7-a-r1/lab_check.py <repo_root>
Prints one line per lab: id, code_equal, expected_equal, run exit code, stderr length.
"""
import html
import re
import subprocess
import sys
import os
import tempfile

root = sys.argv[1]
labs = [
    ("course/modules/M/M7/L01.html", "lab-M7-L01-1"),
    ("course/modules/M/M7/L02.html", "lab-M7-L02-1"),
    ("course/modules/M/M7/L03.html", "lab-M7-L03-1"),
]
for page, lab_id in labs:
    text = open(os.path.join(root, page), encoding="utf-8").read()
    m = re.search(r'<section class="lab" id="%s".*?</section>' % re.escape(lab_id), text, re.S)
    sec = m.group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin_path = os.path.join(root, "tests/labs/M7", lab_id + ".py")
    twin = open(twin_path, encoding="utf-8").read()
    code_equal = code.rstrip("\n") == twin.rstrip("\n")
    with tempfile.TemporaryDirectory() as work:
        r = subprocess.run(
            [sys.executable, "-I", "-W", "error", twin_path],
            capture_output=True, text=True, cwd=work, timeout=120,
            env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"},
        )
    expected_equal = expected.rstrip("\n") == r.stdout.rstrip("\n")
    print(f"{lab_id}: code_equal_twin={code_equal} expected_equal_output={expected_equal} exit={r.returncode} stderr_len={len(r.stderr)} lines={len(r.stdout.splitlines())}")
    if not expected_equal:
        import difflib
        for line in difflib.unified_diff(expected.rstrip("\n").splitlines(), r.stdout.rstrip("\n").splitlines(), "expected", "output", lineterm=""):
            print("   ", line)
