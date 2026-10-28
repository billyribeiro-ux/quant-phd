"""Generate the M5 grader's correct alternatives and student-error mutants from the reference solution.

Each mutant is the reference with exactly one change (one replacement). Each alternative is a different correct
algorithm for the same contract. The generated files are written to ledgers/M5/mutants and ledgers/M5/alternatives.
Run from the repository root:

    .venv/bin/python ledgers/M5/scripts/make_variants.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REFERENCE = ROOT / "course/modules/M/M5/grader/reference.py"
MUTANTS = ROOT / "ledgers/M5/mutants"
ALTERNATIVES = ROOT / "ledgers/M5/alternatives"

SWEEP_OLD = """    out: list[float] = []
    for k in grid:
        available = k**alpha
        best = -math.inf
        for successor, continuation in zip(grid, values, strict=True):
            if successor <= available:
                best = max(best, math.sqrt(available - successor) + beta * continuation)
        out.append(best)
    return out
"""

SOLVE_LOOP_OLD = """    factor = beta / (1 - beta)
    values = [0.0] * len(points)
    iterations = 0
    certified = math.inf
    while iterations < budget:
        new = _sweep(beta, alpha, points, values)
        iterations += 1
        change = max(abs(a - b) for a, b in zip(new, values, strict=True))
        values = new
        certified = factor * change
        if certified <= target:
            break
"""

MUTANTS_SPEC: list[tuple[str, str, str, str]] = [
    # (file stem, description, old text, new text)
    (
        "m01_continuation_divided_by_beta",
        "the continuation value is divided by beta instead of multiplied, which inverts the discount",
        "math.sqrt(available - successor) + beta * continuation)",
        "math.sqrt(available - successor) + continuation / beta)",
    ),
    (
        "m02_certificate_without_beta_factor",
        "the certified error is the last change without the factor beta over one minus beta, which is unsound for beta above one half",
        "        certified = factor * change\n",
        "        certified = change\n",
    ),
    (
        "m03_stop_on_change_report_tol",
        "stops when the last change is at most tol and reports certified_error equal to tol, whatever the true error",
        "        certified = factor * change\n        if certified <= target:\n",
        "        certified = target if change <= target else factor * change\n        if change <= target:\n",
    ),
    (
        "m04_infeasible_successors_clipped_to_zero_utility",
        "successors above the resources are allowed, with consumption clipped at zero, so saving more than one has is possible",
        "            if successor <= available:\n                best = max(best, math.sqrt(available - successor) + beta * continuation)\n",
        "            best = max(best, math.sqrt(max(available - successor, 0.0)) + beta * continuation)\n",
    ),
    (
        "m05_output_equals_capital",
        "resources are the capital itself, so the production exponent alpha is dropped from the model",
        "        available = k**alpha\n        best = -math.inf\n",
        "        available = k\n        best = -math.inf\n",
    ),
    (
        "m06_off_by_one_sweep_budget",
        "the sweep loop runs one sweep past max_iter, so iterations can exceed the budget by one",
        "    while iterations < budget:\n",
        "    while iterations <= budget:\n",
    ),
    (
        "m07_resources_snapped_down_to_grid",
        "resources are snapped down to the largest grid point before the feasibility test, which changes the fixed point",
        "        available = k**alpha\n        best = -math.inf\n",
        "        available = max(g for g in grid if g <= k**alpha)\n        best = -math.inf\n",
    ),
    (
        "m08_max_replaced_by_min",
        "the successor choice takes the minimum instead of the maximum",
        "best = max(best, math.sqrt(available - successor) + beta * continuation)",
        "best = min(best, math.sqrt(available - successor) + beta * continuation)",
    ),
    (
        "m09_boolean_budget_accepted",
        "max_iter accepts a boolean, so True is read as a budget of one sweep",
        "    if isinstance(max_iter, bool) or not isinstance(max_iter, int) or max_iter < 1:\n",
        "    if not isinstance(max_iter, int) or max_iter < 1:\n",
    ),
    (
        "m10_beta_equal_to_one_accepted",
        "beta equal to one is accepted, although the operator is then not a contraction",
        "    if not 0 < beta < 1:\n",
        "    if not 0 < beta <= 1:\n",
    ),
    (
        "m11_equal_grid_points_accepted",
        "a grid with two equal points is accepted, although the grid must be strictly increasing",
        "    if any(points[i] >= points[i + 1] for i in range(len(points) - 1)):\n",
        "    if any(points[i] > points[i + 1] for i in range(len(points) - 1)):\n",
    ),
    (
        "m12_zero_tolerance_accepted",
        "a tolerance of zero is accepted instead of refused",
        "    if not number > 0:\n",
        "    if not number >= 0:\n",
    ),
    (
        "m13_first_grid_point_bound_loosened",
        "a first grid point up to 1.5 is accepted, so a state may have no feasible successor",
        "    if points[0] > 1:\n",
        "    if points[0] > 1.5:\n",
    ),
]

ALTERNATIVES_SPEC: list[tuple[str, str, list[tuple[str, str]]]] = [
    (
        "alt1_gauss_seidel_in_place",
        "Alternative: the solver's sweeps are in place (Gauss-Seidel); the operator stays synchronous; the bound is the same.",
        [
            (
                "def bellman_operator(",
                """def _in_place(beta: float, alpha: float, grid: list[float], values: list[float]) -> list[float]:
    \"\"\"One in-place (Gauss-Seidel) sweep for the solver: each state uses the successors already updated.\"\"\"
    out = list(values)
    for index, k in enumerate(grid):
        available = k**alpha
        best = -math.inf
        for successor, continuation in zip(grid, out, strict=True):
            if successor <= available:
                best = max(best, math.sqrt(available - successor) + beta * continuation)
        out[index] = best
    return out


