"""Round 1 (M5 slice d, closing delta): per-seed kill check of the three round-6 mutants on seeds 0-9, the
collect-only count and the seed-0 pass count of the grader on the reference, and each project twin run alone under
python -I -W error. Usage: r6_seeds_collect_twins_r1.py <repo-root> <scratch-dir>
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(sys.argv[1])
SCRATCH = Path(sys.argv[2])
PY = str(REPO / ".venv/bin/python")
G = REPO / "course/modules/M/M5/grader"


def workspace(solver: Path) -> Path:
    work = Path(tempfile.mkdtemp(prefix="m5d1r_", dir=SCRATCH))
    shutil.copy(G / "test_project.py", work / "test_project.py")
    shutil.copy(G / "instance.py", work / "instance.py")
    shutil.copy(solver, work / "contraction_solver.py")
    return work


def pytest_run(work: Path, seed: int, extra: list[str]) -> subprocess.CompletedProcess[str]:
    env = {"QF_SEED": str(seed), "PATH": "/usr/bin:/bin"}
    return subprocess.run(
        [PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", *extra],
        cwd=work,
        env=env,
        capture_output=True,
        text=True,
    )


for mut in sorted((REPO / "ledgers/M5/mutants").glob("r6_*.py")):
    work = workspace(mut)
    try:
        rcs = [pytest_run(work, s, ["test_project.py"]).returncode for s in range(10)]
        print(f"{mut.name}: rc per seed 0-9 {rcs}; killed on {sum(1 for r in rcs if r != 0)}/10")
    finally:
        shutil.rmtree(work, ignore_errors=True)

ref = REPO / "course/modules/M/M5/grader/reference.py"
work = workspace(ref)
try:
    col = subprocess.run(
        [PY, "-I", "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "test_project.py"],
        cwd=work,
        env={"QF_SEED": "0", "PATH": "/usr/bin:/bin"},
        capture_output=True,
        text=True,
    )
    print("collect-only tail:", col.stdout.strip().splitlines()[-1] if col.stdout.strip() else col.stderr[-300:])
    ok = pytest_run(work, 0, ["test_project.py"])
    print("reference seed 0 rc:", ok.returncode, ok.stdout.strip().splitlines()[-1])
finally:
    shutil.rmtree(work, ignore_errors=True)

for lab in ["lab-M5-project-1", "lab-M5-project-2", "lab-M5-project-3"]:
    twin = REPO / "tests/labs/M5" / f"{lab}.py"
    scratch = Path(tempfile.mkdtemp(prefix="m5d1t_", dir=SCRATCH))
    try:
        r = subprocess.run([PY, "-I", "-W", "error", str(twin)], cwd=scratch, capture_output=True, text=True)
        print(f"{lab}: rc {r.returncode}, stdout lines {len(r.stdout.splitlines())}, stderr bytes {len(r.stderr)}")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
