"""Round 4 check: page code equals twin; expected block equals twin output; twin runs alone under python -I -W error."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
for page, lab in (("L07", "lab-E3-L07-1"), ("L08", "lab-E3-L08-1")):
    text = (ROOT / f"course/modules/E/E3/{page}.html").read_text(encoding="utf-8")
    sec = re.search(rf'<section class="lab" id="{lab}".*?</section>', text, re.S).group(0)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin_path = ROOT / f"tests/labs/E3/{lab}.py"
    twin = twin_path.read_text(encoding="utf-8")
    print(page, "page code == twin.rstrip('\\n'):", code == twin.rstrip("\n"), "| == twin exact:", code == twin)
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True)
    print(page, "twin exit", r.returncode, "stderr:", repr(r.stderr[:200]))
    print(page, "expected == stdout:", expected.rstrip("\n") == r.stdout.rstrip("\n"))
    if expected.rstrip("\n") != r.stdout.rstrip("\n"):
        import difflib
        print("\n".join(difflib.unified_diff(expected.splitlines(), r.stdout.splitlines(), lineterm="")))
