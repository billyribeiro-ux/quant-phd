"""Sample seeds 0-19 of grader/instance.py: validity, interior root, and material difference. Usage: python -I <script> <root>."""

import importlib.util
import math
import sys
from pathlib import Path

root = Path(sys.argv[1])


def load(path: str, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, root / path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


inst = load("course/modules/E/E4/grader/instance.py", "inst")
ref = load("course/modules/E/E4/grader/reference.py", "ref")
rows = []
for seed in range(20):
    d = inst.make_instance(seed)
    sd, c = d["noise_sd"], d["info_cost"]
    valid = all(math.isfinite(x) and x > 0 for x in (sd, c))
    out = ref.solve_model(sd, c)
    interior = 0.0 < out["informed_fraction"] < 1.0
    rows.append((seed, sd, c, valid, interior, round(out["informed_fraction"], 6), round(out["price_informativeness"], 6)))
for r in rows:
    print("seed %2d sd %.3f c %.3f valid %s interior %s lam %.6f inf %.6f" % r)
print("all valid:", all(r[3] for r in rows), "| all interior:", all(r[4] for r in rows))
print("distinct (sd,c):", len({(r[1], r[2]) for r in rows}), "| distinct lam:", len({r[5] for r in rows}))
