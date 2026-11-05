import glob, os, shutil, subprocess, tempfile
ROOT = "/Users/billyribeiro/.fanout/wt/verifyE8-PC3-c"
GRADER = f"{ROOT}/course/modules/PC/PC3/grader"
PY = f"{ROOT}/.venv/bin/python"
files = sorted(glob.glob(f"{ROOT}/ledgers/PC3/alternatives/alt*.py")
               + glob.glob(f"{ROOT}/ledgers/PC3/scripts/PC3-c-r*/alts/*.py")
               + glob.glob(f"{ROOT}/ledgers/PC3/scripts/PC3-c-r*/alt*.py"))
flags = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
seeds = list(range(0, 50)) + [50, 848197495]
for path in files:
    if "alt_r8_" in path:
        continue
    work = tempfile.mkdtemp(prefix="pc3alt-old-")
    for name in ("engine.py", "instance.py", "test_project.py"):
        shutil.copy(os.path.join(GRADER, name), work)
    shutil.copy(path, os.path.join(work, "market_maker.py"))
    failed = []
    for seed in seeds:
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        r = subprocess.run([PY, "-m", "pytest", *flags, "test_project.py"], cwd=work, env=env, capture_output=True, text=True)
        if r.returncode != 0:
            failed.append(seed)
    print(f"{os.path.relpath(path, ROOT)}: fails on {len(failed)} of {len(seeds)} seeds {failed[:8]}")
    shutil.rmtree(work, ignore_errors=True)
