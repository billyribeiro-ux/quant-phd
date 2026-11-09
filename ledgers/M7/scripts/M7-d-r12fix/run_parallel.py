"""Run candidate solutions through the M7 suite on seeds first..last, in parallel, with the browser's pytest flags.

Usage: python -I run_parallel.py <repo_root> <first_seed> <last_seed> <candidate.py> [...]
Prints one line per candidate: the number of seeds that pass, the failing seeds, and the first failing test names.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

root = Path(sys.argv[1]).resolve()
first, last = int(sys.argv[2]), int(sys.argv[3])
grader = root / "course/modules/M/M7/grader"
flags = ["-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]


def run_one(cand: Path, seed: int) -> tuple[int, bool, str, float]:
    import time

    work = Path(tempfile.mkdtemp(prefix="m7r12fix-"))
    try:
        shutil.copy(grader / "test_project.py", work / "test_project.py")
        shutil.copy(grader / "instance.py", work / "instance.py")
        shutil.copy(cand, work / "constrained_allocator.py")
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "QF_SEED": str(seed), "PYTHONHASHSEED": "0"}
        started = time.monotonic()
        res = subprocess.run(
            [sys.executable, "-I", "-m", "pytest", *flags, "test_project.py"],
            cwd=work, capture_output=True, text=True, check=False, env=env, timeout=900,
        )
        elapsed = time.monotonic() - started
        names = re.findall(r"^FAILED test_project.py::(\S+)", res.stdout, re.M)
        return seed, res.returncode == 0, ", ".join(names[:3]), elapsed
    finally:
        shutil.rmtree(work, ignore_errors=True)


for cand_name in sys.argv[4:]:
    cand = Path(cand_name).resolve()
    seeds = list(range(first, last + 1))
    with ThreadPoolExecutor(max_workers=24) as pool:
        results = sorted(pool.map(lambda s: run_one(cand, s), seeds))
    passed = [s for s, ok, _, _ in results if ok]
    failed = [(s, names) for s, ok, names, _ in results if not ok]
    slowest = max(t for _, _, _, t in results)
    print(f"{cand.name}: seeds passing {len(passed)}/{len(seeds)}; slowest seed run {slowest:.1f} s")
    for s, names in failed[:5]:
        print(f"   seed {s}: {names}")
    sys.stdout.flush()
