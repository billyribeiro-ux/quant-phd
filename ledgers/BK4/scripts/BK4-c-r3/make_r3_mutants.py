"""Write the round-3 student-error mutants of reference.py into ledgers/BK4/mutants/ (one change each)."""

from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyE3-BK4-c")
REF = (ROOT / "course/modules/BK/BK4/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/BK4/mutants"

MUTANTS = {
    "r3a_dedupe_before_sizing.py": (
        "Student error: the sizing sorts the distinct losses only, so a repeated loss counts once in the order statistic.",
        "    return sorted(losses_cents)[index - 1]",
        "    return sorted(set(losses_cents))[index - 1]",
    ),
    "r3b_cover_counts_distinct_losses.py": (
        "Student error: the cover counts each distinct loss once, not each of the S scenarios, so a repeated loss is lost.",
        "    covered = sum(1 for loss in losses_cents if loss <= margin_cents)",
        "    covered = sum(1 for loss in set(losses_cents) if loss <= margin_cents)",
    ),
    "r3c_defaulter_checked_upper_bound_only.py": (
        "Student error: the defaulter id is refused only when it exceeds the number of members, so id 0 is accepted.",
        "    if defaulter_id not in default_fund_cents or defaulter_id not in initial_margin_cents:",
        "    if defaulter_id > len(default_fund_cents):",
    ),
    "r3d_negative_check_defaulter_only.py": (
        "Student error: a negative initial margin or default fund is refused only for the defaulter, not for every member.",
        "    for member, amount in initial_margin_cents.items():\n        if amount < 0:",
        "    for member, amount in initial_margin_cents.items():\n        if amount < 0 and member == defaulter_id:",
    ),
}

for name, (doc, old, new) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    body = REF.replace(old, new, 1)
    # the one-line docstring names the student error, as mutate_graders.py expects
    body = body.replace('"""Reference solution for the BK4 clearing-house simulator (clearing_house.py).',
                        f'"""{doc}', 1)
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)

# Second batch: the same single-change method, for two more plausible student errors.
MUTANTS_2 = {
    "r3e_sizing_counts_distinct_losses.py": (
        "Student error: the sizing counts the distinct losses for S and sorts only the distinct losses, so k uses the distinct count.",
        "    count = len(losses_cents)\n    index = -((-target_bps * count) // 10_000)\n    return sorted(losses_cents)[index - 1]",
        "    count = len(set(losses_cents))\n    index = -((-target_bps * count) // 10_000)\n    return sorted(set(losses_cents))[index - 1]",
    ),
    "r3f_defaulter_upper_bound_from_max_id.py": (
        "Student error: the defaulter id is refused only when it exceeds the largest member id, so id 0 is accepted.",
        "    if defaulter_id not in default_fund_cents or defaulter_id not in initial_margin_cents:",
        "    if defaulter_id > max(default_fund_cents):",
    ),
}
for name, (doc, old, new) in MUTANTS_2.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    body = REF.replace(old, new, 1).replace(
        '"""Reference solution for the BK4 clearing-house simulator (clearing_house.py).', f'"""{doc}', 1)
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
