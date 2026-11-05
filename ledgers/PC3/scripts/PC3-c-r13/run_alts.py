"""Run each alternative as market_maker.py against test_project.py for seeds 0-49 (QF_SEED = seed), in scratch copies."""
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE13-PC3-c")
GRADER = ROOT / "course/modules/PC/PC3/grader"
PY = str(ROOT / ".venv/bin/python")
ALTS = sorted((ROOT / "ledgers/PC3/scripts/PC3-c-r13/alts").glob("*.py")) + [
    ROOT / "ledgers/PC3/scripts/PC3-c-r12/alts/alt_r12_a_turn_indexed_history.py"
]
for alt in ALTS:
    work = Path("/tmp/pc3c-r13-alt") / alt.stem
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    for name in ("engine.py", "instance.py", "test_project.py"):
        shutil.copy(GRADER / name, work / name)
    shutil.copy(alt, work / "market_maker.py")
    fails = []
    for seed in range(50):
        env = dict(os.environ, QF_SEED=str(seed))
        run = subprocess.run(
            [PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work, env=env, capture_output=True, text=True,
        )
        if run.returncode != 0:
            names = sorted({line.split("::")[1].split("[")[0] for line in run.stdout.splitlines() if line.startswith("FAILED")})
            last = run.stdout.strip().splitlines()[-1]
            fails.append((seed, names, last))
    print(f"{alt.name}: fails on {len(fails)} of 50 seeds")
    for seed, names, last in fails[:3]:
        print(f"   seed {seed}: {names} | {last}")
    if fails:
        print("   distinct failing tests:", sorted({n for _, ns, _ in fails for n in ns}))
    sys.stdout.flush()
