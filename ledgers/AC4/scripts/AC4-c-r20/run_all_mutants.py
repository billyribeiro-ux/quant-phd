"""Run every lab-twin mutant and alternative for AC4 slice c (L05, L06) under python -I -W error.

Each mutant is a standalone twin file. Its stdout is compared with the baseline twin's stdout.
Outcome per file: SAME (exit 0, identical stdout), DIFF (exit 0, different stdout), ERR (non-zero exit or stderr).
Usage: run_all_mutants.py <checkout> <scratch-dir>
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

checkout = pathlib.Path(sys.argv[1])
scratch = pathlib.Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
py = str(checkout / ".venv/bin/python")
mut_root = checkout / "ledgers/AC4/mutants"
twins = {"L05": checkout / "tests/labs/AC4/lab-AC4-L05-1.py", "L06": checkout / "tests/labs/AC4/lab-AC4-L06-1.py"}


def run(path: pathlib.Path, cwd: pathlib.Path) -> tuple[int, str, str]:
    p = subprocess.run([py, "-I", "-W", "error", str(path)], cwd=cwd, capture_output=True, text=True, timeout=60)
    return p.returncode, p.stdout, p.stderr


base = {}
for name, twin in twins.items():
    rc, out, err = run(twin, scratch)
    assert rc == 0 and err == "", (name, rc, err)
    base[name] = out
    print(f"BASE {name} exit {rc} lines {len(out.splitlines())}")

files = sorted(p for d in mut_root.glob("AC4-c-r*") for p in d.rglob("*.py") if p.is_file())
files += sorted(p for p in mut_root.glob("*.py") if p.name.startswith(("L05", "L06")) and "AC4-c" in p.name)
for f in files:
    lab = "L05" if "L05" in f.name else "L06"
    rel = f.relative_to(mut_root)
    if "L05" not in f.name and "L06" not in f.name:
        lab = "L06"  # every AC4-c-r* mutant without a lab id is a L06 variant; checked against its own twin below

    rc, out, err = run(f, scratch)
    if rc != 0 or err:
        status = "ERR"
        detail = (err.strip().splitlines() or [""])[-1][:160]
    elif out == base[lab]:
        status = "SAME"
        detail = ""
    else:
        status = "DIFF"
        detail = ""
    print(f"{status} {lab} {rel} {detail}")
