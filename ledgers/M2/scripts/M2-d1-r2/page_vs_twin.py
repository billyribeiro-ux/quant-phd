"""Compare each lab block of L19-L21 with its twin: page code equals twin source, expected equals twin stdout."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
for lid in ("L19", "L20", "L21"):
    page = (ROOT / f"course/modules/M/M2/{lid}.html").read_text(encoding="utf-8")
    twin = (ROOT / f"tests/labs/M2/lab-M2-{lid}-1.py").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1)
    code = html.unescape(code)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)
    expected = html.unescape(expected)
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/M2/lab-M2-{lid}-1.py")],
                         capture_output=True, text=True, cwd=str(ROOT / "tests/labs/M2")).stdout
    print(lid, "code==twin:", code.strip() == twin.strip(), "expected==stdout:", expected.strip() == out.strip(),
          "code_len", len(code), "twin_len", len(twin))
    if code.strip() != twin.strip():
        import difflib
        print("\n".join(list(difflib.unified_diff(twin.strip().splitlines(), code.strip().splitlines(), lineterm=""))[:40]))
    if expected.strip() != out.strip():
        import difflib
        print("\n".join(list(difflib.unified_diff(out.strip().splitlines(), expected.strip().splitlines(), lineterm=""))[:40]))
