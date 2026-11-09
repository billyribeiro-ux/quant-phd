"""FC1-a round 3: lab student-error mutants (scratch copies under /tmp/fc1a-r3-mut). Labs are demonstrations, so a mutant
is 'killed' when the lab's own printed claim line flips from True to False (the claim a lesson sentence makes)."""
import subprocess
import sys
from pathlib import Path

REPO = Path("/Users/billyribeiro/.fanout/wt/verifyS3-FC1-a")
OUT = Path("/tmp/fc1a-r3-mut")
OUT.mkdir(parents=True, exist_ok=True)
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
    path = OUT / f"mut_{page}.py"
    path.write_text(src.replace(old, new), encoding="utf-8")
    res = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True)
    flipped = claim not in res.stdout or (claim.replace(": True", ": False") in res.stdout)
    print(f"{page}: mutant exit={res.returncode} stderr={res.stderr.strip()[:120]!r} claim_line_still_True={claim in res.stdout} killed={not (claim in res.stdout)}")
    for line in res.stdout.splitlines():
        if page == "L01" and "partial sums" in line:
            print("   ", line)
        if page == "L02" and "malformed" in line:
            print("   ", line)
        if page == "L03" and "mark-to-mid P&L equals" in line:
            print("   ", line)
