"""LX2 slice c, round 1: compare each project lab block on project.html with its twin and with the twin's output.

Run as: python3 -I -W error ledgers/LX2/scripts/LX2-c-r1/page_vs_twin.py
Reads course/modules/LX/LX2/project.html and tests/labs/LX2/lab-LX2-project-N.py, runs each twin under the same
interpreter, and compares: (a) every page code line equals the twin line, or the page line contains a blank (___);
(b) the page 'expected' block equals the twin's stdout exactly.
"""

import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
page = (ROOT / "course/modules/LX/LX2/project.html").read_text(encoding="utf-8")
ok = True
for n in (1, 2, 3):
    lab_id = f"lab-LX2-project-{n}"
    m = re.search(rf'<section class="lab[^"]*" id="{lab_id}".*?<pre><code[^>]*data-run>(.*?)</code></pre>', page, re.S)
    e = re.search(rf'<section class="lab[^"]*" id="{lab_id}".*?<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(e.group(1))
    twin = (ROOT / f"tests/labs/LX2/{lab_id}.py").read_text(encoding="utf-8")
    page_lines = code.rstrip("\n").split("\n")
    twin_lines = twin.rstrip("\n").split("\n")
    diffs = []
    if len(page_lines) != len(twin_lines):
        diffs.append(f"line count page={len(page_lines)} twin={len(twin_lines)}")
    for i, (a, b) in enumerate(zip(page_lines, twin_lines), 1):
        if a != b and "___" not in a:
            diffs.append(f"line {i}: page={a!r} twin={b!r}")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/LX2/{lab_id}.py")],
                         capture_output=True, text=True)
    out_ok = run.stdout == expected.rstrip("\n") + "\n" or run.stdout.rstrip("\n") == expected.rstrip("\n")
    print(f"{lab_id}: code_diffs={len(diffs)} exit={run.returncode} expected_equals_output={out_ok}")
    for d in diffs:
        print("   ", d)
    if diffs or run.returncode != 0 or not out_ok:
        ok = False
print("RESULT", "PASS" if ok else "FAIL")
