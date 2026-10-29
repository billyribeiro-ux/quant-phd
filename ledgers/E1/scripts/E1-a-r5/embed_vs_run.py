"""Compare each E1 lab twin's stdout (python -I -W error) with the output block embedded in its page."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for page, lab in (("L01", "lab-E1-L01-1"), ("L02", "lab-E1-L02-1"), ("L03", "lab-E1-L03-1")):
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(root / "tests/labs/E1" / f"{lab}.py")],
        capture_output=True, text=True, check=True,
    ).stdout
    src = (root / "course/modules/E/E1" / f"{page}.html").read_text(encoding="utf-8")
    blocks = re.findall(r"<pre[^>]*>(.*?)</pre>", src, flags=re.S)
    hits = [html.unescape(re.sub(r"<[^>]+>", "", b)) for b in blocks if "grid" in b or "case" in b]
    print(page, lab, "run lines:", len(run.splitlines()), "matching pre blocks:", len(hits))
    for h in hits:
        print("  pre identical to run output:", h.strip() == run.strip())
