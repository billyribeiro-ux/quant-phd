"""Write the round-3 verifier mutants (student errors) for the M7 project into ledgers/M7/mutants/.

Each mutant is the reference solution with exactly one replacement; the script asserts that each old text occurs once,
so a mutant cannot silently equal the reference. Run from the checkout root: .venv/bin/python <this file> <checkout>.
"""

from __future__ import annotations

import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")
out_dir = root / "ledgers/M7/mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "w01_start_sum_tolerance_1e-8.py": (
        "Student error w01: the starting-portfolio sum is accepted to a tolerance of 1e-8, where the page states 1e-9.",
        [('if abs(sum(w0, Fraction(0)) - 1) > TOL:', 'if abs(sum(w0, Fraction(0)) - 1) > Fraction(1, 10**8):')],
    ),
    "w02_sector_multiplier_sign_flipped_in_certificate.py": (
        "Student error w02: the sector multiplier enters the certificate's stationarity residual with a minus sign.",
        [('+ sol["sector"][problem.sector[i]]', '- sol["sector"][problem.sector[i]]')],
    ),
    "w03_gamma_below_one_hundred_thousandth_refused.py": (
        "Student error w03: a risk aversion below 1e-5 is refused as not positive, so the valid gamma of 1e-6 is lost.",
        [('    if gamma <= 0:\n        raise ValueError("gamma must be positive")',
          '    if gamma < Fraction(1, 10**5):\n        raise ValueError("gamma must be positive")')],
    ),
    "w04_turnover_multipliers_split_evenly.py": (
        "Student error w04: the total turnover multiplier is split evenly between the plus and minus multipliers, ignoring the sign of each displacement.",
        [('        plus[i] = (kappa + net) / 2\n        minus[i] = (kappa - net) / 2',
          '        plus[i] = kappa / 2\n        minus[i] = kappa / 2')],
    ),
    "w07_sector_cap_for_empty_sector_truncated.py": (
        "Student error w07: a sector_caps list with one cap too many is cut to the number of sector labels, so a cap for an empty sector is silently ignored.",
        [('    caps = _vector(instance["sector_caps"], "sector_caps")',
          '    caps = _vector(instance["sector_caps"], "sector_caps")[: max(instance["sector"]) + 1]')],
    ),
    "w06_turnover_as_signed_sum.py": (
        "Student error w06: the turnover limit is written as one signed sum of displacements, so only the all-plus sign form is imposed.",
        [('for signs in product((1, -1), repeat=n):', 'for signs in [(1,) * n]:')],
    ),
}

for name, (description, replacements) in MUTANTS.items():
    text = ref
    for old, new in replacements:
        if text.count(old) != 1:
            raise SystemExit(f"{name}: expected one occurrence of {old!r}, found {text.count(old)}")
        text = text.replace(old, new)
    if not text.startswith('"""'):
        raise SystemExit(f"{name}: the reference no longer opens with a docstring")
    text = '"""' + description + "\n\n" + text[3:]
    (out_dir / name).write_text(text, encoding="utf-8")
    print("wrote", name)
