"""Run each AC4 project mutant against the current grader for each seed; print KILLED/SURVIVED per mutant."""
import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(sys.argv[1]).resolve()  # checkout
SCR = pathlib.Path(sys.argv[2]).resolve()  # scratch dir
seeds = [int(s) for s in sys.argv[3].split(",")]
MUT_DIRS = [ROOT / "ledgers/AC4/mutants"]
if len(sys.argv) > 4:
    MUT_DIRS = [pathlib.Path(p).resolve() for p in sys.argv[4].split(",")]
GRADER = ROOT / "course/modules/AC/AC4/grader"
PY = str(ROOT / ".venv/bin/python")
for mdir in MUT_DIRS:
    for m in sorted(mdir.glob("*.py")):
        results = []
        for seed in seeds:
            d = SCR / m.stem / str(seed)
            if d.exists():
                shutil.rmtree(d)
            d.mkdir(parents=True)
            for f in ("instance.py", "test_project.py", "starter.py"):
                shutil.copy(GRADER / f, d / f)
            shutil.copy(m, d / "budget_engine.py")
            env = dict(os.environ, QF_SEED=str(seed), PYTHONHASHSEED="0")
            p = subprocess.run(
                [PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                cwd=d,
                env=env,
                capture_output=True,
                text=True,
                timeout=300,
            )
            failed = [line for line in p.stdout.splitlines() if line.startswith("FAILED")]
            results.append((seed, p.returncode, failed[0][:160] if failed else ""))
        killed = any(rc != 0 for _, rc, _ in results)
        print(("KILLED  " if killed else "SURVIVED"), m.name, flush=True)
        for seed, rc, failed in results:
            print("    seed", seed, "rc", rc, failed, flush=True)
