"""Compare each lesson page's data-run block and pre.expected block with its lab twin and with the twin's stdout.

Usage: python -I twin_page_compare.py <checkout_root>
Reads the pages and twins only; prints one line per check and exits 1 on any mismatch.
"""
import html
import os
import re
import subprocess
import sys

root = sys.argv[1]
ok = True
for lesson in ("L04", "L05", "L06"):
    page_path = os.path.join(root, "course/modules/PC/PC3", f"{lesson}.html")
    twin_path = os.path.join(root, "tests/labs/PC3", f"lab-PC3-{lesson}-1.py")
    page = open(page_path, encoding="utf-8").read()
    twin = open(twin_path, encoding="utf-8").read()
    m_run = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    m_exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    run_block = html.unescape(m_run.group(1))
    exp_block = html.unescape(m_exp.group(1))
    same_code = run_block == twin
    same_code_no_nl = run_block.rstrip("\n") == twin.rstrip("\n")
    proc = subprocess.run([sys.executable, "-I", "-W", "error", twin_path], capture_output=True, text=True, cwd=root)
    out = proc.stdout
    same_exp = exp_block.rstrip("\n") == out.rstrip("\n")
    print(f"{lesson}: code_identical={same_code} code_identical_ignoring_trailing_newlines={same_code_no_nl} "
          f"expected_equals_stdout={same_exp} twin_exit={proc.returncode} stderr_bytes={len(proc.stderr)} "
          f"run_block_lines={run_block.count(chr(10))} twin_lines={twin.count(chr(10))}")
    if not same_code_no_nl or not same_exp or proc.returncode != 0:
        ok = False
        if not same_exp:
            import difflib
            for line in list(difflib.unified_diff(exp_block.rstrip("\n").splitlines(), out.rstrip("\n").splitlines(), lineterm=""))[:40]:
                print("   ", line)
        if not same_code_no_nl:
            import difflib
            for line in list(difflib.unified_diff(twin.rstrip("\n").splitlines(), run_block.rstrip("\n").splitlines(), lineterm=""))[:40]:
                print("   ", line)
print("ALL_EQUAL" if ok else "MISMATCH")
sys.exit(0 if ok else 1)
