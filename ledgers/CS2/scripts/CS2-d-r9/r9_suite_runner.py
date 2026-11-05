"""Round-9 runner: run the CS2 autograder suite against one candidate streamstats.py for a list of seeds.

Usage: python -I r9_suite_runner.py <candidate.py> <seeds like 0-49> [--collect]
Each seed runs in a fresh temporary workspace holding instance.py, test_project.py and the candidate as
streamstats.py, exactly as the local run instructions describe. Prints one line per seed and a summary.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "CS" / "CS2" / "grader"
PY = ROOT / ".venv" / "bin" / "python"


def run(candidate: Path, seed: int, collect: bool) -> tuple[bool, str, int]:
    work = Path(tempfile.mkdtemp(prefix="cs2r9_"))
    try:
        shutil.copy(GRADER / "instance.py", work / "instance.py")
        shutil.copy(GRADER / "test_project.py", work / "test_project.py")
        shutil.copy(candidate, work / "streamstats.py")
        env = dict(os.environ, QF_SEED=str(seed))
        args = [str(PY), "-m", "pytest", "-q", "-p", "no:cacheprovider", "--assert=plain", "-W", "error"]
        if collect:
            args.append("--collect-only")
        args.append("test_project.py")
        proc = subprocess.run(args, cwd=work, env=env, capture_output=True, text=True, timeout=300)
        out = proc.stdout + proc.stderr
        m = re.search(r"(\d+) tests? collected", out)
        collected = int(m.group(1)) if m else -1
        return proc.returncode == 0, out, collected
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main() -> int:
    candidate = Path(sys.argv[1]).resolve()
    spec = sys.argv[2]
    collect = "--collect" in sys.argv
    lo, _, hi = spec.partition("-")
    seeds = range(int(lo), int(hi or lo) + 1)
    passed = 0
    failing = []
    counts = []
    for seed in seeds:
        ok, out, collected = run(candidate, seed, collect)
        counts.append(collected)
        if ok:
            passed += 1
        else:
            failing.append((seed, (re.findall(r"FAILED \S+", out) or ["(no FAILED line)"])[:3]))
    print(f"candidate {candidate.name}: {passed}/{len(seeds)} seeds all-pass")
    if collect:
        print("collected counts:", sorted(set(counts)))
    for seed, why in failing:
        print("  seed", seed, why)
    return 0 if passed == len(seeds) else 1


if __name__ == "__main__":
    sys.exit(main())
