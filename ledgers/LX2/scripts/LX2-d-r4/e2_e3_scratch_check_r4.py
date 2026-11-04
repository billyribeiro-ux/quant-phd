"""LX2-d round 4: reproduce the two scratch-copy predictions of L02 E2 and E3 (run with python3 -I).

Builds two copies of the L02 twin in a scratch directory: E2 sets P2's tipper benefit to 'reputational';
E3 sets P7's source-told flag to False. Each copy is run under -W error and its summary line is printed.
Usage: python3 -I e2_e3_scratch_check_r4.py <checkout-root> <scratch-dir>
"""
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
src = (root / "tests/labs/LX2/lab-LX2-L02-1.py").read_text(encoding="utf-8")

e2 = src.replace('tipper_benefit="none",', 'tipper_benefit="reputational",', 1)
i = src.index('label="P7"')
j = src.index("source_told_of_trade=True", i)
e3 = src[:j] + "source_told_of_trade=False" + src[j + len("source_told_of_trade=True"):]

for name, text in (("e2_copy.py", e2), ("e3_copy.py", e3)):
    path = scratch / name
    path.write_text(text, encoding="utf-8")
    out = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True, check=True)
    print(f"== {name}")
    for line in out.stdout.splitlines():
        if line.startswith("fired:"):
            print(line)
        if line.startswith("P2 ") or line.startswith("P7 "):
            print(line)
