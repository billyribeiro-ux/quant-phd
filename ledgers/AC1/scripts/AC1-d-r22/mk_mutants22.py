# Writes three round-22 student-error mutants of the reference solution into ledgers/AC1/mutants/.
# Usage: python -I mk_mutants22.py <checkout>
import sys
from pathlib import Path

checkout = Path(sys.argv[1])
ref = (checkout / "course/modules/AC/AC1/grader/reference.py").read_text(encoding="utf-8")
out = checkout / "ledgers/AC1/mutants"

def make(name: str, pairs: list[tuple[str, str]]) -> None:
    text = ref
    for old, new in pairs:
        assert text.count(old) == 1, (name, text.count(old))
        text = text.replace(old, new)
    (out / f"{name}.py").write_text(text, encoding="utf-8")

# Student: a transaction without a date is posted under a default date instead of being refused.
make(
    "v22_m01_missing_transaction_date_defaults",
    [
        (
            '        if not isinstance(entry, Mapping) or "date" not in entry or "lines" not in entry:',
            '        if not isinstance(entry, Mapping) or "lines" not in entry:',
        ),
        ('        day = _iso_date(entry["date"])', '        day = _iso_date(entry.get("date", "2024-01-01"))'),
    ],
)
# Student: a line without an account is posted to cash instead of being refused.
make(
    "v22_m02_missing_line_account_defaults_to_cash",
    [
        (
            '            if not isinstance(line, Mapping) or not {"account", "debit", "credit"} <= set(line):',
            '            if not isinstance(line, Mapping) or not {"debit", "credit"} <= set(line):',
        ),
        ('            account = line["account"]', '            account = line.get("account", "cash")'),
    ],
)
# Student: the account check skips the empty string, so an empty account name is posted.
make(
    "v22_m03_empty_account_name_accepted",
    [
        (
            '            if not isinstance(account, str) or account not in ACCOUNTS:',
            '            if not isinstance(account, str) or (account != "" and account not in ACCOUNTS):',
        ),
    ],
)
print("written")
