"""Writes the round-10 verifier mutants m54 to m58 of M1-d from the grader reference (run with python -I)."""
import pathlib
import sys

REF = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
src = REF.read_text(encoding="utf-8")


def rep(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, old
    return text.replace(old, new)


muts = {
    "m54_growing_perpetuity_refuses_negative_growth.py": (
        "Growing perpetuity refuses any negative growth (student reads growth as non-negative): the value of a negative-growth stream is refused, though -1 < g < r is the rule.",
        rep(src, '    if g <= -1:\n        raise ValueError("growth must be above -1")',
            '    if g < 0:\n        raise ValueError("growth must be non-negative")'),
    ),
    "m55_perpetuity_refuses_rates_below_a_small_floor.py": (
        "Perpetuity adds a small-rate guard (rate below 1e-9 refused as implausible), although the rule is only r > 0.",
        rep(src, '    if r <= 0:\n        raise ValueError("a perpetuity needs a rate above zero: at a rate of zero or less its value is not finite")',
            '    if r < 1e-9:\n        raise ValueError("a perpetuity needs a rate above zero: at a rate of zero or less its value is not finite")'),
    ),
    "m56_schedule_interest_tie_rounds_down.py": (
        "Schedule interest rounds an exact half cent down (ceiling of amount minus one half), not up as the rule says.",
        rep(src, "        interest = _nearest_cent(opening * i)",
            "        interest = -math.floor(-(opening * i - Fraction(1, 2)))"),
    ),
    "m57_term_capped_at_480_months.py": (
        "Term capped at 480 months (forty years), a limit the specification does not state, so a 481-month loan is refused.",
        rep(src, '    if isinstance(value, bool) or not isinstance(value, int) or value < 1:\n        raise ValueError("months must be a whole number of months, one or more")',
            '    if isinstance(value, bool) or not isinstance(value, int) or value < 1 or value > 480:\n        raise ValueError("months must be a whole number of months, one or more")'),
    ),
    "m58_annuity_refuses_rates_below_minus_half.py": (
        "Annuity factor adds a guard refusing any rate at or below minus one half, although the rule is only r > -1 (the test of r = -0.999 is valid).",
        rep(src, '    if r <= -1:\n        raise ValueError("rate must be greater than -1 per period")',
            '    if r <= -0.5:\n        raise ValueError("rate must be greater than -1 per period")'),
    ),
}
for name, (doc, text) in muts.items():
    body = f'"""{doc}"""\n' + text.split('"""', 2)[2]
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
