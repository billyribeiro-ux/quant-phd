"""Run every PC3 lab twin under python -I -W error and keep its stdout (round-4 slice d).

usage: python -I run_twins_r4.py   (writes twins/<twin>.out next to this file; prints exit codes)
"""
import subprocess
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
root = here.parents[3]  # ledgers/PC3/scripts/PC3-d-r4 -> checkout root
out_dir = here / "twins"
out_dir.mkdir(exist_ok=True)
for twin in sorted((root / "tests/labs/PC3").glob("lab-PC3-L*-1.py")) + sorted((root / "tests/labs/PC3").glob("lab-PC3-project-*.py")):
    proc = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, check=False)
    (out_dir / f"{twin.stem}.out").write_text(proc.stdout, encoding="utf-8")
    print(f"{twin.stem} exit {proc.returncode} stderr_bytes {len(proc.stderr)} stdout_lines {proc.stdout.count(chr(10))}")
