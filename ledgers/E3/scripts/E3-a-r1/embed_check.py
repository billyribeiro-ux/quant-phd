"""Verifier E3-a round 1: run each L01-L03 twin under python -I -W error and compare its stdout with the
<pre class="expected"> block embedded in the lesson page. Run from the checkout root:
    .venv/bin/python -I ledgers/E3/scripts/E3-a-r1/embed_check.py
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[4]
ok_all = True
for lesson in ("L01", "L02", "L03"):
    page = (root / "course/modules/E/E3" / f"{lesson}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(m.group(1)).strip()
    twin = root / "tests/labs/E3" / f"lab-E3-{lesson}-1.py"
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, timeout=120)
    same = run.returncode == 0 and run.stdout.strip() == expected
    ok_all = ok_all and same
    print(f"{lesson} exit {run.returncode} embedded_equals_run {same} lines {len(expected.splitlines())}")
print("ALL", ok_all)
