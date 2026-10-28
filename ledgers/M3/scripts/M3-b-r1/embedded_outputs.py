"""Compare each M3 L04-L06 lab twin: run it under python -I -W error, then check the code and output blocks embedded in its page."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
for lesson in ("L04", "L05", "L06"):
    twin = ROOT / f"tests/labs/M3/lab-M3-{lesson}-1.py"
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, check=True).stdout
    page = (ROOT / f"course/modules/M/M3/{lesson}.html").read_text(encoding="utf8")
    blocks = [html.unescape(re.sub(r"<[^>]+>", "", b)).strip() for b in re.findall(r"<pre[^>]*>(.*?)</pre>", page, re.S)]
    code = twin.read_text(encoding="utf8").strip()
    print(lesson, "code block equals twin:", code in blocks, "| output block equals run:", run.strip() in blocks)
