# Round 2, slice M3-a: compare each lab's embedded expected output and embedded code with the twin and a fresh run.
# Run as: <checkout>/.venv/bin/python -I ledgers/M3/scripts/M3-a-r2/embedded_vs_run.py <checkout>
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for f in ["L01", "L02", "L03"]:
    page = (root / f"course/modules/M/M3/{f}.html").read_text(encoding="utf-8")
    twin = (root / f"tests/labs/M3/lab-M3-{f}-1.py").read_text(encoding="utf-8")
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S).group(1))
    expected = [html.unescape(x).strip() for x in re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)]
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M3/lab-M3-{f}-1.py")],
        capture_output=True, text=True, check=False,
    )
    print(f, "embedded code == twin:", code.strip() == twin.strip(),
          "| expected blocks:", len(expected),
          "| expected == run stdout:", [x == run.stdout.strip() for x in expected],
          "| exit:", run.returncode)
