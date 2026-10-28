"""Write ten student-error mutants of the M7 reference into ledgers/M7/mutants/ (round 5, slice d, fixer).

Each mutant is grader/reference.py with one replaced text; every search text must occur exactly once.
The ten cover the enumerated refusal classes of the page: sign and tolerance at each named limit, each bound order
for every asset (not only asset 0), symmetry for every pair, sector labels, the starting-portfolio tolerance.
Usage: python3 make_fixer_mutants_r5.py <checkout-root>
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REFERENCE = ROOT / "course/modules/M/M7/grader/reference.py"
OUT = ROOT / "ledgers/M7/mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "y01_gamma_at_most_one_billionth_refused": (
        "Student error y01: a gamma of at most 1e-9 is refused as not positive, so a small valid gamma is lost.",
        [("    if gamma <= 0:", "    if gamma <= Fraction(1, 10**9):")],
    ),
    "y02_gamma_tolerance_accepts_small_negative": (
        "Student error y02: a gamma down to minus 1e-9 is accepted, so a slightly negative risk aversion passes.",
        [("    if gamma <= 0:", "    if gamma <= -TOL:")],
    ),
    "y03_turnover_tolerance_accepts_small_negative": (
        "Student error y03: a turnover limit down to minus 1e-9 is accepted, so only clearly negative limits fail.",
        [("    if tau < 0:", "    if tau < -TOL:")],
    ),
    "y04_turnover_zero_refused": (
        "Student error y04: a turnover limit of exactly zero is refused, so the valid boundary is lost.",
        [("    if tau < 0:", "    if tau <= 0:")],
    ),
    "y05_bound_order_tolerance_1e-9": (
        "Student error y05: a lower bound above its upper bound is accepted when the excess is at most 1e-9.",
        [
            (
                "    if any(lower[i] > upper[i] for i in range(n)):",
                "    if any(lower[i] > upper[i] + TOL for i in range(n)):",
            )
        ],
    ),
    "y06_bound_order_checked_for_first_asset_only": (
        "Student error y06: the lower-above-upper check looks at asset 0 only, so a later asset passes.",
        [("    if any(lower[i] > upper[i] for i in range(n)):", "    if lower[0] > upper[0]:")],
    ),
    "y07_symmetry_checked_for_first_pair_only": (
        "Student error y07: symmetry of sigma is checked for the pair (0, 1) only, so an asymmetric later pair passes.",
        [
            (
                "    if any(sigma[i][j] != sigma[j][i] for i in range(n) for j in range(n)):",
                "    if sigma[0][1] != sigma[1][0]:",
            )
        ],
    ),
    "y08_sector_label_negative_wraps": (
        "Student error y08: a sector label of minus one is read as the last sector (negative indexing).",
        [("        if not 0 <= label < len(caps):", "        if not -len(caps) <= label < len(caps):")],
    ),
    "y09_start_upper_tolerance_1e-8": (
        "Student error y09: the starting weight may exceed its upper bound by 1e-8, not the 1e-9 the page states.",
        [("w0[i] > upper[i] + TOL for i in range(n)):", "w0[i] > upper[i] + Fraction(1, 10**8) for i in range(n)):")],
    ),
    "y10_sector_cap_checked_for_first_sector_only": (
        "Student error y10: the starting sector caps are checked for sector 0 only, so a later breach passes.",
        [("    for k, cap in enumerate(caps):", "    for k, cap in enumerate(caps[:1]):")],
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
        _, _, rest = text.partition('"""')
        _, _, body = rest.partition('"""')
        mutant = (
            f'"""{description}\n\nOne change to grader/reference.py, written by the M7 fixer (round 5).\n"""' + body
        )
        (OUT / f"{name}.py").write_text(mutant, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
