"""CF8-a round 3: page code equals twin, expected block equals twin output, twin runs under python -I -W error."""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = {"L01": "lab-CF8-L01-1", "L02": "lab-CF8-L02-1"}
for page, lab in PAGES.items():
    text = (ROOT / f"course/modules/CF/CF8/{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', text, re.S).group(1)
    code = html.unescape(code)
    twin = (ROOT / f"tests/labs/CF8/{lab}.py").read_text(encoding="utf-8")
    print(page, "code==twin (exact):", code == twin, "| len page", len(code), "len twin", len(twin), "| code.rstrip==twin.rstrip:", code.rstrip() == twin.rstrip())
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1))
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/CF8/{lab}.py")],
        capture_output=True, text=True, cwd="/tmp", env={"PYTHONHASHSEED": "0", "PATH": "/usr/bin:/bin"},
    )
    print(page, "twin exit", run.returncode, "stderr:", repr(run.stderr[:300]))
    print(page, "expected==stdout:", expected.strip() == run.stdout.strip())
    if expected.strip() != run.stdout.strip():
        import difflib
        print("\n".join(difflib.unified_diff(expected.strip().splitlines(), run.stdout.strip().splitlines(), lineterm="")))
    print(page, "stdout:")
    print(run.stdout)
