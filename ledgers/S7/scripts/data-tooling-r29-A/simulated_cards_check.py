"""Round 29: run the twins behind the simulated cards (S7-c082, c112, c165, c198, c199) and check each number the card
states against the twin's printed output (run in a scratch directory with the embedded snapshots as data/, under
python -I -W error, as run_labs does). Prints each check as found/not found with the matching output line.
Run: .venv/bin/python -I ledgers/S7/scripts/data-tooling-r29-A/simulated_cards_check.py <repo root>
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1])
TWINS = {"L05-1": "lab-S7-L05-1.py", "L05-3": "lab-S7-L05-3.py", "L05-4": "lab-S7-L05-4.py",
         "L05-6": "lab-S7-L05-6.py", "L08-2": "lab-S7-L08-2.py"}
CHECKS = {
    "L08-2": ["0.0317", "0.769", "0.03", "0.77", "0.20"],  # card S7-c082 (estimates 0.03 to 0.77, sd near 0.20); c209 0.03
    "L05-4": ["45.5", "84.8", "3.023", "3.031", "2.508", "17"],  # card S7-c112
    "L05-6": ["1.105", "1.645", "2.837", "0.853", "10.08"],  # card S7-c165
    "L05-1": ["0.031", "0.045"],  # card S7-c198 (Lab 1's FWER single-step and step-down)
    "L05-3": ["1.601", "2.566", "1.6", "2.6"],  # card S7-c199 (critical values 1.6 and 2.6)
}
outputs = {}
for key, name in TWINS.items():
    twin = root / "tests/labs/S7" / name
    with tempfile.TemporaryDirectory() as work:
        (Path(work) / "data").mkdir()
        for f in (root / "course/assets/data/market").glob("*.csv"):
            shutil.copy(f, Path(work) / "data" / f.name)
        r = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], cwd=work, capture_output=True, text=True,
                           env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"})
        outputs[key] = r.stdout
        print(f"{key}: exit {r.returncode}, stderr {len(r.stderr)} bytes, {len(r.stdout.splitlines())} output lines")
for key, tokens in CHECKS.items():
    for tok in tokens:
        hits = [ln.strip() for ln in outputs[key].splitlines() if tok in ln]
        print(f"{key} card number {tok!r}: {'FOUND' if hits else 'not found'} {hits[:1]}")
print("--- full outputs ---")
for key, text in outputs.items():
    print(f"[{key}]\n{text}")
