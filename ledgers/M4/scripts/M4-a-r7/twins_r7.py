"""Verify M4 slice-a lab twins: alone under python -I -W error; page code == twin; expected == stdout.

Usage: .venv/bin/python -I ledgers/M4/scripts/M4-a-r7/twins_r7.py <checkout>
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
labs = {
    "L01": "lab-M4-L01-1",
    "L02": "lab-M4-L02-1",
    "L03": "lab-M4-L03-1",
    "L04": "lab-M4-L04-1",
}
ok = True
for lesson, lab in labs.items():
    page = (root / f"course/modules/M/M4/{lesson}.html").read_text(encoding="utf-8")
    twin_path = root / f"tests/labs/M4/{lab}.py"
    twin = twin_path.read_text(encoding="utf-8")
    # page code block belonging to this lab section
    sec = re.search(r'<section class="lab" id="%s".*?</section>' % re.escape(lab), page, re.S)
    if not sec:
        print(lesson, "no lab section found")
        ok = False
        continue
    body = sec.group(0)
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    page_code = html.unescape(code_m.group(1))
    page_exp = html.unescape(exp_m.group(1))
    code_equal = page_code == twin
    if not code_equal:
        # tolerate only a single trailing newline difference, report otherwise
        code_equal = page_code.rstrip("\n") == twin.rstrip("\n")
    proc = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)],
        capture_output=True, text=True, cwd="/tmp", timeout=120,
    )
    out = proc.stdout
    exp_equal = page_exp.rstrip("\n") == out.rstrip("\n")
    print(f"{lesson} {lab}: exit={proc.returncode} stderr_len={len(proc.stderr)} "
          f"stdout_lines={len(out.splitlines())} code_equals_twin={code_equal} "
          f"expected_equals_stdout={exp_equal} data-tolerance={exp_m.group(0)[:60]!r}")
    if proc.returncode != 0 or proc.stderr or not code_equal or not exp_equal:
        ok = False
        if not exp_equal:
            print("--- page expected ---\n" + page_exp + "\n--- stdout ---\n" + out)
print("ALL OK" if ok else "FAILURES")
