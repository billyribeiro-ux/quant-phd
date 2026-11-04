"""Run the L02 twin with 300 different seeds and check that the two identity lines hold for every seed.

Run: .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r3/seed_identity_check.py
"""

import contextlib
import io
import re
from pathlib import Path

src = Path("tests/labs/SC1/lab-SC1-L02-1.py").read_text(encoding="utf-8")
assert src.count("SEED = 20260101") == 1
bad_dyadic = []
bad_sup = []
bad_bound_flag_count = 0
for seed in range(1, 301):
    code = src.replace("SEED = 20260101", f"SEED = {seed}")
    buf = io.StringIO()
    g: dict = {"__name__": "lab"}
    with contextlib.redirect_stdout(buf):
        exec(compile(code, f"seed{seed}", "exec"), g)
    lines = buf.getvalue().splitlines()
    if lines[0] != "dyadic values fixed from level n on (n <= 4, n <= M <= 8): 216 of 216 cases":
        bad_dyadic.append((seed, lines[0]))
    if not lines[1].endswith("for levels 1 to 8: True"):
        bad_sup.append((seed, lines[1]))
print(f"seeds tested: 300; dyadic line not 216 of 216 for seeds: {bad_dyadic[:5]} (count {len(bad_dyadic)})")
print(f"grid-sup line not True for seeds: {bad_sup[:5]} (count {len(bad_sup)})")
