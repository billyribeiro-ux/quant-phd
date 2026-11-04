"""Compare each SC1 slice-b lab page with its twin: page code == twin, expected block == twin output.

Run from the checkout root: .venv/bin/python -I ledgers/SC1/scripts/SC1-b-r1/twin_match.py
"""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = {
    "L04": ROOT / "course/modules/SC/SC1/L04.html",
    "L05": ROOT / "course/modules/SC/SC1/L05.html",
    "L06": ROOT / "course/modules/SC/SC1/L06.html",
}
ok = True
for name, page in PAGES.items():
    text = page.read_text(encoding="utf-8")
    twin_id = f"lab-SC1-{name}-1"
    twin = ROOT / "tests/labs/SC1" / f"{twin_id}.py"
    twin_src = twin.read_text(encoding="utf-8")
    m = re.search(r'<section class="lab" id="%s".*?<pre><code class="language-python" data-run>(.*?)</code></pre>' % twin_id, text, re.S)
    code = html.unescape(m.group(1))
    same_code = code.strip() == twin_src.strip()
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(e.group(1)).strip()
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, cwd=ROOT)
    out = run.stdout.strip()
    same_out = out == expected
    print(f"{name}: twin={twin.name} exit={run.returncode} page_code_equals_twin={same_code} expected_equals_output={same_out}")
    if run.returncode != 0 or not same_code or not same_out:
        ok = False
        print(run.stderr)
        if not same_out:
            print("OUTPUT:\n" + out)
            print("EXPECTED:\n" + expected)
print("ALL MATCH" if ok else "MISMATCH")
