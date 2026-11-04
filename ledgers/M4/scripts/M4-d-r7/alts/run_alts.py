"""Round-7 verifier (slice d): run the full grader suite on each alternative for seeds 0-9 (same pytest flags as run_graders)."""
import os, pathlib, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(sys.argv[1])  # checkout root
ALTS = sorted(pathlib.Path(__file__).resolve().parent.glob("alt*.py"))
G = ROOT / "course/modules/M/M4/grader"
FLAGS = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
seeds = range(0, 10)
total_fail = 0
for alt in ALTS:
    results = []
    for s in seeds:
        work = pathlib.Path(tempfile.mkdtemp(prefix="alt-r7-"))
        shutil.copy(G / "test_project.py", work / "test_project.py")
        shutil.copy(G / "instance.py", work / "instance.py")
        shutil.copy(alt, work / "tail_risk.py")
        r = subprocess.run([sys.executable, "-m", "pytest", *FLAGS, "test_project.py"], cwd=work,
                           capture_output=True, text=True,
                           env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(s), "PYTHONHASHSEED": "0"})
        tail = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
        failed = [l for l in r.stdout.splitlines() if l.startswith("FAILED")]
        results.append((s, r.returncode == 0, tail, failed[:2]))
        shutil.rmtree(work, ignore_errors=True)
    passed = sum(1 for _, ok, _, _ in results if ok)
    total_fail += len(results) - passed
    print(f"{alt.name}: {passed}/10 seeds PASS")
    for s, ok, tail, failed in results:
        if not ok:
            print(f"   seed {s}: {tail}")
            for f in failed: print(f"      {f[:220]}")
print("TOTAL seed-runs failing:", total_fail)
