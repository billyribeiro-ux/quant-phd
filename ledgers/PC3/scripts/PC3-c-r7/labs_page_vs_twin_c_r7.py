"""Compare each project lab's page code with its twin, and each expected block with the twin's own output.

Read-only on the repo: writes nothing into it. Runs each twin with python -I -W error in a temp directory."""

import difflib
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE7-PC3-c")
PAGE = ROOT / "course/modules/PC/PC3/project.html"
PY = ROOT / ".venv/bin/python"
text = PAGE.read_text(encoding="utf-8")
for lab in ("lab-PC3-project-1", "lab-PC3-project-2", "lab-PC3-project-3"):
    m = re.search(rf'<section class="lab[^"]*" id="{lab}".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin = (ROOT / f"tests/labs/PC3/{lab}.py").read_text(encoding="utf-8")
    d = list(difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""))
    print(f"== {lab}: page code vs twin: {'IDENTICAL' if not d else 'DIFFERS'}; diff lines {len(d)}")
    for line in d[:40]:
        print("   ", line)
    work = Path(tempfile.mkdtemp(prefix="pc3lab7-"))
    (work / "twin.py").write_text(twin, encoding="utf-8")
    r = subprocess.run([str(PY), "-I", "-W", "error", "twin.py"], cwd=work, capture_output=True, text=True)
    print(f"   twin exit {r.returncode}; stderr bytes {len(r.stderr)}")
    out = r.stdout.rstrip("\n")
    exp = expected.rstrip("\n")
    print(f"   expected block == twin output: {out == exp}")
    if out != exp:
        for line in list(difflib.unified_diff(exp.splitlines(), out.splitlines(), "expected", "output", lineterm=""))[:30]:
            print("   ", line)
