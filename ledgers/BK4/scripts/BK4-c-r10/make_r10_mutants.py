"""Round-10 verifier mutants for BK4 (student-error modules derived from the reference by one exact text edit each).

Writes ledgers/BK4/mutants/x10*.py. Each replacement must match exactly once, or the script stops.
Usage: python make_r10_mutants.py <repo_root>
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/BK/BK4/grader/reference.py").read_text(encoding="utf-8")
out = root / "ledgers/BK4/mutants"

EDITS = {
    "x10a_pool_uses_survivor_margins": (
        "Student error: the survivors' pool is summed from their initial margins instead of their default funds.",
        "    total_fund = sum(default_fund_cents[member] for member in survivors)\n",
        "    total_fund = sum(initial_margin_cents[member] for member in survivors)\n",
    ),
    "x10b_cover_counts_strictly_below": (
        "Student error: cover_bps counts only losses strictly below the margin, so a loss equal to the margin is not covered.",
        "    covered = sum(1 for loss in losses_cents if loss <= margin_cents)\n",
        "    covered = sum(1 for loss in losses_cents if loss < margin_cents)\n",
    ),
    "x10c_survivors_include_the_defaulter": (
        "Student error: the survivors are every member, so the defaulter is listed in survivor_cents and its default fund joins the pool.",
        "    survivors = sorted(member for member in default_fund_cents if member != defaulter_id)\n",
        "    survivors = sorted(member for member in default_fund_cents)\n",
    ),
    "x10d_uncovered_ignores_the_capital": (
        "Student error: the uncovered loss is the loss less the margin, fund and survivors' pool, so the CCP capital is left out of the uncovered amount.",
        "        uncovered = residual - total_fund\n",
        "        uncovered = loss_cents - margin_paid - fund_paid - total_fund\n",
    ),
}

for name, (description, old, new) in EDITS.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    head = f'"""{description}\n\n'
    body = ref.replace('"""Reference solution for the BK4 clearing-house simulator (clearing_house.py).\n\n', "", 1)
    text = head + body
    assert text.count(old) == 1
    text = text.replace(old, new, 1)
    (out / f"{name}.py").write_text(text, encoding="utf-8")
    print("wrote", name)
