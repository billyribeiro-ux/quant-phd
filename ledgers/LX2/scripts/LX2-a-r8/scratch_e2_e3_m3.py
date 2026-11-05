"""Round 8: re-run the three predictions of L02 (E2, E3, M3) on scratch copies of the lab twin.

Usage: python -I ledgers/LX2/scripts/LX2-a-r8/scratch_e2_e3_m3.py <twin.py> <scratch_dir>
Each copy changes one flag in the twin, runs it as python -I -W error, and prints the P-rows and the summary lines.
"""

import os
import subprocess
import sys

TWIN, SCRATCH = sys.argv[1], sys.argv[2]
os.makedirs(SCRATCH, exist_ok=True)
base = open(TWIN, encoding="utf-8").read()

CHANGES = {
    "e2": ('label="P2"', 'tipper_benefit="none"', 'tipper_benefit="reputational"'),
    "e3": ('label="P7"', "source_told_of_trade=True", "source_told_of_trade=False"),
    "m3": ('label="P3"', 'tipper_benefit="pecuniary"', 'tipper_benefit="none"'),
}
for name, (anchor, old, new) in CHANGES.items():
    i = base.index(anchor)
    j = base.index(old, i)
    text = base[:j] + new + base[j + len(old) :]
    path = os.path.join(SCRATCH, f"{name}.py")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    proc = subprocess.run([sys.executable, "-I", "-W", "error", path], capture_output=True, text=True, timeout=60)
    print(f"== {name}: exit={proc.returncode} stderr_bytes={len(proc.stderr)}")
    for line in proc.stdout.splitlines():
        if line.startswith(("P2 ", "P3 ", "P7 ", "fired:", "not fired:")):
            print(line)
