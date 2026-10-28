"""Writes the round-16 verifier-written student-error mutants from the reference (not the grader).

Usage: python3 -I mk_mutants16.py <reference.py> <mutant dir>
"""
import sys
from pathlib import Path

out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
ref = Path(sys.argv[1]).read_text(encoding="utf-8")

HELPER = '''def _manual_iso_date(value: object) -> str:
    text = _iso_date(value)
    year, month, day = int(text[:4]), int(text[5:7]), int(text[8:10])
    LEAP_RULE
    lengths = {2: 29 if leap else 28, 4: 30, 6: 30, 9: 30, 11: 30}.get(month, 31)
    if not 1 <= day <= lengths:
        raise ValueError("a date must be a real calendar date")
    return text


def post('''

OLD_POST_HEAD = "def post(transactions"
assert ref.count(OLD_POST_HEAD) == 1
OLD_DAY = '        day = _iso_date(entry["date"])\n'
assert ref.count(OLD_DAY) == 1

# m01: the posting rule for dates uses a leap rule with no century rule (2100-02-29 is accepted as a transaction date).
m01 = ref.replace(OLD_POST_HEAD, HELPER.replace("LEAP_RULE", "leap = year % 4 == 0") + "transactions", 1)
m01 = m01.replace(OLD_DAY, '        day = _manual_iso_date(entry["date"])\n')
(out / "v16_m01_post_accepts_2100_02_29_as_a_date.py").write_text(m01, encoding="utf-8")

# m02: the posting rule for dates uses a leap rule with the 100 exception but no 400 exception (2000-02-29 is rejected).
m02 = ref.replace(OLD_POST_HEAD, HELPER.replace("LEAP_RULE", "leap = year % 4 == 0 and year % 100 != 0") + "transactions", 1)
m02 = m02.replace(OLD_DAY, '        day = _manual_iso_date(entry["date"])\n')
(out / "v16_m02_post_rejects_2000_02_29_as_a_date.py").write_text(m02, encoding="utf-8")

# m03: articulation_check does not check the period end at all.
OLD_ART = "def articulation_check(ledger: Ledger, period_end: str) -> dict[str, int]:\n"
assert ref.count(OLD_ART) == 1
OLD_ART_HEAD = OLD_ART + "    end = _month_end(period_end)\n"
assert ref.count(OLD_ART_HEAD) == 1
m03 = ref.replace(OLD_ART_HEAD, OLD_ART + "    end = period_end\n")
(out / "v16_m03_articulation_check_skips_the_month_end_test.py").write_text(m03, encoding="utf-8")
print("wrote", sorted(x.name for x in out.iterdir()))
