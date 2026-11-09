import shutil, subprocess, sys, tempfile, os
from pathlib import Path
REPO = Path(sys.argv[1]); seeds = range(int(sys.argv[2]), int(sys.argv[3])); cands = [Path(p) for p in sys.argv[4:]]
G = REPO / "course/modules/M/M5/grader"; PY = Path("/Users/billyribeiro/dev/quant-phd/.venv/bin/python")
for cand in cands:
    killed_seeds = []; first = None
    for seed in seeds:
        work = Path(tempfile.mkdtemp(prefix="m5k_", dir="/tmp/m5d5/tmp"))
        try:
            for f in ("test_project.py", "instance.py"): shutil.copy(G / f, work / f)
            shutil.copy(cand, work / "contraction_solver.py")
            env = {"QF_SEED": str(seed), "PATH": "/usr/bin:/bin"}
            r = subprocess.run([str(PY), "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                               cwd=work, env=env, capture_output=True, text=True)
            if r.returncode != 0:
                killed_seeds.append(seed)
                if first is None:
                    fl = [ln for ln in r.stdout.splitlines() if ln.startswith("FAILED")]
                    first = (seed, fl[:1])
        finally:
            shutil.rmtree(work, ignore_errors=True)
    print(f"{cand.name}: killed on {len(killed_seeds)}/{len(list(seeds))} seeds; first {first}")
