"""Round 9, slice e: run each alternative engine against the current M2 suite on seeds 0-49 (scratch workspaces)."""

import concurrent.futures as cf
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHECK = Path("/Users/billyribeiro/.fanout/wt/verifyD9-M2-e")
GRADER = CHECK / "course/modules/M/M2/grader"
PY = str(CHECK / ".venv/bin/python")
SCRIPTS = CHECK / "ledgers/M2/scripts"
ALTS = [
    SCRIPTS / "M2-e-r3/alts/alt1/sensitivity_engine.py",
    SCRIPTS / "M2-e-r3/alts/alt2/sensitivity_engine.py",
    SCRIPTS / "M2-e-r3/alts/alt3/sensitivity_engine.py",
    *sorted((SCRIPTS / "M2-e-r5/alts_r5").glob("*.py")),
    *sorted((SCRIPTS / "M2-e-r6/alts_r6").glob("*.py")),
    *sorted((SCRIPTS / "M2-e-r7/alts_new").glob("*.py")),
    *sorted((SCRIPTS / "M2-e-r8/alts_r8").glob("*.py")),
    *sorted((SCRIPTS / "M2-e-r9/alts_r9").glob("*.py")),
]


def run(alt: Path, seed: int) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="m2e_r9_alt_"))
    try:
        for name in ("test_project.py", "instance.py"):
            shutil.copy(GRADER / name, work / name)
        shutil.copy(alt, work / "sensitivity_engine.py")
        env = dict(os.environ, QF_SEED=str(seed))
        proc = subprocess.run(
            [PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error", "test_project.py"],
            cwd=work, env=env, capture_output=True, text=True, timeout=300,
        )
        last = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else proc.stderr[-200:]
        return proc.returncode == 0, last
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    worst = 0
    for alt in ALTS:
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            results = list(ex.map(lambda s: (s, *run(alt, s)), range(50)))
        passed = sum(1 for _, ok, _ in results if ok)
        fails = [(s, last) for s, ok, last in results if not ok]
        rel = alt.relative_to(CHECK)
        print(f"{passed}/50 {rel}" + (f" FIRST_FAIL seed {fails[0][0]}: {fails[0][1]}" if fails else ""), flush=True)
        worst = max(worst, 0 if passed == 50 else 1)
    return worst


if __name__ == "__main__":
    sys.exit(main())
