"""Run every alternative engine of this checkout (all rounds, de-duplicated by content) against the CF1 suite, seeds 0-9."""
import glob, hashlib, os, shutil, subprocess, tempfile

CHK = "/tmp/verify22-CF1-d"
G = f"{CHK}/course/modules/CF/CF1/grader"
PY = f"{CHK}/.venv/bin/python"
files = sorted(glob.glob(f"{CHK}/ledgers/CF1/scripts/CF1-d-r*/alts/*.py") + glob.glob(f"{CHK}/ledgers/CF1/scripts/CF1-d-r*/e/alts/*.py"))
seen: dict[str, str] = {}
for f in files:
    digest = hashlib.sha256(open(f, "rb").read()).hexdigest()
    seen.setdefault(digest, f)
print(f"{len(files)} files, {len(seen)} unique", flush=True)
for digest, alt in seen.items():
    bad = []
    for s in range(10):
        w = tempfile.mkdtemp(prefix="alt22-")
        shutil.copy(f"{G}/test_project.py", w)
        shutil.copy(f"{G}/instance.py", w)
        shutil.copy(alt, os.path.join(w, "capbudget.py"))
        r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                           cwd=w, capture_output=True, text=True,
                           env={"PATH": os.environ["PATH"], "QF_SEED": str(s), "PYTHONHASHSEED": "0"})
        if r.returncode != 0:
            bad.append((s, [l for l in r.stdout.splitlines() if l.startswith("FAILED")][:2]))
        shutil.rmtree(w)
    rel = os.path.relpath(alt, CHK)
    print(f"{rel}: " + ("PASS (10 seeds)" if not bad else f"FAIL seeds={[b[0] for b in bad]} {bad[0][1]}"), flush=True)
print("done", flush=True)
