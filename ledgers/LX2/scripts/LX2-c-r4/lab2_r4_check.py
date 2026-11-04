"""LX2-c round 4: run every rung-2 instant-check candidate against the page's expected block (whole-block equality).

Mutants (ledgers/LX2/mutants/*lab2*.py, complete programs) must NOT equal the expected block (killed).
Correct alternatives (scripts/LX2-c-r4/alts/*.py) MUST equal it (pass).
Run from the checkout root: .venv/bin/python -I ledgers/LX2/scripts/LX2-c-r4/lab2_r4_check.py
"""

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
PAGE = (ROOT / "course/modules/LX/LX2/project.html").read_text(encoding="utf-8")
EXP_RE = re.compile(r'<pre class="expected"[^>]*>(.*?)</pre>', re.S)
expected = html.unescape(EXP_RE.findall(PAGE)[1]).rstrip("\n")
scratch = Path(tempfile.mkdtemp(prefix="lx2c-r4-lab2-"))


def run(path: Path) -> tuple[int, str, str]:
    p = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True, cwd=str(scratch))
    return p.returncode, p.stdout.rstrip("\n"), p.stderr.strip()


mutants = sorted((ROOT / "ledgers/LX2/mutants").glob("*lab2*.py"))
alts = sorted((ROOT / "ledgers/LX2/scripts/LX2-c-r4/alts").glob("*.py"))
bad = 0
for m in mutants:
    rc, out, err = run(m)
    killed = (rc != 0) or (out != expected)
    first_diff = next((i for i, (a, b) in enumerate(zip(out.split("\n"), expected.split("\n"))) if a != b), None)
    print(f"MUTANT {m.name}: exit={rc} killed={killed} first_differing_line={first_diff} stderr={err[:80]!r}")
    print(f"    line: {out.split(chr(10))[first_diff] if first_diff is not None and out else '-'}")
for a in alts:
    rc, out, err = run(a)
    passed = rc == 0 and out == expected
    bad += 0 if passed else 1
    print(f"ALT {a.name}: exit={rc} whole_block_equal={out == expected} stderr={err[:80]!r}")
print("alternatives failing:", bad)
