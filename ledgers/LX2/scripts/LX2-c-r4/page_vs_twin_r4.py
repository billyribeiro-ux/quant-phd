"""LX2-c round 4: compare project.html lab code and expected blocks with the lab twins.

Run from the checkout root: .venv/bin/python -I ledgers/LX2/scripts/LX2-c-r4/page_vs_twin_r4.py
Writes nothing into the repository. Page code is executed from a fresh scratch directory under /tmp.
"""

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
PAGE = (ROOT / "course/modules/LX/LX2/project.html").read_text(encoding="utf-8")
CODE_RE = re.compile(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', re.S)
EXP_RE = re.compile(r'<pre class="expected"[^>]*>(.*?)</pre>', re.S)
codes = [html.unescape(m) for m in CODE_RE.findall(PAGE)]
expecteds = [html.unescape(m) for m in EXP_RE.findall(PAGE)]
print(f"code blocks {len(codes)}, expected blocks {len(expecteds)}")
assert len(codes) == 3 and len(expecteds) == 3, "unexpected block count"

scratch = Path(tempfile.mkdtemp(prefix="lx2c-r4-page-"))
ok = True
for n in (1, 2, 3):
    twin = (ROOT / f"tests/labs/LX2/lab-LX2-project-{n}.py").read_text(encoding="utf-8")
    code = codes[n - 1]
    exp = expecteds[n - 1]
    same_twin = code.rstrip("\n") == twin.rstrip("\n")
    diff_lines = [
        (i + 1, a, b)
        for i, (a, b) in enumerate(zip(code.rstrip("\n").split("\n"), twin.rstrip("\n").split("\n")))
        if a != b
    ]
    print(f"lab {n}: page code == twin (modulo final newline): {same_twin}; differing lines: {diff_lines}")
    if n != 2 and not same_twin:
        ok = False
    # run the page code (blanks filled with the twin lines for lab 2)
    run_src = code
    if n == 2:
        if "___" not in code:
            print("lab 2: no blanks found")
            ok = False
        run_src = code.replace("hit_rate = ___", "hit_rate = Fraction(hits, horizon)").replace(
            "bias = ___", "bias = Fraction(sum(errors), horizon)"
        )
    path = scratch / f"page_lab{n}.py"
    path.write_text(run_src, encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True, cwd=str(scratch)
    )
    out = proc.stdout.rstrip("\n")
    match = out == exp.rstrip("\n")
    print(f"lab {n}: page code run exit={proc.returncode} stderr={proc.stderr!r} stdout==expected block: {match}")
    if proc.returncode != 0 or not match:
        ok = False
    twin_proc = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/LX2/lab-LX2-project-{n}.py")],
        capture_output=True,
        text=True,
        cwd=str(scratch),
    )
    print(f"lab {n}: twin stdout==expected block: {twin_proc.stdout.rstrip(chr(10)) == exp.rstrip(chr(10))}")
    if twin_proc.stdout.rstrip("\n") != exp.rstrip("\n"):
        ok = False
print("RESULT:", "PASS" if ok else "FAIL")
