"""Round-5 check (M3-c): page code and expected block equal the lab twin; twin output equals expected block.

Run from the checkout root with the repository venv:  .venv/bin/python -I ledgers/M3/scripts/M3-c-r5/m3c_r5_twin_vs_page.py
For each lesson it reads the page, extracts the <code data-run> text and the <pre class="expected"> text,
compares them with tests/labs/M3/<twin>, then runs the twin alone under python -I -W error from an empty
temporary directory and compares its stdout with the expected block.
"""
import html
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD5-M3-c")
PAGES = {"L07": "lab-M3-L07-1.py", "L08": "lab-M3-L08-1.py", "L09": "lab-M3-L09-1.py"}
PYTHON = str(ROOT / ".venv" / "bin" / "python")

ok = True
for page, twin_name in PAGES.items():
    html_text = (ROOT / "course/modules/M/M3" / f"{page}.html").read_text(encoding="utf-8")
    code_m = re.search(r'<code class="language-python" data-run>(.*?)</code>', html_text, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', html_text, re.S)
    code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    twin_path = ROOT / "tests/labs/M3" / twin_name
    twin = twin_path.read_text(encoding="utf-8")
    same_code = code.rstrip("\n") == twin.rstrip("\n")
    print(f"{page}: page code equals twin ({twin_name}): {same_code}")
    ok &= same_code
    with tempfile.TemporaryDirectory(prefix="m3c-r5-") as tmp:
        proc = subprocess.run(
            [PYTHON, "-I", "-W", "error", str(twin_path)],
            cwd=tmp,
            capture_output=True,
            text=True,
            timeout=60,
        )
    print(f"{page}: twin exit={proc.returncode} stderr_bytes={len(proc.stderr.encode())}")
    same_out = proc.stdout.rstrip() == expected.rstrip()
    print(f"{page}: twin stdout equals expected block (rstrip): {same_out}")
    if not same_out:
        print("---- expected ----")
        print(expected)
        print("---- actual ----")
        print(proc.stdout)
    ok &= same_out and proc.returncode == 0 and not proc.stderr
print("ALL OK" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
