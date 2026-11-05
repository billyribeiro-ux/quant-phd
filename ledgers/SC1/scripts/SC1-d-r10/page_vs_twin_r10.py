"""Compare each project.html lab's data-run code and expected block with its twin and with the twin's run output."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
page = (root / "course/modules/SC/SC1/project.html").read_text(encoding="utf-8")
sections = re.findall(r'<section class="lab[^"]*" id="(lab-SC1-project-\d)".*?</section>', page, re.S)
for lab_id in sections:
    m = re.search(r'id="%s".*?<pre><code class="language-python" data-run>(.*?)</code></pre>' % lab_id, page, re.S)
    code = html.unescape(m.group(1))
    e = re.search(r'id="%s".*?<pre class="expected"[^>]*>(.*?)</pre>' % lab_id, page, re.S)
    expected = html.unescape(e.group(1))
    twin = (root / "tests/labs/SC1" / f"{lab_id}.py").read_text(encoding="utf-8")
    same = code == twin
    print(f"{lab_id}: page code == twin: {same}; code lines {len(code.splitlines())}, twin lines {len(twin.splitlines())}")
    if not same:
        import difflib
        for line in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm="", n=0):
            print("   ", line)
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(root / "tests/labs/SC1" / f"{lab_id}.py")],
                         capture_output=True, text=True, cwd=root)
    print(f"{lab_id}: twin exit {out.returncode}; expected block == twin stdout: {expected.strip() == out.stdout.strip()}")
    if expected.strip() != out.stdout.strip():
        print("EXPECTED:", repr(expected)); print("STDOUT:", repr(out.stdout))
