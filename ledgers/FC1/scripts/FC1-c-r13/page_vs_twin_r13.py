"""Round-13: compare each project lab's page code block with its twin, and the expected block with the twin's output."""
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/FC/FC1/project.html").read_text(encoding="utf-8")
for lab in ("lab-FC1-project-1", "lab-FC1-project-2", "lab-FC1-project-3"):
    m = re.search(rf'<section class="lab[^"]*" id="{lab}".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin = (root / f"tests/labs/FC1/{lab}.py").read_text(encoding="utf-8")
    print(lab, "page code == twin:", code == twin, "| code lines", code.count("\n"), "twin lines", twin.count("\n"))
    if code != twin:
        import difflib
        print("\n".join(difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm="")))
    out = subprocess.run([str(root / ".venv/bin/python"), "-I", "-W", "error", str(root / f"tests/labs/FC1/{lab}.py")],
                         capture_output=True, text=True)
    print(lab, "twin exit", out.returncode, "stderr", repr(out.stderr[:200]))
    print(lab, "expected == output:", expected.strip() == out.stdout.strip())
    if expected.strip() != out.stdout.strip():
        print("EXPECTED:\n" + expected + "\nOUTPUT:\n" + out.stdout)
