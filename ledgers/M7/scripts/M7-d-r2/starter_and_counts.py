"""Round-2 checks: collected count on seeds 0-49, starter fails the suite, instance diversity, decode command."""
import json, subprocess, sys, shutil, tempfile, pathlib, os
G = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD2-M7-d/course/modules/M/M7/grader")
PY = "/Users/billyribeiro/.fanout/wt/verifyD2-M7-d/.venv/bin/python"
sys.path.insert(0, str(G))
from instance import make_instance
counts = set()
for seed in range(50):
    w = pathlib.Path(tempfile.mkdtemp())
    for f in ("test_project.py", "instance.py"):
        shutil.copy(G / f, w / f)
    shutil.copy(G / "reference.py", w / "constrained_allocator.py")
    r = subprocess.run([PY, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider", "test_project.py"],
                       cwd=w, capture_output=True, text=True, env={"QF_SEED": str(seed), "PATH": os.environ["PATH"]})
    counts.add(r.stdout.strip().splitlines()[-1])
    shutil.rmtree(w, ignore_errors=True)
print("collected lines over seeds 0-49:", counts)
# starter must fail the suite
w = pathlib.Path(tempfile.mkdtemp())
for f in ("test_project.py", "instance.py"):
    shutil.copy(G / f, w / f)
shutil.copy(G / "starter.py", w / "constrained_allocator.py")
r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                   cwd=w, capture_output=True, text=True, env={"QF_SEED": "0", "PATH": os.environ["PATH"]})
print("starter suite exit code:", r.returncode, "|", r.stdout.strip().splitlines()[-1])
shutil.rmtree(w, ignore_errors=True)
# diversity: answers differ across seeds 0-19 (reference answers)
sys.path.insert(0, str(G))
import reference as R
answers = []
labels = []
for seed in range(20):
    case = json.loads(make_instance(seed)["payload"])
    out = R.allocate(case)
    answers.append(tuple(round(x, 9) for x in out["weights"]))
    labels.append((len(case["mu"]), tuple(case["sector"])))
print("distinct reference answers, seeds 0-19:", len(set(answers)), "of 20; distinct (n, labels):", len(set(labels)))
# decode command on the page
print(json.loads(make_instance(0)["payload"])["gamma"], "decode ok" if isinstance(json.loads(make_instance(0)["payload"]), dict) else "")
