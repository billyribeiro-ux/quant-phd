"""Checks each project lab: page code vs twin (differing lines), twin run alone under python -I -W error in CWD (argv[3]), expected block vs stdout."""
import difflib
import html
import re
import subprocess
import sys

PAGE, TWIN_DIR, CWD = sys.argv[1], sys.argv[2], sys.argv[3]
src = open(PAGE, encoding="utf-8").read()
pattern = r'<section class="lab[^"]*" id="(lab-LX1-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>'
for m in re.finditer(pattern, src, re.S):
    lab_id = m.group(1)
    code = html.unescape(m.group(2))
    expected = html.unescape(m.group(3))
    twin_path = f"{TWIN_DIR}/{lab_id}.py"
    twin = open(twin_path, encoding="utf-8").read()
    code_lines = code.rstrip("\n").split("\n")
    twin_lines = twin.rstrip("\n").split("\n")
    diffs = [d for d in difflib.ndiff(twin_lines, code_lines) if d[:1] in "+-"]
    print(f"== {lab_id}: page code lines={len(code_lines)} twin lines={len(twin_lines)}; differing lines={len(diffs)}")
    for d in diffs:
        print("   ", d)
    r = subprocess.run([sys.executable, "-I", "-W", "error", twin_path], capture_output=True, text=True, cwd=CWD)
    print(f"   twin rc={r.returncode} stderr={r.stderr!r}")
    out_ok = r.stdout.rstrip() == expected.rstrip()
    print(f"   expected block equals stdout (trailing whitespace ignored): {out_ok}")
    if not out_ok:
        for d in difflib.unified_diff(expected.split("\n"), r.stdout.split("\n"), "expected", "stdout", lineterm=""):
            print("   ", d)
