"""Compare each project lab's code block on project.html with its twin, and its expected block with the twin's output."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/SC/SC1/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    m = re.search(rf'<section[^>]*id="lab-SC1-project-{n}".*?<pre><code[^>]*>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin = (root / f"tests/labs/SC1/lab-SC1-project-{n}.py").read_text(encoding="utf-8")
    print(f"lab {n}: page code == twin: {code == twin} (page {len(code)} chars, twin {len(twin)} chars)")
    if code != twin:
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))[:60]))
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / f"tests/labs/SC1/lab-SC1-project-{n}.py")], capture_output=True, text=True).stdout
    print(f"lab {n}: expected == output: {out.strip() == expected.strip()}")
    if out.strip() != expected.strip():
        print("OUTPUT:\n" + out + "EXPECTED:\n" + expected)
