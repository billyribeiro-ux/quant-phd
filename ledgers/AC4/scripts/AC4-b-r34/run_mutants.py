"""Run each mutant of a lab twin under python -I and compare its stdout with the page's embedded expected block.

usage: run_mutants.py <expected.txt> <mutant.py> [<mutant.py> ...]
A mutant is KILLED when it exits non-zero or its stdout differs from the expected block; otherwise SURVIVED.
"""

import subprocess
import sys

expected_path, mutants = sys.argv[1], sys.argv[2:]
expected = open(expected_path, encoding="utf-8").read().rstrip("\n")
for path in mutants:
    proc = subprocess.run([sys.executable, "-I", "-W", "error", path], capture_output=True, text=True, timeout=60)
    out = proc.stdout.rstrip("\n")
    if proc.returncode != 0:
        verdict = f"KILLED (exit {proc.returncode}: {proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else ''})"
    elif out != expected:
        verdict = "KILLED (stdout differs from expected block)"
    else:
        verdict = "SURVIVED (exit 0, stdout identical)"
    print(f"{path.rsplit('/', 1)[-1]}: {verdict}")
