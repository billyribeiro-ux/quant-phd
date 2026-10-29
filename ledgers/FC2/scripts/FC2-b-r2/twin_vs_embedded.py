"""FC2-b round 2: each twin run under python -I -W error and compared with the output embedded in its page; code embedded vs twin."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for page in ("L04", "L05", "L06"):
    text = (root / f"course/modules/FC/FC2/{page}.html").read_text()
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1))
    twin_path = root / f"tests/labs/FC2/lab-FC2-{page}-1.py"
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp")
    print(page, "rc", run.returncode, "stdout==embedded:", run.stdout == expected + "\n", "embedded code==twin:", code.strip() == twin_path.read_text().strip())
