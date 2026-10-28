"""Compare each page's class="expected" block with the twin's run output (run with python -I -W error)."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
ok = True
for lid, page in (("L01", "L01.html"), ("L02", "L02.html"), ("L03", "L03.html")):
    text = (root / "course/modules/M/M1" / page).read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    expected = html.unescape(m.group(1)).strip("\n")
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(root / f"tests/labs/M1/lab-M1-{lid}-1.py")],
        capture_output=True, text=True, check=True,
    ).stdout.strip("\n")
    same = expected == run
    ok &= same
    print(lid, "lines", len(run.splitlines()), "IDENTICAL" if same else "DIFFERENT")
print("ALL IDENTICAL" if ok else "MISMATCH")
