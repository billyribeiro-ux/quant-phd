"""Compare project.html lab blocks with their twins and run each twin under python -I -W error.

Usage: python -I ledgers/E4/scripts/E4-d-r3/cmp_project_labs.py <repo-root>
Prints, per lab: the number of code lines on the page and in the twin, the non-blank differing lines, whether the
twin's stdout equals the expected block, and the exit code. Pure stdlib.
"""

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/E/E4/project.html").read_text(encoding="utf-8")
PY = sys.executable
for n in (1, 2, 3):
    lab_id = f"lab-E4-project-{n}"
    sec = re.search(rf'<section[^>]*id="{lab_id}".*?</section>', page, flags=re.S)
    assert sec, lab_id
    body = sec.group(0)
    code_m = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', body, flags=re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, flags=re.S)
    page_code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    twin = (root / f"tests/labs/E4/{lab_id}.py").read_text(encoding="utf-8")
    pl, tl = page_code.splitlines(), twin.splitlines()
    diffs = [(i, a, b) for i, (a, b) in enumerate(zip(pl, tl)) if a != b and (a.strip() or b.strip())]
    with tempfile.TemporaryDirectory(prefix="e4d3-lab-") as d:
        f = Path(d) / "twin.py"
        f.write_text(twin, encoding="utf-8")
        res = subprocess.run([PY, "-I", "-W", "error", str(f)], capture_output=True, text=True, cwd=d, timeout=120)
    print(f"{lab_id}: page lines={len(pl)} twin lines={len(tl)} code_equal={page_code == twin} "
          f"nonblank_diffs={diffs[:5]} exit={res.returncode}")
    print(f"  stdout == expected block: {res.stdout.rstrip() == expected.rstrip()}")
    if res.stdout.rstrip() != expected.rstrip():
        print("  stdout:", res.stdout)
        print("  expected:", expected)
    if res.stderr.strip():
        print("  stderr:", res.stderr.strip()[:500])
