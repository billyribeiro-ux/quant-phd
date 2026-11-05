"""Sample 20 seeds (0-19) of the M7 instance generator and print each case's n, its gamma, and the reference answer.

Verifier helper, round 10. Run from the checkout root: python ledgers/M7/scripts/M7-d-r10/instance_sample_r10.py
It checks that every instance is valid (the generator's own feasibility, and the reference accepts it) and that the
answers differ across seeds, not only the labels.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course/modules/M/M7/grader"


def load(name: str, path: Path) -> object:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    sys.path.insert(0, str(GRADER))
    inst = load("instance_m7", GRADER / "instance.py")
    ref = load("reference_m7", GRADER / "reference.py")
    make_instance = inst.make_instance  # type: ignore[attr-defined]
    allocate = ref.allocate  # type: ignore[attr-defined]
    answers = []
    for seed in range(20):
        case = json.loads(make_instance(seed)["payload"])
        n = len(case["mu"])
        feasible_start = abs(sum(case["w0"]) - 1) < 1e-12
        out = allocate(case)
        w = [round(x, 6) for x in out["weights"]]
        active = {
            "lower": sum(1 for m in out["multipliers"]["lower"] if m > 1e-12),
            "upper": sum(1 for m in out["multipliers"]["upper"] if m > 1e-12),
            "sector": sum(1 for m in out["multipliers"]["sector"] if m > 1e-12),
            "turn": out["multipliers"]["turnover_total"] > 1e-12,
        }
        answers.append(tuple(w))
        print(seed, f"n={n}", f"gamma={case['gamma']}", "start_sum_ok", feasible_start, "weights", w, "active", active)
    print("distinct answers over 20 seeds:", len(set(answers)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
