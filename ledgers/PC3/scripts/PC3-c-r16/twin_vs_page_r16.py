"""Compare each project lab's page code and expected block with its twin and with the twin's own output.

Usage: python -I twin_vs_page_r16.py <repo root>
Prints, per lab: whether the page code equals the twin (after HTML unescape) or differs only at blank lines (rung 2),
and whether the expected block equals the twin's stdout under python -I -W error.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/PC/PC3/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    lab_id = f"lab-PC3-project-{n}"
    m = re.search(rf'<section class="lab[^"]*" id="{lab_id}".*?</section>', page, re.S)
    sec = m.group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin = (root / f"tests/labs/PC3/{lab_id}.py").read_text(encoding="utf-8")
    code_lines = code.rstrip("\n").split("\n")
    twin_lines = twin.rstrip("\n").split("\n")
    print(f"== {lab_id}: page code lines={len(code_lines)} twin lines={len(twin_lines)} twin==page: {code.rstrip() == twin.rstrip()}")
    if len(code_lines) == len(twin_lines):
        for i, (a, b) in enumerate(zip(code_lines, twin_lines), 1):
            if a != b:
                print(f"  line {i}: page={a!r}")
                print(f"  line {i}: twin={b!r}")
                if "___" not in a:
                    print("  NOTE: differing line without blank")
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/PC3/{lab_id}.py")],
                       capture_output=True, text=True, cwd=str(root / "tests/labs/PC3"))
    print(f"  twin exit={r.returncode} stderr={r.stderr.strip()[:200]!r}")
    print(f"  expected block == twin stdout: {expected.strip() == r.stdout.strip()}")
    if expected.strip() != r.stdout.strip():
        print("  STDOUT:", r.stdout)
        print("  EXPECTED:", expected)
