"""Verifier (FC1-b r3): does Lab 1 L04 actually detect violations of its two checked invariants?

Mutant A: limit orders rest without matching (book can cross). Mutant B: traded term counted once, X not 2X.
Each mutant is written to a scratch dir and run under python -I -W error. The lesson claims the lab checks both.
"""
import pathlib
import re
import subprocess
import sys
import tempfile

TWIN = pathlib.Path(sys.argv[1]) / "tests/labs/FC1/lab-FC1-L04-1.py"
src = TWIN.read_text(encoding="utf-8")
scratch = pathlib.Path(tempfile.mkdtemp(prefix="fc1b_l04_"))


def run(text, name):
    p = scratch / f"{name}.py"
    p.write_text(text, encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(p)], capture_output=True, text=True, cwd=scratch, timeout=60)
    return r.returncode, r.stderr, [l for l in r.stdout.splitlines() if "failures" in l or "crossed" in l or "submitted" in l]


rc, err, lines = run(src, "base")
print("base", rc, repr(err), lines)

mut_a = src.replace(
    "        self.submitted += order.qty\n        while order.qty > 0:",
    "        self.submitted += order.qty\n        while order.qty > 0 and order.kind != 'limit':",
    1,
)
assert mut_a != src
print("mutant A (limit orders never match)", *run(mut_a, "mutA"))

mut_b = src.replace("self.traded += fill", "self.traded += fill // 2 if fill % 2 == 0 else fill", 1)
assert mut_b != src
print("mutant B (traded term halved)", *run(mut_b, "mutB"))
