"""Round 6 (AC2 project): writes three NEW student-error mutants (m11-m13) from the reference solution, one edit each."""
from pathlib import Path

REPO = Path("/tmp/verify-ac2r6-p")
REF = REPO / "course/modules/AC/AC2/grader/reference.py"
OUT = REPO / "ledgers/AC2/mutants"
EDITS = {
    "m11_roic_zero_capital_returns_zero.py": (
        '    if avg_capital <= 0.0:\n        raise ValueError("average invested capital must be positive for ROIC to be defined")\n',
        "    if avg_capital <= 0.0:\n        return 0.0\n",
        "MUTANT m11: ROIC returns 0.0 for non-positive average invested capital instead of raising ValueError, a guard that hides an undefined ratio.",
    ),
    "m12_accruals_balance_sheet_adds_current_liabilities_change.py": (
        "numerator = (d_current_assets - d_cash) - d_current_liabilities - depreciation",
        "numerator = (d_current_assets - d_cash) + d_current_liabilities - depreciation",
        "MUTANT m12: balance-sheet accruals add the change in current liabilities instead of subtracting it (a sign error).",
    ),
    "m13_piotroski_gross_margin_weak_inequality.py": (
        "        int(gm > gm_prev),",
        "        int(gm >= gm_prev),",
        "MUTANT m13: Piotroski gross-margin signal uses a weak inequality (>=), so an unchanged margin scores one point.",
    ),
}
src = REF.read_text(encoding="utf-8")
assert src.startswith('"""'), "reference docstring layout changed"
for name, (old, new, doc) in EDITS.items():
    assert src.count(old) == 1, (name, src.count(old))
    text = src.replace(old, new, 1)
    body = text[len('"""'):]
    text = '"""' + doc + "\n\n" + body
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
