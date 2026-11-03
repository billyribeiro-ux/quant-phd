"""Compare each slice page's lab code and expected block with its twin (run from the checkout root)."""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
PY = str(ROOT / ".venv" / "bin" / "python")
for page, twin in [("L22", "lab-M2-L22-1.py"), ("L23", "lab-M2-L23-1.py"), ("L24", "lab-M2-L24-1.py")]:
    text = (ROOT / "course/modules/M/M2" / f"{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S).group(1)
    code = html.unescape(code)
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1))
    twin_src = (ROOT / "tests/labs/M2" / twin).read_text(encoding="utf-8")
    print(f"{page}: page code == twin: {code == twin_src} (page {len(code)} chars, twin {len(twin_src)} chars)")
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / twin
        p.write_text(twin_src, encoding="utf-8")
        r = subprocess.run([PY, "-I", "-W", "error", str(p)], capture_output=True, text=True, cwd=d)
        print(f"{page}: twin exit {r.returncode}, stderr bytes {len(r.stderr.encode())}")
        out = r.stdout
        print(f"{page}: expected == stdout: {expected.strip() == out.strip()} (expected lines {len(expected.strip().splitlines())}, stdout lines {len(out.strip().splitlines())})")
        Path(sys.argv[1] if len(sys.argv) > 1 else f"/dev/null").parent  # no-op
        (ROOT / "ledgers/M2/scripts/M2-d2-r3" / f"twin_{page}.stdout").write_text(out, encoding="utf-8")
        for a, b in zip(expected.strip().splitlines(), out.strip().splitlines()):
            if a != b:
                print("  DIFF expected:", a)
                print("  DIFF stdout:  ", b)
