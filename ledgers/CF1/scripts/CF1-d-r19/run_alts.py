import glob, os, shutil, subprocess, sys, tempfile
G = "/tmp/verify19-CF1-d/course/modules/CF/CF1/grader"
PY = "/tmp/verify19-CF1-d/.venv/bin/python"
alts = sorted(set(glob.glob("/tmp/verify19-CF1-d/ledgers/CF1/scripts/CF1-d-r*/alts/*.py") + glob.glob("/tmp/CF1-v/d19/alts/*.py")))
seeds = list(range(int(sys.argv[1]) if len(sys.argv) > 1 else 10))
for alt in alts:
    results = []
    for s in seeds:
        w = tempfile.mkdtemp(prefix="alt19-")
        shutil.copy(f"{G}/test_project.py", w)
        shutil.copy(f"{G}/instance.py", w)
        shutil.copy(alt, os.path.join(w, "capbudget.py"))
        r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                           cwd=w, capture_output=True, text=True, env={"PATH": os.environ["PATH"], "QF_SEED": str(s), "PYTHONHASHSEED": "0"})
        if r.returncode != 0:
            fails = [l for l in r.stdout.splitlines() if l.startswith("FAILED")]
            results.append((s, fails[:2] or r.stdout[-300:]))
        shutil.rmtree(w)
    status = "PASS" if not results else f"FAIL {results[0]}"
    print(f"{os.path.basename(alt)}: {status} ({len(seeds)} seeds)" if not results else f"{os.path.basename(alt)}: FAIL seeds={[x[0] for x in results]} {results[0][1]}")
