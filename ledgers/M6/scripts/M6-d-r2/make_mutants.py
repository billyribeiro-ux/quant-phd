"""Write the verifier's round-2 student-error mutants (m31-m36) for the M6 grader.

Each mutant is the reference solution with one plausible student error applied. Every replacement must match exactly
once, or the script stops. Run from the checkout root: python -I make_mutants.py <checkout>.
"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/M/M6/grader/reference.py").read_text(encoding="utf-8")
out = root / "ledgers/M6/mutants"
specs = {
    "m31_stopped_walk_unhit_paths_count_zero.py": (
        "Stopped walk: paths that never reach the level count as 0 instead of the walk's value at the cap.",
        "    total += sum((weight * position for position, weight in alive.items()), Fraction(0))",
        "    total += sum((weight * position for position, weight in alive.items() if position == level), Fraction(0))",
    ),
    "m32_stop_when_at_or_below_level.py": (
        "Stopping test written as at-or-below the level, so a level of +2 fires at the first step up to +1.",
        "                if new_position == level:",
        "                if new_position <= level:",
    ),
    "m33_doob_maximum_of_signed_walk.py": (
        "Doob's maximum taken over the signed walk, so excursions below zero are never counted in the probability.",
        "                key = (new_position, reached or abs(new_position) >= lam)",
        "                key = (new_position, reached or new_position >= lam)",
    ),
    "m34_ruin_wealth_loses_only_last_stake.py": (
        "Wealth after ruin taken as capital minus the last stake, instead of minus the sum of all the stakes lost.",
        "    wealth_on_ruin = capital - base * (2**bets - 1)",
        "    wealth_on_ruin = capital - base * 2 ** (bets - 1)",
    ),
    "m35_dyadic_error_divided_by_cell_count.py": (
        "Dyadic error divided once more by the number of cells, so each cell's integral is weighted by 2**-n twice.",
        "    return total\n\n\ndef dyadic_martingale_value",
        "    return total / cells\n\n\ndef dyadic_martingale_value",
    ),
    "m36_probabilities_rounded_before_expectation.py": (
        "Probabilities rounded to six decimals before the expected wealth is formed, not once at the end.",
        "    expected = win * wealth_on_win + ruin * wealth_on_ruin",
        "    win_r = Fraction(round(float(win), 6))\n    expected = win_r * wealth_on_win + (1 - win_r) * wealth_on_ruin",
    ),
}
for name, (doc, old, new) in specs.items():
    if ref.count(old) != 1:
        raise SystemExit(f"{name}: anchor found {ref.count(old)} times, expected 1")
    body = ref.replace(old, new)
    head = '"""Reference solution'
    if body.count(head) != 1:
        raise SystemExit(f"{name}: module docstring anchor not found once")
    body = body.replace(head, f'"""{doc}\n\nReference solution', 1)
    (out / name).write_text(body, encoding="utf-8")
    print("wrote", name)
