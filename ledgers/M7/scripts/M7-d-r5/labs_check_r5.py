"""Check the three project labs: page code vs twin, twin run alone under python -I -W error, output vs expected block."""

import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD5-M7-d")
PY = str(ROOT / ".venv/bin/python")
page = (ROOT / "course/modules/M/M7/project.html").read_text(encoding="utf-8")
for n in (1, 2, 3):
    lab_id = f"lab-M7-project-{n}"
    sec = page[page.index(f'id="{lab_id}"'):]
    sec = sec[: sec.index("</section>")]
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin_path = ROOT / f"tests/labs/M7/{lab_id}.py"
    twin = twin_path.read_text(encoding="utf-8")
    same = code.rstrip("\n") == twin.rstrip("\n")
    print(f"{lab_id}: page code == twin: {same}")
    if not same:
        for line in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm="", n=0):
            print("   ", line)
    # run the twin alone (as the twin file) under -I -W error
    res = subprocess.run([PY, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp")
    print(f"{lab_id}: twin exit {res.returncode}, stderr bytes {len(res.stderr)}")
    print(f"{lab_id}: twin output == expected block: {res.stdout.rstrip(chr(10)) == expected.rstrip(chr(10))}")
    if res.stdout.rstrip("\n") != expected.rstrip("\n"):
        print(res.stdout)
        print("--- expected ---")
        print(expected)
