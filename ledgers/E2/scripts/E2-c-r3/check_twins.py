"""Verifier check (E2 slice c, round 3): page code equals twin; expected block equals twin output.

Run from the checkout root: python -I -W error ledgers/E2/scripts/E2-c-r3/check_twins.py
"""
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(".")
for page in ("L07", "L08", "L09"):
    src = (ROOT / f"course/modules/E/E2/{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    lab_id = f"lab-E2-{page}-1"
    twin_path = ROOT / f"tests/labs/E2/{lab_id}.py"
    twin = twin_path.read_text(encoding="utf-8")
    page_code = html.unescape(code.group(1))
    print(f"{page} page_code_equals_twin: {page_code == twin} (page {len(page_code)} chars, twin {len(twin)} chars)")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, timeout=120)
    print(f"{page} twin_exit: {run.returncode} stderr_len: {len(run.stderr)}")
    out = run.stdout
    page_expected = html.unescape(expected.group(1))
    print(f"{page} expected_equals_output: {page_expected == out}")
    if page_expected != out:
        import difflib
        for line in difflib.unified_diff(page_expected.splitlines(), out.splitlines(), "expected", "output", lineterm=""):
            print("   ", line)
    # ends with an unconditional main() call and no __main__ guard
    print(f"{page} has_main_guard: {'__main__' in twin}; last_line: {twin.strip().splitlines()[-1]!r}")
