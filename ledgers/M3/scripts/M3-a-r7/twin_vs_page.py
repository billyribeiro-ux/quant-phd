"""Compare each page's embedded lab code and expected block with its twin and a fresh run (M3 slice a, round 6)."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for lid in ["L01", "L02", "L03"]:
    page = (root / f"course/modules/M/M3/{lid}.html").read_text(encoding="utf-8")
    twin = (root / f"tests/labs/M3/lab-M3-{lid}-1.py").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1))
    print(lid, "page code == twin:", code.rstrip("\n") == twin.rstrip("\n"), "| code lines", code.count("\n"))
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M3/lab-M3-{lid}-1.py")],
                         capture_output=True, text=True)
    print(lid, "twin exit", run.returncode, "| expected == output:", expected.strip() == run.stdout.strip())
    if expected.strip() != run.stdout.strip():
        print("EXPECTED:\n" + expected + "\nOUTPUT:\n" + run.stdout)
