"""Round 17 (verifier E17, BK4 slice c): five student-error mutants written from reference.py, one change each.
Each change is asserted to apply exactly once. Output: ledgers/BK4/mutants/r17*.py (run from the checkout root)."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
MUT = ROOT / "ledgers/BK4/mutants"
REF = (ROOT / "course/modules/BK/BK4/grader/reference.py").read_text(encoding="utf-8")
HEAD = '"""Reference solution for the BK4 clearing-house simulator (clearing_house.py).'
assert REF.count(HEAD) == 1

SPECS = [
    ("r17a_capital_layer_ignores_margin_paid.py",
     "Student error: the CCP capital is sized on the loss less the default fund only, so the margin's cents are paid again by the capital.",
     "    capital_paid = min(loss_cents - margin_paid - fund_paid, ccp_capital_cents)",
     "    capital_paid = min(loss_cents - fund_paid, ccp_capital_cents)"),
    ("r17b_sizing_drops_the_last_loss.py",
     "Student error: the sizing reads the k-th smallest of the losses without the last scenario, so the largest scenario is never counted.",
     "    return sorted(losses_cents)[index - 1]",
     "    return sorted(losses_cents[:-1])[index - 1]"),
    ("r17c_margin_layer_reads_the_fund_table.py",
     "Student error: the defaulter's margin layer reads the default-fund table, a dictionary mix-up, so the margin is taken from the fund.",
     "    margin_paid = min(loss_cents, initial_margin_cents[defaulter_id])",
     "    margin_paid = min(loss_cents, default_fund_cents[defaulter_id])"),
    ("r17d_zero_margin_covers_nothing.py",
     "Student error: a margin of zero is read as no margin, so cover_bps returns zero even when zero losses are at the margin.",
     "    covered = sum(1 for loss in losses_cents if loss <= margin_cents)",
     "    if margin_cents <= 0:\n        return 0\n    covered = sum(1 for loss in losses_cents if loss <= margin_cents)"),
    ("r17e_uncovered_subtracts_the_capital_again.py",
     "Student error: the uncovered loss subtracts the CCP capital a second time, so an uncovered loss is understated.",
     "        uncovered = residual - total_fund",
     "        uncovered = max(0, residual - total_fund - ccp_capital_cents)"),
]
for name, error, old, new in SPECS:
    body = REF.replace(HEAD, '"""' + error + "\n\nVerifier-written mutant (round 17, slice c) of the reference, for the BK4 grader. Not a solution.\n\n" + HEAD[3:], 1)
    assert body.count(old) == 1, (name, body.count(old))
    body = body.replace(old, new, 1)
    (MUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
