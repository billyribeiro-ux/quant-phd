"""Run each correct alternative as market_maker.py through the checkout's grader on seeds 0-49, with the page's pytest flags.

Scratch copies under /tmp/pc3c-r14-alt only. Usage: run_alts_r14.py <checkout-root> <alt.py> [<alt.py> ...]
"""
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

root = Path(sys.argv[1])
grader = root / "course/modules/PC/PC3/grader"
py = str(root / ".venv/bin/python")
flags = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def run_one(args):
    alt, seed = args
    work = Path("/tmp/pc3c-r14-alt") / alt.stem / f"s{seed}"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    for name in ("engine.py", "instance.py", "test_project.py"):
        shutil.copy(grader / name, work / name)
    shutil.copy(alt, work / "market_maker.py")
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONDONTWRITEBYTECODE": "1"}
    r = subprocess.run([py, "-B", "-m", "pytest", *flags, "test_project.py"], cwd=work, env=env,
                       capture_output=True, text=True)
    shutil.rmtree(work, ignore_errors=True)
    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[-200:]
    return alt, seed, r.returncode, tail


alts = [Path(a).resolve() for a in sys.argv[2:]]
jobs = [(a, s) for a in alts for s in range(50)]
results = {}
with ThreadPoolExecutor(max_workers=8) as ex:
    for alt, seed, code, tail in ex.map(run_one, jobs):
        results.setdefault(alt, []).append((seed, code, tail))
for alt in alts:
    rows = results[alt]
    failed = [s for s, c, _ in rows if c != 0]
    print(f"{alt.relative_to(root)}: fails on {len(failed)} of 50 seeds {failed[:12]}", flush=True)
    for s, c, t in rows:
        if c != 0:
            print(f"    seed {s}: {t}", flush=True)
            break
