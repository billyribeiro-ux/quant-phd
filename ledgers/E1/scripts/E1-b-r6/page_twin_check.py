"""Compare each lab's page code and expected block with its twin and with the twin's real output.

Usage: python -I ledgers/E1/scripts/E1-b-r6/page_twin_check.py <checkout-root>
"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
ok = True
for lesson, lab in [("L04", "lab-E1-L04-1"), ("L05", "lab-E1-L05-1"), ("L06", "lab-E1-L06-1")]:
    page = (root / f"course/modules/E/E1/{lesson}.html").read_text(encoding="utf-8")
    m = re.search(
        r'<section class="lab" id="' + lab + r'".*?<code class="language-python" data-run>(.*?)</code></pre>'
        r'.*?<pre class="expected"[^>]*>(.*?)</pre>',
        page,
        re.S,
    )
    if not m:
        print(lesson, "no lab section found")
        ok = False
        continue
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin = (root / f"tests/labs/E1/{lab}.py").read_text(encoding="utf-8")
    same_code = code.strip() == twin.strip()
    out = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(root / f"tests/labs/E1/{lab}.py")],
        capture_output=True,
        text=True,
    ).stdout
    same_out = expected.strip() == out.strip()
    print(f"{lesson} {lab}: page_code_eq_twin={same_code} expected_eq_output={same_out} "
          f"code_len={len(code)} expected_lines={len(expected.splitlines())} output_lines={len(out.splitlines())}")
    if not same_code:
        ok = False
    if not same_out:
        ok = False
        import difflib
        print("\n".join(list(difflib.unified_diff(out.splitlines(), expected.splitlines(), lineterm=""))[:40]))
print("ALL OK" if ok else "MISMATCH")
