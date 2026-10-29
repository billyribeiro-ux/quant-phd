"""Compare each lesson's data-run block and expected block with its twin and the twin's stdout (round 5)."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
for n in ("07", "08", "09"):
    page = (ROOT / f"course/modules/E/E2/L{n}.html").read_text(encoding="utf-8")
    m = re.search(r'<code class="language-python" data-run>(.*?)</code>', page, re.S)
    code = html.unescape(m.group(1))
    twin = (ROOT / f"tests/labs/E2/lab-E2-L{n}-1.py").read_text(encoding="utf-8")
    print(f"L{n} data-run == twin (modulo trailing newline):", code.rstrip("\n") == twin.rstrip("\n"), "lines", twin.count("\n"))
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    exp = html.unescape(re.sub(r"<[^>]+>", "", e.group(1)))
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/E2/lab-E2-L{n}-1.py")], capture_output=True, text=True)
    print(f"L{n} expected == stdout (modulo trailing newline):", exp.rstrip("\n") == run.stdout.rstrip("\n"), "lines", exp.count("\n") + 1, "stderr", len(run.stderr))
    print(f"L{n} data-run count of matches:", len(re.findall(r"data-run>", page)))
