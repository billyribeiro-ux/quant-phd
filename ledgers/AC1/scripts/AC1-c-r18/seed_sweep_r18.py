"""Round 18 (AC1-c): seed sweep of both lab twins and of the m18a mutant.
Usage: python -I seed_sweep_r18.py <checkout> <scratch_dir>
Each twin must exit 0 for every seed (its assertions hold); m18a must be killed by some seeds.
"""

import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
seeds = [0, 1, 2, 3, 7, 42, 999, 123456789, 20260701, 20260702]
for lab in ("L07", "L08"):
    text = (root / f"tests/labs/AC1/lab-AC1-{lab}-1.py").read_text(encoding="utf-8")
    for seed in seeds:
        path = scratch / f"{lab}-{seed}.py"
        path.write_text(re.sub(r"^SEED = [0-9_]+", f"SEED = {seed}", text, flags=re.M), encoding="utf-8")
        proc = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True)
        print(f"{lab} seed={seed} exit={proc.returncode}")
m18a = (
    (root / "tests/labs/AC1/lab-AC1-L07-1.py")
    .read_text(encoding="utf-8")
    .replace(
        "        expensed = sum(yearly_expense(grant, year) for year in range(1, HORIZON + 1))\n",
        "        expensed = sum(yearly_expense(grant, year) for year in range(1, HORIZON))\n",
    )
)
for seed in seeds:
    path = scratch / f"m18a-{seed}.py"
    path.write_text(re.sub(r"^SEED = [0-9_]+", f"SEED = {seed}", m18a, flags=re.M), encoding="utf-8")
    proc = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True)
    print(f"m18a seed={seed} exit={proc.returncode} (nonzero = killed)")
