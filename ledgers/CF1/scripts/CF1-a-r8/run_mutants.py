"""Run each lab mutant against the unmutated twin it was derived from (round 7, slice CF1-a).

A mutant is killed when its stdout differs from the twin's stdout (the twin's stdout is the page's expected block,
which run_labs checks), or when it raises.
Usage: python -I run_mutants.py <checkout> <mutant-dir> <out-json>
"""
import difflib
import json
import subprocess
import sys
from pathlib import Path

checkout, mdir, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
twins = {"L01": checkout / "tests/labs/CF1/lab-CF1-L01-1.py", "L02": checkout / "tests/labs/CF1/lab-CF1-L02-1.py"}


def run(path: Path) -> tuple[int, str]:
    p = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True, timeout=60)
    return p.returncode, p.stdout


base_out = {k: run(v) for k, v in twins.items()}
results = []
for m in sorted(mdir.glob("*.py")):
    src = m.read_text()
    # the base twin is the one whose body the mutant shares the most lines with
    best = max(twins, key=lambda k: difflib.SequenceMatcher(None, twins[k].read_text(), src).ratio())
    rc, so = run(m)
    base_rc, base_so = base_out[best]
    killed = (rc != 0) or (so != base_so)
    results.append({"mutant": m.name, "base": best, "returncode": rc, "killed": killed,
                    "first_diff_line": next((d for d in difflib.unified_diff(base_so.splitlines(), so.splitlines(), lineterm="", n=0)
                                             if d.startswith(("+", "-")) and not d.startswith(("+++", "---"))), "")})
out.write_text(json.dumps(results, indent=1))
for r in results:
    print(r["mutant"], r["base"], "killed" if r["killed"] else "SURVIVED", r["first_diff_line"][:90])
