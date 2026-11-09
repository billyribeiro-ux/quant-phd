"""Run copies of the L08 Lab 1 twin with BETA changed, and report the solver iteration counts.

Checks the L08 claims: 'In a copy of the lab code with BETA set to 0.5 ... prints 40 iterations',
'with BETA set to 0.95 ... prints 527', and the E1 solution's a priori thresholds (40.66, 282.74, 594.29).
Usage: python3 -I l08_beta_copies.py <repo-root>
"""

import math
import pathlib
import re
import subprocess
import sys
import tempfile

root = pathlib.Path(sys.argv[1])
twin = (root / "tests/labs/M5/lab-M5-L08-1.py").read_text(encoding="utf-8")
assert "BETA = 0.9\n" in twin
for beta in ("0.5", "0.9", "0.95"):
    src = twin.replace("BETA = 0.9\n", f"BETA = {beta}\n", 1)
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "copy.py"
        p.write_text(src, encoding="utf-8")
        out = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(p)], capture_output=True, text=True, check=False
        )
    lines = [ln for ln in out.stdout.splitlines() if "iterations until" in ln]
    print(f"BETA={beta} exit={out.returncode} stderr={out.stderr.strip()!r} :: {lines}")
    for ln in out.stdout.splitlines():
        if ln.startswith("part A: residual") or ln.startswith("part B: largest") or "largest sampled" in ln:
            print("   ", ln)

# a priori thresholds: least n >= 1 with beta^n * d/(1-beta) <= tau, d = sqrt(3)/2, tau = 1e-12
d = math.sqrt(3) / 2
tau = 1e-12
for beta in (0.5, 0.9, 0.95):
    thr = math.log(tau * (1 - beta) / d) / math.log(beta)
    n = next(n for n in range(1, 100000) if beta**n * d / (1 - beta) <= tau)
    print(f"a priori beta={beta}: threshold {thr:.2f}, least n {n}")

# monotonicity of the solver count over a fine beta grid, using the twin's own solve() logic
ns = {}
prog = twin.split("def part_a()")[0].replace("main()", "")
prog = prog.replace("\nSEED =", "\nSEED =")
g = {"__name__": "lab"}
exec(compile(prog.replace("from __future__ import annotations", ""), "twin_head", "exec"), g)
counts = []
for beta in [0.5 + 0.01 * i for i in range(0, 50)]:
    _, _, c = g["solve"](g["GRID"], beta)
    counts.append((round(beta, 2), c))
mono = all(counts[i][1] <= counts[i + 1][1] for i in range(len(counts) - 1))
print("solver count over beta in [0.50, 0.99] step 0.01 monotone nondecreasing:", mono)
print("first, last:", counts[0], counts[-1])
print("counts at 0.5, 0.9, 0.95:", [c for b, c in counts if b in (0.5, 0.9, 0.95)])
