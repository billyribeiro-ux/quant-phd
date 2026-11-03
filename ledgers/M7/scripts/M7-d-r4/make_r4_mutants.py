"""Round-4 student-error mutants of grader/reference.py: one change each, written to ledgers/M7/mutants/.

Each replacement must match exactly once. The docstring's first line describes the error (mutate_graders prints it).
"""

from __future__ import annotations

import ast
import pathlib

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD4-M7-d")
REF = (ROOT / "course/modules/M/M7/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M7/mutants"

MUTANTS: list[tuple[str, str, list[tuple[str, str]]]] = [
    (
        "r4_01_lower_multipliers_reported_with_sign_flipped",
        "Student error r4-01: the lower-bound multipliers are reported with the sign flipped, so non-negative multipliers come out non-positive.",
        [('"lower": [float(v) for v in sol["lower"]],', '"lower": [-float(v) for v in sol["lower"]],')],
    ),
    (
        "r4_02_turnover_plus_and_minus_multipliers_swapped",
        "Student error r4-02: the turnover_plus and turnover_minus multipliers are swapped in the output.",
        [
            ('"turnover_plus": [float(v) for v in sol["plus"]],', '"turnover_plus": [float(v) for v in sol["minus"]],'),
            ('"turnover_minus": [float(v) for v in sol["minus"]],', '"turnover_minus": [float(v) for v in sol["plus"]],'),
        ],
    ),
    (
        "r4_03_budget_multiplier_reported_with_the_opposite_sign",
        "Student error r4-03: the budget multiplier is reported with the opposite sign, as if the budget were written one minus the sum.",
        [('"budget": float(sol["budget"]),', '"budget": -float(sol["budget"]),')],
    ),
    (
        "r4_04_starting_budget_tolerance_one_millionth",
        "Student error r4-04: the starting-portfolio budget check uses a tolerance of 1e-6 instead of 1e-9, so a starting sum 2e-9 off the budget is accepted.",
        [('if abs(sum(w0, Fraction(0)) - 1) > TOL:', 'if abs(sum(w0, Fraction(0)) - 1) > Fraction(1, 10**6):')],
    ),
    (
        "r4_05_turnover_limit_measured_from_zero_in_the_solver",
        "Student error r4-05: the turnover limit is applied to the sum of absolute weights, measured from zero rather than from the starting portfolio, in the solver's sign constraints.",
        [('rows.append((a, problem.tau + _dot(a, problem.w0), ("turn", signs)))', 'rows.append((a, problem.tau, ("turn", signs)))')],
    ),
    (
        "r4_06_only_the_first_sector_cap_enforced",
        "Student error r4-06: only the cap of sector 0 enters the search, so the other sector caps are never imposed.",
        [('    for k, cap in enumerate(problem.caps):\n        rows.append(', '    for k, cap in list(enumerate(problem.caps))[:1]:\n        rows.append(')],
    ),
]


def build(name: str, description: str, replacements: list[tuple[str, str]]) -> str:
    text = REF
    for old, new in replacements:
        count = text.count(old)
        assert count == 1, (name, old[:60], count)
        text = text.replace(old, new)
    # replace the module docstring (the first triple-quoted block) with the error description
    start = text.index('"""')
    end = text.index('"""', start + 3) + 3
    doc = f'"""{description}\n\nMutant of grader/reference.py: one change, as the first line states.\n"""'
    text = text[:start] + doc + text[end:]
    ast.parse(text)
    return text


def main() -> None:
    for name, description, replacements in MUTANTS:
        (OUT / f"{name}.py").write_text(build(name, description, replacements), encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
