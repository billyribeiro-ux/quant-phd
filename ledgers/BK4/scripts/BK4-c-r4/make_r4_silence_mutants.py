"""Write two round-4 silence mutants (a debug print left in one refusal path, and one in a valid uncovered path).

The page's Constraints: "On a valid input and on each named refused input, no function prints or warns." Run from the
checkout root: python make_r4_silence_mutants.py <root>.
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/BK/BK4/grader/reference.py").read_text(encoding="utf-8")
head = '"""Reference solution for the BK4 clearing-house simulator (clearing_house.py).'
assert ref.count(head) == 1
out = root / "ledgers/BK4/mutants"
mutants = {
    "r4g_debug_print_on_defaulter_refusal.py": (
        "Student error: a debug print is left in the defaulter-not-a-member refusal, so a refused input prints before it raises.",
        [
            (
                '        raise ValueError(f"defaulter_id {defaulter_id} is not one of the member ids")',
                '        print(f"debug: defaulter {defaulter_id} checked")\n'
                '        raise ValueError(f"defaulter_id {defaulter_id} is not one of the member ids")',
            )
        ],
    ),
    "r4h_debug_print_on_uncovered_loss.py": (
        "Student error: a debug print is left in the uncovered-loss branch, so a valid call with an uncovered loss prints.",
        [
            (
                "        uncovered = residual - total_fund\n",
                "        uncovered = residual - total_fund\n        print(f\"debug: uncovered {uncovered}\")\n",
            )
        ],
    ),
}
for name, (description, edits) in mutants.items():
    text = ref.replace(head, '"""' + description + "\n\nMutant of reference.py for the BK4 project (round 4 verifier).", 1)
    for old, new in edits:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new, 1)
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)
