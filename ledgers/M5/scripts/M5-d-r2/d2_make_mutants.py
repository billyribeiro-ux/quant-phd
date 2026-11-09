"""Write the round-2 verifier mutants (complete modules derived from reference.py, one deliberate error each).

Each mutant's docstring first line describes the error. Run once; the outputs are ledgers/M5/mutants/d3_*.py.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
REF = os.path.join(REPO, "course/modules/M/M5/grader/reference.py")
OUT = os.path.join(REPO, "ledgers/M5/mutants")

with open(REF, encoding="utf-8") as fh:
    REFERENCE = fh.read()


def mutate(name: str, description: str, old: str, new: str) -> None:
    assert REFERENCE.count(old) == 1, (name, REFERENCE.count(old))
    body = REFERENCE.replace(old, new, 1)
    # replace the module docstring with one whose first line describes the error
    end = body.index('"""', 3) + 3
    doc = f'"""{description}\n\nDerived from grader/reference.py by one change; see the round-2 scripts.\n"""'
    body = doc + body[end:]
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(body)


mutate(
    "d3_01_feasibility_allows_a_tie_tolerance_of_1e-12.py",
    "Student-error mutant (M5 round 2): feasibility allows a successor up to 1e-12 above k**alpha, a tie tolerance the "
    "exact test k' <= k**alpha does not have.",
    "            if successor <= available:",
    "            if successor <= available + 1e-12:",
)
mutate(
    "d3_02_first_point_bound_checked_only_for_longer_grids.py",
    "Student-error mutant (M5 round 2): the first-point-at-most-one check runs only for grids of two or more points, so "
    "the one-point grid [1.5] is accepted.",
    '    if points[0] > 1:\n        raise ValueError("the first grid point must be at most 1")',
    '    if len(points) > 1 and points[0] > 1:\n        raise ValueError("the first grid point must be at most 1")',
)
mutate(
    "d3_03_value_is_the_penultimate_iterate_when_the_budget_runs_out.py",
    "Student-error mutant (M5 round 2): when the budget runs out without convergence, value is the vector before the "
    "last sweep, while certified_error refers to the last sweep.",
    '        values = new\n        certified = factor * change\n        if certified <= target:\n            break\n'
    '    return {\n        "value": values,',
    '        previous = values\n        values = new\n        certified = factor * change\n        if certified <= target:\n            break\n'
    '    return {\n        "value": values if certified <= target else previous,',
)
print("written")
