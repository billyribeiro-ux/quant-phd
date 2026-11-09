"""Write the round-14 student-error mutants of the FC2 reference solution, one exact replacement each.

Each replacement must match exactly once in grader/reference.py; the script asserts that.
"""

from __future__ import annotations

import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/FC/FC2/grader/reference.py").read_text(encoding="utf-8")
out = root / "ledgers/FC2/mutants"

MUTANTS = {
    "r14_a_convexity_flags_a_call_exactly_on_the_chord.py": (
        "Convexity flags a call exactly on the chord (the test is <= 0, not < 0).",
        "if _second_difference(strikes_cents, calls_cents, j) < 0]",
        "if _second_difference(strikes_cents, calls_cents, j) <= 0]",
    ),
    "r14_b_fee_charged_once_per_finding_not_per_leg.py": (
        "Fee charged once per finding while the half-spread is still paid on each of three legs.",
        "per_finding = LEGS_PER_FINDING * (fee + spread)",
        "per_finding = fee + LEGS_PER_FINDING * spread",
    ),
    "r14_c_parity_gap_cents_skips_the_strike_check.py": (
        "parity_gap_cents accepts a zero or negative strike, which the page names as a ValueError condition.",
        '    if isinstance(strike_cents, bool) or not isinstance(strike_cents, int) or strike_cents <= 0:\n'
        '        raise ValueError("strikes must be strictly increasing and positive")\n',
        "",
    ),
    "r14_d_gross_rounded_with_builtin_round_half_to_even.py": (
        "Gross amount rounded with Python's round() on the float value, which sends a half cent to the even cent.",
        "        gross = _half_up(abs(gap))\n",
        "        gross = round(float(abs(gap)))\n",
    ),
    "r14_e_cost_terms_checked_only_when_a_finding_is_kept.py": (
        "scan validates the cost terms only inside the finding branch, so a chain with no finding skips the check.",
        "    _check_cost(fee, spread)\n    per_finding",
        "    per_finding",
    ),
}

for name, (description, old, new) in MUTANTS.items():
    count = ref.count(old)
    assert count == 1, f"{name}: pattern found {count} times"
    text = ref.replace(old, new, 1)
    if name.startswith("r14_e"):
        text = text.replace(
            "        if net > 0:\n            findings.append(\n                {\n                    \"kind\": \"parity\"",
            "        if net > 0:\n            _check_cost(fee, spread)\n            findings.append(\n                {\n                    \"kind\": \"parity\"",
            1,
        )
    body = f'"""{description}\n\nRound-14 verifier mutant of the FC2 reference (grader/reference.py).\n"""\n'
    text = text.replace('"""Reference solution', '"""Mutant of the reference solution', 1)
    text = text.split('"""', 2)[2]
    (out / name).write_text(body + text, encoding="utf-8")
    print("wrote", name)
