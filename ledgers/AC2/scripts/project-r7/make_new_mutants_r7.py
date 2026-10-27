"""Round 7 (AC2 project): writes three NEW student-error mutants (m14-m16) from the reference solution, one edit each."""
from pathlib import Path

REPO = Path("/tmp/verify-ac2r7-p")
REF = REPO / "course/modules/AC/AC2/grader/reference.py"
OUT = REPO / "ledgers/AC2/mutants"
EDITS = {
    "m14_modified_jones_regressors_unscaled.py": (
        "design = np.column_stack([1.0 / lag, (data[:, 2] - data[:, 3]) / lag, data[:, 4] / lag])",
        "design = np.column_stack([1.0 / lag, (data[:, 2] - data[:, 3]), data[:, 4] / lag])",
        "MUTANT m14: modified Jones divides the intercept and PP&E regressors by lagged assets but leaves the revenue-less-receivables regressor unscaled.",
    ),
    "m15_dso_without_365_days.py": (
        "    return _div(_get(statements, end, \"receivables\"), revenue, \"revenue\") * _DAYS_PER_YEAR",
        "    return _div(_get(statements, end, \"receivables\"), revenue, \"revenue\")",
        "MUTANT m15: days_sales_outstanding returns receivables over revenue as a fraction of a year, without the 365-day factor.",
    ),
    "m16_previous_year_is_earliest_in_window.py": (
        "        if _YEAR_MIN <= (t - e).days <= _YEAR_MAX and (best is None or e > best):",
        "        if _YEAR_MIN <= (t - e).days <= _YEAR_MAX and (best is None or e < best):",
        "MUTANT m16: _previous picks the earliest period end in the 350-380 day window instead of the latest.",
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
