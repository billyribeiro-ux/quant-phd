# Writes three correct alternative implementations of the AC1 project from the round-18 reference solution.
# Each edit is asserted, so an edit that does not apply stops the script.
import pathlib
REF = pathlib.Path("/tmp/verify19-AC1-d/course/modules/AC/AC1/grader/reference.py")
OUT = pathlib.Path("/tmp/verify19-AC1-d/ledgers/AC1/scripts/AC1-d-r19/alts")
src = REF.read_text(encoding="utf-8")

def edit(text, old, new, count=1):
    assert text.count(old) == count, (text.count(old), old[:60])
    return text.replace(old, new)

# A: previous month end by year/month arithmetic and calendar.monthrange; month-end test by monthrange.
a = edit(src, '''def _previous_month_end(end: str) -> str:
    first = date.fromisoformat(end).replace(day=1)
    return (first - timedelta(days=1)).isoformat()''', '''def _previous_month_end(end: str) -> str:
    parsed = date.fromisoformat(end)
    year, month = (parsed.year - 1, 12) if parsed.month == 1 else (parsed.year, parsed.month - 1)
    return date(year, month, calendar.monthrange(year, month)[1]).isoformat()''')
a = edit(a, "from datetime import date, timedelta", "from datetime import date")
(OUT / "alt_r19_a_month_arithmetic.py").write_text(a, encoding="utf-8")

# B: the cash flow statement and the articulation check compute the net income and the balances without
# calling income_statement (a single flow dictionary is built once and reused).
b = edit(src, '''def cash_flow_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    now, before, flow = _flows(ledger, period_end)
    net_income = income_statement(ledger, period_end)["net_income"]''', '''def _net_income_from_flow(flow: dict[str, int]) -> int:
    return -flow["sales"] - flow["cost_of_goods_sold"] - flow["operating_expenses"] - flow["depreciation_expense"]


def cash_flow_statement(ledger: Ledger, period_end: str) -> dict[str, int]:
    now, before, flow = _flows(ledger, period_end)
    net_income = _net_income_from_flow(flow)''')
b = edit(b, '''    cash_flow = cash_flow_statement(ledger, end)
    net_income = income_statement(ledger, end)["net_income"]''', '''    cash_flow = cash_flow_statement(ledger, end)
    _, _, flow = _flows(ledger, end)
    net_income = _net_income_from_flow(flow)''')
b = edit(b, '''        - income_statement(ledger, end)["depreciation_expense"],''', '''        - flow["depreciation_expense"],''')
(OUT / "alt_r19_b_single_flow_dictionary.py").write_text(b, encoding="utf-8")

# C: balances are cut off by ordinal day numbers instead of ISO string comparison.
c = edit(src, '''def _balances(ledger: Ledger, end: str) -> dict[str, int]:
    totals = dict.fromkeys(ACCOUNTS, 0)
    for day, account, signed in ledger:
        if day <= end:
            totals[account] += signed
    return totals''', '''def _balances(ledger: Ledger, end: str) -> dict[str, int]:
    totals = dict.fromkeys(ACCOUNTS, 0)
    cutoff = date.fromisoformat(end).toordinal()
    for day, account, signed in ledger:
        if date.fromisoformat(day).toordinal() <= cutoff:
            totals[account] += signed
    return totals''')
(OUT / "alt_r19_c_ordinal_cutoff.py").write_text(c, encoding="utf-8")
print("written", sorted(p.name for p in OUT.glob("alt_r19_*.py")))
