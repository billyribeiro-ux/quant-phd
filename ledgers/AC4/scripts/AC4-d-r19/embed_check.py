"""Compare each page's data-run code block and class=expected output with the twin and a fresh run.

Usage: python -I embed_check.py <checkout>. Prints OK/DIFF per page. Read-only.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for page, twin in (("L07", "lab-AC4-L07-1.py"), ("L08", "lab-AC4-L08-1.py")):
    text = (root / f"course/modules/AC/AC4/{page}.html").read_text(encoding="utf-8")
    code = re.search(r'data-run>(.*?)</code></pre>', text, re.S).group(1)
    code = html.unescape(code)
    src = (root / "tests/labs/AC4" / twin).read_text(encoding="utf-8")
    print(page, "code block equals twin:", code.strip() == src.strip())
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1))
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / "tests/labs/AC4" / twin)],
                         capture_output=True, text=True, check=True).stdout
    print(page, "expected block equals fresh run output:", expected.strip() == run.strip(), "lines:", len(run.splitlines()))
