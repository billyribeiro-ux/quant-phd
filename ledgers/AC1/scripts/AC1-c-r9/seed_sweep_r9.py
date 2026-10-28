"""Run each AC1-c lab twin with SEED replaced by 0..199 and count exit codes; E2/E3 claim 'pass for any seed'."""
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
for lab in ("lab-AC1-L07-1", "lab-AC1-L08-1"):
    text = (root / f"tests/labs/AC1/{lab}.py").read_text(encoding="utf-8")
    passed = 0
    failed = []
    for seed in range(200):
        new = re.sub(r"^SEED = \d+", f"SEED = {seed}", text, count=1, flags=re.M)
        path = scratch / f"{lab}-s{seed}.py"
        path.write_text(new, encoding="utf-8")
        proc = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True)
        if proc.returncode == 0:
            passed += 1
        else:
            failed.append(seed)
    print(lab, "seeds 0-199 passing:", passed, "failing:", failed[:10])
