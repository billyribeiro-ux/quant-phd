"""Round-5 independent check of LX1 project labs (slice c).

Twin run under python -I -W error in a scratch directory (data copied in), page code vs twin, expected block vs output.
"""

import difflib
import html
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE5-LX1-c")
OUT = ROOT / "ledgers/LX1/scripts/LX1-c-r5/out"
PAGE = (ROOT / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
DATA = ROOT / "course/assets/data/market/fx_monthly.csv"

for n in (1, 2, 3):
    lab_id = f"lab-LX1-project-{n}"
    sec = re.search(r'<section class="lab[^"]*" id="%s".*?</section>' % lab_id, PAGE, re.S)
    body = sec.group(0)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S).group(1)
    code = html.unescape(code)
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1))
    twin = (ROOT / f"tests/labs/LX1/{lab_id}.py").read_text(encoding="utf-8")
    same = code.rstrip("\n") == twin.rstrip("\n")
    print(f"{lab_id}: page code == twin (trailing newline aside): {same}")
    if not same:
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))[:80]))
    wd = tempfile.mkdtemp(prefix="lx1c-r5-")
    os.makedirs(f"{wd}/data")
    shutil.copy(DATA, f"{wd}/data/fx_monthly.csv")
    r = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/LX1/{lab_id}.py")],
        cwd=wd,
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin"},
    )
    print(f"  rc={r.returncode} stderr={r.stderr!r}")
    print(f"  stdout == expected block: {r.stdout.rstrip() == exp.rstrip()}")
    open(OUT / f"{lab_id}.stdout", "w").write(r.stdout)
    open(OUT / f"{lab_id}.expected", "w").write(exp)
    shutil.rmtree(wd)
