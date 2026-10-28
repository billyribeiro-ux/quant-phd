"""Compare each lesson's embedded code and expected output with its lab twin and a live run."""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PY = sys.argv[2]
for lesson in ("L01", "L02", "L03"):
    page = (ROOT / f"course/modules/E/E1/{lesson}.html").read_text(encoding="utf-8")
    twin = (ROOT / f"tests/labs/E1/lab-E1-{lesson}-1.py").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    page_code = html.unescape(code.group(1))
    page_out = html.unescape(expected.group(1))
    print(lesson, "code identical to twin:", page_code.rstrip("\n") == twin.rstrip("\n"))
    run = subprocess.run([PY, "-I", "-W", "error", str(ROOT / f"tests/labs/E1/lab-E1-{lesson}-1.py")],
                         capture_output=True, text=True, check=False)
    print(lesson, "live run exit:", run.returncode, "stderr bytes:", len(run.stderr))
    print(lesson, "page expected equals live stdout:", page_out.strip("\n") == run.stdout.strip("\n"))
    if page_out.strip("\n") != run.stdout.strip("\n"):
        import difflib
        for line in difflib.unified_diff(page_out.splitlines(), run.stdout.splitlines(), lineterm=""):
            print("   ", line)
