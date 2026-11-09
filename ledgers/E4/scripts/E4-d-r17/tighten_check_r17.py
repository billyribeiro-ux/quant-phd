"""Round 17: scratch experiment, not a change to the suite. Copies the suite and instance.py to a scratch root outside
the checkout, replaces TOL_GAP by 1e-14 in the three gap comparisons at (original) lines 251, 312 and 377, and runs
run_candidate_r17.py on seeds 0-49 for reference.py, alt_1..alt_8 and mutant_v17_02. Usage: tighten_check_r17.py <checkout>"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(tempfile.mkdtemp(prefix="e4tight-"))
grader = root / "course/modules/E/E4/grader"
dst = scratch / "course/modules/E/E4/grader"
dst.mkdir(parents=True)
shutil.copy(grader / "instance.py", dst / "instance.py")
src = (grader / "test_project.py").read_text(encoding="utf-8")
reps = [
    ('abs(out["indifference_gap"] - oracle_gap(out["informed_fraction"], sd, cost)) <= TOL_GAP,',
     'abs(out["indifference_gap"] - oracle_gap(out["informed_fraction"], sd, cost)) <= 1e-14,'),
    ('abs(out["indifference_gap"] - oracle_gap(0.0, 0.6, 2.0)) <= TOL_GAP,',
     'abs(out["indifference_gap"] - oracle_gap(0.0, 0.6, 2.0)) <= 1e-14,'),
    ('abs(out["indifference_gap"] - oracle_gap(0.0, 0.6, 0.30)) <= TOL_GAP,',
     'abs(out["indifference_gap"] - oracle_gap(0.0, 0.6, 0.30)) <= 1e-14,'),
]
for old, new in reps:
    assert src.count(old) == 1, old
    src = src.replace(old, new)
(dst / "test_project.py").write_text(src, encoding="utf-8")
env = dict(os.environ, E4_ROOT=str(scratch))
cands = [grader / "reference.py"] + sorted((root / "ledgers/E4/alternatives").glob("alt_*.py")) + [
    root / "ledgers/E4/mutants/mutant_v17_02_price_slope_drops_uninformed_term.py"]
for cand in cands:
    r = subprocess.run([str(root / ".venv/bin/python"), "-I", str(root / "ledgers/E4/scripts/E4-d-r17/run_candidate_r17.py"), str(cand), "0-49"],
                       capture_output=True, text=True, env=env)
    print(r.stdout.strip().splitlines()[0] if r.stdout.strip() else r.stderr[-200:])
print("scratch root", scratch)
