"""Run one candidate bm_checks.py against the SC1 grader suite, as the page does (QF_SEED, --assert=plain, -W error).

Usage: python -I run_candidate.py <candidate.py> <seed> [timeout_seconds]
Copies grader/test_project.py and grader/instance.py and the candidate (as bm_checks.py) into a fresh scratch
directory under /tmp, runs pytest there, prints VERDICT, the first FAILED line and the wall time, then removes the scratch.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

REPO = "/Users/billyribeiro/.fanout/wt/verifyE9-SC1-d"
PY = os.path.join(REPO, ".venv", "bin", "python")
GRADER = os.path.join(REPO, "course", "modules", "SC", "SC1", "grader")


def main() -> None:
    candidate, seed = sys.argv[1], sys.argv[2]
    timeout = float(sys.argv[3]) if len(sys.argv) > 3 else 120.0
    work = tempfile.mkdtemp(prefix="sc1d-r9-cand-")
    try:
        shutil.copy(os.path.join(GRADER, "instance.py"), work)
        # TEST_FILE overrides the suite (used only to check a proposed fix in scratch, never the repo).
        shutil.copy(os.environ.get("TEST_FILE", os.path.join(GRADER, "test_project.py")), os.path.join(work, "test_project.py"))
        shutil.copy(candidate, os.path.join(work, "bm_checks.py"))
        env = dict(os.environ, QF_SEED=seed)
        start = time.perf_counter()
        try:
            proc = subprocess.run(
                [PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
                cwd=work, env=env, capture_output=True, text=True, timeout=timeout,
            )
            out = proc.stdout + proc.stderr
            failed = re.findall(r"FAILED \S+", out)
            verdict = "KILLED" if proc.returncode != 0 else "SURVIVED"
            tail = out.strip().splitlines()[-1] if out.strip() else ""
            first = failed[0] if failed else "-"
            print(f"{verdict} {os.path.basename(candidate)} seed={seed} rc={proc.returncode} first={first} last=[{tail}]")
        except subprocess.TimeoutExpired:
            print(f"TIMEOUT {os.path.basename(candidate)} seed={seed} after {timeout}s")
        print(f"wall {time.perf_counter() - start:.2f}s")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
