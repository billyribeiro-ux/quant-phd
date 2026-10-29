"""For each E1 slice lab: the page code equals the twin file, the expected block equals the twin's stdout under python -I -W error."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for page, lab in (("L01", "lab-E1-L01-1"), ("L02", "lab-E1-L02-1"), ("L03", "lab-E1-L03-1")):
    twin = (root / "tests/labs/E1" / f"{lab}.py").read_text(encoding="utf-8")
    src = (root / "course/modules/E/E1" / f"{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, flags=re.S).group(1)
    code = html.unescape(code)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, flags=re.S).group(1)
    expected = html.unescape(re.sub(r"<[^>]+>", "", expected))
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(root / "tests/labs/E1" / f"{lab}.py")],
                         capture_output=True, text=True, check=True).stdout
    print(page, lab, "page code == twin:", code.strip() == twin.strip(),
          "| expected == run stdout:", expected.strip() == run.strip(), "| lines:", len(run.splitlines()))
    if expected.strip() != run.strip():
        for a, b in zip(expected.splitlines(), run.splitlines()):
            if a != b:
                print("  DIFF expected:", a, "| run:", b)
