import pathlib
ref = pathlib.Path('/tmp/verifyC1-M6-d/course/modules/M/M6/grader/reference.py').read_text()
out = pathlib.Path('/tmp/verifyC1-M6-d/ledgers/M6/mutants')
specs = {
 'm11_bet_must_be_strictly_affordable.py': (
  "Strict affordability: a bet is placed only if its stake is strictly less than the wealth on hand.",
  "    while base * 2 ** (bets + 1) <= capital + base:",
  "    while base * 2 ** (bets + 1) < capital + base:"),
 'm12_doob_strict_exceedance.py': (
  "Doob's maximum taken with a strict exceedance, so a path that reaches the level exactly is not counted.",
  "        key = (new_position, reached or abs(new_position) >= lam)",
  "        key = (new_position, reached or abs(new_position) > lam)"),
 'm13_python_round_half_even.py': (
  "Python's built-in round() on the exact expectation, which rounds half to even, so one half cent rounds down.",
  "    return math.floor(amount + Fraction(1, 2))",
  "    return round(amount)"),
 'm14_dyadic_value_no_last_cell_clamp.py': (
  "Dyadic value without the clamp to the last cell, so x = 1 is assigned to a non-existent cell beyond [1 - 2^-n, 1].",
  "    index = min(int(point * cells), cells - 1)  # point is in [0, 1], so truncation is the floor",
  "    index = int(point * cells)  # point is in [0, 1], so truncation is the floor"),
 'm15_stopping_rule_uses_horizon_not_cap.py': (
  "Stopping rule that runs to the horizon N instead of the stopping cap, so the stopped walk ignores the cap.",
  "    for _ in range(cap):\n        nxt: dict[int, Fraction] = {}",
  "    for _ in range(horizon):\n        nxt: dict[int, Fraction] = {}"),
 'm16_ruin_probability_one_bet_short.py': (
  "Ruin probability counts one bet too few, so the ruin branch has the wrong probability.",
  "    ruin = (1 - p) ** bets\n",
  "    ruin = (1 - p) ** (bets - 1)\n"),
}

specs.update({
 'm17_doob_endpoint_only.py': (
  "Doob's probability taken at the horizon only, P(|S_N| >= lam), instead of the maximum over every k up to N.",
  "    probability = sum((w for (_, reached), w in alive.items() if reached), Fraction(0))",
  "    probability = sum((w for (pos, _), w in alive.items() if abs(pos) >= lam), Fraction(0))"),
 'm18_wealth_on_win_uses_last_stake.py': (
  "Wealth on a win taken as the capital plus the last stake placed, instead of the capital plus the base stake.",
  "    wealth_on_win = capital + base\n",
  "    wealth_on_win = capital + base * 2 ** (bets - 1)\n"),
 'm19_float_probability_in_stopped_walk.py': (
  "Stopped-walk probability converted to float, so the control walk's expectation is no longer exact.",
  "    p = _win_probability(instance)\n    alive",
  "    p = float(_win_probability(instance))\n    alive"),
})

specs.update({
 'm20_doob_bound_divided_as_float.py': (
  "Doob's bound divided in floating point, E|S_N| / float(lam), so the bound is not an exact Fraction.",
  "    return probability, expected_abs / lam",
  "    return probability, expected_abs / float(lam)"),
})

for name, (doc, old, new) in specs.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    src = ref.replace(old, new)
    # docstring first line describes the error
    first, rest = src.split('\n', 1)
    if first.startswith('"""'):
        pass
    src = '"""' + doc + '\n\n' + src.split('"""', 2)[2].lstrip('\n') if False else src
    body = src
    # prepend a module docstring whose first line names the error (the reference has its own module docstring)
    assert body.startswith('"""Reference solution')
    body = '"""' + doc + '\n\n' + body[3:]
    (out / name).write_text(body)
    print('wrote', name)
