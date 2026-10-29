"""Round 21 re-run of every committed AC4-a lab-twin mutant (r18, r19, r20).

For each mutant file, the lab id is read from its name prefix (L01 or L02). The mutant is run under
python -I -W error from a scratch directory. KILLED = nonzero exit, stderr output, or stdout that differs
from the page's embedded expected block. Lab mutants are demonstrations (architect ruling), so a survivor
is recorded as PASS (out of scope) unless a lesson sentence claims the lab checks that property.
"""
import html
import pathlib
import re
import subprocess
import sys
import tempfile

root = pathlib.Path(sys.argv[1]).resolve()
mut_root = root / "ledgers/AC4/mutants"


def expected(lab: str) -> str:
    page = "L01" if lab == "L01" else "L02"
    s = (root / "course/modules/AC/AC4" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', s, re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).rstrip("\n")


exp = {"L01": expected("L01"), "L02": expected("L02")}
results = []
for f in sorted(mut_root.glob("AC4-a-r*/*.py")):
    lab = f.name[:3]
    with tempfile.TemporaryDirectory() as d:
        p = subprocess.run([sys.executable, "-I", "-W", "error", str(f)], cwd=d, capture_output=True, text=True, timeout=60)
    out = p.stdout.rstrip("\n")
    if p.returncode != 0 or p.stderr:
        status = f"KILLED rc={p.returncode} stderr={bool(p.stderr)}"
    elif out != exp[lab]:
        status = "KILLED stdout differs"
    else:
        status = "SURVIVED (stdout identical, rc=0)"
    results.append(f"{f.relative_to(mut_root)}: {status}")
print("\n".join(results))
print(f"total {len(results)}")
