"""Write the four round-12 verifier mutants (BK4-c) as single-change copies of grader/reference.py.

Usage: python3 -I make_r12_mutants.py <checkout>. Each mutant's first docstring line names the student error.
"""

import sys
from pathlib import Path

checkout = Path(sys.argv[1])
ref = (checkout / "course/modules/BK/BK4/grader/reference.py").read_text(encoding="utf-8")
out_dir = checkout / "ledgers/BK4/mutants"
HEAD = '"""Reference solution for the BK4 clearing-house simulator (clearing_house.py).'


def make(name, doc, old, new, extra_import=False):
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new)
    if extra_import:
        assert body.count("from dataclasses import dataclass\n") == 1
        body = body.replace("from dataclasses import dataclass\n", "import math\nfrom dataclasses import dataclass\n", 1)
    assert body.count(HEAD) == 1
    body = body.replace(HEAD, f'"""Student error: {doc}\n\nReference solution for the BK4 clearing-house simulator (clearing_house.py).', 1)
    (out_dir / f"{name}.py").write_text(body, encoding="utf-8")


make(
    "r12a_survivor_share_rounded_up",
    "each survivor's pro rata share is rounded up to a whole cent (a ceiling), not floored, so the shares can exceed the residual.",
    "survivor_cents[member] = residual * default_fund_cents[member] // total_fund",
    "survivor_cents[member] = -((-residual * default_fund_cents[member]) // total_fund)",
)
make(
    "r12b_sizing_index_float",
    "the sizing index is computed in floats as target / 10000 * count and rounded up, not in integers as the page requires.",
    "    index = -((-target_bps * count) // 10_000)",
    "    index = math.ceil(target_bps / 10_000 * count)",
    extra_import=True,
)
make(
    "r12c_only_one_leftover_cent",
    "the leftover cents are paid one cent only, to the first survivor with a positive fund, so a residual with two or more leftover cents leaves cents unpaid.",
    "        for member in survivors:\n            if leftover == 0:\n                break\n            if default_fund_cents[member] > 0:\n                survivor_cents[member] += 1\n                leftover -= 1\n",
    "        for member in survivors:\n            if leftover == 0:\n                break\n            if default_fund_cents[member] > 0:\n                survivor_cents[member] += 1\n                leftover = 0\n",
)
make(
    "r12d_uncovered_added_to_first_survivor",
    "the uncovered loss is added to the first survivor's payment, so the survivors pay more than their whole default funds.",
    "        uncovered = residual - total_fund\n",
    "        uncovered = residual - total_fund\n        survivor_cents[survivors[0]] += uncovered\n",
)
print("wrote r12a-r12d")
