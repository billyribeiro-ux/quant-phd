"""Writes the round-8 student-error mutants m42-m44 into ledgers/AC1/mutants/ from grader/reference.py.

Each mutant changes exactly one line of reference.py; the old text must match exactly once.
Run: /tmp/verify8-AC1-d/.venv/bin/python ledgers/AC1/scripts/AC1-d-r8/make_r8_mutants.py
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path("/tmp/verify8-AC1-d")
REF_PATH = ROOT / "course/modules/AC/AC1/grader/reference.py"
OUT = ROOT / "ledgers/AC1/mutants"

MUTANTS = [
    (
        "m42_month_end_uses_previous_month_length.py",
        "a student who takes the month length from the month before the period end (February ends are checked against January)",
        '    if parsed.day != calendar.monthrange(parsed.year, parsed.month)[1]:\n',
        '    if parsed.day != calendar.monthrange(parsed.year, parsed.month - 1 or 12)[1]:\n',
    ),
    (
        "m43_negative_credit_taken_as_absolute.py",
        "a student who takes the absolute value of a credit before the non-negative check",
        '    debit, credit = _cents(line["debit"]), _cents(line["credit"])\n',
        '    debit, credit = _cents(line["debit"]), _cents(abs(line["credit"]))\n',
    ),
    (
        "m44_unbalanced_only_when_debits_exceed_credits.py",
        "a student who refuses an entry only when its debits exceed its credits",
        '        if total != 0:\n',
        '        if total > 0:\n',
    ),
]

REF = REF_PATH.read_text(encoding="utf-8")
for name, _description, old, new in MUTANTS:
    assert REF.count(old) == 1, (name, REF.count(old))
    (OUT / name).write_text(REF.replace(old, new), encoding="utf-8")
    print("wrote", name)
