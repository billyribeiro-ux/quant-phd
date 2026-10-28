"""Writes ten round-10 student-error mutants (full modules) derived from the reference by one replacement each."""
import ast
from pathlib import Path

REF = Path("/Users/billyribeiro/dev/quant-phd/course/modules/M/M1/grader/reference.py").read_text(encoding="utf-8")
OUT = Path("/Users/billyribeiro/dev/quant-phd/ledgers/M1/mutants")

MUTANTS = [
    ("r10_01_due_coerces_periods_with_int",
     "Due annuity coerces its period count with int(), so 12.0 and True are accepted instead of refused.",
     '    return annuity_factor(rate, periods) * (1 + _real("rate", rate))',
     '    return annuity_factor(rate, int(periods)) * (1 + _real("rate", rate))'),
    ("r10_02_perpetuity_accepts_a_string_rate",
     "Perpetuity converts its rate with float(), so the string '0.05' is accepted as a rate.",
     '    r = _real("rate", rate)\n    if r <= 0:\n        raise ValueError("a perpetuity',
     '    r = float(rate)\n    if r <= 0:\n        raise ValueError("a perpetuity'),
    ("r10_03_perpetuity_accepts_infinite_rate",
     "Perpetuity keeps a float rate without the finiteness check, so an infinite rate returns 0.0 instead of raising.",
     '    r = _real("rate", rate)\n    if r <= 0:\n        raise ValueError("a perpetuity',
     '    r = float(rate) if isinstance(rate, float) else _real("rate", rate)\n    if r <= 0:\n        raise ValueError("a perpetuity'),
    ("r10_04_growing_perpetuity_has_no_growth_floor",
     "Growing perpetuity drops the guard that growth is above -1, so a growth of -1.5 is evaluated, not refused.",
     '    if g <= -1:\n        raise ValueError("growth must be above -1")\n',
     ''),
    ("r10_05_growing_perpetuity_margin_below_the_rate",
     "Growing perpetuity refuses any growth within 0.001 of the rate, although growth below the rate is valid.",
     '    if g >= r:\n        raise ValueError("growth must be below the rate',
     '    if g >= r - 0.001:\n        raise ValueError("growth must be below the rate'),
    ("r10_06_schedule_refuses_a_one_cent_loan",
     "A principal check of two or more cents: a one-cent loan is refused, although the specification allows one cent.",
     '    if isinstance(value, bool) or not isinstance(value, int) or value < 1:\n        raise ValueError("principal_cents',
     '    if isinstance(value, bool) or not isinstance(value, int) or value < 2:\n        raise ValueError("principal_cents'),
    ("r10_07_final_payment_overshoots_by_one_cent",
     "The last payment is the balance plus its interest plus one cent, so the schedule closes at -1 cent, not zero.",
     '        paid = payment if period < n else opening + interest\n',
     '        paid = payment if period < n else opening + interest + 1\n'),
    ("r10_08_interest_rounded_up_to_whole_cents",
     "Monthly interest is rounded up to whole cents (ceiling), so a fraction below half a cent goes up, not down.",
     '        interest = _nearest_cent(opening * i)\n',
     '        interest = math.ceil(opening * i)\n'),
    ("r10_09_growing_denominator_uses_absolute_growth",
     "Growing perpetuity computes 1 / (rate - |growth|), so a negative growth lowers the value instead of raising it.",
     '    return 1 / (r - g)\n',
     '    return 1 / (r - abs(g))\n'),
    ("r10_10_level_payment_accepts_a_string_rate",
     "Level payment reads a string annual rate as a decimal, so '0.05' is accepted instead of refused.",
     '    i = _exact_rate(_annual_rate(annual_rate)) / 12\n',
     '    i = (Fraction(annual_rate) if isinstance(annual_rate, str) else _exact_rate(_annual_rate(annual_rate))) / 12\n'),
]

for name, doc, old, new in MUTANTS:
    assert REF.count(old) == 1, (name, REF.count(old))
    text = REF.replace(old, new)
    text = text.replace('"""Reference solution', f'"""{doc}\n\nMutant of the reference (student error). Original header follows.\n\n"""Reference solution', 1) \
        if False else text
    # the mutant's description is its module docstring, first line
    body = text.split('"""', 2)[2]
    text = f'"""{doc}"""\n' + body
    ast.parse(text)
    (OUT / f"{name}.py").write_text(text, encoding="utf-8")
    print("wrote", name)
