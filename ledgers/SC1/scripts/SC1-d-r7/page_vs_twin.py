"""Round 7 (SC1-d): compare each project lab's page code and expected block with its twin and its run output.

Usage (from the checkout root): .venv/bin/python -I ledgers/SC1/scripts/SC1-d-r7/page_vs_twin.py
Prints, per lab: whether the page code equals the twin, whether every page line equals the twin line or contains
a blank (___), and whether the expected block equals the twin's stdout under python -I -W error.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGE = ROOT / "course/modules/SC/SC1/project.html"
TWINS = ROOT / "tests/labs/SC1"
text = PAGE.read_text(encoding="utf-8")
blocks = re.findall(r'<section class="lab[^"]*" id="(lab-SC1-project-\d)"[^>]*>(.*?)</section>', text, re.S)
ok_all = True
for lab_id, body in blocks:
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S).group(1)
    code = html.unescape(code)
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1))
    twin = (TWINS / f"{lab_id.replace('lab-SC1-project', 'lab-SC1-project')}.py").read_text(encoding="utf-8")
    same = code.strip() == twin.strip()
    page_lines = code.strip().splitlines()
    twin_lines = twin.strip().splitlines()
    blank_ok = len(page_lines) == len(twin_lines) and all(
        p == t or "___" in p for p, t in zip(page_lines, twin_lines))
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(TWINS / f"{lab_id}.py")],
                         capture_output=True, text=True, cwd=ROOT)
    out_ok = run.returncode == 0 and run.stdout.strip() == expected.strip()
    print(f"{lab_id}: page code == twin: {same}; blank-only differences: {blank_ok}; "
          f"run exit {run.returncode}; expected == stdout: {out_ok}")
    if not (out_ok and (same or blank_ok)):
        ok_all = False
        print("  stdout:", run.stdout.strip()[:400])
        print("  stderr:", run.stderr.strip()[:400])
print("ALL OK" if ok_all else "MISMATCH")
