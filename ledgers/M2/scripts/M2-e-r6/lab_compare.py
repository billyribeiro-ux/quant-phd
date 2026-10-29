"""Compare each project lab's page code with its twin, and run the twin under python -I -W error against the page's expected block."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
page = (ROOT / "course/modules/M/M2/project.html").read_text(encoding="utf-8")
sections = re.findall(r'<section class="lab[^"]*" id="(lab-M2-project-\d)".*?</section>', page, re.S)
for lab_id in ("lab-M2-project-1", "lab-M2-project-2", "lab-M2-project-3"):
    m = re.search(rf'id="{lab_id}".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin_path = ROOT / f"tests/labs/M2/{lab_id}.py"
    twin = twin_path.read_text(encoding="utf-8")
    print(f"== {lab_id}: page code == twin: {code == twin}  (page {len(code)} chars, twin {len(twin)} chars)")
    if code != twin:
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))[:60]))
    res = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, timeout=120)
    print(f"   twin exit={res.returncode} stderr={res.stderr.strip()[:300]!r}")
    print(f"   stdout == expected block: {res.stdout.rstrip() == expected.rstrip()}")
    if res.stdout.rstrip() != expected.rstrip():
        print("   ACTUAL:\n" + res.stdout)
