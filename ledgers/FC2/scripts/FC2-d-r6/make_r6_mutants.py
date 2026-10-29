# Round 6 FC2-d: three new student-error mutants written as complete modules, derived from the reference.
# Each replacement must occur exactly once in the reference, so the mutant differs from it in one place only.
import re
import sys

REF = sys.argv[1]
OUT = sys.argv[2]
src = open(REF, encoding="utf-8").read()
DOC_END = src.index("from __future__ import annotations")


def mutate(name: str, summary: str, old: str, new: str) -> None:
    assert src.count(old) == 1, (name, old[:70])
    body = src[DOC_END:].replace(old, new)
    head = f'"""{summary}\n\nNot deployed (BLUEPRINT section 7). Round 6 verifier mutant for FC2-d.\n"""\n\n'
    open(f"{OUT}/{name}.py", "w", encoding="utf-8").write(head + body)


mutate(
    "r6_a_ties_away_from_zero_on_negative_gap",
    "Student error: a parity gap tie is rounded away from zero, so an exact -14.5 cents becomes -15 instead of -14.",
    "    return _half_up(gap)\n",
    "    n = (2 * abs(gap.numerator) + gap.denominator) // (2 * gap.denominator)\n    return n if gap >= 0 else -n\n",
)
mutate(
    "r6_b_convexity_strike_is_left_neighbour",
    "Student error: a convexity finding reports the strike of its left neighbour instead of the strike of the middle call.",
    '        "strike_cents": strikes[j],\n',
    '        "strike_cents": strikes[j - 1],\n',
)
mutate(
    "r6_c_zero_fee_rejected",
    "Student error: a fee of exactly zero is rejected, because the cost check tests for a positive fee instead of a non-negative one.",
    "    if fee < 0 or spread < 0:\n",
    "    if fee <= 0 or spread < 0:\n",
)
print("written")
