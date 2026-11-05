"""Round-13 BK4-c: write four new single-change student-error mutants of reference.py under ledgers/BK4/mutants/.

Each replacement must match exactly once in the reference, or the script stops. The first docstring line of each
mutant names the student error (the mutate tool reads it).
"""

import os
import sys

ROOT = os.getcwd()
REF = os.path.join(ROOT, "course", "modules", "BK", "BK4", "grader", "reference.py")
OUT = os.path.join(ROOT, "ledgers", "BK4", "mutants")
REF_FIRST = '"""Reference solution for the BK4 clearing-house simulator (clearing_house.py).'

MUTANTS = {
    "r13a_leftover_only_to_positive_share.py": (
        "Student error: the leftover cents go only to survivors whose computed share is already positive, so a residual "
        "smaller than the survivor count leaves cents unpaid.",
        [(
            "            if default_fund_cents[member] > 0:\n                survivor_cents[member] += 1",
            "            if default_fund_cents[member] > 0 and survivor_cents[member] > 0:\n"
            "                survivor_cents[member] += 1",
        )],
    ),
    "r13b_uncovered_negative_below_pool.py": (
        "Student error: the uncovered loss is set to the residual less the survivors' pool in both branches, so it is "
        "negative when the residual is below the pool.",
        [(
            "            survivor_cents[member] = residual * default_fund_cents[member] // total_fund\n",
            "            survivor_cents[member] = residual * default_fund_cents[member] // total_fund\n"
            "        uncovered = residual - total_fund\n",
        )],
    ),
    "r13c_cover_skips_the_last_scenario.py": (
        "Student error: the cover loop stops one scenario early (it reads the losses without the last one) but still "
        "divides by the full count of scenarios.",
        [(
            "    covered = sum(1 for loss in losses_cents if loss <= margin_cents)\n"
            "    return 10_000 * covered // len(losses_cents)",
            "    covered = sum(1 for loss in losses_cents[:-1] if loss <= margin_cents)\n"
            "    return 10_000 * covered // len(losses_cents)",
        )],
    ),
    "r13d_fund_layer_capped_at_survivor_pool.py": (
        "Student error: the defaulter's default fund is capped at the surviving members' pool, so the fund layer can pay "
        "less than the defaulter's whole contribution when the pool is smaller.",
        [(
            "    fund_paid = min(loss_cents - margin_paid, default_fund_cents[defaulter_id])\n",
            "    fund_paid = min(loss_cents - margin_paid, default_fund_cents[defaulter_id], "
            "sum(v for m, v in default_fund_cents.items() if m != defaulter_id))\n",
        )],
    ),
}

text = open(REF, encoding="utf-8").read()
assert text.count(REF_FIRST) == 1, "reference first docstring line not found once"
for name, (description, replacements) in MUTANTS.items():
    body = text.replace(REF_FIRST, '"""' + description + "\n\n" + REF_FIRST[3:], 1)
    for old, new in replacements:
        count = body.count(old)
        if count != 1:
            sys.exit(f"{name}: replacement target found {count} times, expected 1")
        body = body.replace(old, new, 1)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as handle:
        handle.write(body)
    print("wrote", name)
