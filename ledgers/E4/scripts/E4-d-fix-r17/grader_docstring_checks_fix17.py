"""Fixer round 17: numeric checks of numbers quoted in grader docstrings (test_project.py).

Checks the docstring of test_gap_at_zero_fraction_is_the_limit_to_full_precision:
'The gap at fraction 1e-12 differs from the limit by 1e-13 to 4e-13 at these inputs, and the oracle agrees with the
limit to at most 1.1e-16 at them.'

Run: .venv/bin/python -I ledgers/E4/scripts/E4-d-fix-r17/grader_docstring_checks_fix17.py
"""

import importlib.util
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[4]


def load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ref = load(ROOT / "course/modules/E/E4/grader/reference.py", "ref_solution")
# the test module imports solver and instance by name; load its oracle functions with stub modules
import sys  # noqa: E402

sys.modules["solver"] = ref
sys.path.insert(0, str(ROOT / "course/modules/E/E4/grader"))
test = load(ROOT / "course/modules/E/E4/grader/test_project.py", "test_project_mod")


def main() -> None:
    worst_gap_diff = 0.0
    worst_gap_diff_min = float("inf")
    worst_oracle_vs_limit = 0.0
    for sd, cost in [(0.5, 0.30), (0.6, 0.30), (0.75, 0.30), (0.5, 0.50), (0.6, 0.50), (0.75, 0.50)]:
        limit_closed = ref.gap_at_zero(sd, cost)
        limit_oracle = test.oracle_gap(0.0, sd, cost)
        at_small = ref.indifference_gap(1e-12, sd, cost)
        d_small = abs(at_small - limit_closed)
        worst_gap_diff = max(worst_gap_diff, d_small)
        worst_gap_diff_min = min(worst_gap_diff_min, d_small)
        worst_oracle_vs_limit = max(worst_oracle_vs_limit, abs(limit_oracle - limit_closed))
        print(
            f"sd {sd} cost {cost}: |gap(1e-12) - limit| = {d_small:.3e}; "
            f"|oracle(0) - limit| = {abs(limit_oracle - limit_closed):.3e}"
        )
    print(f"|gap(1e-12) - limit| over the six inputs: min {worst_gap_diff_min:.3e}, max {worst_gap_diff:.3e}")
    print(f"|oracle(0) - limit| over the six inputs: max {worst_oracle_vs_limit:.3e}")


if __name__ == "__main__":
    main()
