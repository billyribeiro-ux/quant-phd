"""Round 19 (BK4 slice c): run each alternative correct implementation (ledgers/BK4/alternatives/alt1..alt5 and the
round-16 alt6 archived under scripts/BK4-c-r16/alts) and the reference through the suite for seeds 0-49, in scratch dirs.
Usage: python -I run_alts_r17.py <checkout-root>"""
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(sys.argv[1])
G = ROOT / "course/modules/BK/BK4/grader"
PY = str(ROOT / ".venv/bin/python")
cands = sorted((ROOT / "ledgers/BK4/alternatives").glob("alt*.py"))
cands.append(ROOT / "ledgers/BK4/scripts/BK4-c-r16/alts/alt6_bisect_module.py")
cands.append(G / "reference.py")
for cand in cands:
    fails = []
    for seed in range(50):
        W = pathlib.Path(tempfile.mkdtemp(prefix="bk4c_r19_alt_"))
        try:
            shutil.copy(G / "test_project.py", W / "test_project.py")
            shutil.copy(G / "instance.py", W / "instance.py")
            shutil.copy(cand, W / "clearing_house.py")
            env = dict(os.environ, QF_SEED=str(seed))
            r = subprocess.run([PY, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error",
                                "test_project.py"], cwd=W, env=env, capture_output=True, text=True)
            if r.returncode != 0:
                last = [ln for ln in r.stdout.splitlines() if ln.startswith("FAILED")][:2]
                fails.append((seed, r.returncode, last))
        finally:
            shutil.rmtree(W, ignore_errors=True)
    print(f"{cand.name}: {50 - len(fails)}/50 seeds pass" + ("" if not fails else f" FAILS {fails[:3]}"))
