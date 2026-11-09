"""FC1-a round 4: lab-claim mutants. Each mutant is a copy of a lab twin with one defect; a printed claim of the page must flip.

Run from the checkout root: .venv/bin/python -I ledgers/FC1/scripts/FC1-a-r4/lab_mutants_r4.py <outdir>
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
PY = str(ROOT / ".venv" / "bin" / "python")
MUTANTS = [
    (
        "tests/labs/FC1/lab-FC1-L01-1.py",
        "    return (1 - q ** (n + 1)) / reserve_ratio",
        "    return (1 - q ** n) / reserve_ratio",
        "L01 Part A 'the partial sums equal the closed form exactly for n = 0 to 10: True' must flip to False",
        "the partial sums equal the closed form exactly for n = 0 to 10:",
    ),
    (
        "tests/labs/FC1/lab-FC1-L02-1.py",
        "    return all(len(values[axis]) == 1 and values[axis][0] in allowed for axis, allowed in AXES.items())",
        "    return all(len(values[axis]) >= 1 and values[axis][0] in allowed for axis, allowed in AXES.items())",
        "L02 Part D 'malformed entry rejected: True' must flip to False",
        "malformed entry rejected:",
    ),
    (
        "tests/labs/FC1/lab-FC1-L03-1.py",
        "    return half * sum(t.shares for t in trades)",
        "    return 2 * half * sum(t.shares for t in trades)",
        "L03 Part B 'mark-to-mid P&L equals spread capture plus mid-move term: True' must flip to False",
        "mark-to-mid P&L equals spread capture plus mid-move term:",
    ),
]
for i, (twin, old, new, claim, marker) in enumerate(MUTANTS, 1):
    src = (ROOT / twin).read_text(encoding="utf-8")
    assert src.count(old) == 1, (twin, src.count(old))
    path = OUT / f"lab_mutant_r4_{i:02d}.py"
    path.write_text(src.replace(old, new), encoding="utf-8")
    run = subprocess.run([PY, "-I", str(path)], capture_output=True, text=True)
    line = next((ln for ln in run.stdout.splitlines() if marker in ln), "<marker absent>")
    print(f"mutant {i:02d} ({twin}): exit={run.returncode}; printed: {line}")
    print(f"   claim: {claim}")
    print(f"   killed (claim text no longer prints True): {line.endswith('True') is False and marker in line}")
