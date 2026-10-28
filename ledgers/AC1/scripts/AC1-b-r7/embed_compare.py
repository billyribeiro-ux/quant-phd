"""Compare each lab page's code block and expected block with its twin and its run output."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
py = sys.executable
pages = {"L04": "lab-AC1-L04-1", "L05": "lab-AC1-L05-1", "L06": "lab-AC1-L06-1"}
for page, lab in pages.items():
    text = (root / "course/modules/AC/AC1" / f"{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S).group(1)
    code = html.unescape(code)
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1)
    exp = html.unescape(exp)
    twin = (root / "tests/labs/AC1" / f"{lab}.py").read_text(encoding="utf-8")
    out = subprocess.run([py, "-I", "-W", "error", str(root / "tests/labs/AC1" / f"{lab}.py")],
                         capture_output=True, text=True, check=True).stdout
    print(page, "code identical to twin:", code.rstrip() == twin.rstrip(),
          "| expected identical to output:", exp.rstrip() == out.rstrip(),
          "| lines", len(out.rstrip().splitlines()), "| code lines", len(twin.splitlines()))
