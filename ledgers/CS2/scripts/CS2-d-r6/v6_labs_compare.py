"""Round-6 lab check for CS2 project labs: page code vs twin, expected block vs twin output (run alone, -I -W error)."""

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/CS/CS2/project.html").read_text(encoding="utf-8")
for i in (1, 2, 3):
    sec = re.search(rf'<section class="lab[^"]*" id="lab-CS2-project-{i}".*?</section>', page, re.S).group(0)
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin_path = root / f"tests/labs/CS2/lab-CS2-project-{i}.py"
    twin = twin_path.read_text(encoding="utf-8")
    print(f"== lab {i}: page code == twin: {code == twin}; page code len {len(code)} twin len {len(twin)}")
    if code != twin:
        import difflib
        for line in list(difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""))[:40]:
            print("   ", line)
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp")
    print(f"   twin exit={out.returncode} stderr={out.stderr.strip()[:200]!r}")
    print(f"   expected block == twin stdout: {expected.strip() == out.stdout.strip()}")
    if expected.strip() != out.stdout.strip():
        print("   expected:", repr(expected.strip()[:300]))
        print("   stdout:  ", repr(out.stdout.strip()[:300]))
    print("   stdout:")
    print("   " + out.stdout.replace("\n", "\n   "))
