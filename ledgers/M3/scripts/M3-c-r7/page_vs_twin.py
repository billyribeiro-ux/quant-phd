"""Compare each M3 lesson page's lab code and expected block with its twin and with the twin's live output.

Usage: python -I -W error ledgers/M3/scripts/M3-c-r7/page_vs_twin.py <repo_root>
Reads course/modules/M/M3/L07.html, L08.html, L09.html and tests/labs/M3/lab-M3-L0x-1.py.
Prints PAGE_CODE_EQ, EXPECTED_EQ_OUTPUT (exact text after whitespace strip per line) for each lesson.
"""
import html
import io
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for lesson in ("L07", "L08", "L09"):
    page = (root / f"course/modules/M/M3/{lesson}.html").read_text(encoding="utf-8")
    twin = (root / f"tests/labs/M3/lab-M3-{lesson}-1.py").read_text(encoding="utf-8")
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    code_eq = code.strip() == twin.strip()
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M3/lab-M3-{lesson}-1.py")],
        capture_output=True,
        text=True,
        cwd="/tmp",
    )
    out_lines = [line.rstrip() for line in run.stdout.splitlines()]
    exp_lines = [line.rstrip() for line in expected.splitlines()]
    print(f"{lesson}: PAGE_CODE_EQ={code_eq} TWIN_EXIT={run.returncode} STDERR_BYTES={len(run.stderr)}")
    print(f"{lesson}: EXPECTED_EQ_OUTPUT={exp_lines == out_lines} lines={len(exp_lines)}/{len(out_lines)}")
    for a, b in zip(exp_lines, out_lines):
        if a != b:
            print("  DIFF expected:", a)
            print("  DIFF output  :", b)
