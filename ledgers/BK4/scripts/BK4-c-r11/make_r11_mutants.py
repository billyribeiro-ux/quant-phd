"""Round-11 (BK4-c) verifier-written student-error mutants of grader/reference.py.

Each mutant is reference.py with exactly one change. The first docstring line names the student error.
Usage: python make_r11_mutants.py <repo_root>   (stdlib only; writes ledgers/BK4/mutants/y11*.py)
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
src = (root / "course/modules/BK/BK4/grader/reference.py").read_text(encoding="utf-8")
ref_first = '"""Reference solution for the BK4 clearing-house simulator (clearing_house.py).'
assert src.count(ref_first) == 1

MUTANTS = {
    "y11a_residual_forgets_the_capital": (
        "Student error: the residual subtracts the margin and the default fund but not the CCP capital, "
        "so the capital is paid twice.",
        [("    residual = loss_cents - margin_paid - fund_paid - capital_paid",
          "    residual = loss_cents - margin_paid - fund_paid")],
    ),
    "y11b_cover_divides_the_count_before_multiplying": (
        "Student error: the cover divides the count by S before multiplying by 10000, so it is zero "
        "unless every scenario is covered.",
        [("    return 10_000 * covered // len(losses_cents)",
          "    return 10_000 * (covered // len(losses_cents))")],
    ),
    "y11c_survivors_prorated_even_past_the_pool": (
        "Student error: when the residual reaches the surviving pool, the survivors are still charged pro rata "
        "to the residual, so no survivor pays its whole default fund and no uncovered loss is reported.",
        [("    if residual >= total_fund:", "    if False:")],
    ),
    "y11d_unknown_defaulter_treated_as_zero_exposure": (
        "Student error: a defaulter id that is not a member is treated as holding zero margin and zero fund "
        "instead of raising ValueError.",
        [
            ("    if defaulter_id not in default_fund_cents or defaulter_id not in initial_margin_cents:\n"
             "        raise ValueError(f\"defaulter_id {defaulter_id} is not one of the member ids\")\n", ""),
            ("    margin_paid = min(loss_cents, initial_margin_cents[defaulter_id])",
             "    margin_paid = min(loss_cents, initial_margin_cents.get(defaulter_id, 0))"),
            ("    fund_paid = min(loss_cents - margin_paid, default_fund_cents[defaulter_id])",
             "    fund_paid = min(loss_cents - margin_paid, default_fund_cents.get(defaulter_id, 0))"),
        ],
    ),
}

for name, (first_line, edits) in MUTANTS.items():
    text = src.replace(ref_first, '"""' + first_line, 1)
    for old, new in edits:
        assert text.count(old) == 1, (name, old[:60])
        text = text.replace(old, new, 1)
    out = root / "ledgers/BK4/mutants" / f"{name}.py"
    out.write_text(text, encoding="utf-8")
    print("wrote", out.relative_to(root))
