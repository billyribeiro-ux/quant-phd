"""Round-3 verifier (E3-d): each E3 project lab's page code vs its twin, the twin run alone under python -I -W error,
and its stdout vs the page's expected block. Run from the repository root:
    .venv/bin/python -B ledgers/E3/scripts/E3-d-r3/labs_twins_r3.py
"""
import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(".")
page = (root / "course/modules/E/E3/project.html").read_text(encoding="utf-8")
pairs = {
    "lab-E3-project-1": "tests/labs/E3/lab-E3-project-1.py",
    "lab-E3-project-2": "tests/labs/E3/lab-E3-project-2.py",
    "lab-E3-project-3": "tests/labs/E3/lab-E3-project-3.py",
}
for lid, twin in pairs.items():
    start = page.index(f'id="{lid}"')
    block = page[start : page.index("</section>", start)]
    code = html.unescape(re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', block, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', block, re.S).group(1))
    twin_text = (root / twin).read_text(encoding="utf-8")
    diff = [
        line
        for line in difflib.unified_diff(
            code.rstrip("\n").splitlines(), twin_text.rstrip("\n").splitlines(), lineterm="", n=0
        )
        if not line.startswith(("---", "+++", "@@"))
    ]
    print(f"{lid}: page code vs twin differing lines: {len(diff)}")
    for line in diff:
        print("   ", line[:140])
    run = subprocess.run([sys.executable, "-I", "-W", "error", twin], capture_output=True, text=True, check=False)
    print(f"{lid}: twin exit={run.returncode} stderr_bytes={len(run.stderr)}")
    out = run.stdout.rstrip("\n").splitlines()
    exp = expected.rstrip("\n").splitlines()
    print(f"{lid}: stdout lines={len(out)} expected lines={len(exp)} identical={out == exp}")
