import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1])
PY = str(ROOT / ".venv/bin/python")
MUTDIR = ROOT / "ledgers/CF1/mutants/CF1-b-r17"
NEWDIR = ROOT / "ledgers/CF1/mutants/CF1-b-r23"


def expected(lab: str) -> list[str]:
    s = (ROOT / f"course/modules/CF/CF1/{lab}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', s, re.S)
    return html.unescape(m.group(1)).strip().splitlines()


files = sorted(MUTDIR.glob("*.py")) + sorted(NEWDIR.glob("*.py")) if NEWDIR.exists() else sorted(MUTDIR.glob("*.py"))
for f in files:
    lab = "L04" if "L04" in f.name else "L03"
    r = subprocess.run([PY, "-I", "-W", "error", str(f)], capture_output=True, text=True)
    got = r.stdout.strip().splitlines()
    exp = expected(lab)
    if r.returncode != 0:
        status = "KILLED (nonzero exit)"
    elif got == exp:
        status = "SURVIVES (exit 0, output identical to page expected block)"
    else:
        diffs = [i for i, (a, b) in enumerate(zip(got, exp)) if a != b]
        status = f"KILLED (output differs at line {diffs[:1] or [min(len(got), len(exp))]}, expected {exp[diffs[0]] if diffs else '<end>'!r} got {got[diffs[0]] if diffs else '<end>'!r})"
    print(f.name, status, "rc", r.returncode)
