"""Run the two scratch-copy experiments that L02 problems E2 and E3 describe, on copies of the lab twin.

Usage: python3 -I l02_scratch_experiments.py <repo_root> <scratch_dir>
E2: P2's tipper benefit changed from none to reputational. E3: P7's source_told_of_trade changed from True to False.
Prints the full decision table of each copy. The repository twin is not modified.
"""

import subprocess
import sys
from pathlib import Path


def run_variant(twin: Path, out: Path, label: str, pattern: str, old: str, new: str) -> None:
    src = twin.read_text(encoding="utf-8")
    start = src.index(pattern)
    idx = src.index(old, start)
    variant = src[:idx] + new + src[idx + len(old):]
    out.write_text(variant, encoding="utf-8")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(out)], capture_output=True, text=True, timeout=60)
    print(f"== {label} (exit {run.returncode})")
    print(run.stdout[run.stdout.index("pattern"):] if "pattern" in run.stdout else run.stdout + run.stderr)


def main() -> None:
    root = Path(sys.argv[1])
    scratch = Path(sys.argv[2])
    scratch.mkdir(parents=True, exist_ok=True)
    twin = root / "tests/labs/LX2/lab-LX2-L02-1.py"
    run_variant(twin, scratch / "e2.py", "E2 P2 benefit reputational", 'label="P2"', 'tipper_benefit="none"', 'tipper_benefit="reputational"')
    run_variant(twin, scratch / "e3.py", "E3 P7 source told False", 'label="P7"', "source_told_of_trade=True", "source_told_of_trade=False")


if __name__ == "__main__":
    main()
