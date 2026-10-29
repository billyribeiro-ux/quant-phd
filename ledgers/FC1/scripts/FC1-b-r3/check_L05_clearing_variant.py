"""L05 interpretation claim: changing a parameter changes only the lines that print it. Checks CLEARING_OFFSET 0 -> 1
and SETTLEMENT_LAG 2 -> 1 against the twin's printed lines. Run: .venv/bin/python -I <this file> <twin path>
"""

from __future__ import annotations

import contextlib
import io
import sys
import types

twin_path = sys.argv[1]
src = open(twin_path, encoding="utf-8").read().replace("\nmain()\n", "\n")


def run(text: str) -> list[str]:
    mod = types.ModuleType("twin")
    sys.modules["twin"] = mod
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(text + "\nmain()\n", twin_path, "exec"), mod.__dict__)
    return buf.getvalue().splitlines()


base = run(src)
for name, old, new in [("CLEARING_OFFSET", "CLEARING_OFFSET = 0 ", "CLEARING_OFFSET = 1 "),
                       ("SETTLEMENT_LAG", "SETTLEMENT_LAG = 2 ", "SETTLEMENT_LAG = 1 ")]:
    assert old in src, old
    alt = run(src.replace(old, new))
    changed = [i for i, (a, b) in enumerate(zip(base, alt, strict=True)) if a != b]
    print(name, "changed line indices", changed, "lengths", len(base), len(alt))
    for i in changed:
        print("  base:", base[i][:90])
        print("  alt :", alt[i][:90])
    print("  offsets_nondecreasing:", [l for l in alt if l.startswith("offsets_nondecreasing")])
    print("  lines from index 14 (offsets, batch) unchanged:", base[14:] == alt[14:])
