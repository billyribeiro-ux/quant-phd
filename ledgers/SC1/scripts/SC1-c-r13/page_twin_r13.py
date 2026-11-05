"""Compare each SC1 lesson lab block (L07, L08) with its twin and expected output.

Usage: python -I page_twin_r13.py <checkout-root>
Reads the page <pre><code class="language-python" data-run> block (HTML-unescaped) and the
<pre class="expected"> block, and compares them with tests/labs/SC1/<twin> and the twin's
stdout captured from a fresh `python -I -W error` run.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
cases = {"L07": "lab-SC1-L07-1.py", "L08": "lab-SC1-L08-1.py"}
ok_all = True
for lesson, twin in cases.items():
    page = (root / f"course/modules/SC/SC1/{lesson}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin_src = (root / "tests/labs/SC1" / twin).read_text(encoding="utf-8")
    same_code = code.rstrip(chr(10)) == twin_src.rstrip(chr(10))  # final newline only (embed convention)
    m2 = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(m2.group(1))
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(root / "tests/labs/SC1" / twin)],
        capture_output=True, text=True, cwd="/tmp",
    )
    out = run.stdout
    same_out = expected.rstrip("\n") == out.rstrip("\n")
    print(f"{lesson} exit={run.returncode} stderr_bytes={len(run.stderr)} page_code_equals_twin={same_code} "
          f"expected_equals_stdout={same_out} stdout_lines={out.count(chr(10))} expected_lines={expected.count(chr(10))}")
    if not (same_code and same_out and run.returncode == 0 and not run.stderr):
        ok_all = False
        if not same_out:
            import difflib
            print("".join(difflib.unified_diff(expected.splitlines(True), out.splitlines(True), "expected", "stdout")))
    with open(root / f"ledgers/SC1/scripts/SC1-c-r13/out/{lesson}_stdout_r13.txt", "w", encoding="utf-8") as fh:
        fh.write(out)
print("ALL_OK" if ok_all else "MISMATCH")
