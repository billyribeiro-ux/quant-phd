"""Run each unique alternative correct engine against the CF1 suite on seeds 0-9 (suite and instance copied from the grader)."""
import hashlib, os, pathlib, shutil, subprocess, tempfile, glob
CHK = pathlib.Path("/tmp/verify25-CF1-d")
G = CHK / "course/modules/CF/CF1/grader"
PY = CHK / ".venv/bin/python"
os.makedirs("/tmp/CF1-v/d25", exist_ok=True)
files = sorted(glob.glob(str(CHK / "ledgers/CF1/scripts/CF1-d-r*/alts/*.py")) + glob.glob(str(CHK / "ledgers/CF1/scripts/CF1-d-r*/e/alts/*.py")))
seen = {}
for f in files:
    seen.setdefault(hashlib.sha256(open(f, "rb").read()).hexdigest(), f)
print(len(files), "files,", len(seen), "unique", flush=True)
for alt in [pathlib.Path(f) for f in seen.values()]:
    bad = []
    for s in range(10):
        w = tempfile.mkdtemp(prefix="alt25-", dir="/tmp/CF1-v/d25")
        shutil.copy(G / "test_project.py", w)
        shutil.copy(G / "instance.py", w)
        shutil.copy(alt, os.path.join(w, "capbudget.py"))
        r = subprocess.run([str(PY), "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                           cwd=w, capture_output=True, text=True, env={"PATH": os.environ["PATH"], "QF_SEED": str(s), "PYTHONHASHSEED": "0"})
        if r.returncode != 0:
            bad.append((s, [l for l in r.stdout.splitlines() if l.startswith("FAILED")][:2]))
        shutil.rmtree(w)
    print(f"{alt.parent.parent.name}/{alt.name}: " + ("PASS (10 seeds)" if not bad else f"FAIL seeds={[b[0] for b in bad]} {bad[0][1]}"), flush=True)
