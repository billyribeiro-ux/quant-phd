"""Write the SC1 project-grader mutants as complete modules (VERIFIER_RULES 2.6 item 3).

Each mutant is the reference solution with exactly one change. Every replacement must match exactly once,
or the generator stops. The first docstring line of each mutant names the student error.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
REFERENCE = ROOT / "course/modules/SC/SC1/grader/reference.py"
OUT = ROOT / "ledgers/SC1/mutants"

MUTANTS: list[tuple[str, str, list[tuple[str, str]]]] = [
    (
        "m01_reflection_factor_dropped",
        "Reflection factor dropped: reflection_tail returns P(B_t >= a) with no factor 2.",
        [("    return math.erfc(a / math.sqrt(2.0 * t))", "    return 0.5 * math.erfc(a / math.sqrt(2.0 * t))")],
    ),
    (
        "m02_scale_sqrt_2t_became_sqrt_t",
        "Scale confusion: reflection_tail uses sqrt(t) in the erfc argument instead of sqrt(2t).",
        [("    return math.erfc(a / math.sqrt(2.0 * t))", "    return math.erfc(a / math.sqrt(t))")],
    ),
    (
        "m03_horizon_off_by_one",
        "Horizon off by one: the grid maximum drops the final grid point (k <= n - 1 only).",
        [
            (
                "    indicators = [1.0 if max(values) >= level else 0.0 for values in paths]",
                "    indicators = [1.0 if max(values[:-1], default=-math.inf) >= level else 0.0 for values in paths]",
            )
        ],
    ),
    (
        "m04_lookahead_extra_point",
        "Lookahead: the grid maximum includes one extra grid point beyond the horizon (n + 1 steps).",
        [("    paths = _grid_paths(instance, n_steps)\n    indicators", "    paths = _grid_paths(instance, n_steps + 1)\n    indicators")],
    ),
    (
        "m05_standard_error_ignored",
        "Standard error ignored: discrete_max_exceedance returns a standard error of 0.0 with a correct estimate.",
        [("    return mean, math.sqrt(variance) / math.sqrt(count)\n\n\ndef nested", "    return mean, 0.0\n\n\ndef nested")],
    ),
    (
        "m06_divisor_n_not_n_minus_one",
        "Divisor error: the sample variance of the indicators uses divisor N instead of N - 1.",
        [("    variance = sum((x - mean) ** 2 for x in indicators) / (count - 1)", "    variance = sum((x - mean) ** 2 for x in indicators) / count")],
    ),
    (
        "m07_nested_counts_swapped",
        "Nested grids reversed: nested_grid_counts returns the coarse and fine counts in swapped order.",
        [("    return fine, coarse", "    return coarse, fine")],
    ),
    (
        "m08_level_doubled_in_tail",
        "Level doubled: reflection_tail(a, t) is computed as reflection_tail(2 a, t).",
        [("    return math.erfc(a / math.sqrt(2.0 * t))", "    return math.erfc(2.0 * a / math.sqrt(2.0 * t))")],
    ),
    (
        "m09_seed_zero_hard_coded",
        "Hard-coded answer: discrete_max_exceedance returns the Lab 3 numbers whenever the instance seed is 0.",
        [
            (
                '    if n_steps < 1:\n        raise ValueError("the grid needs at least one step")\n    if int(instance["n_paths"]) < 2:',
                '    if int(instance["seed"]) == 0:\n        return 0.059548, 0.010735\n'
                '    if n_steps < 1:\n        raise ValueError("the grid needs at least one step")\n    if int(instance["n_paths"]) < 2:',
            )
        ],
    ),
    (
        "m10_nonpositive_time_accepted",
        "Invalid input accepted: reflection_tail returns 0.0 for t <= 0 instead of raising ValueError.",
        [
            (
                '    if t <= 0:\n        raise ValueError("the time t must be positive for the reflection tail")',
                "    if t <= 0:\n        return 0.0",
            )
        ],
    ),
    (
        "m11_coarse_grid_shifted_by_one",
        "Coarse grid off by one: samples steps 1, 1 + s, 1 + 2s, ... instead of s, 2s, ..., so it is not a subset of the fine grid.",
        [
            (
                "    coarse = sum(1 for values in paths if max(values[stride - 1 :: stride]) >= level)",
                "    coarse = sum(1 for values in paths if max(values[0::stride]) >= level)",
            )
        ],
    ),
    (
        "m12_srw_strict_inequality",
        "Strict inequality: srw_terminal_count counts S_n > a and drops the endpoint a itself.",
        [("if 2 * j - n >= a)", "if 2 * j - n > a)")],
    ),
    (
        "m13_divisibility_check_omitted",
        "Divisibility check omitted: a coarse grid that does not divide the fine grid is silently accepted.",
        [("    if n_coarse < 1 or n_fine % n_coarse != 0:", "    if n_coarse < 1:")],
    ),
    (
        "m14_srw_max_forgets_reflection_term",
        "Reflection term forgotten: srw_max_count returns the endpoint count at a alone.",
        [("    return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)", "    return srw_terminal_count(n, a)")],
    ),
    (
        "m16_nested_fine_zero_not_rejected",
        "Named condition skipped: nested_grid_counts does not reject n_fine < 1 (no ValueError for an empty fine grid).",
        [('    if n_fine < 1:\n        raise ValueError("the fine grid needs at least one step")\n', "")],
    ),
    (
        "m17_nested_coarse_zero_not_rejected",
        "Named condition skipped: nested_grid_counts does not reject n_coarse < 1 (the divisibility test alone runs).",
        [('    if n_coarse < 1 or n_fine % n_coarse != 0:', "    if n_fine % n_coarse != 0:")],
    ),
    (
        "m15_increment_scale_missing_square_root",
        "Increment scale: the Gaussian increments use H / n as the standard deviation (square root missing).",
        [('    sd = math.sqrt(float(instance["H"]) / n_steps)', '    sd = float(instance["H"]) / n_steps')],
    ),
]


def main() -> None:
    source = REFERENCE.read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    body_start = re.search(r'^""".*?"""\n', source, flags=re.S)
    if body_start is None:
        raise SystemExit("reference.py has no module docstring")
    rest = source[body_start.end() :]
    for name, description, edits in MUTANTS:
        text = rest
        for old, new in edits:
            count = text.count(old)
            if count != 1:
                raise SystemExit(f"{name}: replacement matched {count} times")
            text = text.replace(old, new)
        module = f'"""{description}\n\nSingle-change copy of grader/reference.py, written by the verifier.\n"""\n' + text
        (OUT / f"{name}.py").write_text(module, encoding="utf-8")
        print(f"wrote {name}.py")


if __name__ == "__main__":
    main()
