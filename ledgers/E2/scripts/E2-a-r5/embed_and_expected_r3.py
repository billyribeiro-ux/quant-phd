"""Round-3 check for E2 hub-slice lessons L01-L03: page code block equals the lab twin byte for byte,
and the page's expected block equals the twin's stdout under python -I -W error.

Usage (from the repository root): .venv/bin/python ledgers/E2/scripts/E2-a-r3/embed_and_expected_r3.py
"""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = ROOT / "course" / "modules" / "E" / "E2"
TWINS = ROOT / "tests" / "labs" / "E2"
PY = ROOT / ".venv" / "bin" / "python"

ok = True
for n in (1, 2, 3):
    page = (PAGES / f"L0{n}.html").read_text(encoding="utf-8")
    lab_id = f"lab-E2-L0{n}-1"
    section = re.search(rf'<section class="lab" id="{lab_id}".*?</section>', page, re.S)
    if not section:
        print(lab_id, "section missing")
        ok = False
        continue
    body = section.group(0)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S).group(1)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1)
    code_text = html.unescape(code)
    twin_text = (TWINS / f"{lab_id}.py").read_text(encoding="utf-8")
    same_code = code_text.rstrip("\n") == twin_text.rstrip("\n")
    run = subprocess.run([str(PY), "-I", "-W", "error", str(TWINS / f"{lab_id}.py")], capture_output=True, text=True)
    same_out = html.unescape(expected).rstrip("\n") == run.stdout.rstrip("\n")
    print(f"{lab_id}: page code == twin: {same_code} (len {len(code_text)} vs {len(twin_text)}); "
          f"expected == stdout: {same_out}; twin rc={run.returncode}; stderr bytes={len(run.stderr)}")
    if not (same_code and same_out and run.returncode == 0):
        ok = False
        if not same_code:
            for i, (a, b) in enumerate(zip(code_text.splitlines(), twin_text.splitlines())):
                if a != b:
                    print("  first differing line", i + 1, repr(a)[:120], repr(b)[:120])
                    break
        if not same_out:
            print("  expected:", repr(html.unescape(expected))[:400])
            print("  stdout:  ", repr(run.stdout)[:400])
print("ALL OK" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
