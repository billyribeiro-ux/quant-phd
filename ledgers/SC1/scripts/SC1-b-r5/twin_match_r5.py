"""Round-5 check: each lab's page code equals its twin, the twin runs under python -I -W error
in an empty scratch directory with empty stderr, and the stdout equals the page's expected block.
Run as: python3 -I ledgers/SC1/scripts/SC1-b-r5/twin_match_r5.py  (from the checkout root)."""

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
LABS = {
    "L04": "lab-SC1-L04-1",
    "L05": "lab-SC1-L05-1",
    "L06": "lab-SC1-L06-1",
}
ok_all = True
for page, lab in LABS.items():
    html_text = (ROOT / f"course/modules/SC/SC1/{page}.html").read_text(encoding="utf-8")
    sec = re.search(r'<section class="lab" id="%s".*?</section>' % lab, html_text, re.S)
    assert sec, lab
    body = sec.group(0)
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    twin = (ROOT / f"tests/labs/SC1/{lab}.py").read_text(encoding="utf-8")
    code_equals_twin = code.rstrip("\n") == twin.rstrip("\n")
    with tempfile.TemporaryDirectory() as scratch:
        twin_copy = Path(scratch) / "twin_copy.py"
        twin_copy.write_text(twin, encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(twin_copy)],
            cwd=scratch,
            capture_output=True,
            text=True,
            timeout=300,
        )
    out_equals = proc.stdout.rstrip("\n") == expected.rstrip("\n")
    print(
        f"{page} {lab}: code_equals_twin={code_equals_twin} exit={proc.returncode} "
        f"stderr_empty={proc.stderr == ''} expected_equals_output={out_equals}"
    )
    if not (code_equals_twin and proc.returncode == 0 and proc.stderr == "" and out_equals):
        ok_all = False
        print("--- stdout ---")
        print(proc.stdout)
        print("--- expected ---")
        print(expected)
print("ALL MATCH" if ok_all else "MISMATCH")
