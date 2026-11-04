"""Sample seeds 0-19: validity, interior root and distinctness of the instances (round 5).
Usage: python -I sample_instances_r5.py <checkout-root>
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
g = root / "course/modules/E/E4/grader"


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


inst = load(g / "instance.py", "inst")
ref = load(g / "reference.py", "ref")
pairs, fracs, bad = set(), set(), []
for seed in range(20):
    d = inst.make_instance(seed)
    sd, c = d["noise_sd"], d["info_cost"]
    assert set(d) == {"noise_sd", "info_cost"}
    valid = inst.NOISE_SD_RANGE[0] <= sd <= inst.NOISE_SD_RANGE[1] and inst.INFO_COST_RANGE[0] <= c <= inst.INFO_COST_RANGE[1]
    out = ref.solve_model(sd, c)
    lam = out["informed_fraction"]
    interior = 0.0 < lam < 1.0 and ref.gap_at_zero(sd, c) > 0.0 and ref.indifference_gap(1.0, sd, c) < 0.0
    if not (valid and interior):
        bad.append(seed)
    pairs.add((sd, c))
    fracs.add(round(lam, 9))
    print(f"seed {seed:2d}: noise_sd={sd:.3f} info_cost={c:.3f} informed_fraction={lam:.9f} "
          f"informativeness={out['price_informativeness']:.9f} interior={interior}")
print(f"valid and interior: {20 - len(bad)} of 20; bad seeds {bad}; distinct (sd, c) pairs {len(pairs)}; distinct fractions {len(fracs)}")
