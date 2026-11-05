"""Round-11 probe: is the stop-when-either alternative (alt10) bitwise different from the reference on some input?

Loads both modules by path (no import of learner code into the verifier's namespace), runs projection_repair with
tol in {1e-3, 1e-6, 1e-10} on seeded instances, and counts differing outputs. Run from the checkout root.
"""

import importlib.util
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "course/modules/M/M3/grader"))
from instance import make_instance  # noqa: E402


def load(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


ref = load("ref", ROOT / "course/modules/M/M3/grader/reference.py")
alt = load("alt10", ROOT / "ledgers/M3/alternatives/alt10_stop_when_either_gap_or_change.py")
differ = 0
total = 0
for seed in range(50):
    inst = make_instance(seed)
    for tol in (1e-3, 1e-6, 1e-10):
        total += 1
        a = ref.projection_repair(inst["corr"], tol=tol)
        b = alt.projection_repair(inst["corr"], tol=tol)
        if a != b:
            differ += 1
print(f"projection_repair outputs differing between reference and alt10: {differ} of {total} (seeds 0-49)")
