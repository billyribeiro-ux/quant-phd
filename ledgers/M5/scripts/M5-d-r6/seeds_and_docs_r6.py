"""Round 6 (M5 slice d): per-seed kill check for the new and r5 mutants, docstring check for every mutant,
and collect-only count plus reference pass count on seeds 0-9 in a scratch workspace.
Usage: seeds_and_docs_r6.py <repo-root> <scratch-dir>
"""
import ast
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(sys.argv[1])
SCRATCH = Path(sys.argv[2])
G = REPO / "course/modules/M/M5/grader"
MUT = REPO / "ledgers/M5/mutants"
PY = REPO / ".venv/bin/python"


def run(candidate: Path, seed: int) -> int:
    work = Path(tempfile.mkdtemp(prefix="m5k6_", dir=SCRATCH))
    try:
        shutil.copy(G / "test_project.py", work / "test_project.py")
        shutil.copy(G / "instance.py", work / "instance.py")
        shutil.copy(candidate, work / "contraction_solver.py")
        r = subprocess.run(
            [str(PY), "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
             "test_project.py"],
            cwd=work, env={"QF_SEED": str(seed), "PATH": "/usr/bin:/bin"}, capture_output=True, text=True,
        )
        return r.returncode
    finally:
        shutil.rmtree(work, ignore_errors=True)


print("== per-seed kill check (rc != 0 means killed)")
for name in ["r6_01_stop_only_when_certified_error_strictly_below_tol.py",
             "r6_02_saving_must_leave_strictly_positive_consumption.py",
             "r6_03_solve_starts_from_the_ones_vector.py",
             "r5_01_resources_are_capital_below_one.py",
             "r5_02_value_is_the_bellman_image.py",
             "r5_03_utility_splits_the_root_of_the_difference.py"]:
    rcs = [run(MUT / name, s) for s in range(10)]
    print(f"{name}: killed on {sum(1 for rc in rcs if rc != 0)}/10 seeds; rc per seed {rcs}")

print("== reference on seeds 0-9 (rc 0 means pass)")
ref = REPO / "course/modules/M/M5/grader/reference.py"
print("reference:", [run(ref, s) for s in range(10)])

print("== docstrings of all mutants")
empty = []
files = sorted(MUT.glob("*.py"))
for f in files:
    doc = ast.get_docstring(ast.parse(f.read_text(encoding="utf-8")))
    if not doc or not doc.strip():
        empty.append(f.name)
print(f"mutant files: {len(files)}; empty docstrings: {empty}")
