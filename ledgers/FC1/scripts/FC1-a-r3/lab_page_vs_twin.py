"""Round 3 check: for each FC1 slice lab, (1) the page code block equals the twin, (2) the expected block equals the twin's output under python -I -W error, (3) the output is byte-identical across two runs."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for lab in ("L01", "L02", "L03"):
    page = (root / f"course/modules/FC/FC1/{lab}.html").read_text(encoding="utf-8")
    twin_path = root / f"tests/labs/FC1/lab-FC1-{lab}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1))
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1))
    run1 = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True)
    run2 = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True)
    out = run1.stdout
    print(f"{lab}: twin exit={run1.returncode} stderr={run1.stderr!r} code_eq_twin={code.strip() == twin.strip()} "
          f"expected_eq_output={exp.strip() == out.strip()} deterministic={run1.stdout == run2.stdout}")
    if code.strip() != twin.strip():
        import difflib
        print("".join(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page")))
    if exp.strip() != out.strip():
        import difflib
        print("".join(difflib.unified_diff(out.splitlines(True), exp.splitlines(True), "output", "expected")))
