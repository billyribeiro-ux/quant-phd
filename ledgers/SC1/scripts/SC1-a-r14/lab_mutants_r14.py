"""Round-14 SC1-a: run the three new lab student-error mutants (ledgers/SC1/lab-mutants/*.py)
alone under python -I -W error from an empty cwd, and compare stdout with the page's expected block."""
import difflib
import glob
import html
import os
import re
import subprocess
import tempfile

ROOT = "/Users/billyribeiro/.fanout/wt/verifyE14-SC1-a"
PY = os.path.join(ROOT, ".venv/bin/python")
PAGE_FOR = {"L01": "L01", "L02": "L02", "L03": "L03"}
for mpath in sorted(glob.glob(os.path.join(ROOT, "ledgers/SC1/lab-mutants/*.py"))):
    name = os.path.basename(mpath)
    page = re.search(r"-(L0[123])-", name).group(1)
    src = open(os.path.join(ROOT, "course/modules/SC/SC1", page + ".html"), encoding="utf-8").read()
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S).group(1)).strip()
    with tempfile.TemporaryDirectory() as d:
        r = subprocess.run([PY, "-I", "-W", "error", mpath], cwd=d, capture_output=True, text=True)
    out = r.stdout.strip()
    killed = out != exp
    print(f"{name}: rc={r.returncode} stderr={r.stderr.strip()[-200:]!r} killed_by_expected_block={killed}")
    if killed:
        print("\n".join(list(difflib.unified_diff(exp.splitlines(), out.splitlines(), lineterm=""))[:12]))
