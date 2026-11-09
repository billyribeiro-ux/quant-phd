"""Verifier helper (round 17): print the failing test ids and their assertion messages for one candidate and seed."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v17_lib  # noqa: E402

cand = Path(sys.argv[1]).resolve()
seed = int(sys.argv[2])
code, out = v17_lib.run(cand, seed)
print(f"exit={code}")
for line in out.splitlines():
    if line.startswith("FAILED") or line.startswith("E   ") or "AssertionError" in line:
        print(line[:400])
print(out.strip().splitlines()[-1] if out.strip() else "(no output)")
