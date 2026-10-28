"""Writes round-7 survivors m39-m41 (student errors in post) into ledgers/AC1/mutants/ from the reference solution.

Each mutant changes one part of grader/reference.py; the replacement must match exactly once.
Run: /tmp/verify7-AC1-d/.venv/bin/python ledgers/AC1/scripts/AC1-d-r7/make_r7_mutants_b.py
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path("/tmp/verify7-AC1-d")
REF = (ROOT / "course/modules/AC/AC1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/AC1/mutants"
body = REF[REF.index('"""', 3) + 3 :]  # drop the reference module docstring
MUT = {
    "m39_account_name_whitespace_stripped.py": (
        "a student who strips spaces from account names before the chart check, so ' cash ' is accepted as cash",
        '            account = line["account"]\n',
        '            account = line["account"].strip() if isinstance(line["account"], str) else line["account"]\n',
    ),
    "m40_credit_float_accepted.py": (
        "a student who checks the debit amount but lets an integral float on the credit side (5.0) through as 5",
        '            debit, credit = _cents(line["debit"]), _cents(line["credit"])\n',
        '            debit, credit = _cents(line["debit"]), (_cents(line["credit"]) if not isinstance(line["credit"], float) else int(line["credit"]))\n',
    ),
    "m41_week_date_accepted.py": (
        "a student who length-checks a date and trusts date.fromisoformat, so the ISO week form 2024-W01-1 (ten characters) is accepted",
        '    if parsed.isoformat() != value:\n        raise ValueError("a date must be an ISO date, YYYY-MM-DD")\n',
        "",
    ),
}
for name, (desc, old, new) in MUT.items():
    assert body.count(old) == 1, (name, body.count(old))
    text = body.replace(old, new)
    (OUT / name).write_text(f'"""{desc}; one part of the reference solution changed."""\n' + text, encoding="utf-8")
    print("wrote", name)
