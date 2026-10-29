"""Run the L07 lab twin with ETA set to 1 (the setting the L07 problem E3 solution predicts about), in a temp directory.

Usage: python -I ledgers/E3/scripts/E3-c-r3/eta_one_check.py
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
twin = (ROOT / "tests/labs/E3/lab-E3-L07-1.py").read_text(encoding="utf-8")
assert "\nETA = 0.5\n" in twin
with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "eta1_twin.py"
    path.write_text(twin.replace("\nETA = 0.5\n", "\nETA = 1.0\n"), encoding="utf-8")
    proc = subprocess.run([str(ROOT / ".venv/bin/python"), "-I", "-W", "error", str(path)], capture_output=True, text=True, cwd=tmp)
    print("exit", proc.returncode)
    print("stdout:")
    print(proc.stdout)
    print("stderr tail:")
    print(proc.stderr.strip().splitlines()[-3:])
sys.exit(0)