def bellman_operator(""",
            ),
            ("        new = _sweep(beta, alpha, points, values)\n", "        new = _in_place(beta, alpha, points, values)\n"),
        ],
    ),
    (
        "alt2_residual_stop",
        "Alternative: stops on the residual of the current iterate, reports residual over one minus beta.",
        [
            (
                SOLVE_LOOP_OLD,
                """    values = [0.0] * len(points)
    iterations = 0
    certified = math.inf
    while iterations < budget:
        new = _sweep(beta, alpha, points, values)
        iterations += 1
        certified = max(abs(a - b) for a, b in zip(new, values, strict=True)) / (1 - beta)
        if certified <= target:
            break
        values = new
""",
            )
        ],
    ),
    (
        "alt3_comprehension_with_feasible_index_lists",
        "Alternative: vectorized-style comprehension over precomputed feasible index lists, with a half power.",
        [
            (
                SWEEP_OLD,
                """    out: list[float] = []
    for k in grid:
        available = k**alpha
        feasible = [j for j, successor in enumerate(grid) if successor <= available]
        out.append(max([(available - grid[j]) ** 0.5 + beta * values[j] for j in feasible]))
    return out
""",
            )
        ],
    ),
    (
        "alt4_bisect_for_feasible_successors",
        "Alternative: the feasible successors are the prefix of the sorted grid found by bisection.",
        [
            (
                "import math\n",
                "import math\nfrom bisect import bisect_right\n",
            ),
            (
                SWEEP_OLD,
                """    out: list[float] = []
    for k in grid:
        available = k**alpha
        last = bisect_right(grid, available)
        out.append(max(math.sqrt(available - grid[j]) + beta * values[j] for j in range(last)))
    return out
""",
            ),
        ],
    ),
    (
        "alt5_reverse_order_synchronous_sweep",
        "Alternative: synchronous sweep that visits the states from the largest to the smallest.",
        [
            (
                SWEEP_OLD,
                """    out: list[float] = [0.0] * len(grid)
    for index in reversed(range(len(grid))):
        available = grid[index] ** alpha
        best = -math.inf
        for successor, continuation in zip(grid, values, strict=True):
            if successor <= available:
                best = max(best, math.sqrt(available - successor) + beta * continuation)
        out[index] = best
    return out
""",
            )
        ],
    ),
]


def replaced(source: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        if source.count(old) != 1:
            raise SystemExit(f"anchor text occurs {source.count(old)} times, expected once: {old[:60]!r}")
        source = source.replace(old, new)
    return source


def with_docstring(source: str, text: str) -> str:
    """Replace the module docstring with one line that describes the change; mutate_graders reads that line."""
    start = source.index('"""')
    end = source.index('"""', start + 3) + 3
    return '"""' + text + '"""' + source[end:]


def seed_zero_answer() -> str:
    """The seed-0 parameters and the reference output for seed 0, as literals for the hard-coded mutant."""
    import importlib.util

    grader = ROOT / "course/modules/M/M5/grader"
    spec = importlib.util.spec_from_file_location("instance_m5", grader / "instance.py")
    ref_spec = importlib.util.spec_from_file_location("reference_m5", grader / "reference.py")
    assert spec is not None and spec.loader is not None and ref_spec is not None and ref_spec.loader is not None
    instance = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(instance)
    reference = importlib.util.module_from_spec(ref_spec)
    ref_spec.loader.exec_module(reference)
    inst = instance.make_instance(0)
    out = reference.solve({"beta": inst["beta"], "alpha": inst["alpha"]}, inst["grid"], inst["tol"], 100_000)
    return f"{inst['beta']!r}, {inst['alpha']!r}, {len(inst['grid'])}, {out!r}"


def main() -> int:
    source = REFERENCE.read_text(encoding="utf-8")
    beta0, alpha0, size0, canned = seed_zero_answer().split(", ", 3)
    seed_zero_mutant = (
        "m14_hard_coded_seed_zero_answer",
        "returns a stored answer whenever beta, alpha and the grid size match seed 0, whatever tol and max_iter are",
        "    target = _tolerance(tol)\n",
        f"    if beta == {beta0} and alpha == {alpha0} and len(points) == {size0}:\n"
        f"        return {canned}\n"
        "    target = _tolerance(tol)\n",
    )
    MUTANTS_SPEC.append(seed_zero_mutant)
    MUTANTS.mkdir(parents=True, exist_ok=True)
    ALTERNATIVES.mkdir(parents=True, exist_ok=True)
    for stem, description, old, new in MUTANTS_SPEC:
        text = replaced(source, [(old, new)])
        (MUTANTS / f"{stem}.py").write_text(with_docstring(text, description) + "\n", encoding="utf-8")
    for stem, description, pairs in ALTERNATIVES_SPEC:
        text = replaced(source, pairs)
        (ALTERNATIVES / f"{stem}.py").write_text(with_docstring(text, description) + "\n", encoding="utf-8")
    print(f"wrote {len(MUTANTS_SPEC)} mutants and {len(ALTERNATIVES_SPEC)} alternatives")
    return 0


if __name__ == "__main__":
    sys.exit(main())
