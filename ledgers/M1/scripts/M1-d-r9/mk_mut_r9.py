"""Writes the round-9 student-error mutants m51 to m53 from the reference (verifier-written, round 9)."""
import pathlib
import sys

REF = pathlib.Path("/tmp/verify9-M1-d/course/modules/M/M1/grader/reference.py").read_text(encoding="utf-8")
OUT = pathlib.Path("/tmp/verify9-M1-d/ledgers/M1/mutants")


def mutate(name: str, description: str, old: str, new: str) -> None:
    head, sep, body = REF.partition('"""')
    _, sep2, rest = body.partition('"""')
    assert sep and sep2 and old in rest, name
    text = '"""' + description + '"""' + rest
    assert text.count(old) == 1 or old in text, name
    text = text.replace(old, new, 1)
    (OUT / name).write_text(text, encoding="utf-8")


mutate(
    "m51_tiny_rate_cutoff_1e-8_treated_as_zero.py",
    "Numerical cutoff: an annual rate below 1e-8 is taken as zero, so the level payment is the loan over the months.",
    "    if i == 0:\n        return _nearest_cent(Fraction(principal, n))",
    "    if i == 0 or _annual_rate(annual_rate) < 1e-8:\n        return _nearest_cent(Fraction(principal, n))",
)
mutate(
    "m52_float_closed_form_for_small_rates.py",
    "Float arithmetic for small rates: below an annual rate of 1e-5 the level payment is computed in binary floats.",
    "    if i == 0:\n        return _nearest_cent(Fraction(principal, n))",
    "    if i == 0:\n        return _nearest_cent(Fraction(principal, n))\n"
    "    if 0 < annual_rate < 1e-5:\n"
    "        f = annual_rate / 12\n"
    "        return math.floor(principal * f / (1 - (1 + f) ** -n) + 0.5)",
)
mutate(
    "m53_term_capped_at_360_months.py",
    "Over-tight validation: a term above 360 months is refused, although the specification sets no upper limit.",
    "    if isinstance(value, bool) or not isinstance(value, int) or value < 1:\n        raise ValueError(\"months must be a whole number of months, one or more\")",
    "    if isinstance(value, bool) or not isinstance(value, int) or value < 1 or value > 360:\n        raise ValueError(\"months must be a whole number of months, one or more\")",
)
print("written")
