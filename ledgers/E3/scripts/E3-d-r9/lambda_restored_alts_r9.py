# Round 9: the local-maximum test with lambda moved again (test_project_lambda.py in the scratch workspace), run on the
# alternative correct implementations alt1, alt2, alt3, alt5 (built by run_alternatives.build) for seeds 0-9.
import os, shutil, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, "ledgers/E3/scripts")
from run_alternatives import build, GRADER
LAMBDA_TEST = Path("/tmp/E3d_r9_ws/test_project_lambda.py")
PY = sys.executable
for name in ("alt1", "alt2", "alt3", "alt5"):
    work = Path(tempfile.mkdtemp(prefix=f"r9lam-{name}-"))
    try:
        shutil.copy(GRADER / "instance.py", work / "instance.py")
        shutil.copy(LAMBDA_TEST, work / "test_project.py")
        (work / "elicit.py").write_text(build(name), encoding="utf-8")
        res = []
        for seed in range(10):
            r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                                "test_project.py", "-k", "local_maximum"], cwd=work, capture_output=True, text=True,
                               env={"PATH": os.environ["PATH"], "QF_SEED": str(seed), "PYTHONHASHSEED": "0"})
            res.append(f"{seed}:{'ok' if r.returncode == 0 else 'FAIL'}")
        print(name, " ".join(res), flush=True)
    finally:
        shutil.rmtree(work, ignore_errors=True)
print("DONE", flush=True)
