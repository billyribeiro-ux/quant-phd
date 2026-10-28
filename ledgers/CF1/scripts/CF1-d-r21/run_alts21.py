"""Run every alternative engine (all rounds, de-duplicated by content) against the CF1 suite of this checkout, seeds 0-9."""
import glob, hashlib, os, shutil, subprocess, sys, tempfile

CHK = "/tmp/verify21-CF1-d"
G = f"{CHK}/course/modules/CF/CF1/grader"
PY = f"{CHK}/.venv/bin/python"
files = sorted(glob.glob(f"{CHK}/ledgers/CF1/scripts/CF1-d-r*/alts/*.py"))
seen: dict[str, str] = {}
for f in files:
    digest = hashlib.sha256(open(f, "rb").read()).hexdigest()
    if digest in seen:
        continue
    seen[digest] = f
seeds = range(10)
print(f"{len(files)} files, {len(seen)} unique")
for digest, alt in seen.items():
    if os.path.basename(alt).startswith("ref_"):
        pass
    bad = []
    for s in seeds:
        w = tempfile.mkdtemp(prefix="alt20-")
        shutil.copy(f"{G}/test_project.py", w)
        shutil.copy(f"{G}/instance.py", w)
        shutil.copy(alt, os.path.join(w, "capbudget.py"))
        r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                           cwd=w, capture_output=True, text=True, env={"PATH": os.environ["PATH"], "QF_SEED": str(s), "PYTHONHASHSEED": "0"})
        if r.returncode != 0:
            bad.append((s, [l for l in r.stdout.splitlines() if l.startswith("FAILED")][:2]))
        shutil.rmtree(w)
    rel = os.path.relpath(alt, CHK)
    print(f"{rel}: " + ("PASS (10 seeds)" if not bad else f"FAIL seeds={[b[0] for b in bad]} {bad[0][1]}"), flush=True)
print("done")
