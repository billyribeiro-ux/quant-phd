"""Writes the round-11 verifier alternatives of M1-d from the grader reference (run with python -I).

The three alt_r11_* engines are correct by project.html lines 169-178 (different algebraic form, a direct
summation, and integer half-up rounding). The witness raises TypeError (not ValueError) for values of a
non-numeric type, to test whether the suite over-constrains the exception type.
usage: make_alts_r11.py <reference.py> <outdir>
"""

import pathlib
import sys

REF = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
src = REF.read_text(encoding="utf-8")


def rep(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old
    return text.replace(old, new)


witness = src
witness = rep(
    witness,
    '    if isinstance(value, bool) or not isinstance(value, (int, float)):\n        raise ValueError(f"{name} must be a real number")',
    '    if isinstance(value, bool):\n        raise ValueError(f"{name} must be a real number")\n'
    '    if not isinstance(value, (int, float)):\n        raise TypeError(f"{name} must be a real number")',
)
witness = rep(
    witness,
    '    if isinstance(value, bool) or not isinstance(value, int) or value < 0:\n        raise ValueError(f"{name} must be a whole number of periods, zero or more")',
    '    if isinstance(value, (bool, float)):\n        raise ValueError(f"{name} must be a whole number of periods, zero or more")\n'
    '    if not isinstance(value, int):\n        raise TypeError(f"{name} must be a whole number of periods")\n'
    '    if value < 0:\n        raise ValueError(f"{name} must be a whole number of periods, zero or more")',
)
witness = rep(
    witness,
    '    if isinstance(value, bool) or not isinstance(value, int) or value < 1:\n        raise ValueError("months must be a whole number of months, one or more")',
    '    if isinstance(value, (bool, float)):\n        raise ValueError("months must be a whole number of months, one or more")\n'
    '    if not isinstance(value, int):\n        raise TypeError("months must be a whole number")\n'
    '    if value < 1:\n        raise ValueError("months must be a whole number of months, one or more")',
)
witness = rep(
    witness,
    '    if isinstance(value, bool) or not isinstance(value, int) or value < 1:\n        raise ValueError("principal_cents must be a whole number of cents, one or more")',
    '    if isinstance(value, (bool, float)):\n        raise ValueError("principal_cents must be a whole number of cents, one or more")\n'
    '    if not isinstance(value, int):\n        raise TypeError("principal_cents must be a whole number")\n'
    '    if value < 1:\n        raise ValueError("principal_cents must be a whole number of cents, one or more")',
)

alts = {
    "alt_r11_a_direct_sum_annuity.py": rep(
        src,
        "    if r == 0:\n        return float(n)\n    return (1 - (1 + r) ** -n) / r",
        "    if r == 0:\n        return float(n)\n    return sum((1 + r) ** -k for k in range(1, n + 1))",
    ),
    "alt_r11_b_exact_form_without_inverse.py": rep(
        src,
        "    return _nearest_cent(principal * i / (1 - (1 + i) ** -n))",
        "    growth = (1 + i) ** n\n    return _nearest_cent(principal * i * growth / (growth - 1))",
    ),
    "alt_r11_c_integer_half_up.py": rep(
        src,
        "    return math.floor(amount + Fraction(1, 2))",
        "    num, den = amount.numerator, amount.denominator\n    return (2 * num + den) // (2 * den)",
    ),
    "witness_r11_type_error_for_wrong_types.py": witness,
}
for name, text in alts.items():
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
