"""Run each probe quote/replay module as market_maker.py through the full PC3 suite (one process per seed, page flags)."""
import glob, os, shutil, subprocess, sys, tempfile
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE9-PC3-c"
GRADER = f"{ROOT}/course/modules/PC/PC3/grader"
PY = f"{ROOT}/.venv/bin/python"
flags = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
seeds = [int(s) for s in sys.argv[2].split(",")]
for path in sorted(glob.glob(sys.argv[1])):
    work = tempfile.mkdtemp(prefix="pc3probe-r9v-")
    for name in ("engine.py", "instance.py", "test_project.py"):
        shutil.copy(os.path.join(GRADER, name), work)
    shutil.copy(path, os.path.join(work, "market_maker.py"))
    res = []
    for seed in seeds:
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        r = subprocess.run([PY, "-m", "pytest", *flags, "test_project.py"], cwd=work, env=env, capture_output=True, text=True)
        last = (r.stdout.strip().splitlines() or [""])[-1]
        res.append((seed, r.returncode, last[:160]))
    failed = [s for s in res if s[1] != 0]
    print(f"{os.path.basename(path)}: failing {len(failed)}/{len(res)} seeds")
    for s in res[:3]:
        print("   ", s)
    shutil.rmtree(work, ignore_errors=True)
