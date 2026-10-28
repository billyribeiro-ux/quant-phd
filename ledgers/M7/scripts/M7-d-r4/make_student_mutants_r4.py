"""Write ten student-error mutants of the M7 reference, one change each, into ledgers/M7/mutants/.

Each mutant is the reference with a single replaced text; the script asserts that every search text occurs exactly
once, so no mutant is silently a different program. The first docstring line names the student error.
Usage: python3 make_student_mutants_r4.py <worktree-root>
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REFERENCE = ROOT / "course/modules/M/M7/grader/reference.py"
OUT = ROOT / "ledgers/M7/mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "s01_sigma_pd_checked_on_diagonal_only": (
        "Student error s01: positive definiteness is checked on the diagonal only, so an indefinite Sigma is accepted.",
        [
            (
                '    if not _positive_definite(sigma):\n        raise ValueError("sigma must be positive definite")',
                '    if any(sigma[i][i] <= 0 for i in range(n)):\n        raise ValueError("sigma must be positive definite")',
            )
        ],
    ),
    "s02_empty_sector_cap_never_checked": (
        "Student error s02: a sector cap with no asset in it is never checked, so the extra cap is accepted.",
        [
            (
                '    if any(label not in sector for label in range(len(caps))):\n'
                '        raise ValueError("every sector cap must belong to at least one asset")\n',
                "",
            )
        ],
    ),
    "s03_start_cap_checked_without_tolerance": (
        "Student error s03: the starting sector weight is compared with its cap without the 1e-9 tolerance.",
        [("> cap + TOL:", "> cap:")],
    ),
    "s04_zero_turnover_limit_refused": (
        "Student error s04: a turnover limit of exactly zero is refused, so the zero-turnover case is lost.",
        [('    if tau < 0:\n        raise ValueError("the turnover limit must not be negative")', '    if tau <= 0:\n        raise ValueError("the turnover limit must not be negative")')],
    ),
    "s05_start_sum_tolerance_1e-10": (
        "Student error s05: the starting-portfolio tolerance is 1e-10, so a sum off by 5e-10 is refused.",
        [("TOL = Fraction(1, 10**9)", "TOL = Fraction(1, 10**10)")],
    ),
    "s06_missing_turnover_limit_defaults_to_zero": (
        "Student error s06: a missing turnover_limit field is read as zero instead of refused.",
        [
            ('"sector_caps", "turnover_limit")', '"sector_caps")'),
            ('tau = _scalar(instance["turnover_limit"], "turnover_limit")', 'tau = _scalar(instance.get("turnover_limit", 0.0), "turnover_limit")'),
        ],
    ),
    "s07_non_finite_value_silently_zeroed": (
        "Student error s07: a NaN or infinite scalar is silently read as zero instead of refused.",
        [('            raise ValueError(f"{name} must be finite")', "            return Fraction(0)")],
    ),
    "s08_gamma_must_exceed_1e-5": (
        "Student error s08: gamma must exceed 1e-5, so the valid boundary gamma equal to 1e-6 is refused.",
        [("    if gamma <= 0:\n        raise ValueError(\"gamma must be positive\")", "    if gamma < Fraction(1, 10**5):\n        raise ValueError(\"gamma must be positive\")")],
    ),
    "s09_lower_equal_upper_refused": (
        "Student error s09: a lower bound equal to its upper bound is refused as if the order were strict.",
        [("    if any(lower[i] > upper[i] for i in range(n)):", "    if any(lower[i] >= upper[i] for i in range(n)):")],
    ),
    "s10_top_sector_label_refused": (
        "Student error s10: the highest sector label is refused (labels accepted only below K minus 1).",
        [("        if not 0 <= label < len(caps):", "        if not 0 <= label < len(caps) - 1:")],
    ),
}


def main() -> None:
    source = REFERENCE.read_text(encoding="utf-8")
    for name, (description, replacements) in MUTANTS.items():
        text = source
        for old, new in replacements:
            count = text.count(old)
            if count != 1:
                raise SystemExit(f"{name}: search text occurs {count} times: {old!r}")
            text = text.replace(old, new)
        header, _, rest = text.partition('"""')
        _, _, body = rest.partition('"""')
        mutant = f'"""{description}\n\nOne change to grader/reference.py, written by the M7 fixer (round 4).\n"""' + body
        (OUT / f"{name}.py").write_text(mutant, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
