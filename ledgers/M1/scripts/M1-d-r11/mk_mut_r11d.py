"""Writes the round-11 verifier student-error mutants r11d_01 to r11d_04 of M1-d from the grader reference (run with python -I).

usage: mk_mut_r11d.py <reference.py> <outdir>
"""

import pathlib
import sys

REF = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
src = REF.read_text(encoding="utf-8")


def rep(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old
    return text.replace(old, new)


muts = {
    "r11d_01_closing_balance_ignores_interest.py": (
        "Closing balance is the opening balance less the whole payment, so the interest is never repaid and the schedule does not clear.",
        rep(src, "        closing = opening - principal_paid", "        closing = opening - paid"),
    ),
    "r11d_02_growing_perpetuity_first_payment_at_time_zero.py": (
        "Growing perpetuity values the stream one period early, as (1 + growth) / (rate - growth), a timing error on the first payment.",
        rep(src, "    return 1 / (r - g)\n", "    return (1 + g) / (r - g)\n"),
    ),
    "r11d_03_annuity_tiny_rate_treated_as_zero.py": (
        "Annuity factor treats any rate below 1e-9 in size as zero and returns the number of periods, a cutoff the specification does not state.",
        rep(src, "    if r == 0:\n        return float(n)\n    return (1 - (1 + r) ** -n) / r",
            "    if abs(r) < 1e-9:\n        return float(n)\n    return (1 - (1 + r) ** -n) / r"),
    ),
    "r11d_04_final_payment_level_principal_opening.py": (
        "The final month pays the level amount, while its principal is the whole opening balance, so the last row does not add up: payment is not interest plus principal.",
        rep(src, "        paid = payment if period < n else opening + interest\n        principal_paid = paid - interest",
            "        paid = payment\n        principal_paid = opening if period == n else paid - interest"),
    ),
}
for name, (doc, text) in muts.items():
    body = f'"""{doc}"""\n' + text.split('"""', 2)[2]
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
