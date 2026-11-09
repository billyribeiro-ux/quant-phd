"""Round-4 independent check: page lab code equals its twin; expected block equals the twin's stdout.

Run from the checkout root: python -I ledgers/FC2/scripts/FC2-b-r4/twin_vs_page_ind_r4.py
"""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(".")
PAGES = {
    "L04": ("course/modules/FC/FC2/L04.html", "tests/labs/FC2/lab-FC2-L04-1.py", "lab-FC2-L04-1"),
    "L05": ("course/modules/FC/FC2/L05.html", "tests/labs/FC2/lab-FC2-L05-1.py", "lab-FC2-L05-1"),
    "L06": ("course/modules/FC/FC2/L06.html", "tests/labs/FC2/lab-FC2-L06-1.py", "lab-FC2-L06-1"),
}
for name, (page, twin, lab_id) in PAGES.items():
    text = (ROOT / page).read_text(encoding="utf-8")
    sec = re.search(r'<section class="lab"[^>]*id="%s".*?</section>' % re.escape(lab_id), text, re.S)
    assert sec, f"{name}: lab section not found"
    body = sec.group(0)
    code = re.search(r"<code[^>]*data-run[^>]*>(.*?)</code>", body, re.S)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    tcode = (ROOT / twin).read_text(encoding="utf-8")
    pcode = html.unescape(code.group(1))
    same_code = pcode.rstrip("\n") == tcode.rstrip("\n")
    proc = subprocess.run(
        [sys.executable, "-I", "-W", "error", twin], capture_output=True, text=True, cwd=ROOT, timeout=60
    )
    pexp = html.unescape(exp.group(1))
    print(f"{name} page-code-equals-twin={same_code} twin-exit={proc.returncode} stderr-empty={proc.stderr == ''}")
    print(f"{name} expected==stdout (strip trailing ws)={pexp.strip() == proc.stdout.strip()} lines={len(proc.stdout.splitlines())}")
    print(f"{name} data-tolerance line:", re.search(r'<pre class="expected"[^>]*>', body).group(0))
    if not same_code:
        import difflib
        print("".join(difflib.unified_diff(tcode.splitlines(True), pcode.splitlines(True), "twin", "page")))
    if pexp.strip() != proc.stdout.strip():
        import difflib
        print("".join(difflib.unified_diff(proc.stdout.splitlines(True), pexp.splitlines(True), "stdout", "expected")))
