"""Round-9 checks: starter fails on seeds 0-49 with named messages only; v9 mutant failure text on seed 0 under --assert=plain."""
import os, pathlib, shutil, subprocess, sys, tempfile
ROOT = pathlib.Path(sys.argv[1])
PY = ROOT / ".venv/bin/python"
G = ROOT / "course/modules/BK/BK4/grader"
def run(candidate, seed):
    work = pathlib.Path(tempfile.mkdtemp(prefix="bk4r9_"))
    try:
        shutil.copy(G / "test_project.py", work); shutil.copy(G / "instance.py", work)
        shutil.copy(candidate, work / "clearing_house.py")
        env = dict(os.environ, QF_SEED=str(seed), PYTHONDONTWRITEBYTECODE="1")
        p = subprocess.run([str(PY), "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                           cwd=work, env=env, capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr
    finally:
        shutil.rmtree(work, ignore_errors=True)
starter = G / "starter.py"
passes = 0; nameless = 0; tracebacks = 0
for seed in range(50):
    rc, out = run(starter, seed)
    passes += rc == 0
    if "has no implementation for" not in out: nameless += 1
    if "NotImplementedError" in out or "Traceback" in out: tracebacks += 1
print(f"starter: passed {passes}/50; seeds without the named message {nameless}; seeds with traceback text {tracebacks}")
rc, out = run(starter, 0)
print("starter seed 0 first lines:"); print("\n".join(out.splitlines()[:6]))
for name in ["v9b_waterfall_always_prorates_the_residual.py", "v9d_margin_for_cover_scan_is_strict.py"]:
    rc, out = run(ROOT / "ledgers/BK4/mutants" / name, 0)
    print("==", name, "rc", rc)
    print("\n".join(l for l in out.splitlines() if l.startswith("E ") or "fail" in l.lower())[:900])
