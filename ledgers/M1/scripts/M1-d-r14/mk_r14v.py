"""Writes three new student-error mutants (r14v_01 to r14v_03) as edits of the reference solution."""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/M/M1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M1/mutants"
HEAD = '"""Reference solution for the M1 project: annuity_engine.py, the annuity and mortgage engine.'

cases = {
    "r14v_01_schedule_interest_float_rate_over_twelve.py": (
        "Schedule interest multiplies the opening balance by the float annual rate divided by 12 and rounds that float "
        "product, so an exact half cent can land just below the tie.",
        "        interest = _nearest_cent(opening * i)\n",
        "        interest = _nearest_cent(Fraction(opening * (rate / 12)))\n",
    ),
    "r14v_02_level_payment_rounded_to_whole_units.py": (
        "Level payment is rounded to the nearest whole unit of 100 cents instead of the nearest cent.",
        "    return _nearest_cent(principal * i / (1 - (1 + i) ** -n))\n",
        "    return 100 * _nearest_cent(principal * i / (1 - (1 + i) ** -n) / 100)\n",
    ),
    "r14v_03_annual_rate_simplified_to_denominator_1000.py": (
        "The annual rate is simplified with limit_denominator(1000) before the monthly rate is taken, so a rate with "
        "more decimal places is altered.",
        '    return Fraction(repr(annual_rate))\n',
        '    return Fraction(repr(annual_rate)).limit_denominator(1000)\n',
    ),
}
for name, (doc, old, new) in cases.items():
    assert REF.count(old) == 1, name
    body = REF.replace(old, new)
    body = body[body.index('"""', 3) + 3 :]
    text = f'"""{doc}"""' + body
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
