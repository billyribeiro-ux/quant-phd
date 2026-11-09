"""Round-15 check: do the mutants that carry the stale 200-halving cap still fail when the cap is restored to the
reference's 240? Writes a copy of each cap-200 mutant with MAX_BISECTION_STEPS = 240 to a scratch directory and runs
the E4 suite on seeds 0-9 with run_candidate.py. Prints each mutant that survives (passes all seeds) with the cap fixed.
Usage: python -I cap_fix_check_r15.py  (run from the checkout root)"""
import glob
import re
import subprocess
import sys
from pathlib import Path

scratch = Path("/tmp/e4d15/fixed")
scratch.mkdir(parents=True, exist_ok=True)
survivors = []
checked = 0
for path in sorted(glob.glob("ledgers/E4/mutants/*.py")):
    text = Path(path).read_text(encoding="utf-8")
    if "MAX_BISECTION_STEPS = 200" not in text:
        continue
    fixed = text.replace("MAX_BISECTION_STEPS = 200", "MAX_BISECTION_STEPS = 240", 1)
    out = scratch / Path(path).name
    out.write_text(fixed, encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", "ledgers/E4/scripts/E4-d-r15/run_candidate.py", str(out), "0-9"],
                       capture_output=True, text=True, check=False)
    checked += 1
    first = r.stdout.splitlines()[0] if r.stdout else r.stderr[-200:]
    if not first.startswith(f"{out.name}: 0/10") and " 0/10 seeds pass" not in first:
        survivors.append((Path(path).name, first))
    print(Path(path).name, "->", first, flush=True)
print("checked", checked, "cap-200 mutants with the cap restored to 240; still killed on seeds 0-9:", checked - len(survivors))
for name, first in survivors:
    print("SURVIVES WITH CAP 240:", name, first)
