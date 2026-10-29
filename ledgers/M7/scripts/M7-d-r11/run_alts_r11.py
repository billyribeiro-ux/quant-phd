"""Round 11: run one alternative solution against the grader on seeds 0-49, each in a fresh scratch directory.
usage: run_alts_r11.py <checkout> <solution.py> <label>"""
import os, shutil, subprocess, sys, pathlib
wd, sol, label = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
grader = wd / "course/modules/M/M7/grader"
py = wd / ".venv/bin/python"
passed = 0
for seed in range(50):
    w = pathlib.Path(f"/tmp/m7d_r11_{label}_{seed}")
    shutil.rmtree(w, ignore_errors=True)
    w.mkdir(parents=True)
    shutil.copy(grader / "test_project.py", w)
    shutil.copy(grader / "instance.py", w)
    shutil.copy(sol, w / "constrained_allocator.py")
    env = {"QF_SEED": str(seed), "PATH": os.environ.get("PATH", "")}
    r = subprocess.run([str(py), "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                       cwd=w, env=env, capture_output=True, text=True)
    last = (r.stdout.strip().splitlines() or ["<no output>"])[-1]
    ok = r.returncode == 0 and " passed" in last and "failed" not in last
    passed += ok
    print(f"{label} seed {seed}: rc={r.returncode} {last}")
print(f"{label}: {passed} of 50 seeds pass")
