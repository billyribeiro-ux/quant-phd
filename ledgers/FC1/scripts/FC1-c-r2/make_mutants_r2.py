"""Writes three verifier-authored student-error mutants (round 2, FC1 slice c) into ledgers/FC1/mutants/.

Each mutant is reference.py with one change; the first line of each module docstring names the error.
Run from the checkout root: .venv/bin/python ledgers/FC1/scripts/FC1-c-r2/make_mutants_r2.py
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/FC/FC1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/FC1/mutants"


def write(name: str, description: str, old: str, new: str) -> None:
    body = REF.split('"""', 2)[2]  # drop the reference's module docstring
    assert body.count(old) == 1, (name, old)
    text = '"""' + description + "\n\nWritten by the verifier for FC1 slice c, round 2: a student-error mutant of reference.py.\n\"\"\"" + body
    (OUT / name).write_text(text.replace(old, new), encoding="utf-8")


write(
    "c2n01_warns_on_long_schedule.py",
    "Bond warns (a UserWarning) when it has more than eight periods, although the page says no function warns on a valid input.",
    "        self.face_cents = face\n",
    "        if count > 8:\n"
    "            import warnings\n\n"
    "            warnings.warn('long schedule', UserWarning)\n"
    "        self.face_cents = face\n",
)
write(
    "c2n02_refuses_quantity_above_500.py",
    "CashTrade refuses a quantity above 500 units, a limit the page never states; the page names only quantity below 1.",
    "        if units < 1:\n",
    "        if units > 500:\n            raise ValueError('quantity above 500 is not allowed')\n        if units < 1:\n",
)
write(
    "c2n03_price_drops_periods_after_six.py",
    "bond_price_cents discounts only the events of periods 1 to 6, so a bond longer than six periods is priced short.",
    "    for period, amount in bond.events():\n",
    "    for period, amount in bond.events():\n        if period > 6:\n            continue\n",
)
print("written")
