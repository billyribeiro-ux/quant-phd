"""Lab mutants for FC1-a round 2 (scratch only). Each mutant is a copy of a twin with one student-error edit.

The check is whether the lab's own printed verdict line flips from True to False (the claim the lesson makes).
"""
import subprocess
import sys
from pathlib import Path

REPO = Path("/Users/billyribeiro/.fanout/wt/verifyS2-FC1-a")
OUT = Path("/tmp/fc1a-r2-mut")
CASES = [
    ("L01", "tests/labs/FC1/lab-FC1-L01-1.py",
     "return (1 - q ** (n + 1)) / reserve_ratio",
     "return (1 - q ** n) / reserve_ratio",
     "the partial sums equal the closed form exactly for n = 0 to 10: True"),
    ("L02", "tests/labs/FC1/lab-FC1-L02-1.py",
     "return all(len(values[axis]) == 1 and values[axis][0] in allowed for axis, allowed in AXES.items())",
     "return all(len(values[axis]) >= 1 and set(values[axis]) <= set(allowed) for axis, allowed in AXES.items())",
     "malformed entry rejected: True"),
    ("L03", "tests/labs/FC1/lab-FC1-L03-1.py",
     "return half * sum(t.shares for t in trades)",
     "return 2 * half * sum(t.shares for t in trades)",
     "mark-to-mid P&L equals spread capture plus mid-move term: True"),
]
for page, twin, old, new, claim in CASES:
    src = (REPO / twin).read_text(encoding="utf-8")
    assert src.count(old) == 1, (page, src.count(old))
    mutated = src.replace(old, new)
    path = OUT / f"mut_{page}.py"
    path.write_text(mutated, encoding="utf-8")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True, check=False)
    flipped = claim not in run.stdout
    print(f"{page}: mutant exit {run.returncode}; claim line still printed True: {claim in run.stdout}; killed (line changed): {flipped}")
    if run.returncode != 0:
        print("  stderr tail:", run.stderr.strip().splitlines()[-1] if run.stderr.strip() else "")
