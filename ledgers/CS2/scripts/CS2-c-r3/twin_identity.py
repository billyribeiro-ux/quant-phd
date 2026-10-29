"""Compare each embedded data-run block and expected block with its twin and its real output."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
for lab in ("L09", "L10", "L11"):
    page = (ROOT / f"course/modules/CS/CS2/{lab}.html").read_text(encoding="utf-8")
    run = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    twin = (ROOT / f"tests/labs/CS2/lab-CS2-{lab}-1.py").read_text(encoding="utf-8")
    embedded = html.unescape(run.group(1)).strip()
    print(lab, "embedded==twin:", embedded == twin.strip())
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/CS2/lab-CS2-{lab}-1.py")],
                         capture_output=True, text=True, cwd="/tmp").stdout.strip()
    print(lab, "expected==run output:", html.unescape(exp.group(1)).strip() == out)
    if html.unescape(exp.group(1)).strip() != out:
        print("EXPECTED:\n" + html.unescape(exp.group(1)).strip() + "\nRUN:\n" + out)
