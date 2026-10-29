"""For each lab on the M3 hub-slice lesson pages, compare the <pre><code data-run> block with its twin file,
and the <pre class="expected"> block with the twin's stdout. Usage: python -I ledgers/.../page_code_equals_twin.py REPO_ROOT"""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for lesson in ["L01", "L02", "L03"]:
    page = (root / "course/modules/M/M3" / f"{lesson}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code = html.unescape(m.group(1))
    twin = (root / f"tests/labs/M3/lab-M3-{lesson}-1.py").read_text(encoding="utf-8")
    print(lesson, "code==twin:", code.strip() == twin.strip(), "len", len(code), len(twin))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(e.group(1)).strip()
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M3/lab-M3-{lesson}-1.py")],
                         capture_output=True, text=True, check=True).stdout.strip()
    print(lesson, "expected==output:", expected == out)
