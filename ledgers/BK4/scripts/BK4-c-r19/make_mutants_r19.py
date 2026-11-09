"""Round 19 (BK4 slice c): write five new student-error mutants of grader/reference.py into ledgers/BK4/mutants/.

Each mutant is the reference with one change; the script asserts that its search text occurs exactly once, so a
mutant cannot silently equal the reference. Usage: python -I make_mutants_r19.py <checkout-root>
"""

import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
REF = (ROOT / "course/modules/BK/BK4/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/BK4/mutants"

MUTANTS = {
    "r19a_leftover_to_every_positive_survivor.py": (
        '"""Student error: the leftover cents are given one each to every survivor with a positive fund, not only to as many survivors as there are leftover cents."""',
        """        for member in survivors:
            if leftover == 0:
                break
            if default_fund_cents[member] > 0:
                survivor_cents[member] += 1
                leftover -= 1
""",
        """        for member in survivors:
            if default_fund_cents[member] > 0:
                survivor_cents[member] += 1
""",
    ),
    "r19b_share_denominator_includes_defaulter_fund.py": (
        '"""Student error: the pro rata share divides by the survivors\' pool plus the defaulter\'s own default fund, so the shares are cut too small."""',
        "residual * default_fund_cents[member] // total_fund",
        "residual * default_fund_cents[member] // (total_fund + default_fund_cents[defaulter_id])",
    ),
    "r19c_negative_check_looks_at_first_loss_only.py": (
        '"""Student error: the negative-loss check looks only at the first scenario, so a negative loss later in the list is accepted."""',
        """def _no_negative_losses(losses_cents: list[int]) -> None:
    if any(loss < 0 for loss in losses_cents):
        raise ValueError("losses cannot be negative")""",
        """def _no_negative_losses(losses_cents: list[int]) -> None:
    if losses_cents and losses_cents[0] < 0:
        raise ValueError("losses cannot be negative")""",
    ),
    "r19d_sizing_memo_keyed_by_target_only.py": (
        '"""Student error: margin_for_cover caches its answer by target alone, so a second case with the same target gets the first case\'s margin."""',
        """    return sorted(losses_cents)[index - 1]""",
        """    if target_bps in _MEMO:
        return _MEMO[target_bps]
    _MEMO[target_bps] = sorted(losses_cents)[index - 1]
    return _MEMO[target_bps]


_MEMO: dict[int, int] = {}""",
    ),
    "r19e_index_floor_plus_one.py": (
        '"""Student error: the sizing index is the floor of target times count over 10000, plus one, so an exact position is taken one loss too high."""',
        "    index = -((-target_bps * count) // 10_000)",
        "    index = (target_bps * count) // 10_000 + 1",
    ),
}

for name, (docline, old, new) in MUTANTS.items():
    if old.count("\n") > 0 and "leftover" in name:
        pass
    occurrences = REF.count(old)
    if occurrences != 1:
        raise SystemExit(f"{name}: search text occurs {occurrences} times in the reference (need exactly 1)")
    text = REF.replace(old, new, 1)
    # The module docstring is the reference's; the mutant's first docstring line is the student error.
    lines = text.split("\n", 1)
    # Replace the reference module docstring (first triple-quoted block) by the one-line error description.
    start = text.index('"""')
    end = text.index('"""', start + 3) + 3
    body = text[end:]
    mutant = docline + body
    (OUT / name).write_text(mutant, encoding="utf-8")
    print(f"wrote {name}")
