"""Write round-4 student-error mutants of the BK4 reference as complete modules under ledgers/BK4/mutants/.

Each mutant is reference.py with one replaced fragment (asserted to match exactly once). The first docstring line of
each mutant names the student error. Run from the checkout root: python make_r4_mutants.py <root>.
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/BK/BK4/grader/reference.py").read_text(encoding="utf-8")
head = '"""Reference solution for the BK4 clearing-house simulator (clearing_house.py).'
assert ref.count(head) == 1
out = root / "ledgers/BK4/mutants"

mutants = {
    "r4a_leftover_in_mapping_order.py": (
        "Student error: the leftover cents go in the order of the default-fund dictionary, not in ascending id order.",
        [
            (
                "    survivors = sorted(member for member in default_fund_cents if member != defaulter_id)",
                "    survivors = [member for member in default_fund_cents if member != defaulter_id]",
            )
        ],
    ),
    "r4b_sizing_index_round_half_up.py": (
        "Student error: the sizing index is round-half-up of target times count over 10000, not its ceiling.",
        [
            (
                "    index = -((-target_bps * count) // 10_000)",
                "    index = int(target_bps * count / 10_000 + 0.5)",
            )
        ],
    ),
    "r4c_share_integer_division_first.py": (
        "Student error: each survivor's share is (residual // pool) times its fund, so the pro rata share is truncated first.",
        [
            (
                "        survivor_cents[member] = residual * default_fund_cents[member] // total_fund",
                "        survivor_cents[member] = (residual // total_fund) * default_fund_cents[member]",
            )
        ],
    ),
    "r4d_zero_loss_refused.py": (
        "Student error: a loss of zero cents is refused as if it were not a scenario, so the zero-loss boundary is rejected.",
        [
            (
                "    if loss_cents < 0:\n        raise ValueError(f\"loss_cents is negative",
                "    if loss_cents <= 0:\n        raise ValueError(f\"loss_cents must be positive, and a loss cannot be negative",
            )
        ],
    ),
    "r4e_cover_round_half_up.py": (
        "Student error: the cover is rounded half up to the nearest basis point instead of floored.",
        [
            (
                "    return 10_000 * covered // len(losses_cents)",
                "    return int(10_000 * covered / len(losses_cents) + 0.5)",
            )
        ],
    ),
    "r4f_sizing_sorts_caller_list_in_place.py": (
        "Student error: margin_for_cover sorts the caller's list in place before indexing it.",
        [
            (
                "    return sorted(losses_cents)[index - 1]",
                "    losses_cents.sort()\n    return losses_cents[index - 1]",
            )
        ],
    ),
}

for name, (description, edits) in mutants.items():
    text = ref.replace(
        head,
        '"""' + description + "\n\nMutant of reference.py for the BK4 project (round 4 verifier).",
        1,
    )
    for old, new in edits:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new, 1)
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)
