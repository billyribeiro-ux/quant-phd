import os, subprocess, sys, pathlib, shutil, tempfile
from concurrent.futures import ThreadPoolExecutor
G = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD7-M4-d/course/modules/M/M4/grader")
variants = ["cross_p03", "cross_p05", "cross_m05", "reference"]
def run(args):
    v, s = args
    W = pathlib.Path(tempfile.mkdtemp(prefix="cx-"))
    shutil.copy(G / "test_project.py", W / "test_project.py"); shutil.copy(G / "instance.py", W / "instance.py")
    src = G / "reference.py" if v == "reference" else pathlib.Path(f"/tmp/M4-d-r7-chk/{v}.py")
    shutil.copy(src, W / "tail_risk.py")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py", "-k", "test_student_t_cross_term"],
                       cwd=W, capture_output=True, text=True, env={"PATH": os.environ["PATH"], "QF_SEED": str(s), "PYTHONHASHSEED": "0"})
    shutil.rmtree(W, ignore_errors=True)
    return v, s, r.returncode == 0
jobs = [(v, s) for v in variants for s in range(50)]
with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(run, jobs))
for v in variants:
    fails = [s for vv, s, ok in res if vv == v and not ok]
    print(f"{v}: detected (fails cross-term test) on {len(fails)} of 50 seeds")
