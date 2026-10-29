"""Verifier check (E5 slice b, round 3): page expected blocks vs twin output, and twin code vs page code.

Usage: python3 -I ledgers/E5/scripts/E5-b-r3/check_labs_b.py <checkout_root>
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
py = root / ".venv" / "bin" / "python"
ok = True
for page, lab in (("L04", "lab-E5-L04-1"), ("L05", "lab-E5-L05-1"), ("L06", "lab-E5-L06-1")):
    text = (root / "course/modules/E/E5" / f"{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S).group(1)
    code = html.unescape(code).rstrip("\n")
    twin = (root / "tests/labs/E5" / f"{lab}.py").read_text(encoding="utf-8").rstrip("\n")
    same_code = code == twin
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1)).rstrip("\n")
    out = subprocess.run([str(py), "-I", "-W", "error", str(root / "tests/labs" / "E5" / f"{lab}.py")],
                         capture_output=True, text=True, cwd="/tmp").stdout.rstrip("\n")
    same_out = out == expected
    ok = ok and same_code and same_out
    print(f"{page} {lab}: page_code_equals_twin={same_code} expected_equals_output={same_out} "
          f"lines_out={len(out.splitlines())}")
    if not same_out:
        for a, b in zip(out.splitlines(), expected.splitlines()):
            if a != b:
                print("  DIFF out:", a, "| expected:", b)
print("ALL_OK" if ok else "MISMATCH")
