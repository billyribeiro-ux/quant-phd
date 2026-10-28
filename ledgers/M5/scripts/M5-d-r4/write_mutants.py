"""Write the round-4 student-error mutants (m62-m67) as complete modules derived from grader/reference.py.

Each mutant is the reference with exactly one replacement; the script asserts the replacement matches once.
Usage: python -I write_mutants.py <checkout-root>
"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/M/M5/grader/reference.py").read_text(encoding="utf-8")
out = root / "ledgers/M5/mutants"

MUTANTS = {
    "m62_alpha_zero_accepted.py": (
        "alpha equal to zero is accepted, because the lower bound of the interval is not strict.",
        'if not 0 < alpha < 1:\n        raise ValueError("alpha must lie in the open interval (0, 1)")',
        'if not 0 <= alpha < 1:\n        raise ValueError("alpha must lie in the open interval (0, 1)")',
    ),
    "m63_iteration_starts_from_utility_of_the_grid.py": (
        "the iteration starts from the utility sqrt(k) of each grid point instead of from the zero vector.",
        "    values = [0.0] * len(points)\n",
        "    values = [math.sqrt(k) for k in points]\n",
    ),
    "m64_change_measured_at_the_last_point_only.py": (
        "the change is measured at the last grid point only, so the certified error can be too small.",
        "        change = max(abs(a - b) for a, b in zip(new, values, strict=True))\n",
        "        change = abs(new[-1] - values[-1])\n",
    ),
    "m65_converged_with_ten_times_the_tolerance.py": (
        "converged is read against ten times the tolerance, so a run above tol reports converged.",
        '        "converged": certified <= target,\n',
        '        "converged": certified <= 10 * target,\n',
    ),
    "m66_iterations_report_the_budget.py": (
        "iterations reports the sweep budget, not the number of sweeps actually made.",
        '        "iterations": iterations,\n',
        '        "iterations": budget,\n',
    ),
    "m67_negative_grid_point_accepted.py": (
        "a negative grid point is accepted, because only a zero point is refused.",
        'if any(point <= 0 for point in points):',
        'if any(point == 0 for point in points):',
    ),
}

for name, (doc, old, new) in MUTANTS.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new, 1)
    text = f'"""{doc}"""\n\n' + body.split('"""', 2)[2].lstrip("\n")
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)
