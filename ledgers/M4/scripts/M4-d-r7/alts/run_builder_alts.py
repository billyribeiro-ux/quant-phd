"""Round-7 verifier (slice d): run the grader suite on the builder's alt_1..alt_5 files (ledgers/M4/scripts/alt_*.py) for seeds 0-9."""
import os, pathlib, shutil, subprocess, sys, tempfile

ROOT = pathlib.Path(sys.argv[1])
G = ROOT / "course/modules/M/M4/grader"
for alt in sorted((ROOT / "ledgers/M4/scripts").glob("alt_*.py")):
    ok_count, fails = 0, []
    for s in range(10):
        w = pathlib.Path(tempfile.mkdtemp(prefix="altb-"))
        shutil.copy(G / "test_project.py", w)
        shutil.copy(G / "instance.py", w)
        shutil.copy(alt, w / "tail_risk.py")
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                           cwd=w, capture_output=True, text=True, env={"PATH": os.environ["PATH"], "QF_SEED": str(s), "PYTHONHASHSEED": "0"})
        if r.returncode == 0:
            ok_count += 1
        else:
            fails.append((s, [l[:150] for l in r.stdout.splitlines() if l.startswith("FAILED")][:2]))
        shutil.rmtree(w, ignore_errors=True)
    print(f"{alt.name}: {ok_count}/10 seeds PASS")
    for f in fails:
        print("   ", f)
