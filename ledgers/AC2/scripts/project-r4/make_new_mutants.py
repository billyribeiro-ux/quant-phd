"""Round 4 (AC2 project): writes three NEW student-error mutants (m01-m05) from the reference solution, one edit each."""
import sys
from pathlib import Path

REF = Path("/tmp/verify-ac2r4-p/course/modules/AC/AC2/grader/reference.py")
OUT = Path("/tmp/verify-ac2r4-p/ledgers/AC2/mutants")
EDITS = {
    "m01_roe_on_year_end_equity.py": (
        '"roe": _div(net_income, avg_equity, "average equity"),',
        '"roe": _div(net_income, _get(statements, end, "equity"), "year-end equity"),',
        "MUTANT m01: roe divides net income by year-end equity while leverage uses average equity.",
    ),
    "m02_roic_tax_rate_zero_rejected.py": (
        "if not 0.0 <= rate < 1.0:",
        "if not 0.0 < rate < 1.0:",
        "MUTANT m02: ROIC rejects a zero tax rate (strict lower bound), though the contract allows 0 <= tax_rate.",
    ),
    "m03_piotroski_asset_turnover_current_assets.py": (
        'ato = _div(rev_t, ta_t1, "total assets of the previous year")',
        'ato = _div(rev_t, ta_t, "total assets of the period end")',
        "MUTANT m03: Piotroski asset turnover (signal 9) divides revenue by year-end total assets, not the previous year's.",
    ),
    "m04_roic_negative_capital_passes.py": (
        "if avg_capital <= 0.0:",
        "if avg_capital == 0.0:",
        "MUTANT m04: ROIC raises only on exactly zero average invested capital; negative capital is divided through.",
    ),
    "m05_piotroski_cfo_signal_uses_net_income.py": (
        "int(cfo > 0.0),",
        "int(_get(statements, t, \"net_income\") > 0.0),",
        "MUTANT m05: Piotroski signal 2 tests net income instead of cash flow from operations.",
    ),
}
src = REF.read_text(encoding="utf-8")
for name, (old, new, doc) in EDITS.items():
    assert src.count(old) == 1, (name, src.count(old))
    text = src.replace(old, new, 1)
    # the mutant description is the first line of the module docstring (ast.get_docstring); no second statement
    # is inserted before the __future__ import
    assert text.startswith('"""Reference solution'), name
    text = '"""' + doc + '\n\nReference solution' + text[len('"""Reference solution'):]
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
