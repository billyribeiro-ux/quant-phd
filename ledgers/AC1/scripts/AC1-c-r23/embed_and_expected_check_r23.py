"""Compare each lab's embedded code and expected block in L07/L08 with its twin and with a fresh run."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
pairs = {"L07": "lab-AC1-L07-1", "L08": "lab-AC1-L08-1"}
for page, lab in pairs.items():
    text = (root / f"course/modules/AC/AC1/{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', text, re.S).group(1)
    code = html.unescape(code)
    twin = (root / f"tests/labs/AC1/{lab}.py").read_text(encoding="utf-8")
    print(page, "embedded code == twin:", code.rstrip("\n") == twin.rstrip("\n"))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1))
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/AC1/{lab}.py")],
                         capture_output=True, text=True, check=True).stdout
    exp_lines = [line.rstrip() for line in expected.strip().splitlines()]
    run_lines = [line.rstrip() for line in run.strip().splitlines()]
    print(page, "expected == run output:", exp_lines == run_lines, len(exp_lines), len(run_lines))
