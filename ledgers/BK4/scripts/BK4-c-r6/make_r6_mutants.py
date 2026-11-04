"""Writes four new student-error mutants of reference.py (verifier round 6) into ledgers/BK4/mutants/.

Usage: make_r6_mutants.py <checkout>. Each replacement must match exactly once, or the script stops."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/BK/BK4/grader/reference.py").read_text(encoding="utf-8")
out = root / "ledgers/BK4/mutants"
edits = {
    "n1_defaulter_checked_in_margins_only.py": (
        "Student error: the defaulter is checked against the margin dictionary only, so a defaulter present in the margins but absent from the default funds is accepted (the member ids are the keys of default_fund_cents).",
        "    if defaulter_id not in default_fund_cents or defaulter_id not in initial_margin_cents:",
        "    if defaulter_id not in initial_margin_cents:",
    ),
    "n2_cover_skips_negative_loss_check.py": (
        "Student error: cover_bps does not refuse a negative loss; only margin_for_cover checks the sign of the losses.",
        "    _no_negative_losses(losses_cents)\n    covered = sum(",
        "    covered = sum(",
    ),
    "n3_remainder_to_highest_id_first.py": (
        "Student error: the leftover cents go to the surviving members in descending id order, so the highest id is paid first.",
        "        for member in survivors:\n            if leftover == 0:",
        "        for member in reversed(survivors):\n            if leftover == 0:",
    ),
    "n4_margin_layer_pools_all_margins.py": (
        "Student error: the defaulter's margin layer uses the sum of every member's initial margin instead of the defaulter's own.",
        "    margin_paid = min(loss_cents, initial_margin_cents[defaulter_id])",
        "    margin_paid = min(loss_cents, sum(initial_margin_cents.values()))",
    ),
}
for name, (doc, old, new) in edits.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new, 1)
    body = body[body.index('"""', 3) + 3:].lstrip("\n")
    text = f'"""{doc}"""\n\n' + body
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)
