"""Verify, for each E4 lab page L04-L06: (1) the page's data-run code is byte-identical to its twin,
(2) the page's expected block equals the stdout of the twin run alone under python -I -W error.

Usage: python -I -W error expected_vs_output.py <checkout-root>
Prints one line per lab and exits nonzero on any mismatch.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
ok = True
for page in ("L04", "L05", "L06"):
    text = (root / f"course/modules/E/E4/{page}.html").read_text(encoding="utf-8")
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    twin_path = root / f"tests/labs/E4/lab-E4-{page}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    code_eq = code == twin.rstrip("\n")  # embed_labs.py strips the trailing newline (line 117)
    proc = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)],
        capture_output=True,
        text=True,
        cwd=twin_path.parent,
        check=False,
    )
    out_eq = proc.stdout == expected
    # the page block may end without a trailing newline in the HTML; compare with rstrip too
    out_eq_loose = proc.stdout.rstrip("\n") == expected.rstrip("\n")
    print(
        f"{page}: code_equals_twin={code_eq} expected_equals_output={out_eq} "
        f"(loose={out_eq_loose}) exit={proc.returncode} stderr_bytes={len(proc.stderr)} "
        f"code_chars={len(code)} twin_chars={len(twin)} out_lines={proc.stdout.count(chr(10))}"
    )
    ok = ok and code_eq and out_eq_loose and proc.returncode == 0 and not proc.stderr
sys.exit(0 if ok else 1)
