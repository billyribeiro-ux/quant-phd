"""Write round-4 student-error mutants of the M6 reference into ledgers/M6/mutants/.

Each mutant is the reference solution with exactly one replacement, asserted to match exactly once.
Usage: make_mutants.py REPO_ROOT
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
REF = ROOT / "course/modules/M/M6/grader/reference.py"
OUT = ROOT / "ledgers/M6/mutants"

MUTANTS: list[tuple[str, str, str, str]] = [
    (
        "r4_01_stop_level_checked_at_time_zero.py",
        "A stopping level equal to the start is treated as reached at time 0, so the stopped value is 0 before any step.",
        "    alive: dict[int, Fraction] = {0: Fraction(1)}\n    total = Fraction(0)\n",
        "    if level == 0:\n        return Fraction(0)\n    alive: dict[int, Fraction] = {0: Fraction(1)}\n    total = Fraction(0)\n",
    ),
    (
        "r4_02_exact_fit_bet_refused.py",
        "The bet count uses a strict inequality, so a stake that exactly equals the wealth on hand is never placed.",
        "    while base * 2 ** (bets + 1) <= capital + base:",
        "    while base * 2 ** (bets + 1) < capital + base:",
    ),
    (
        "r4_03_cents_rounded_through_float.py",
        "The expected cents are formed as a float before the half-up rounding, so an exact half-cent below the half is lost.",
        "    return math.floor(amount + Fraction(1, 2))",
        "    return math.floor(float(amount) + 0.5)",
    ),
    (
        "r4_04_wealth_on_win_forgets_the_stake.py",
        "After a win the wealth is taken as the capital alone, without the stake that the win pays.",
        "    wealth_on_win = capital + base\n",
        "    wealth_on_win = capital\n",
    ),
    (
        "r4_05_ruin_uses_win_probability.py",
        "The probability that every placed bet loses is computed with the win probability p instead of 1 - p.",
        "    ruin = (1 - p) ** bets\n",
        "    ruin = p ** bets\n",
    ),
    (
        "r4_06_down_step_weight_is_p.py",
        "The stopped walk gives a down step the weight p, not 1 - p, so the weights do not sum to 1 on a biased coin.",
        "        for step, prob in ((1, p), (-1, 1 - p)):",
        "        for step, prob in ((1, p), (-1, p)):",
    ),
    (
        "r4_07_stopping_ignored_value_at_cap.py",
        "The stopping rule is ignored: the expectation is the walk's value at the cap, even on paths that reached the level.",
        "                if new_position == level:\n                    total += branch * new_position\n                else:\n                    nxt[new_position] = nxt.get(new_position, Fraction(0)) + branch\n",
        "                nxt[new_position] = nxt.get(new_position, Fraction(0)) + branch\n",
    ),
    (
        "r4_08_dyadic_error_integrates_from_left_endpoint.py",
        "The dyadic error integrates the squared deviation from the cell's left endpoint, not from its midpoint.",
        "        total += ((b - c) ** 3 - (a - c) ** 3) / 3\n",
        "        total += ((b - a) ** 3 - (a - a) ** 3) / 3\n",
    ),
]

HEADER = (
    "Based on the reference solution; the single change is marked in the code.\n\n"
    "Every probability is an exact Fraction. Every money amount is an integer number of cents, computed from an exact\n"
    "Fraction and rounded once, half up.\n"
)


def main() -> None:
    source = REF.read_text(encoding="utf-8")
    for name, description, old, new in MUTANTS:
        count = source.count(old)
        if count != 1:
            raise SystemExit(f"{name}: anchor occurs {count} times, expected 1")
        body = source.replace(old, new + "  # MUTANT: the single change\n", 1)
        text = f'"""{description}\n\n{HEADER}"""' + body.split('"""', 2)[2]
        (OUT / name).write_text(text, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
