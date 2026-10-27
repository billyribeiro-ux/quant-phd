"""Round-4 verifier: embedded lab code and expected output in L07/L08 vs the twins; twin stdout vs expected block."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for page, twin in (("L07", "lab-AC2-L07-1.py"), ("L08", "lab-AC2-L08-1.py")):
    text = (root / "course/modules/AC/AC2" / f"{page}.html").read_text(encoding="utf-8")
    run = re.search(r'<code class="language-python" data-run>(.*?)</code>', text, re.S).group(1)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1)
    code = html.unescape(run)
    expected = html.unescape(exp)
    twin_code = (root / "tests/labs/AC2" / twin).read_text(encoding="utf-8")
    out = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(root / "tests/labs/AC2" / twin)],
        capture_output=True, text=True, check=True).stdout
    print(page, "embedded code == twin:", code.strip() == twin_code.strip())
    print(page, "expected block == twin stdout:", expected.strip() == out.strip())
    if expected.strip() != out.strip():
        import difflib
        print("\n".join(difflib.unified_diff(expected.strip().splitlines(), out.strip().splitlines(), lineterm="")))
