"""Compare each page's data-run code block with its twin file, and each expected block with the twin's output.

Usage: python3 -I ledgers/CS2/scripts/CS2-a-r4/twin_equality_r4.py <repo-root>
Prints one line per lesson: CODE_EQUAL and OUTPUT_EQUAL (the output is produced by running the twin with -I -W error).
"""

import html
import pathlib
import re
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
for n in range(1, 5):
    page = (root / f"course/modules/CS/CS2/L0{n}.html").read_text(encoding="utf-8")
    twin_path = root / f"tests/labs/CS2/lab-CS2-L0{n}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    code_m = re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S)
    code = html.unescape(code_m.group(1))
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(exp_m.group(1))
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd=str(root)
    )
    out = run.stdout
    print(
        f"L0{n}: code_equal={code.strip() == twin.strip()} "
        f"expected_equal_output={expected.strip() == out.strip()} exit={run.returncode} "
        f"twin_lines={len(twin.splitlines())} expected_lines={len(expected.splitlines())}"
    )
