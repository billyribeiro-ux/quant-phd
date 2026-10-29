"""Round 5 verifier script (M3-c). Compares each slice lab's real output with the expected block embedded in its page,
and recomputes the unrounded numbers the pages print or quote. Run as: .venv/bin/python -I -W error <this file>."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
py = sys.argv[2]
for page in ("L07", "L08", "L09"):
    text = (root / "course/modules/M/M3" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(m.group(1)).strip()
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', text, re.S).group(1))
    lab = root / "tests/labs/M3" / f"lab-M3-{page}-1.py"
    twin = lab.read_text(encoding="utf-8")
    run = subprocess.run([py, "-I", "-W", "error", str(lab)], capture_output=True, text=True, cwd="/tmp")
    same_code = code.strip() == twin.strip()
    print(page, "embedded code == twin:", same_code, "| actual output == expected block:", run.stdout.strip() == expected, "| rc", run.returncode)
    if run.stdout.strip() != expected:
        print("ACTUAL:\n" + run.stdout)
        print("EXPECTED:\n" + expected)
