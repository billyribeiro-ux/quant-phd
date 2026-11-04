"""Sample instances for seeds 0-49 (grader/instance.py): ranges, determinism, interior condition, material variation.

Usage: python -I ledgers/E4/scripts/E4-d-r1/sample_instances.py <repo-root>
Uses the verifier's independent model code (indep_model.py) for the interior check, not the reference solver.
"""

import importlib.util
import sys
from pathlib import Path

root = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("inst", root / "course/modules/E/E4/grader/instance.py")
inst = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inst)  # type: ignore[union-attr]
sys.path.insert(0, str(root / "ledgers/E4/scripts/E4-d-r1"))
import indep_model as im  # noqa: E402

rows = []
for seed in range(50):
    a = inst.make_instance(seed)
    b = inst.make_instance(seed)
    assert a == b, f"nondeterministic at seed {seed}"
    sd, c = a["noise_sd"], a["info_cost"]
    in_range = 0.5 <= sd <= 0.75 and 0.12 <= c <= 0.15
    g0 = im.gap_quadrature(1e-9, sd, c)
    g1 = im.gap_quadrature(1.0, sd, c)
    interior = g0 > 0 and g1 < 0
    lam = im.independent_root(sd, c) if interior else None
    rows.append((seed, sd, c, in_range, interior, lam))
bad = [r for r in rows if not (r[3] and r[4])]
print("seeds 0-49: out-of-range or non-interior instances:", bad)
print("distinct (noise, cost) pairs:", len({(r[1], r[2]) for r in rows}))
print("distinct informed fractions (quadrature root, rounded 6 dp):", len({round(r[5], 6) for r in rows if r[5] is not None}))
print("informed fraction range over seeds 0-49:", f"{min(r[5] for r in rows):.4f} .. {max(r[5] for r in rows):.4f}")
print("seed 0:", rows[0][1:3], "seed 1:", rows[1][1:3], "seed 2:", rows[2][1:3])
print("seed 0-19 lambda:", [round(r[5], 4) for r in rows[:20]])
