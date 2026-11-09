"""Round-14 BK4-c: write four single-change student-error mutants of reference.py into ledgers/BK4/mutants/.

Each replacement must match exactly once (asserted). Run from the checkout root: python3 -I <this file>.
"""

import os

ROOT = os.getcwd()
REF = os.path.join(ROOT, "course", "modules", "BK", "BK4", "grader", "reference.py")
DOC_OLD = '"""Reference solution for the BK4 clearing-house simulator (clearing_house.py).'
MUTANTS = {
    "r14a_defaulter_id_range_fixed_at_four_members.py": (
        "Student error: the defaulter id is checked against a fixed range of 1 to 4, as if there were four members, so a "
        "valid defaulter in a five- or six-member set is refused.",
        "    if defaulter_id not in default_fund_cents or defaulter_id not in initial_margin_cents:\n",
        "    if not 1 <= defaulter_id <= 4 or defaulter_id not in default_fund_cents or defaulter_id not in initial_margin_cents:\n",
    ),
    "r14b_survivors_in_dictionary_order.py": (
        "Student error: the survivors are taken in the order the default-fund dictionary lists them, not in ascending id "
        "order, so the leftover cent goes to whichever surviving member the dictionary lists first.",
        "    survivors = sorted(member for member in default_fund_cents if member != defaulter_id)\n",
        "    survivors = [member for member in default_fund_cents if member != defaulter_id]\n",
    ),
    "r14c_negative_fund_check_skips_survivors.py": (
        "Student error: a negative default fund for a surviving member is accepted, because the non-negative check is "
        "applied to the defaulter's fund only, so a negative share can follow.",
        "    for member, amount in default_fund_cents.items():\n        if amount < 0:\n",
        "    for member, amount in default_fund_cents.items():\n        if amount < 0 and member == defaulter_id:\n",
    ),
    "r14d_warns_on_uncovered_loss.py": (
        "Student error: a warning is issued when a loss is uncovered, which is a valid output, so the module warns on a "
        "valid input and the suite run with warnings as errors fails.",
        "        uncovered = residual - total_fund\n",
        "        uncovered = residual - total_fund\n        if uncovered > 0:\n            import warnings\n\n            warnings.warn(\"uncovered loss\")\n",
    ),
}
text = open(REF, encoding="utf-8").read()
assert text.count(DOC_OLD) == 1
for name, (summary, old, new) in MUTANTS.items():
    assert text.count(old) == 1, (name, text.count(old))
    body = text.replace(old, new).replace(DOC_OLD, '"""' + summary + "\n\n" + DOC_OLD[3:])
    with open(os.path.join(ROOT, "ledgers", "BK4", "mutants", name), "w", encoding="utf-8") as fh:
        fh.write(body)
    print("wrote", name)
