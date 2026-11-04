"""For each slice lab: page code equals twin, expected block equals the twin's real stdout (python -I -W error)."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PY = ROOT / ".venv/bin/python"
for lab in ["L04", "L05", "L06"]:
    page = (ROOT / f"course/modules/E/E4/{lab}.html").read_text(encoding="utf-8")
    sec = re.search(r'<section class="lab" id="lab-E4-%s-1".*?</section>' % lab, page, re.S).group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin_path = ROOT / f"tests/labs/E4/lab-E4-{lab}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    print(lab, "page code == twin:", code == twin, "(len page", len(code), "twin", len(twin), ")")
    if code != twin:
        import difflib
        for line in list(difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm=""))[:40]:
            print("   ", line)
    out = subprocess.run([str(PY), "-I", "-W", "error", str(twin_path)], capture_output=True, text=True,
                         cwd="/tmp/e4-v/b-r1")
    print(lab, "twin exit", out.returncode, "stderr", repr(out.stderr[:200]))
    print(lab, "expected == stdout:", expected.strip("\n") == out.stdout.strip("\n"))
    if expected.strip("\n") != out.stdout.strip("\n"):
        import difflib
        for line in difflib.unified_diff(expected.strip("\n").splitlines(), out.stdout.strip("\n").splitlines(), lineterm=""):
            print("   ", line)
