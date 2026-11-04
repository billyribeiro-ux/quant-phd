import os, pathlib, shutil, subprocess, sys, tempfile
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD7-M4-d")
G = ROOT / "course/modules/M/M4/grader"
alt = ROOT / "ledgers/M4/equivalent/m17_student_t_second_seed.py"
ok = 0; bad = []
for s in range(50):
    w = pathlib.Path(tempfile.mkdtemp(prefix="m17-"))
    shutil.copy(G / "test_project.py", w); shutil.copy(G / "instance.py", w); shutil.copy(alt, w / "tail_risk.py")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"], cwd=w, capture_output=True, text=True, env={"PATH": os.environ["PATH"], "QF_SEED": str(s), "PYTHONHASHSEED": "0"})
    (ok := ok + 1) if r.returncode == 0 else bad.append(s)
    shutil.rmtree(w, ignore_errors=True)
print("m17 pass seeds:", ok, "of 50; failing:", bad[:10])
