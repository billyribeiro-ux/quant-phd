"""Round-5: run every LX1 lab mutant (ledgers/LX1/mutants) and every alternative correct implementation (gen/)
against the expected block of its lab on the project page. Mutants must NOT match (killed); alternatives MUST match.
Token compare follows course/assets/js/labs.js compareOutput (numeric tokens within tol*(1+|e|))."""

import glob
import html
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE8-LX1-c")
PAGE = (ROOT / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
DATA = ROOT / "course/assets/data/market/fx_monthly.csv"
OUT = ROOT / "ledgers/LX1/scripts/LX1-c-r8/out"


def expected_for(n):
    sec = re.search(r'<section class="lab[^"]*" id="lab-LX1-project-%d".*?</section>' % n, PAGE, re.S).group(0)
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*data-tolerance="([^"]+)"[^>]*>(.*?)</pre>', sec, re.S).group(2))
    tol = float(re.search(r'<pre class="expected"[^>]*data-tolerance="([^"]+)"', sec).group(1))
    return exp, tol


def is_num(t):
    try:
        float(t)
        return True
    except ValueError:
        return False


def compare(actual, expected, tol):
    a = actual.strip().split()
    e = expected.strip().split()
    if len(a) != len(e):
        return False, f"token count {len(a)} vs {len(e)}"
    for x, y in zip(a, e):
        if is_num(x) and is_num(y):
            if abs(float(x) - float(y)) > tol * (1 + abs(float(y))):
                return False, f"numeric {x} vs {y}"
        elif x != y:
            return False, f"token {x!r} vs {y!r}"
    return True, "match"


def lab_of(path, text):
    m = re.search(r"project lab (\d)", text)
    if m:
        return int(m.group(1))
    m = re.search(r"lab(\d)", os.path.basename(path))
    return int(m.group(1))


def run(path, lab):
    exp, tol = expected_for(lab)
    wd = tempfile.mkdtemp(prefix="lx1c-r8-mut-")
    os.makedirs(f"{wd}/data")
    shutil.copy(DATA, f"{wd}/data/fx_monthly.csv")
    r = subprocess.run(
        [sys.executable, "-I", "-W", "error", path],
        cwd=wd,
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin"},
    )
    shutil.rmtree(wd)
    if r.returncode != 0:
        return False, f"rc={r.returncode} {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ''}"
    return compare(r.stdout, exp, tol)


rows = []
for path in sorted(glob.glob(str(ROOT / "ledgers/LX1/mutants/*.py"))):
    text = open(path, encoding="utf-8").read()
    lab = lab_of(path, text)
    ok, why = run(path, lab)
    rows.append(("MUTANT", os.path.basename(path), lab, "KILLED" if not ok else "SURVIVED", why))
for path in sorted(glob.glob(str(ROOT / "ledgers/LX1/scripts/LX1-c-r5/gen/*.py")) + glob.glob(str(ROOT / "ledgers/LX1/scripts/LX1-c-r6/gen/*.py")) + glob.glob(str(ROOT / "ledgers/LX1/scripts/LX1-c-r7/gen/*.py")) + glob.glob(str(ROOT / "ledgers/LX1/scripts/LX1-c-r8/gen/*.py"))):
    lab = lab_of(path, "")
    ok, why = run(path, lab)
    rows.append(("ALT", os.path.basename(path), lab, "MATCHES" if ok else "REJECTED", why))
for r in rows:
    print(" | ".join(str(x) for x in r))
open(OUT / "mutants_alts_r8.txt", "w").write("\n".join(" | ".join(str(x) for x in r) for r in rows) + "\n")
