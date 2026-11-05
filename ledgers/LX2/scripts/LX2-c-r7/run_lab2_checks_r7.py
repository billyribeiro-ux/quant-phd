"""Run each candidate Lab 2 solution (mutant or alternative) under python -I -W error and apply the page's compare rule
(labs.js compareOutput: token count equal; numbers within 1e-6 * (1 + |expected|); other tokens exact)."""
import glob
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
html = (ROOT / "course/modules/LX/LX2/project.html").read_text(encoding="utf-8")
exp = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', html, re.S)[1]
import html as H
exp = H.unescape(exp)
NUM = re.compile(r"^[+-]?\d+(\.\d+)?$")


def same(actual: str, expected: str) -> tuple[bool, str]:
    a = actual.strip().split()
    e = expected.strip().split()
    if len(a) != len(e):
        return False, f"token count {len(a)} vs {len(e)}"
    for i, (x, y) in enumerate(zip(a, e)):
        if NUM.match(x) and NUM.match(y):
            if not abs(float(x) - float(y)) <= 1e-6 * (1 + abs(float(y))):
                return False, f"token {i + 1}: {x} vs {y}"
        elif x != y:
            return False, f"token {i + 1}: {x!r} vs {y!r}"
    return True, ""


files = sorted(set(glob.glob(str(ROOT / "ledgers/LX2/mutants/*lab2*.py"))
                   + glob.glob(str(ROOT / "ledgers/LX2/mutants/alt*.py"))
                   + glob.glob(str(ROOT / "ledgers/LX2/mutants/r7_*.py"))
                   + glob.glob(str(ROOT / "ledgers/LX2/scripts/LX2-c-r5/alts/*.py"))
                   + glob.glob(str(ROOT / "ledgers/LX2/scripts/LX2-c-r6/alts/*.py"))
                   + glob.glob(str(ROOT / "ledgers/LX2/scripts/LX2-c-r7/alts/*.py"))))
killed, survived = [], []
for f in files:
    p = subprocess.run([sys.executable, "-I", "-W", "error", f], capture_output=True, text=True, cwd="/tmp", timeout=60)
    if p.returncode != 0:
        killed.append((Path(f).name, f"exit {p.returncode}: {p.stderr.strip().splitlines()[-1][:120] if p.stderr.strip() else ''}"))
        continue
    ok, why = same(p.stdout, exp)
    if ok:
        survived.append(Path(f).name)
    else:
        killed.append((Path(f).name, why))
print(f"candidates: {len(files)}  killed: {len(killed)}  survived (print the expected block): {len(survived)}")
for n, why in killed:
    print("KILLED  ", n, "|", why)
for n in survived:
    print("SURVIVED", n)
