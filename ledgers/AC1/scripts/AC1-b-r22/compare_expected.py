"""Compare each lab twin's stdout with the pre.expected block of its page (AC1 slice b)."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
py = sys.argv[2]
for n in ("L04", "L05", "L06"):
    page = (root / f"course/modules/AC/AC1/{n}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    if m is None:
        m = re.search(r'<pre[^>]*expected[^>]*>(.*?)</pre>', page, re.S)
    exp = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))) if m else None
    out = subprocess.run([py, "-I", "-W", "error", str(root / f"tests/labs/AC1/lab-AC1-{n}-1.py")],
                         capture_output=True, text=True, check=True).stdout
    print(n, "expected_block_found", m is not None, "match_exact", exp is not None and exp.strip() == out.strip(),
          "lines_expected", len(exp.strip().splitlines()) if exp else None, "lines_stdout", len(out.strip().splitlines()))
    if exp is not None and exp.strip() != out.strip():
        import difflib
        print("\n".join(difflib.unified_diff(exp.strip().splitlines(), out.strip().splitlines(), lineterm="")))
