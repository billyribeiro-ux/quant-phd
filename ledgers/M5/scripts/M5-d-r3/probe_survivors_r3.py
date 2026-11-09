"""Round 3, slice d: behaviour of the three new survivors against the reference, on inputs the page's definition covers.

Usage: python3 -I probe_survivors_r3.py <checkout-root>. Loads modules from files; prints the outputs side by side.
"""

import importlib.util
import math
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


ref = load("ref", root / "course/modules/M/M5/grader/reference.py")
m1 = load("m1", root / "ledgers/M5/mutants/r3_01_operator_clamps_each_image_at_zero.py")
m2 = load("m2", root / "ledgers/M5/mutants/r3_02_continuation_uses_absolute_value.py")
m3 = load("m3", root / "ledgers/M5/mutants/r3_03_feasibility_tie_tolerance_of_1e-14.py")
p = {"beta": 0.9, "alpha": 0.5}
grid = [0.5, 0.9, 1.4]

v = [-1.0, 0.0, 0.5]
print("negative V, reference BV:", ref.bellman_operator(p, grid, v))
print("negative V, r3_01 BV:    ", m1.bellman_operator(p, grid, v))
print("negative V, r3_02 BV:    ", m2.bellman_operator(p, grid, v))

for label, succ in (("0.5+5e-15", 0.5 + 5e-15), ("nextafter(0.5,1)", math.nextafter(0.5, 1.0)), ("0.5+5e-13", 0.5 + 5e-13)):
    g = [0.25, succ]
    for name, mod in (("reference", ref), ("r3_03", m3)):
        try:
            out = mod.bellman_operator(p, g, [0.0, 1.0e6])
        except Exception as exc:  # report, do not hide
            out = f"{type(exc).__name__}: {exc}"
        print(f"successor {label} from k=0.25, {name}: {out}")
