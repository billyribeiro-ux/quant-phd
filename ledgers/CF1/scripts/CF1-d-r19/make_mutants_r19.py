"""Write the round-19 (slice d) student-error mutants of grader/reference.py into ledgers/CF1/mutants/.

Each mutant is the reference with one plausible student error; the one-line docstring is the description that
mutate_graders prints. Each replacement must match exactly once.
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/CF/CF1/grader/reference.py").read_text(encoding="utf-8")
dest = root / "ledgers/CF1/mutants"


def edit(old: str, new: str, header: str) -> str:
    assert ref.count(old) == 1, old
    text = ref.replace(old, new)
    return f'"""{header}\n\nMutant of the reference solution for the CF1 capital-budgeting engine (capbudget.py).\n"""' + text.split('"""', 2)[2]


m1 = edit(
    "    if all(cf == 0 for cf in flows):\n",
    "    if all(cf == 0 for cf in flows[1:]):\n",
    "d19_m01: An IRR request whose inflows are all zero, such as [-100, 0], is refused: the all-zero test skips the outlay.",
)
m2 = edit(
    "    if all(cf == 0 for cf in flows):\n",
    "    if flows[0] == 0:\n        raise ValueError('a leading zero flow is not allowed')\n    if all(cf == 0 for cf in flows):\n",
    "d19_m02: An IRR request with a zero first flow is refused, as if the first flow had to be the outlay.",
)
m3 = edit(
    "    discounted = [cf / (1.0 + rate) ** t for t, cf in enumerate(flows)]\n    cumulative = discounted[0]\n",
    "    discounted = [cf / (1.0 + rate) ** max(t - 1, 0) for t, cf in enumerate(flows)]\n    cumulative = discounted[0]\n",
    "d19_m03: A discounted payback discounts each inflow one year too little: the exponent is t - 1 instead of t.",
)
m4 = edit(
    "    _check_rate(rate)\n    if len(flows) == 0:\n",
    "    _check_rate(rate)\n    if rate > 1.0:\n        raise ValueError('rate must be a percent between -1 and 1')\n    if len(flows) == 0:\n",
    "d19_m04: An NPV refuses any rate above 1, as if rates were given in percent rather than as decimals.",
)
m5 = edit(
    "    if not _finite(volatility) or volatility < 0.0:\n",
    "    if not _finite(volatility) or volatility <= 0.0:\n",
    "d19_m05: A Monte Carlo request with zero volatility is refused: the volatility check is made strict.",
)
m6 = edit(
    "    return (1.0 + real) * (1.0 + inflation) - 1.0\n",
    "    return real + inflation\n",
    "d19_m06: A Fisher conversion adds the two rates, the rule of thumb the page says is not the identity.",
)
for name, text in [
    ("d19_m01_irr_zero_outlay_only_refused.py", m1),
    ("d19_m02_irr_leading_zero_refused.py", m2),
    ("d19_m03_payback_exponent_one_short.py", m3),
    ("d19_m04_npv_rate_above_one_refused.py", m4),
    ("d19_m05_monte_carlo_zero_volatility_refused.py", m5),
    ("d19_m06_fisher_adds_the_rates.py", m6),
]:
    (dest / name).write_text(text, encoding="utf-8")
print("wrote 6 mutants")
