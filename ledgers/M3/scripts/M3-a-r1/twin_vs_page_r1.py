"""Closing-delta check (M3 slice a, round 1): page code block equals twin source; expected block equals twin output.

Run: python -I -W error ledgers/M3/scripts/M3-a-r1/twin_vs_page_r1.py   (runs the twins with -I -W error)
"""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyF21-M3-a")
for n in ("L01", "L02", "L03"):
    page = (ROOT / f"course/modules/M/M3/{n}.html").read_text(encoding="utf-8")
    m = re.search(r'<section class="lab" id="lab-M3-%s-1".*?<pre><code[^>]*data-run>(.*?)</code></pre>\s*<pre>(.*?)</pre>' % n, page, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin = (ROOT / f"tests/labs/M3/lab-M3-{n}-1.py").read_text(encoding="utf-8")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/M3/lab-M3-{n}-1.py")],
                         capture_output=True, text=True, cwd="/tmp")
    print(n, "page code == twin:", code.strip() == twin.strip(), "| twin exit", run.returncode,
          "| expected == twin output:", expected.strip() == run.stdout.strip(), "| stderr bytes", len(run.stderr))
