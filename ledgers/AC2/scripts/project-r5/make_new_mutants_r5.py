"""Round 5 (AC2 project): writes five NEW student-error mutants (m06-m10) from the reference solution, one edit each.

Each edit replaces one unique source line; the assertion makes a mismatch fail loudly instead of silently."""
from pathlib import Path

REF = Path("/tmp/verify-ac2r5-p/course/modules/AC/AC2/grader/reference.py")
OUT = Path("/tmp/verify-ac2r5-p/ledgers/AC2/mutants")
EDITS = {
    "m06_roic_divides_by_year_end_invested_capital.py": (
        "avg_capital = _average(_invested_capital(statements, end), _invested_capital(statements, prev))",
        "avg_capital = _invested_capital(statements, end)",
        "MUTANT m06: ROIC divides NOPAT by year-end invested capital, not by the average of the two year ends.",
    ),
    "m07_accruals_cash_flow_scaled_by_year_end_assets.py": (
        'return _div(_get(statements, end, "net_income") - _get(statements, end, "cfo"), avg_assets, "average assets")',
        'return _div(_get(statements, end, "net_income") - _get(statements, end, "cfo"), _get(statements, end, "total_assets"), "total assets")',
        "MUTANT m07: accruals_cash_flow scales by year-end total assets, although the contract scales by average total assets.",
    ),
    "m08_piotroski_prior_roa_over_prior_year_end_assets.py": (
        'roa_prev = _div(_get(statements, t1, "net_income"), ta_t2, "total assets two years back")',
        'roa_prev = _div(_get(statements, t1, "net_income"), ta_t1, "total assets of the previous year")',
        "MUTANT m08: Piotroski signal 3 scales last year's net income by last year's assets, not by the assets two years back.",
    ),
    "m09_beneish_tata_scaled_by_average_assets.py": (
        'tata = _div(g(t, "net_income") - g(t, "cfo"), ta, "total assets")',
        'tata = _div(g(t, "net_income") - g(t, "cfo"), _average(ta, ta1), "average total assets")',
        "MUTANT m09: Beneish TATA divides by average total assets, not by year-end total assets as the contract states.",
    ),
    "m10_standardize_keeps_the_earliest_filing.py": (
        "options.sort(key=lambda c: (c[0], c[1]), reverse=True)",
        "options.sort(key=lambda c: (c[0], c[1]), reverse=False)",
        "MUTANT m10: standardize keeps the earliest filed annual observation, so the original 10-K wins over a later restatement.",
    ),
}
src = REF.read_text(encoding="utf-8")
assert src.startswith('"""'), "reference docstring layout changed"
for name, (old, new, doc) in EDITS.items():
    assert src.count(old) == 1, (name, src.count(old))
    text = src.replace(old, new, 1)
    head = '"""'
    body = text[len(head):]
    text = head + doc + "\n\n" + body
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
