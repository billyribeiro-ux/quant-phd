"""Recompute L08 numeric claims from the lab twin (scratch copies only; never edits the twin).

Usage: python3 -I ledgers/M5/scripts/M5-c-r6/l08_numeric.py <path-to-twin>
"""
import re
import sys
import tempfile
import pathlib
import subprocess

twin = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
body = twin.rsplit("\nmain()", 1)[0]
ns: dict = {}
exec(compile(body, "twin_no_main", "exec"), ns)

import random
rng = random.Random(ns["SEED"])
worst = 0.0
for _ in range(ns["PAIRS"]):
    v = [rng.uniform(-10.0, 10.0) for _ in ns["GRID"]]
    w = [rng.uniform(-10.0, 10.0) for _ in ns["GRID"]]
    bv, _ = ns["bellman"](v, ns["GRID"], ns["BETA"])
    bw, _ = ns["bellman"](w, ns["GRID"], ns["BETA"])
    num = max(abs(a - b) for a, b in zip(bv, bw, strict=True))
    den = max(abs(a - b) for a, b in zip(v, w, strict=True))
    worst = max(worst, num / den)
print(f"B1 worst ratio repr = {worst!r}; minus beta = {worst - ns['BETA']!r}")

for b in ("0.5", "0.9", "0.95"):
    src = re.sub(r"^BETA = 0\.9$", f"BETA = {b}", twin, count=1, flags=re.M)
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "copy.py"
        p.write_text(src, encoding="utf-8")
        out = subprocess.run([sys.executable, "-I", str(p)], capture_output=True, text=True, cwd=d)
        line = [x for x in out.stdout.splitlines() if "iterations until" in x]
        print(f"B2 BETA={b}: rc={out.returncode} {line[0] if line else out.stderr[-300:]}")
