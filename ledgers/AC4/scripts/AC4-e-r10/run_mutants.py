"""Run each AC4 project mutant against the current grader; print KILLED/SURVIVED per seed set."""
import shutil, subprocess, sys, pathlib, os
ROOT = pathlib.Path(sys.argv[1]).resolve()        # checkout
MUT = ROOT / "ledgers/AC4/mutants"
GRADER = ROOT / "course/modules/AC/AC4/grader"
SCR = pathlib.Path(sys.argv[2]).resolve()          # scratch dir
PY = str(ROOT / ".venv/bin/python")
seeds = [int(s) for s in sys.argv[3].split(",")] if len(sys.argv) > 3 else [0]
for m in sorted(MUT.glob("*.py")):
    results = []
    for seed in seeds:
        d = SCR / m.stem / str(seed)
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
        for f in ("instance.py", "test_project.py", "starter.py"):
            shutil.copy(GRADER / f, d / f)
        shutil.copy(m, d / "budget_engine.py")
        env = dict(os.environ, QF_SEED=str(seed))
        p = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                            "test_project.py"], cwd=d, env=env, capture_output=True, text=True)
        last = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr.strip()[-200:]
        failed = [l for l in p.stdout.splitlines() if l.startswith("FAILED")]
        results.append((seed, p.returncode, last, failed[:1]))
    killed = any(rc != 0 for _, rc, _, _ in results)
    print(("KILLED  " if killed else "SURVIVED"), m.name)
    for seed, rc, last, failed in results:
        print("    seed", seed, "rc", rc, last, failed[0][:150] if failed else "")
