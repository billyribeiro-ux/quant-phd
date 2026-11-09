import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
for page in ("L01", "L02", "L03"):
    text = (root / f"course/modules/BK/BK4/{page}.html").read_text(encoding="utf-8")
    lab_id = f"lab-BK4-{page}-1"
    section = re.search(rf'<section class="lab" id="{lab_id}".*?</section>', text, re.S)
    code = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', section.group(0), re.S)
    twin = (root / f"tests/labs/BK4/{lab_id}.py").read_text(encoding="utf-8")
    code_text = html.unescape(code.group(1))
    print(lab_id, "exact:", code_text == twin, "| equal after trailing-newline strip:", code_text.rstrip("\n") == twin.rstrip("\n"),
          "| twin ends with newline:", twin.endswith("\n"), "| page code ends with newline:", code_text.endswith("\n"))
    print("   page last 30 chars:", repr(code_text[-30:]), " twin last 30:", repr(twin[-30:]))
